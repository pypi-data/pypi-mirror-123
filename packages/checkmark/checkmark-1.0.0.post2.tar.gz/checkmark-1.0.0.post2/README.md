# Checkmark

Checkmark lets you quickly and easily set up a way for you or any other user to submit data to your program through an HTML form. Using a Markdown-like document, you can specify a plethora of form elements.

### Form elements

- [Text](#text)
- [TextArea](#textarea)
- [Selections](#selections)
    - [Checkboxes](#checkboxes)
    - [Radio buttons](#radio-buttons)
    - [Dropdown menu](#dropdown-options)


## Example

```py
from checkmark import MarkupForm

document = """
: Username
> [Username](username "Ex. @user:domain.tld")
: Password
> [Password](password "Choose something not too simple.")
"""

style = """
body {
    background-color: rgb(31, 31, 56);
    color: white;
    font-family: monospace;
}
"""

window = MarkupForm('My Form', document, style, 'Save')
window.launch(close_on_submit=True, min_size(200, 400))

print('[b green]Submitted data:[/b green]')
print(window.form.items())
```

You can try it out with the example below.

```md
## Account

: Username
> [Username](username "Ex. @user:domain.tld")
: Password
> [Password](password "Choose something not too simple.")
: Email address
> [Ex. user@domain.tld](email "So that you can confirm your account.")

+ [x] [Sign me up to the newsletter](newsletter)

>> [My hobbies are ...](hobbies "What do you like to do during your free time?")

## [Message layout](layout)

* [ ] [IRC](irc)
* [x] [Modern](modern)
* [ ] [Message bubbles](bubbles)

## [Language](language)

- [x] [Swedish](se)
- [ ] [English](en)
- [ ] [French](fr)
```


## Rules

Every element has a prefix specification followed by text. The text can be written either plainly or as a Markdown link. Written plainly, URL and title will be generated from the text.

### Link

The title is always used as the `title` argument for any element for which it is specified.
```md
[Text](url "Title.")
```
```md
# This is my text.

is equivalent to

# [This is my text.](This-is-my-text "")
```

### Headings

The standard 6 headings can be made just as in Markdown.
```md
## Heading 2
```

### Label
Labels are simply aesthetic and don't affect the functionality of the form.
```md
: [Super Label](best-label)
```

### Text & TextArea

`Text` uses one `>` as prefix and `TextArea` uses two.
The text of the link is used as the `placeholder` argument.


#### Text
```md
> [Username](username "Ex. @user:domain.tld")
```

#### TextArea
```md
>> [My hobbies are ...](hobbies "What do you like to do during your free time?")
```

### Selections

All these types of elements are defined using list items.
- Checkboxes using `+` as prefix.
- Radio buttons using `*` as prefix.
- Dropdown options using `-` as prefix.

#### Checkboxes

```md
+ [x] [I understand how selections work.](understood)
```

#### Radio buttons & Dropdown options

Both types require that a heading precedes them. It's used to specify in which variable the selected value is to be stored.

The URL of an option is used as the value.

##### Radio buttons

```md
## [Message layout](layout)

* [ ] [IRC](irc)
* [x] [Modern](modern)
* [ ] [Message bubbles](bubbles)
```

##### Dropdown options

```md
## [Language](language)

- [x] [Swedish](se)
- [ ] [English](en)
- [ ] [French](fr)
```

### Paragraph

Any line or lines that aren't matched to another rule is stored as a paragraph.