import sys
import os

def file_search(file_name):
    directory = os.getcwd()
    result = []
    for path, dirs, files in os.walk(directory):
        if file_name in files:
            file_path = os.path.join(path, file_name)
            with open(file_path, 'r') as file:
                for _ in range(5):
                    line = file.readline()
                    if not line:
                        break
                    result.append(line.rstrip())

            return result
    return f"файл {file_name} не найден"


if __name__ == "__main__":
    file_name = sys.argv[1]
    result = file_search(file_name)
    if isinstance(result, str):
        print(result)
    else: 
        for strin in result:
            print(strin)