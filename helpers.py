from IPython.display import Markdown
import fnmatch
import json
import os
import urllib

import ipykernel
import nbformat
from notebook import notebookapp

IGNORE_DIRS = {"assets", "templates"}

def is_ignored_dir(fname):
    return fname.startswith(".") or fname.startswith("_") or fname in IGNORE_DIRS


def list_dir():
    content = ""
    for a, dir_paths, file_paths in os.walk(os.getcwd()):
        nb_paths = fnmatch.filter(file_paths, "*.ipynb")

        pages = []
        for nb_path in nb_paths:
            if nb_path == 'index.ipynb':
                continue
            link = nb_path.replace(".ipynb", ".html")
            nb = nbformat.read(nb_path, as_version=4)
            metadata = nb['metadata'].get('www', {})
            title = metadata.get('title', nb_path)
            subtitle = metadata.get('subtitle', "")

            pages.append("- [{}]({}) {}\n".format(title, link, subtitle))
        if pages:
            content += "## Pages\n\n{}\n".format("\n".join(pages))

        sub_dirs = []
        for f in dir_paths:
            if f.startswith(".") or f.startswith("_") or f in IGNORE_DIRS:
                continue
            if os.path.exists(os.path.join(f, "index.ipynb")):
                sub_dirs.append("- [{}]({})".format(f, f))
                
        sub_dirs = sorted(sub_dirs)
        
        if sub_dirs:
            content += "## Sub Directories\n\n{}\n".format("\n".join(sub_dirs))

        break
    
    return Markdown(content)


# Source: https://stackoverflow.com/questions/12544056/
def notebook_path():
    """Returns the absolute path of the Notebook or None if it cannot be determined
    NOTE: works only when the security is token-based or there is also no password
    """
    connection_file = os.path.basename(ipykernel.get_connection_file())
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]

    for srv in notebookapp.list_running_servers():
        try:
            if srv['token']=='' and not srv['password']:  # No token and no password, ahem...
                req = urllib.request.urlopen(srv['url']+'api/sessions')
            else:
                req = urllib.request.urlopen(srv['url']+'api/sessions?token='+srv['token'])
            sessions = json.load(req)
            for sess in sessions:
                if sess['kernel']['id'] == kernel_id:
                    return os.path.join(srv['notebook_dir'],sess['notebook']['path'])
        except:
            pass  # There may be stale entries in the runtime directory 
    return None

