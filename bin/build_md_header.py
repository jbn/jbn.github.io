#!/usr/bin/env python

import json
import os
import sys
import urllib
import yaml
import nbformat


def is_image_ext(name):
    name = name.lower()
    exts = ".jpeg, .jpg, .gif, .png, .bmp".split(", ")
    return any(name.endswith(ext) for ext in exts)


def identify_share_images(file_path, cfg):
    parts = os.path.split(file_path)
    name, ext = os.path.splitext(parts[-1])
    assert ext == '.ipynb'
    files_dir = os.path.join(*(parts[:-1] + (name + "_files",)))
    if not os.path.exists(files_dir):
        return False

    image_files = list(filter(is_image_ext, os.listdir(files_dir)))
    if image_files:
        base_url = cfg['base_url']
        url_path = os.path.join(files_dir, image_files[0])

        cfg['big_image'] = urllib.parse.urljoin(base_url, url_path)
        return True
    else:
        return False


def build_md_header(file_path):
    cfg = {}
    try:
        with open("config/defaults.json") as f:
            cfg.update(json.load(f).get('www_defaults', {}))
    except FileNotFoundError:
        pass


    nb = nbformat.read(file_path, as_version=4)
    cfg.update(nb['metadata'].get('www', {}))
    url_path = file_path.replace(".ipynb", ".html")
    cfg['url'] = urllib.parse.urljoin(cfg['base_url'], url_path)
    identify_share_images(file_path, cfg)

    return "---\n{}...\n".format(yaml.dump(cfg))


if __name__ == '__main__':
    file_name = sys.argv[-1]
    print(build_md_header(file_name))
