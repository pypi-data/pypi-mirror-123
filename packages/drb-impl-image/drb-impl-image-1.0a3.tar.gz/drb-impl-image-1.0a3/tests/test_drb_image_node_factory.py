import os
import unittest
import io
from pathlib import Path

from drb_impl_file import DrbFileFactory, DrbFileAttributeNames

from drb_impl_image import DrbImageFactory, DrbImageBaseNode
from drb_impl_image.image_common import DrbImageNodesValueNames

IMAGE = DrbImageNodesValueNames.IMAGE.value


class TestDrbNodeFactoryNetcdf(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))

    image_fake = current_path / "files" / "fake.tiff"
    image_tif_one = current_path / "files" / 'GeogToWGS84GeoKey5.tif'
    image_png = current_path / "files" / 'png-248x300.png'
    image_jp2 = current_path / "files" / 'relax.jp2'
    node = None
    node_file = None

    def setUp(self) -> None:
        self.node = None
        self.node_file = None

    def tearDown(self) -> None:
        if self.node is not None:
            self.node.close()
        if self.node_file is not None:
            self.node_file.close()

    def open_node(self, path_file):
        self.node_file = DrbFileFactory().create(path_file)
        self.node = DrbImageFactory().create(self.node_file)
        return self.node

    def test_opened_file_node(self):
        node = self.open_node(str(self.image_tif_one))

        self.assertIsInstance(node, DrbImageBaseNode)
        self.assertEqual(node.name, self.node_file.name)
        self.assertEqual(node.namespace_uri, self.node_file.namespace_uri)

    def test_base_node(self):
        node = self.open_node(str(self.image_tif_one))

        self.assertEqual(node.parent, self.node_file.parent)
        self.assertEqual(node.value, self.node_file.value)

        self.assertIsInstance(node, DrbImageBaseNode)

        self.assertEqual(len(node), 1)
        self.assertTrue(node.has_child())
        self.assertEqual(len(node.children), 1)

    def test_base_node_attribute(self):
        node = self.open_node(str(self.image_tif_one))

        self.assertEqual(node.attributes, self.node_file.attributes)

        self.assertEqual(node.get_attribute(DrbFileAttributeNames.
                                            DIRECTORY.value),
                         self.node_file.get_attribute(
                             DrbFileAttributeNames.DIRECTORY.value))

    def test_base_node_impl(self):
        node = self.open_node(str(self.image_tif_one))

        self.assertEqual(node.has_impl(io.BufferedIOBase),
                         self.node_file.has_impl(io.BufferedIOBase))

        impl = node.get_impl(io.BufferedIOBase)
        self.assertIsNotNone(impl)
        self.assertIsInstance(impl, io.BufferedIOBase)
        impl.close()

    def test_first_group(self):
        node = self.open_node(str(self.image_tif_one))

        self.assertIsInstance(node, DrbImageBaseNode)
        root_node = node[0]
        self.assertIsNotNone(root_node)
        root_node.close()
