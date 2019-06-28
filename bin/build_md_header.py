#!/usr/bin/env python

import json
import os
import sys
import urllib
import yaml
import nbformat


def find_project_root():
    current_dir = os.getcwd()
    
    while not os.path.exists(os.path.join(current_dir, "dat.json")):
        current_dir = os.path.normpath(os.path.join(current_dir, os.path.pardir))
        
    return current_dir


def _read_nb_title_for_crumbs(file_path):
    nb = nbformat.read(file_path, as_version=4)
    return nb['metadata'].get('www', {}).get('title', file_path).lower()


def attach_crumbs(file_path, cfg):
    project_root = os.path.abspath(find_project_root())
    crumbs = []
    current_dir = os.path.abspath(os.path.join(os.path.curdir, os.path.dirname(file_path)))
    
    import sys
    print("\n\n1. ", current_dir, file=sys.stderr)
    
    # The home page doesn't need crumbs.
    if project_root == current_dir:
        return
    
    # Add italic title as a [you are here] marker.
    current_nb = file_path
    if not current_nb.endswith('index.ipynb'):
        title = _read_nb_title_for_crumbs(current_nb)
        crumbs.append(f"*{title}*")

    while True:
        index_file = os.path.join(current_dir, "index.ipynb")
        title = _read_nb_title_for_crumbs(index_file)
        url_path = index_file[len(project_root):-len("index.ipynb")]
        
        # The last crumb should be italicized, not linked.
        snippet = f"[{title}]({url_path})" if crumbs else f"*{title}*"
        crumbs.append(snippet)
        
        if current_dir == project_root:
            break

        current_dir = os.path.normpath(os.path.join(current_dir, os.path.pardir))
    
    cfg['crumbs'] = " &raquo; ".join(reversed(crumbs))


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
    attach_crumbs(file_path, cfg)

    return "---\n{}...\n".format(yaml.dump(cfg))


if __name__ == '__main__':
    file_name = sys.argv[-1]
    print(build_md_header(file_name))
