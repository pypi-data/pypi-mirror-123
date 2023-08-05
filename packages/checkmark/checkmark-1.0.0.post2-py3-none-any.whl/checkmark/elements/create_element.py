import re

from typing import Union

from .link import link

from .basic import Heading, Label, LineBreak, LineBreak, Paragraph
from .inputs import Text, TextArea

from .checkbox import Checkbox
from .radio import RadioOption
from .dropdown import DropdownOption



def create_element(line: str) -> Union[Heading, Label, Text, TextArea, Checkbox,
                                        RadioOption, DropdownOption, Paragraph, LineBreak]:
    """Parse a line and create a new HTML element from it"""

    # Heading
    if m := re.match(r'^(\#{1,6}) (.+)', line):
        level = len(m.group(1))
        l = link(m.group(2))
        return Heading(level, l.text, l.url)

    # Label
    if line.startswith(': '):
        return Label(None, line[2:])

    # Text
    if line.startswith('> '):
        placeholder, name, title = link(line[2:])
        return Text(name, placeholder, title)

    # TextArea
    if line.startswith('>> '):
        placeholder, name, title = link(line[3:])
        return TextArea(name, placeholder, title)

    # Checkbox, Radio, Dropdown
    if m := re.match(r'^([+*-]) \[(?:([xX])|\s)\] (.+)', line):
        prefix = m.group(1)
        active = bool(m.group(2))
        text, url, title = link(m.group(3))
        
        # Checkbox
        if prefix == '+':
            return Checkbox(text, url, active, title)
        
        # Radio
        if prefix == '*':
            return RadioOption(text, url, active, title)

        # Dropdown
        if prefix == '-':
            return DropdownOption(text, url, active, title)


    # Paragraph
    if line:
        return Paragraph(line)

    # LineBreak
    return LineBreak()