from django.db.models.signals import pre_save
from django.dispatch import Signal

## Courtesy of https://github.com/jazzband/django-simple-history/issues/165#issuecomment-264847982

## signal sent whenever a data tracking is performed
track_data_performed = Signal(["instance"])


def track_data(*fields):
    """
    Based on David Cramer's  track_data.py
    See: http://cramer.io/2010/12/06/tracking-changes-to-fields-in-django

    Here we just add a single line to issue the track_data specific
    signal.
    """

    unsaved = {}

    def _store(self, data=None):
        "Updates a local copy of attributes values"
        if self.id:
            if data:
                self.__data = {f: getattr(data, f) for f in fields}
            else:
                self.__data = {f: getattr(self, f) for f in fields}
        else:
            self.__data = unsaved

    def inner(cls):
        # contains a local copy of the previous values of attributes
        cls.__data = {}

        def has_changed(self, field):
            "Returns 'True' if 'field' has changed since initialization."
            if self.__data is unsaved:
                return False
            return self.__data.get(field) != getattr(self, field)

        cls.has_changed = has_changed

        def old_value(self, field):
            "Returns the previous value of 'field'"
            return self.__data.get(field)

        cls.old_value = old_value

        def whats_changed(self):
            "Returns a list of changed attributes."
            changed = {}
            if self.__data is unsaved:
                return changed
            for k, v in self.__data.items():
                value = getattr(self, k)
                if v != value:
                    changed[k] = value
            return changed

        cls.whats_changed = whats_changed

        # Ensure we are updating local attributes on model pre_save
        def _pre_save(sender, instance, **kwargs):
            if not kwargs.get("raw", False):
                inst = None
                if instance.id:
                    # get old values
                    try:
                        inst = sender.objects.get(id=instance.id)
                    except sender.DoesNotExist:
                        pass
                _store(instance, inst)

                # we emit a unique signal so that others can connect to
                track_data_performed.send(sender=cls, instance=instance)

        pre_save.connect(_pre_save, sender=cls, weak=False)

        # Ensure we are updating local attributes on model save
        def save(self, *args, **kwargs):
            save._original(self, *args, **kwargs)
            _store(self)

        save._original = cls.save
        cls.save = save
        return cls

    return inner
