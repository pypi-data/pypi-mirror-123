from edxml_test_corpus import CORPUS_PATH


def test_import_corpus_path():
    assert isinstance(CORPUS_PATH, str)
