__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"


import os
import shutil
import zipfile


def main():
    clean_cache()
    cache_zip(
        os.path.join(os.getcwd(), "files", "data.zip"),
        os.path.join(os.getcwd(), "files", "cache"),
    )
    cached_files()
    print(find_password(cached_files()))


def clean_cache():
    if not os.path.exists(os.path.join(os.getcwd(), "files", "cache")):
        os.mkdir(os.path.join(os.getcwd(), "files", "cache"))
        print("Created the cache folder")
    else:
        shutil.rmtree(os.path.join(os.getcwd(), "files", "cache"), ignore_errors=False)
        os.mkdir(os.path.join(os.getcwd(), "files", "cache"))
        print("Cleared the cache folder")
    return


def cache_zip(zip_file_path, cache_dir_path):
    with zipfile.ZipFile(zip_file_path) as zip_ref:
        zip_ref.extractall(cache_dir_path)
        print("Unpacked zip file")
    return


def cached_files():
    path = os.path.abspath(os.path.join(os.getcwd(), "files", "cache"))
    cached_list = []
    for file in os.listdir(path):
        cached_list.append(os.path.join(path, file))
    return cached_list


def find_password(cached_list):
    for file in cached_list:
        with open(file, "r") as f:
            content = f.readlines()
            for file in content:
                if "password" in file:
                    password = file[file.find(" ") + 1 : file.find("\\n")]
                    return password


if __name__ == "__main__":
    main()
