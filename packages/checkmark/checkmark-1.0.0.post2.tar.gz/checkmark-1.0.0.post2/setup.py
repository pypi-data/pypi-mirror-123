# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['checkmark', 'checkmark.elements', 'checkmark.templating']

package_data = \
{'': ['*']}

install_requires = \
['pywebview>=3.5,<4.0']

setup_kwargs = {
    'name': 'checkmark',
    'version': '1.0.0.post2',
    'description': 'Create launchable HTML form windows using a Markdown-like language',
    'long_description': '# Checkmark\n\nCheckmark lets you quickly and easily set up a way for you or any other user to submit data to your program through an HTML form. Using a Markdown-like document, you can specify a plethora of form elements.\n\n### Form elements\n\n- [Text](#text)\n- [TextArea](#textarea)\n- [Selections](#selections)\n    - [Checkboxes](#checkboxes)\n    - [Radio buttons](#radio-buttons)\n    - [Dropdown menu](#dropdown-options)\n\n\n## Example\n\n```py\nfrom checkmark import MarkupForm\n\ndocument = """\n: Username\n> [Username](username "Ex. @user:domain.tld")\n: Password\n> [Password](password "Choose something not too simple.")\n"""\n\nstyle = """\nbody {\n    background-color: rgb(31, 31, 56);\n    color: white;\n    font-family: monospace;\n}\n"""\n\nwindow = MarkupForm(\'My Form\', document, style, \'Save\')\nwindow.launch(close_on_submit=True, min_size(200, 400))\n\nprint(\'[b green]Submitted data:[/b green]\')\nprint(window.form.items())\n```\n\nYou can try it out with the example below.\n\n```md\n## Account\n\n: Username\n> [Username](username "Ex. @user:domain.tld")\n: Password\n> [Password](password "Choose something not too simple.")\n: Email address\n> [Ex. user@domain.tld](email "So that you can confirm your account.")\n\n+ [x] [Sign me up to the newsletter](newsletter)\n\n>> [My hobbies are ...](hobbies "What do you like to do during your free time?")\n\n## [Message layout](layout)\n\n* [ ] [IRC](irc)\n* [x] [Modern](modern)\n* [ ] [Message bubbles](bubbles)\n\n## [Language](language)\n\n- [x] [Swedish](se)\n- [ ] [English](en)\n- [ ] [French](fr)\n```\n\n\n## Rules\n\nEvery element has a prefix specification followed by text. The text can be written either plainly or as a Markdown link. Written plainly, URL and title will be generated from the text.\n\n### Link\n\nThe title is always used as the `title` argument for any element for which it is specified.\n```md\n[Text](url "Title.")\n```\n```md\n# This is my text.\n\nis equivalent to\n\n# [This is my text.](This-is-my-text "")\n```\n\n### Headings\n\nThe standard 6 headings can be made just as in Markdown.\n```md\n## Heading 2\n```\n\n### Label\nLabels are simply aesthetic and don\'t affect the functionality of the form.\n```md\n: [Super Label](best-label)\n```\n\n### Text & TextArea\n\n`Text` uses one `>` as prefix and `TextArea` uses two.\nThe text of the link is used as the `placeholder` argument.\n\n\n#### Text\n```md\n> [Username](username "Ex. @user:domain.tld")\n```\n\n#### TextArea\n```md\n>> [My hobbies are ...](hobbies "What do you like to do during your free time?")\n```\n\n### Selections\n\nAll these types of elements are defined using list items.\n- Checkboxes using `+` as prefix.\n- Radio buttons using `*` as prefix.\n- Dropdown options using `-` as prefix.\n\n#### Checkboxes\n\n```md\n+ [x] [I understand how selections work.](understood)\n```\n\n#### Radio buttons & Dropdown options\n\nBoth types require that a heading precedes them. It\'s used to specify in which variable the selected value is to be stored.\n\nThe URL of an option is used as the value.\n\n##### Radio buttons\n\n```md\n## [Message layout](layout)\n\n* [ ] [IRC](irc)\n* [x] [Modern](modern)\n* [ ] [Message bubbles](bubbles)\n```\n\n##### Dropdown options\n\n```md\n## [Language](language)\n\n- [x] [Swedish](se)\n- [ ] [English](en)\n- [ ] [French](fr)\n```\n\n### Paragraph\n\nAny line or lines that aren\'t matched to another rule is stored as a paragraph.',
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/deepadmax/checkmark',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
