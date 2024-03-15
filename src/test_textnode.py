import unittest

from htmlnode import (
    LeafNode
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("this is a text node", text_type_bold)
        node2 = TextNode("this is a text node", text_type_text)
        self.assertNotEqual(node, node2)
    
    def test_not_eq2(self):
        node = TextNode("this is a text node", text_type_bold)
        node2 = TextNode("this is a text node1", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", text_type_link, "http://www.wow.com")
        node1 = TextNode("This is a text node", text_type_link, "http://www.wow.com")
        self.assertEqual(node, node1)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_bold)
        self.assertEqual("TextNode(This is a text node, bold, None)", repr(node))


    def test_textnode_to_htmlnode(self):
        node = text_node_to_html_node(TextNode("This is a text node", text_type_link, "http://www.wow.com"))
        node1 = LeafNode("a", "This is a text node", {"href":"http://www.wow.com"})
        self.assertEqual(node.to_html(), node1.to_html())

if __name__ == "__main__":
    unittest.main()