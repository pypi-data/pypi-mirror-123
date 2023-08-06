from unittest import TestCase
import pandas
import tempfile
import shutil
import numpy

from mappable.map import Mappable, MappableDataset


class TestMappableDataset(TestCase):
    def setUp(self):
        self.data = pandas.read_csv("test/fixtures/data.tsv", sep="\t")
        self.out_file = tempfile.mkdtemp()
        self.m = MappableDataset("test", "A test mappable instance.", self.out_file)

    def tearDown(self):

        shutil.rmtree(self.out_file)

    def test_add_dataset(self):
        self.m.add_pandas(self.data)

        # Should be searchable by default
        assert self.m.searchable()

        # Should have lowercased label column name.
        assert "label" in self.m[0]

        # Can't add data twice.
        with self.assertRaises(ValueError):
            self.m.add_pandas(self.data)

    def test_add_column(self):
        self.m.add_pandas(self.data)

        new_col = [x for x in range(0, len(self.data))]
        self.m.add_column("new", new_col)
        assert self.m[0]["new"] == 0

    def test_indexing(self):
        self.m.add_pandas(self.data)
        data_json = self.data.to_dict("records")

        assert self.m[0] == data_json[0]
        assert self.m[-1] == data_json[-1]
        assert self.m[:-1] == data_json[:-1]
        assert self.m[1:] == data_json[1:]
        assert self.m[1:3] == data_json[1:3]

    def test_views(self):
        self.m.add_pandas(self.data)

        two_d = numpy.random.randn(len(self.data), 2)
        three_d = numpy.random.randn(len(self.data), 3)

        self.m.add_points("2d", two_d)
        self.m.add_points("3d", three_d)

        # Adding with the same name is not allowed.
        with self.assertRaises(ValueError):
            self.m.add_points("2d", two_d)

    def test_export(self):

        data = self.data[["text"]]
        self.m.add_pandas(data)
        exported = self.m.to_json()

        # exported data should contain no labels, because
        # no label column was passed in.
        for ex, original in zip(exported, data.to_dict("records")):
            assert ex["text"] == original["text"]
            assert ex["label"] == "None"
