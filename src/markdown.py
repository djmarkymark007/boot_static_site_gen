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

from block import (
    text_node_to_html_node,
    text_to_textnodes,
    block_type_unordered_list,
    block_type_quote,
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    text_type_bold,
    markdown_to_blocks,
)

def text_to_childern(text):
    text_nodes = text_to_textnodes(text)
    childern = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        childern.append(html_node)
    return childern

def block_paragraph_to_html_node(block):
    nodes = []
    lines = block.split("\n")
    paragraph = " ".join(lines)
    childern = text_to_childern(paragraph)
    return ParentNode("p", childern)

def block_heading_to_html_node(block):
    count = 0
    space = 1
    while block[count] == "#":
        count += 1
    if count + space >= len(block): #Not sure about this
        raise ValueError("Invalid heading level: {count}")
    lines = block[count + space:].split("\n")
    heading = " ".join(lines)
    childern = text_to_childern(heading)
    return ParentNode(f"h{count}", childern)
    
def block_code_to_html_node(block):
    nodes = []
    after_markdown = 4   # ```\n
    before_markdown = -4 # \n```
    childern = text_to_childern(block[after_markdown:before_markdown])
    return ParentNode("pre", [ParentNode("code", childern)])

def block_quote_to_html_node(block):
    #ugly code
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        # i think the check be low is point less because checking type before 
        # calling this function would not allow this error through
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    
    quote = " ".join(new_lines)
    childern = text_to_childern(quote)
    return ParentNode("blockquote", childern)

    
def block_unordered_list_to_html_node(block):
    nodes = []
    lines = block.split("\n")
    for line in lines:
        childern = text_to_childern(line[2:])
        nodes.append(ParentNode("li", childern))
    return ParentNode("ul", nodes)


def block_ordered_list_to_html_node(block):
    nodes = []
    lines = block.split("\n")
    for line in lines:
        childern = text_to_childern(line[3:])
        nodes.append(ParentNode("li", childern))
    return ParentNode("ol", nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        if type == block_type_paragraph:
            html_nodes.append(block_paragraph_to_html_node(block))
        if type == block_type_heading:
            html_nodes.append(block_heading_to_html_node(block)) 
        if type == block_type_code:
            html_nodes.append(block_code_to_html_node(block)) 
        if type == block_type_quote:
            html_nodes.append(block_quote_to_html_node(block)) 
        if type == block_type_unordered_list:
            html_nodes.append(block_unordered_list_to_html_node(block)) 
        if type == block_type_ordered_list:
            html_nodes.append(block_ordered_list_to_html_node(block)) 

    result = ParentNode("div", html_nodes) 
    return result