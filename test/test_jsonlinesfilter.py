import json
import tempfile
from itertools import chain
from pathlib import Path

import pytest

from jsonlinesfilter import filter_doc, filter_jsonlines_file


@pytest.fixture()
def resource_dir():
    return Path(__file__).parent / "resources"


@pytest.fixture()
def john_doc(resource_dir):
    return json.loads(Path(resource_dir / "john.json").read_text())


@pytest.fixture()
def adam_doc(resource_dir):
    return json.loads(Path(resource_dir / "adam.json").read_text())


def test_filter_doc__include_one_word_no_chain(john_doc):
    filter_doc(john_doc, ["foo"])
    assert len(john_doc["clusters"]) == 0


def test_filter_doc__include_two_words_no_chain(john_doc):
    filter_doc(john_doc, ["foo", "bar"])
    assert len(john_doc["clusters"]) == 0


def test_filter_doc__include_three_words_no_chain(john_doc):
    filter_doc(john_doc, ["foo", "bar", "baz"])
    assert len(john_doc["clusters"]) == 0


def test_filter_doc__include_one_word_one_chain(john_doc):
    john_cluster = john_doc["clusters"][0]
    filter_doc(john_doc, ["John"])
    assert len(john_doc["clusters"]) == 1
    assert list(chain(*john_doc["clusters"][0])) == list(chain(*john_cluster))


def test_filter_doc__include_another_words_one_chain(john_doc):
    john_cluster = john_doc["clusters"][0]
    filter_doc(john_doc, ["friend"])
    assert len(john_doc["clusters"]) == 1
    assert list(chain(*john_doc["clusters"][0])) == list(chain(*john_cluster))


def test_filter_doc__include_two_words_one_chain(john_doc):
    john_cluster = john_doc["clusters"][0]
    filter_doc(john_doc, ["John", "friend"])
    assert len(john_doc["clusters"]) == 1
    assert list(chain(*john_doc["clusters"][0])) == list(chain(*john_cluster))


def test_filter_doc__include_three_words_one_chain(john_doc):
    john_cluster = john_doc["clusters"][0]
    filter_doc(john_doc, ["foo", "John", "friend"])
    assert len(john_doc["clusters"]) == 1
    assert list(chain(*john_doc["clusters"][0])) == list(chain(*john_cluster))


def test_filter_doc__include_one_word_two_chains(john_doc):
    door_cluster = john_doc["clusters"][1]
    house_cluster = john_doc["clusters"][2]
    filter_doc(john_doc, ["house"])
    assert len(john_doc["clusters"]) == 2
    assert list(chain(*john_doc["clusters"][0])) == list(chain(*door_cluster))
    assert list(chain(*john_doc["clusters"][1])) == list(chain(*house_cluster))


def test_filter_doc__include_two_words_two_chains(john_doc):
    john_cluster = john_doc["clusters"][0]
    door_cluster = john_doc["clusters"][1]
    filter_doc(john_doc, ["John", "door"])
    assert len(john_doc["clusters"]) == 2
    assert list(chain(*john_doc["clusters"][0])) == list(chain(*john_cluster))
    assert list(chain(*john_doc["clusters"][1])) == list(chain(*door_cluster))


def test_filter_doc__same_word_two_chains(adam_doc):
    adam_cluster_1 = adam_doc["clusters"][0]
    adam_cluster_2 = adam_doc["clusters"][1]
    filter_doc(adam_doc, ["Adam"])
    assert len(adam_doc["clusters"]) == 2
    assert list(chain(*adam_doc["clusters"][0])) == list(chain(*adam_cluster_1))
    assert list(chain(*adam_doc["clusters"][1])) == list(chain(*adam_cluster_2))


def test_filter_doc__include_three_words_two_chains(john_doc):
    john_cluster = john_doc["clusters"][0]
    door_cluster = john_doc["clusters"][1]
    filter_doc(john_doc, ["John", "door", "friend"])
    assert len(john_doc["clusters"]) == 2
    assert list(chain(*john_doc["clusters"][0])) == list(chain(*john_cluster))
    assert list(chain(*john_doc["clusters"][1])) == list(chain(*door_cluster))


def test_filter_jsonlines_file__include_one_word_one_chain(resource_dir, john_doc):
    john_cluster = john_doc["clusters"][0]

    with tempfile.TemporaryDirectory() as tempdir:
        outfile = Path(tempdir) / "output.jsonfiles"
        filter_jsonlines_file(resource_dir / "john.jsonlines", outfile, "John")

        with open(outfile) as fh:
            counter = 0
            for line in fh.readlines():
                doc = json.loads(line)
                assert len(doc["clusters"]) == 1
                assert list(chain(*doc["clusters"][0])) == list(chain(*john_cluster))
                counter += 1
            assert counter == 3
