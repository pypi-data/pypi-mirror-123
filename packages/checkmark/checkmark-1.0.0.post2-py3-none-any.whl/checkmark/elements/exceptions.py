

class CheckmarkError(Exception):
    """Generic Checkmark exception"""


class MissingHeading(CheckmarkError):
    """Radio button or option found with no preceding heading"""