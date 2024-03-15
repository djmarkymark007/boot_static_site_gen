import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_italic,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
)

from htmlnode import (
    ParentNode,
    LeafNode,
)

#TODO(Mark): allow nesting delimiter like **this is bold *th is bold and italic* wow**
# need leafnode and parentnode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type is not text_type_text:
            res.append(node)
        else:
            texts = node.text.split(delimiter)
            if len(texts) % 2 == 0:
                raise ValueError(f"Missing delimiter: {delimiter} in {node.text}")
            for index in range(len(texts)):
                text = texts[index]
                if text == "":
                    continue
                if index % 2 == 0:
                    res.append(TextNode(text, text_type_text))
                else:
                    res.append(TextNode(text, text_type))
    
    return res

def split_nodes_image(old_nodes):
    res = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            res.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            res.append(old_node)
            continue
        
        current_text = old_node.text
        for image in images:
            split = current_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split) != 2:
                raise ValueError("Invalid Markdown, image selction not closed")
            if split[0] != "":
                res.append(TextNode(split[0], text_type_text))
            res.append(TextNode(image[0], text_type_image, image[1]))
            current_text = split[1]
        
        if current_text != "":
            res.append(TextNode(current_text, text_type_text))

    return res


def split_nodes_link(old_nodes):
    res = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            res.append(old_node)
            continue

        links = extract_markdown_link(old_node.text)
        if len(links) == 0:
            res.append(old_node)
            continue
        
        current_text = old_node.text
        for link in links:
            split = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if split[0] != "":
                res.append(TextNode(split[0], text_type_text))
            res.append(TextNode(link[0], text_type_link, link[1]))
            current_text = split[1]
        
        if current_text != "":
            res.append(TextNode(current_text, text_type_text))

    return res

def extract_markdown_images(text):
    found = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return found

def extract_markdown_link(text):    
    found = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return found


def text_to_textnodes(text):
    # the order the delimiters and the split functuion are called matter
    delimiters = [
        ("**", text_type_bold),
        ("*", text_type_italic),
        ("`", text_type_code)
    ]
    res = [TextNode(text, text_type_text)]
    res = split_nodes_image(res)
    res = split_nodes_link(res)
    for delimiter in delimiters:
        res = split_nodes_delimiter(res, delimiter[0], delimiter[1])
    return res


def markdown_to_blocks(markdown):
    res = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block != "":
            res.append(block.strip())
    
    return res

def block_to_block_type(block):
    if block[0] == "#":
        i = 1
        while(block[i] == "#" and i <= 6):
            i += 1
        if block[i] == " " and i <= 6:
            return block_type_heading
    lines = block.split("\n") 

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code

    first_line = lines[0]

    if first_line[0] == ">":
        for line in lines:
            if line[0] != ">":
                return block_type_paragraph
        return block_type_quote 

    if first_line[0] == "*" or first_line[0] == "-":
        for line in lines:
            if line[0] != "*" and line[0] != "-":
                return block_type_paragraph
        return block_type_unordered_list

    if first_line[:2]  == "1.":
        count = 1
        for line in lines:
            if line[:2] != f"{count}.":
                return block_type_paragraph
            count += 1
        return block_type_ordered_list

    return block_type_paragraph



block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"