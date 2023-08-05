from typing import Union

from .element import HTMLElement



class DropdownOption(HTMLElement):
    """A dropdown option element"""

    def __init__(self, text: str, value: str, state: bool = False, title: str = None):
        super().__init__('option', value=value, title=title)
        self.state = state
        self.append(text)


    def get_state(self) -> bool:
        """Get the state of the checkbox"""
        return self.kwargs.get('selected') == 'selected'

    def set_state(self, active: bool):
        """Set the state of the checkbox"""

        if active:
            self.kwargs['selected'] = 'selected'
        elif self.state:
            del self.kwargs['selected']

    state = property(get_state, set_state)


class DropdownSelection(HTMLElement):
    """A select element"""

    def __init__(self, name: str, *options: tuple[DropdownOption]):
        super().__init__('select', name=name)
        self.append(*options)

    
    @property
    def options(self) -> list[str]:
        """Get values of all available options"""
        return [element.kwargs['value'] for element in self.content]


    def get_option(self) -> Union[str, None]:
        """Get selected option"""
        for element in self.content:
            if element.state:
                return element.kwargs['value']
        return None

    def set_option(self, value: str):
        """Set selected option"""
        for element in self.content:
            element.state = element.kwargs['value'] == value

    value = property(get_option, set_option)