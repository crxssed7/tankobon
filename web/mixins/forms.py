class HiddenFieldsMixin:
    hidden_fields = []

    def remove_hidden_fields(self):
        if self.conditional():
            for field_name in self.hidden_fields:
                self.fields.pop(field_name, None)

    def conditional(self) -> bool:
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_hidden_fields()


class StyledFieldsMixin:
    ATTRS = {"class": "w-full rounded focus:border-hint focus:ring-hint bg-blay border-whay hover:border-hint transition duration-300 ease-in-out"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(self.ATTRS)
