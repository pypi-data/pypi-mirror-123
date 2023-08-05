import webview

from typing import Union, Any

from webview.window import Window

from .elements import Form
from .templating import generate_html
    


class MarkupForm:
    """An HTML form window generated from markup"""
    
    title: str
    form: Form
    html: str
    style: str
    noscript: bool

    _close_on_submit: bool
    _window: Window


    def __init__(self, title: str, document: str, style: str = "", button_text: str = 'Submit',
                        noscript: bool = False, default_values: dict[str, Union[str, bool]] = None):
        self.title = title
        self.form = Form(document, button_text=button_text)
        self.style = style
        self.noscript = noscript
        self.html = ""

        # Initialize form with specified values
        self.form.update(**(default_values or {}))

    def submit_data(self, data: dict[str, Any]):
        """Receive and save submitted data"""
        self.form.update(**{
            key: value for key, value in data.items()
            if not key.isdigit()
        })

        if self._close_on_submit:
            self._window.destroy()

    def launch(self, close_on_submit: bool = True, *args, **kwargs):
        """Launch form window"""

        # Whether to destroy the window
        # once the form has been submitted
        self._close_on_submit = close_on_submit

        # Generate HTML
        self.html = generate_html(
            self.title,
            self.form.html(),
            self.style,
            self.noscript
        )

        # Create and launch window
        self._window = webview.create_window(
            self.title,
            html=self.html,
            js_api=self,
            *args, **kwargs
        )
        webview.start()