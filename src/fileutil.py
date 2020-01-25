import os
import errno


def write_file(file_name, file_content):

    if not os.path.exists(os.path.dirname(file_name)):
        original_umask = os.umask(0)
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        finally:
            os.umask(original_umask)

    file_out = open(file_name, "w")
    file_out.write(file_content)
    file_out.close()


def read_file(file_path):
    path = os.path.abspath(".")
    ret = {}

    if file_path:
        path = file_path
    if os.path.isfile(path):
        with open(path, 'r') as handle:
            ret = handle.read()
    return ret
