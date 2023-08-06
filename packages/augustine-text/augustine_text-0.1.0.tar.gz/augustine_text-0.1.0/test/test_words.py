from ward import test
from augustine_text.sample_text import words

@test("Not a very good test")
def _():
    assert words(75)
