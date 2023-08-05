from .element import HTMLElement



class Input(HTMLElement):
    """An input element"""

    simplified: bool = True

    def __init__(self, type_: str, *args, **kwargs):
        super().__init__('input', type=type_, *args, **kwargs)


class Submit(Input):
    """A submit element"""

    def __init__(self, text: str):
        super().__init__('submit', value=text)


class Text(Input):
    """A text element"""

    def __init__(self, name: str, placeholder: str = None, title: str = None):
        super().__init__('text', name=name, placeholder=placeholder, title=title)

    def get_value(self):
        """Get the value of the text input"""
        return self['value']

    def set_value(self, value: str):
        """Set the value of the text input"""
        self['value'] = value

    value = property(get_value, set_value)


class TextArea(HTMLElement):
    """A textarea element"""

    def __init__(self, name: str, placeholder: str = None, title: str = None):
        super().__init__('textarea', name=name, placeholder=placeholder, title=title)

    def get_value(self) -> str:
        """Get the value of the text input"""
        return self.content[0] if self.content else ""

    def set_value(self, value: str):
        """Set the value of the text input"""
        self.content = [value]

    value = property(get_value, set_value)