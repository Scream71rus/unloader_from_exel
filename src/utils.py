
import functools
import os


def compose(*functions):
    def compose2(f, g):
        return lambda x: f(g(x))

    return functools.reduce(compose2, functions, lambda x: x)


def get_in_path(path, source):
    for v in path:
        if not source:
            continue
        if isinstance(source, list):
            source = source[v]
            continue
        source = source.get(v)

    return source


def make_ext(func):
    def wrapper(file_path, ext):
        return func(file_path, tuple(map(lambda x: '.%s' % x, ext)))

    return wrapper


def is_folder_exists(folder_path):
    return os.path.isdir(folder_path)


@make_ext
def get_files_by_ext(folder_path, ext):
    files_list = []
    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if file.endswith(ext) and os.access(full_path, os.R_OK) and os.stat(full_path):
            files_list.append(file)
    return files_list


def mb_to_bytes(mb):
    return mb*1024*1024


def get_files_by_filename(folder_path, filename, max_file_size=None):
    result = []
    for path, folder_list, file_list in os.walk(folder_path):
        for name in file_list:
            if filename.strip() in name.strip():
                if max_file_size and os.stat(os.path.join(path, name)).st_size > mb_to_bytes(max_file_size):
                    continue

                result.append({
                    'name': name,
                    'path': path
                })

    return result

