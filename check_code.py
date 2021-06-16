import utils
import os
import os.path as path

for root, subdirs, files in os.walk(utils.DIR_CODE):
    for file in files:
        if not file.endswith(".cs"):
            continue

        f_path = path.join(root, file)
        with open(f_path, 'rb') as f:
            f_content = f.read().decode("utf-8")
            if input("Enter string to search in code") in f_content:
                print(f_path)
