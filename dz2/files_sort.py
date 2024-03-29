import sys
import os

def files_sort(directory_path):
    files_dict = {}
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file)[1]
            if file_extension not in files_dict:
                files_dict[file_extension] = []
            files_dict[file_extension].append(file)

    result = []
    for extension in sorted(files_dict.keys()):
        for file in sorted(files_dict[extension]):
            result.append(file)
    return result


if __name__ == "__main__":
    directory_path = sys.argv[1]
    files = files_sort(directory_path)
    for file in files:
        print(file)