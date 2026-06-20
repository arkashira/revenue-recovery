"""Axentx Product package.

Provides a simple greeting function used by the test suite.
"""

def hello(name: str) -> str:
    """Return a friendly greeting for *name*.

    Args:
        name: The name to greet.

    Returns:
        A greeting string in the form ``"Hello, <name>!"``.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    return f"Hello, {name}!"
