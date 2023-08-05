from typing import Union, Sequence

from .element import HTMLElement



class Heading(HTMLElement):
    """A heading element"""
    
    def __init__(self, level: int, text: str, id_: str = None):
        super().__init__(f'h{level}', id=id_)
        self.level = level
        self.append(text)


class Label(HTMLElement):
    """A label element"""

    def __init__(self, for_: str, *elements: tuple[Union[HTMLElement, str]]):
        super().__init__('label', **{'for': for_})
        self.append(*elements)


class LineBreak(HTMLElement):
    """A line break element"""

    simplified: bool = True

    def __init__(self):
        super().__init__('br')

    def __str__(self) -> str:
        return '<br>'


class Paragraph(HTMLElement):
    """A paragraph element"""

    def __init__(self, *elements: Sequence[Union[HTMLElement, str]]):
        super().__init__('p')
        self.append(*elements)