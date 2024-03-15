from textnode import TextNode
from copy_dir import copy_dir
from generate import generate_pages_recursive 
import os, shutil

dir_path_static = "./static"
dir_path_public = "./public"

if __name__ == "__main__":

    print("Deleting public directory")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_dir(dir_path_static, dir_path_public)

    generate_pages_recursive("./content", "./template.html", "./public")
    
