import os
from markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line.startswith("# ")
        return line[2:]
    raise ValueError("markdown file does not have an h1 header")

def read_file(filepath):
    if not os.path.exists(filepath):
        raise ValueError("file does not exist")
    file = open(filepath, "r")
    text = file.read()
    file.close()
    return text

def write_file(content, dest_path):
    parts = dest_path.split("/")
    temp_path = parts[0] 
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    for part in parts[1:-1]:
        temp_path = f"{temp_path}/{part}"
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
    
    if os.path.exists(dest_path):
        file = open(dest_path, "w")
    else:
        file = open(dest_path, "x")
    file.write(content)
    file.close()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file(from_path)
    template = read_file(template_path)

    html_nodes = markdown_to_html_node(markdown)
    content = html_nodes.to_html() 

    markdown_title = extract_title(markdown)
    template = template.replace("{{ Title }}", markdown_title)
    template = template.replace("{{ Content }}", content)

    dest_path = dest_path.replace(".md", ".html")
    write_file(template, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    for items in os.listdir(dir_path_content):
        new_content_path = os.path.join(dir_path_content, items) 
        new_dest_path = os.path.join(dest_dir_path, items)

        if os.path.isfile(new_content_path):
            print(f"generating page from {new_content_path} to {new_dest_path.replace(".md", ".html")}")
            generate_page(new_content_path, template_path, new_dest_path)
        else:
            print(f"generating page from {new_content_path} to {new_dest_path}")
            generate_pages_recursive(new_content_path, template_path, new_dest_path)

#NOTE(Mark): boot's code below
from pathlib import Path
def generate_pages_recursive_v2(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive_v2(from_path, template_path, dest_path)
