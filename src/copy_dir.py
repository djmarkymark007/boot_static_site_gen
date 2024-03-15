import os
import shutil

def copy_v2(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.chdir(dest_dir)
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(src_dir):
            shutil.copy(src_path, dest_path)
        else:
            copy_v2(src_path, dest_path)
    
        

def find_files(dir):
    files = []
    if not os.path.exists(dir):
        raise ValueError("directory does not exist")
    entries = os.listdir(dir)
    for entrie in entries:
        new_path = os.path.join(dir, entrie)
        if not os.path.isfile(new_path):
            files = files + find_files(new_path)
        else:
            files.append(new_path)
    return files
        
def find_next_slash(path):
    path_len = len(path)
    i = 0
    while i < path_len and path[i] != "/": 
        i += 1

    if i < path_len and path[i] == "/":
        return path[i:]
    return path 

def find_root(path):
    if path[0:2] == "./":
        return find_next_slash(path[2:])
    return find_next_slash(path)

def copy_file(old_path, new_path):
    print(f"copy {old_path} to {new_path}")
    parts = new_path.split("/")

    # root must not be /root
    part_path = parts[0]
    if not os.path.exists(part_path):
        os.mkdir(part_path)
    for part in parts[:-1]:
        part_path = f"{part_path}/{part}"
        if not os.path.exists(part_path):
            os.mkdir(part_path)

    shutil.copy(old_path, new_path)

def change_root(file, new_root):
    # if the file is the root append the file to the new root
    # other wise swap the old root with the new root
    path = find_root(file)
    return f"{new_root}{path}"

def copy_files(old_file_paths, to_dir):
    for old_file_path in old_file_paths:
        new_path = change_root(old_file_path, to_dir)
        copy_file(old_file_path, new_path)
    

def copy_dir(old_dir, new_dir):
    try:
        files = find_files(old_dir)
    except ValueError:
        print("The source directory doesn't exist")
        return

    copy_files(files, new_dir)


#Note(mark): boot's code below

def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
