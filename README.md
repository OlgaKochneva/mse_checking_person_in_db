# mse_checking_person_in_db
## Welcome to our project!
Enjoy the full power of CNN and computer vision finding faces on video and checking their presence in database with mse_checking_person_in_db.
We tried to use best libraries, namely `face_recognition` and `OpenCV`, to create this application.

![res](https://user-images.githubusercontent.com/31550284/71313346-a43e1a00-2448-11ea-855a-24212cbf605a.gif)

## Table of contents
- [Features](#Features)
- [Installation](#Installation)
  * [Requirements](#Requirements)
  * [Installation options](#Installation-options)
- [Usage](#Usage)
  * [Mandatory actions](#Mandatory-actions)
  * [Database administration](#Database-administration)
  * [Checking faces presence in database](#Checking-faces-presence-in-database)
- [Contributing](#Contributing)
- [Authors](#Authors)
- [Example](#Example)

## Features
Use this application to find faces from video and check their presence in database. The project supports .mp4 and .avi video formats.

## Installation
#### Requirements
| System | Python | Distributions
| :---: | :---: |:---: |
| Ubuntu 18.04 | 3.6+, pip3 | MongoDB

#### Installation options
If you don't have MongoDB, visit https://docs.mongodb.com/manual/administration/install-community/.<br>
Make sure you have `virtualenv` and `cmake`.
Install them using:
   ```bash
   pip3 install virtualenv
   sudo apt-get install cmake
   ```
Open terminal and follow these steps:
1. Clone this repo:
    ```bash
    git clone https://github.com/moevm/mse_checking_person_in_db.git
    ```
2. Change directory to `mse_checking_person_in_db`:
    ```bash
    cd mse_checking_person_in_db/
    ```
3. Set up the environment:
    ```bash
    ./setup.sh
    ```  
>If `dlib` library has not been installed correctly by pip, install it manually using following set of commands.  
>In this case, `dlib` would be installed in `~/.dlib` folder.
>```
>git clone https://github.com/davisking/dlib.git ~/.dlib  
>cd ~/.dlib  
>mkdir build; cd build; cmake ..; cmake --build .  
>cd ..  
>python3 setup.py install  
>```   
## Usage

### Mandatory actions
Remember to launch MongoDB before using project:
   ```bash
    sudo service mongod start
   ```
Further it's assumed that you launched MongoDB.

### Database administration

Open terminal in `checking_person_in_db` directory and execute `db_interface.py`:
   ```bash
      python3 ./db_interface.py [--add-group, -ag][--path=directory]
   ```
More options:
   ```bash
        --list, -l, show                list of persons in db
        --delete, -d                    delete person from db
        --add-group, -ag                add group of persons to db
        --add-person, -ap               add single person to db
        --name                          name of person to add/remove
        --path,                         path to image data
        --help, -h                      print command line options
   ```
     
### Checking faces presence in database
   
Open terminal and follow these steps:
1. Log in as root to use keyboard interrupts.
    
    ```bash
    sudo su
    ```
    
2. Activate virtual environment:

    ```bash
    source .venv/bin/activate
    ```

3. Change directory to `checking_person_in_db`:
    ```bash
    cd checking_person_in_db/
    ```

4. Execute person_checker.py:
     ```bash
     python3 ./person_checker.py [options] [-s video source|--source=video source]
   
    Options:
        --source, -s                    file path or cam id
        --skip-frames                   number of skipped frames
        --tolerance                     comparison accuracy (from 0 to 1)
        --upsample-times                processing quality
        --report, --no-report           generate report
        --video, --no-video             generate processed video
        --help, -h                      print command line options
     ```
     If video is processed successfully, the message:

     ```
     video_<timestamp>.mp4 created
     report.txt created
     ```

     will be displayed in terminal. The output video (if you set `--video` flag) and the report will be created in `checking_person_in_db/out/`
     directory.

## Contributing
Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.
Report bugs at https://github.com/moevm/mse_checking_person_in_db/issues.
If you are reporting a bug, please apply label "bug" and  include:
* Any details about your local setup that might be helpful in troubleshooting;
* Detailed steps to reproduce the bug.

## Authors
* [Olga Kochneva](https://github.com/OlgaKochneva)
* [Sergey Petrov](https://github.com/SuperSolik)
* [Antay Yuskovets](https://github.com/VeselAbaya)
* [Denis Derzhavin](https://github.com/Derzhavin)  

## Example
It's assumed that you launched MongoDB.
Let's create database and check faces presence on video.<br>
Suppose you have video file "video.avi" and `persons` directory tree as below:
   ```bash
    .
    +-- _persons
    |   +-- _person1
    |       +-- img1.png
    |       +-- img2.png
    |       ...
    |       +-- img<n>.png
    |   +-- _person2
    |       +-- ...
    |   ...
    |   +-- _person<n>
    |       +-- ...
   ```
Follow these steps:
1. Open terminal in `checking_person_in_db` and activate `virtualenv`:

   ```bash
     source .venv/bin/activate
   ```
2. Execute `db_interface.py`:

   ```bash
    python3 db_interface.py -ag persons
   ```
3. As `db_interface.py` completes run `person_checker.py`:

   ```bash
    python3 ./person_checker.py -s video.avi 
   ```
If video file is processed succesfully, the output video with found faces
and the report will be created in `checking_person_in_db/out/` directory.


