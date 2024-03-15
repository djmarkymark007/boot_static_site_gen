import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_italic,
    text_type_bold,
    text_type_image,
    text_type_link,
)
from block import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_link,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    block_type_heading,
    block_type_code,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list,
)

class TestSpliter(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        want = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(want, new_nodes)
    
    def test_split_empty(self):
        new_nodes = split_nodes_delimiter([], "`", text_type_code)
        self.assertListEqual([], new_nodes)
    
    def test_just_delemiter(self):
        node = TextNode("`code block`", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        want = [
            TextNode("code block", text_type_code),
        ]
        self.assertListEqual(want, new_nodes)

    def test_multi_delemiter(self):
        node = TextNode("hi`code`wow`more code` that is", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        want = [
            TextNode("hi", text_type_text),
            TextNode("code", text_type_code),
            TextNode("wow", text_type_text),
            TextNode("more code", text_type_code),
            TextNode(" that is", text_type_text),
        ]
        self.assertListEqual(want, new_nodes)
    
class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

class TextMarkdownExtract(unittest.TestCase):
    def test_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        got = extract_markdown_images(text)
        want = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/dfsdkjfd.png")]
        self.assertListEqual(got, want)

    def test_no_image(self):
        text = "This is text with no image"
        got = extract_markdown_images(text)
        want = []
        self.assertListEqual(got, want)

    def test_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        want = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        got = extract_markdown_link(text)
        self.assertListEqual(got, want)

    def test_no_link(self):
        text = "This is text with no link"
        got = extract_markdown_link(text)
        want = []
        self.assertListEqual(got, want)
     
    """ passing images to to extract link will break
    def test_link_with_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        got = extract_markdown_images(text)
        want = []
        self.assertListEqual(got, want)
        """

class TestNodeSplits(unittest.TestCase):
    def test_image_split(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        want = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
        ]

        self.assertListEqual(want, new_nodes)

    def test_image_no_image(self):
        node = TextNode("This text has no image", text_type_text)
        node2 = TextNode("This text has an ![image](https://i.imgur.com/zjjcJKZ.png) wow", text_type_text)
        got = split_nodes_image([node, node2])
        want = [
            TextNode("This text has no image", text_type_text),
            TextNode("This text has an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" wow", text_type_text)
        ]
        self.assertListEqual(want, got)

    def test_link_split(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com) and another [second link](https://www.microsoft.com) last part",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        want = [
            TextNode("This is text with an ", text_type_text),
            TextNode("link", text_type_link, "https://www.google.com"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second link", text_type_link, "https://www.microsoft.com"
            ),
            TextNode(" last part", text_type_text),
        ]

        self.assertListEqual(want, new_nodes)

class TestTextToNodes(unittest.TestCase):
    def test_basic(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        got = text_to_textnodes(text)
        want = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertListEqual(got, want)
  
class TestMarkdownToBlocks(unittest.TestCase):
    def test_extra_newline(self):
        text = "this is a test\n\n\nwhat happens"
        got = markdown_to_blocks(text)
        want = ["this is a test", "what happens"]
        self.assertListEqual(got, want)

    def test_extra_newline2(self):
        text = "this is a test\n\n\n\nwhat happens"
        got = markdown_to_blocks(text)
        want = ["this is a test", "what happens"]
        self.assertListEqual(got, want)

    def test_extra_newline3(self):
        text = "this is a test\n\n\n\n\nwhat happens"
        got = markdown_to_blocks(text)
        want = ["this is a test", "what happens"]
        self.assertListEqual(got, want)
    
    def test_markdown_basic(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        got = markdown_to_blocks(text)
        want = ["# This is a heading", 
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item"]
        
        self.assertListEqual(got, want)
    
    def test_markdown_basic2(self):
        text = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        got = markdown_to_blocks(text)
        want = ["This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
        ]
        self.assertListEqual(got, want)
    
    def test_my(self):
        text = "this is a block\n\n\n this is another"
        got = markdown_to_blocks(text)
        want = ["this is a block", "this is another"]
        self.assertListEqual(got, want)
        


class TestBlocks(unittest.TestCase):
    def test_quote(self):
        block = markdown_to_blocks(">this is a quote\n>with a second line")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_quote, got)
    
    def test_heading(self):
        block = markdown_to_blocks("# this is a heading")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_heading, got)
    
    def test_heading6(self):
        block = markdown_to_blocks("###### this is a heading")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_heading, got)

    def test_heading7(self):
        block = markdown_to_blocks("####### this is a heading")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_paragraph, got)

    def test_code(self):
        block = markdown_to_blocks("```\nthis is a code\n```")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_code, got)

    def test_code2(self):
        block = markdown_to_blocks("```this is a code```")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_paragraph, got)

    def test_unordered_list(self):
        block = markdown_to_blocks("*this is a unordered list\n-this is part two\n*wow")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_unordered_list, got)

    def test_unordered_list2(self):
        block = markdown_to_blocks("*this is a unordered list\nthis is part two\n*wow")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_paragraph, got)

    def test_ordered_list(self):
        block = markdown_to_blocks("1.this is a ordered list\n2.this is part two\n3.wow")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_ordered_list, got)
    
    def test_ordered_list2(self):
        block = markdown_to_blocks("1.this is a ordered list\nthis is part two\n3.wow")
        got = block_to_block_type(block[0])
        self.assertEqual(block_type_paragraph, got)


#NOTE(mark): BOOT test below
class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)


if __name__ == "__main__":
    unittest.main()