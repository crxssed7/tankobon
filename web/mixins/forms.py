class HiddenFieldsMixin:
    hidden_fields = []

    def remove_hidden_fields(self):
        if self.conditional():
            for field_name in self.hidden_fields:
                self.fields.pop(field_name, None)

    def conditional(self) -> None:
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_hidden_fields()
