import sys
import os
import shutil
import tempfile
from zipfile import ZipFile
import re

def partition(pred, iterable):
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses

word_text_re = re.compile('<w:t.*?>(.*?)</w:t>', flags=re.DOTALL)
def docxml_to_text(xml):
    return '\n'.join(word_text_re.findall(xml))

def path_to_text(path, temp_dir):
    out_dir = os.path.join(temp_dir, os.path.splitext(path)[0])

    with ZipFile(path, 'r') as zf:
        zf.extractall(out_dir, members=
            [m for m in zf.namelist() if m[0] != '/' and m[0] != '.'])

    with open(os.path.join(out_dir,'word/document.xml'), 'r') as doc:
        return docxml_to_text(doc.read())

def process_path(path, temp_dir):
    try:
        text = path_to_text(path, temp_dir)
    except:
        print path
        sys.exit(1)
    out_path = os.path.splitext(path)[0] + '.txt'
    with open(out_path, 'w') as f:
        f.write(text)

def main():
    current_dir = os.getcwd()
    dirs, files = partition(os.path.isdir, sys.argv[1:])
    files.extend(os.path.join(d, f) for d in dirs for f in os.listdir(d) if f[0] != '.')

    temp_dir = tempfile.mkdtemp()

    for path in files:
        process_path(path, temp_dir)

    shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main()
