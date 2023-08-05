from typing import Union

from .element import HTMLElement
from .inputs import Input
from .basic import Label



class RadioOption(HTMLElement):
    """A radio option element"""

    def __init__(self, text: str, value: str, state: bool = False, title: str = None):
        super().__init__('div', **{'class': 'radio'}, title=title)

        self.radio = Input('radio', id=value, value=value)
        self.state = state

        label = Label(value, text)
        self.append(self.radio, label)

    
    def get_state(self) -> bool:
        """Get the state of the radio option"""
        return 'checked' in self.radio.args

    def set_state(self, active: bool):
        """Set the state of the radio option"""

        if active:
            self.radio.args.add('checked')
        elif self.state:
            self.radio.args.remove('checked')

    state = property(get_state, set_state)


class RadioSelection(HTMLElement):
    """A radio selection element"""

    def __init__(self, name: str, *options: tuple[RadioOption]):
        super().__init__('span', **{'class': 'radio'}, name=name)
        self.append(*options)

    def append(self, *options: tuple[RadioOption]):
        # Add name to every radio option
        for element in options:
            element.radio.kwargs['name'] = self['name']
        
        super().append(*options)

    
    @property
    def options(self) -> list[str]:
        """Get values of all available options"""
        return [element.radio.kwargs['value'] for element in self.content]


    def get_option(self) -> Union[str, None]:
        """Get selected option"""
        for element in self.content:
            if element.state:
                return element.radio.kwargs['value']
        return None

    def set_option(self, value: str):
        """Set selected option"""
        for element in self.content:
            element.state = element.radio.kwargs['value'] == value

    value = property(get_option, set_option)