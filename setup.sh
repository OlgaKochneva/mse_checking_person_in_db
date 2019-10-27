#!/usr/bin/env bash
PROJECT_DIR=`echo $PWD`
python3 -m virtualenv .venv
source .venv/bin/activate

git clone https://github.com/davisking/dlib.git ~/.dlib
cd ~/.dlib
mkdir build; cd build; cmake ..; cmake --build .
cd ..
python3 setup.py install
# Back to project directory
cd $PROJECT_DIR
python3 -m pip install -r ./requirements.txt