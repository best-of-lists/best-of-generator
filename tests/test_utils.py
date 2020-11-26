from best_of import utils


def test_clean_whitespaces():
    assert utils.clean_whitespaces("test  foo") == "test foo"
