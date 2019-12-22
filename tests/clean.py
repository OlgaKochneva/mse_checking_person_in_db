from os import remove
from glob import glob
from shutil import rmtree

files_to_remove = glob('*.csv') + glob('*.jpg') + glob('*.avi') + glob('*.mp4')

for item in files_to_remove:
    remove(item)

dirs_to_remove = glob('.pytest_cache')

for dir in dirs_to_remove:
    rmtree(dir)