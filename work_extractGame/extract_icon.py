import shutil
import subprocess
import json
import os

# KAnimal-SE 下载地址[https://github.com/skairunner/kanimal-SE/releases]
PATH_KAnimal_cli = os.path.abspath("<KAnimal-CE cli执行文件所在路径>") # <你的KAnimal-CE解压目录路径>/kanimal-cli.exe
PATH_sprite_info_file = "<由OniExtract导出的tags.json的路径>"  # "<User Path>/Documents/Klei/OxygenNotIncluded/export/database/tags.json"
PATH_INPUT_KAnim = os.path.abspath("<游戏.assets文件解包后导出的目录>") #将所有TextAsset和Texture2D，复制至同一目录下。
PATH_OUTPUT_scml_dir = os.path.abspath("./scml_ba/")
PATH_OUTPUT_ui_dir = os.path.abspath('./ui/')


def extract(texture_name, ui_raw_name):
    """"导出图片"""
    args = get_agrs(texture_name)
    result = None
    try:
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except:
        print("Failed to extract: " + texture_name)

    if result:
        if result.returncode == 0:
            ui_name = ui_raw_name.split(":")[1]
            find_and_copy_ui(ui_name, args[-1], texture_name.rstrip("_0"))
        else:
            print("STDERR:", result.stderr)


def get_agrs(texture_name):
    """生成调用参数"""
    tuing_name = texture_name.rstrip("_0")
    texture_path = os.path.join(PATH_INPUT_KAnim, texture_name + ".png")
    build_file = tuing_name + "_build"
    anim_file = tuing_name + "_anim"
    build_file_path = find_and_rename_bytes_file(build_file)
    anim_file_path = find_and_rename_bytes_file(anim_file)
    return [PATH_KAnimal_cli, 'scml', texture_path, build_file_path, anim_file_path, '-o',
            os.path.join(PATH_OUTPUT_scml_dir, tuing_name)]


def find_and_rename_bytes_file(file_name):
    for filename in os.listdir(PATH_INPUT_KAnim):
        name, ext = os.path.splitext(filename)
        if (file_name == name):
            if ext.lower() != '.bytes':
                new_filename = name + '.bytes'
                old_file_path = os.path.join(PATH_INPUT_KAnim, filename)
                new_file_path = os.path.join(PATH_INPUT_KAnim, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")
                return new_file_path
            else:
                print(f"Skipped: {filename}")
                return os.path.join(PATH_INPUT_KAnim, filename)


def find_and_copy_ui(ui_name, ui_scml_path, scml_name):
    """筛选出ui图片，并重命名"""
    for filename in os.listdir(ui_scml_path):
        if ui_name in filename:
            source_path = os.path.join(ui_scml_path, filename)
            destination_path = os.path.join(PATH_OUTPUT_ui_dir, create_output_filename(scml_name))
            shutil.copy2(source_path, destination_path)
            return


def create_output_filename(scml_name):
    """"修改导出的文件名"""
    name = scml_name
    # name = name + "_ui"
    return name + ".png"


def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"目录 '{path}' 已创建.")
    else:
        print(f"目录 '{path}' 已存在.")


if __name__ == "__main__":
    create_directory_if_not_exists(PATH_OUTPUT_scml_dir)
    create_directory_if_not_exists(PATH_OUTPUT_ui_dir)
    with open(PATH_sprite_info_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data = data['uiSpriteInfos']
        for entityId, item in data.items():
            extract(item['textureName'], item['spriteName'])
