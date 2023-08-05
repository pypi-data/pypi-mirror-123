from pathlib import Path



# Load the HTML template for inserting the JavaScript function and the form

html_fname = Path(__file__).resolve().parent / 'index.html'

with open(html_fname) as f:
    HTML_TEMPLATE = f.read()


# Load the JavaScript function for submitting data
# and insert it into the HTML template

js_fname = Path(__file__).resolve().parent / 'submit_data.js'

with open(js_fname) as f:
    HTML_TEMPLATE = HTML_TEMPLATE.replace('(( submit.js ))', f.read())


def generate_html(title: str, body: str, style: str, noscript: bool = False):
    """Generates HTML from template"""
    
    # Surround body in <noscript> if script is disabled
    if noscript:
        f'<noscript>\n{body}\n</noscript>'

    # Insert parts into template
    return HTML_TEMPLATE \
                .replace('(( title ))', title) \
                .replace('(( style ))', style) \
                .replace('(( body ))', body)