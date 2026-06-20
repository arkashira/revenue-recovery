"""Basic tests for the axentx_product package."""

import pytest
from axentx_product import hello

def test_hello_returns_correct_greeting():
    assert hello("World") == "Hello, World!"
    assert hello("Axentx") == "Hello, Axentx!"

def test_hello_type_error_on_non_string():
    with pytest.raises(TypeError):
        hello(123)  # type: ignore
