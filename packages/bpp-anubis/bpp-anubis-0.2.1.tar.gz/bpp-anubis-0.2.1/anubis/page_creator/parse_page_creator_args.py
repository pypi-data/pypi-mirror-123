import argparse


def parse_arguments():
    parser = argparse.ArgumentParser('Creating Object')

    parser.add_argument('--base_object_path',      '-bo', default = '_base_page')
    parser.add_argument('--base_locator_path',     '-bl', default = '_base_locator')
    parser.add_argument('--page_object_directory', '-pd', default='page_objects')
    parser.add_argument('--object_directory',      '-obj_dir',  required=True)
    parser.add_argument('--object_name',           '-name',  required=True)
    parser.add_argument('--locator_directory',     '-loc_dir',  required=True)

    return parser.parse_args()
