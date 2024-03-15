import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_repr(self):
        node = HtmlNode("a", "wow", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual("HtmlNode(a, wow, None, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))

    def test_props(self):
        node = HtmlNode("a", "wow", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())
    
    def test_props2(self):
        node = HtmlNode("a", "wow", None, {"hi":"hmm"})
        self.assertEqual(' hi="hmm"', node.props_to_html())

class TestLeafNode(unittest.TestCase):
    def test_text(self):
        node = LeafNode(None, "just text")
        self.assertEqual("just text", node.to_html())

    def test_tag(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>", node.to_html())

    def test_tag_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual("<a href=\"https://www.google.com\">Click me!</a>", node.to_html())
    
    def test_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_props_but_no_tag(self):
        node = LeafNode(None, "wow", {"hmm":"hi"})
        self.assertEqual("wow", node.to_html())

    def test_repr(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("LeafNode(p, This is a paragraph of text., None)", repr(node))
    
class TestParentNode(unittest.TestCase):
    def test_leafnodes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", node.to_html())

    def test_parentnodes(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "a",
                    [
                        LeafNode("b", "Bold link"),
                    ],
                    {"href":"www.wow.com"}
                ),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual("<p><a href=\"www.wow.com\"><b>Bold link</b></a>Normal text</p>", node.to_html())



if __name__ == "__main__":
    unittest.main()