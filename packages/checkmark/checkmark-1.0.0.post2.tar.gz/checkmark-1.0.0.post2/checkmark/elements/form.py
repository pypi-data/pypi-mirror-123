import re

from typing import Union


from .exceptions import MissingHeading

from .element import HTMLElement

from .create_element import create_element

from .basic import Heading, Label, LineBreak, Paragraph

from .radio import RadioOption, RadioSelection
from .dropdown import DropdownOption, DropdownSelection

from .inputs import Submit, Text, TextArea
from .checkbox import Checkbox



class Form(HTMLElement):
    """An HTML form generated from markup"""

    document: str
    button_text: str
    entries: list[HTMLElement]

    def __init__(self, document: str, button_text: str = 'Submit'):
                        
        super().__init__('form', id='markdown-form', onsubmit=f'submit_data(); return false')

        # Remove comments
        document = re.sub(
            r'\<\!\-\-((?:.|\n)*?)\-\-\>',
            # Leave a line break if any are found in match
            lambda m: ('', '\n')['\n' in m.group(1)],
            document
        )

        self.document = document
        self.button_text = button_text

        self.parse()

    def parse(self):
        """Parse document"""
        
        # Include a dummy entry for backward comparison
        root = [None]

        # Keep track of the latest heading
        # for attaching its name to following list elements
        heading = None

        # Parse each line individually,
        # and once retrieved, check if its validly positioned

        for i, line in enumerate(self.document.splitlines()):
            element = create_element(line)

            # Skip line breaks
            if isinstance(element, LineBreak):
                continue


            # Headings
            if isinstance(element, Heading):
                heading = element
                root.append(element)

            # Radio options
            elif isinstance(element, RadioOption):
                # Append radio span if necessary
                if not isinstance(root[-1], RadioSelection):
                    if heading is None:
                        raise MissingHeading(f'Heading missing for radio button on line {i + 1}')
                        
                    root.append(RadioSelection(heading['id']))

                    # Clear heading should any different type of element follow
                    heading = None

                root[-1].append(element)

            # Dropdown options
            elif isinstance(element, DropdownOption):
                # Append select if necessary
                if not isinstance(root[-1], DropdownSelection):
                    if heading is None:
                        raise MissingHeading(f'Heading missing for option on line {i + 1}')
                        
                    root.append(DropdownSelection(heading['id']))

                    # Clear heading should any different type of element follow
                    heading = None

                root[-1].append(element)

            # Paragraphs
            elif isinstance(element, Paragraph) and isinstance(root[-1], Paragraph):
                root[-1].append(*element.content)

            # Anything else
            else:
                root.append(element)


            # Attach any label to its following element
            if isinstance(root[-2], Label):
                root[-2]['for'] = root[-1]['id']


        # Remove dummy
        root.pop(0)


        # Make sure that all radio selections have one option checked
        for element in root:
            if isinstance(element, RadioSelection):
                # Stop at the first checked option
                for option in element.content:
                    if option.state:
                        break
                # If none are found, check the first option
                else:
                    element.content[0].state = True


        # Insert line breaks where appropriate

        for i, element in enumerate(root):
            if not isinstance(root[i], (Heading, LineBreak)):
                root.insert(i + 1, LineBreak())


        # Append all elements to the form except the dummy entry
        self.append(*root)

        # Append a line break and a submit button
        self.append(LineBreak(), Submit(self.button_text))
        

        # References to all configurable elements
        self.entries = {
            element['name']: element
            for element in self.content
            if isinstance(element, (
                Text,
                TextArea,
                Checkbox,
                RadioSelection,
                DropdownSelection
            ))
        }

    def update(self, **kwargs):
        """Update entry values"""

        for name, value in kwargs.items():
            if name not in self.entries:
                raise KeyError(f'{name!r} not in form')

            self.entries[name].value = value

    def items(self) -> dict[str, Union[str, bool]]:
        """Get keys and values of all entries"""
        return {name: element.value for name, element in self.entries.items()}