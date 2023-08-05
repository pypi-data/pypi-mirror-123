import html

from typing import Union, Sequence



class HTMLElement:
    """An HTML element"""

    # Display element without a closing tag
    # Ex. <button type='button' />
    simplified: bool = False

    tag: str
    args: set[str]
    kwargs: dict[str, str]
    content: list[Union['HTMLElement', str]]


    def __init__(self, tag: str, *args: Sequence[str], **kwargs: dict[str, str]):
        self.tag = tag
        self.args = set(args)
        self.kwargs = {key: value for key, value in kwargs.items() if value is not None}
        self.content = []

    def __str__(self):
        return self.html()

    def __getitem__(self, key: str) -> Union[str, None]:
        """Get the value of a keyword argument"""
        return self.kwargs.get(key, None)

    def __setitem__(self, key: str, value: str):
        """Set the value of a keyword argument"""
        if value is not None:
            self.kwargs[key] = value

    
    def append(self, *elements: Sequence[Union['HTMLElement', str]]):
        """Append elements to content"""
        self.content.extend(elements)

    def html(self, indent: int = 0, escape_strings: bool = False) -> str:
        """Render element into HTML"""

        indentation = '\t' * indent


        # 1. Arguments
        args = " ".join(map(str, self.args))

        # 2. Keyword arguments
        kwargs = " ".join([f'{key}={value!r}' for key, value in self.kwargs.items()])


        # 3. Content
        content = '\n'.join(render_element(element, escape_strings) for element in self.content)

        # Keep element on the same row if there is only one
        if len(self.content) == 1:
            render_element(self.content[0], 0, escape_strings)

        # For more than one, separate by line
        elif len(self.content) > 1:
            content = '\n'.join(render_element(element, indent + 1, escape_strings) for element in self.content)
            
            # Add line breaks before and after, plus indentation
            content = f'\n{content}\n' + indentation

        # Empty if empty, straight-forward
        else:
            content = ""

        
        # 4. Finalize the entire element

        inside_tag = " ".join(s for s in [self.tag, args, kwargs] if s)

        if self.simplified and not self.content:
            if not self.args and not self.kwargs:
                whole_element = f'<{self.tag}>'
            else:
                whole_element = f'<{inside_tag} />'
        else:
            whole_element = f'<{inside_tag}>{content}</{self.tag}>'


        # Return with indentation
        return indentation + whole_element


def render_element(
        element: Union[HTMLElement, str],
        indent: int = 0,
        escape_strings: bool = False
    ) -> str:
        
    """Render element into HTML"""
    
    if isinstance(element, HTMLElement):
        return element.html(indent, escape_strings)

    if escape_strings:
        element = html.escape(element)

    return '\t' * indent + element