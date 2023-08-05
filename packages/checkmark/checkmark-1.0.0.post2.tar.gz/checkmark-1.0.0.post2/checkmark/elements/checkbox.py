from .element import HTMLElement
from .inputs import Input
from .basic import Label



class Checkbox(HTMLElement):
    """A checkbox element"""
    

    def __init__(self, text: str, name: str, state: bool = False, title: str = None):
        super().__init__('div', **{'class': 'checkbox'}, title=title, name=name)

        self.checkbox = Input('checkbox', id=name, name=name)
        self.state = state

        label = Label(name, text)
        self.append(self.checkbox, label)


    def get_state(self) -> bool:
        """Get the state of the checkbox"""
        return 'checked' in self.checkbox.args

    def set_state(self, active: bool):
        """Set the state of the checkbox"""

        if active:
            self.checkbox.args.add('checked')
        elif self.state:
            self.checkbox.args.discard('checked')

    value = property(get_state, set_state)