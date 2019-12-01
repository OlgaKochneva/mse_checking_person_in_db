# mse_checking_person_in_db
## Welcome to our project!
Enjoy the full power of CNN and computer vision finding faces on video with mse_checking_person_in_db.
We tried to use the best libraries, namely `face_recognition` and `OpenCV`, to create this application.

![](https://user-images.githubusercontent.com/29632527/67632033-01857700-f8af-11e9-802a-4c99ebbab341.gif)
## Features
Use this application to find faces from video files .avi and .mp4.
Pass the path to the video file to the program and get output video with
highlighted in the square frames faces.

## Installation
#### Requirements
| System | Python |
| :---: | :---: |
| Ubuntu 18.04 | 3.6+, pip3 |

#### Installation options
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
3. Set up the environment, install dependencies and compile `dlib` for `face_recognition` library:
    ```bash
    ./setup.sh
    ```
## Usage    
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

4. Execute person_checker.py with video file as command line argument:
     ```bash
     python3 ./person_checker.py <path to videofile>
     ```
     If video is processed successfully, the message:

     ```
     result.avi created
     report.txt created
     ```

     will be displayed in terminal. The output video with found faces
     will be created in directory `videos`, the report will be created in `resources` directory.

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
Suppose you have video file "video.avi".
Open terminal in `checking_person_in_db` directory and run these commands:
   ```bash
    source .venv/bin/activate
    cd checking_person_in_db/
    python3 ./person_checker.py video.avi
   ```
If video file is processed succesfully, the output video with found faces
will be created in directory `resources`.


