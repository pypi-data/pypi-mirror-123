import argparse


def parse_arguments():
    parser = argparse.ArgumentParser('Creating Object')

    parser.add_argument('--base_object_path',      '-bop', default = '_base_page')
    parser.add_argument('--base_locator_path',     '-blp', default = '_base_locator')
    parser.add_argument('--page_object_directory', '-pob', default='page_objects')
    parser.add_argument('--object_directory',      '-pd',  required=True)
    parser.add_argument('--object_name',           '-on',  required=True)
    parser.add_argument('--locator_directory',     '-ld',  required=True)

    return parser.parse_args()
