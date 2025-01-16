# FIRST Robotics Competiton 2025 Season - Team 3340 - REEFSCAPE - Coding Repository

# Project Information:

## About & To-Do:
Code for the Reefscape 2025 robotics competition season.


## Getting your computer ready
Step 1: Installing Python 3.12 on your computer. _(For consistency, please install Python 3.12.7)_

- [Click here to download and install Python 3.12.7](https://www.python.org/downloads/release/python-3127/) for your operating system. PS: You can also use Homebrew or other package managers for your operating syste,.
- When downloading Python on Windows:
    - Click on custom installation and make sure that **"Install for All Users"** is selected. (on our computers, everything is selected)

Optional: Creating a Virtual Environment 
- It is recommended that you set up a virtual environment (venv) on your computer. That way, if something goes horribly wrong with the packages, you can just nuke the venv and make another one.
- To create a venv, type any of the following: 
    - `python -m venv ./(name-of-venv)`
    - `py -3 -m venv ./(name-of-venv)` (Windows)
    - `python3 -m venv ./(name-of-venv)`
- Note: if you have multiple versions of Python, you may need to specify that you want to create a venv for Python 3.12, as noted below:
    - `py -3.12 -m venv ./(name-of-venv)` (Windows)
    - `python3.12 -m venv ./(name-of-venv)`
- **WARNING**: ADD YOUR VENV TO .gitignore. PLEASE ADD THE NAME OF YOUR VENV TO THE .gitignore SO THAT YOUR COMMITS DO NOT TAKE FOREVER!!!


Step 2: Installing RobotPy and our dependencies
- On the root folder of this repository, you will find the following files: `reqs-2025.txt`, `reqs-2024.txt`.
- Currently, we are using `reqs-2024.txt` so that we can code on our existing roboRIOs. Eventually, we will compile our code for the latest version after updating our RIO's firmware.
- To install the dependencies, copy and paste this command on your terminal with your current directory as `reefscape-2025`:
    - `pip install -r reqs-2024.txt`
- This will install RobotPy as well as its additional dependencies, as well as OpenCV to allow for vision processing, if you are interested on working with Vision.


## Our RobotPy bible
For any of these commands, typing --help will tell you all its options. 
- `robotpy init`: create a new robot project
- `robotpy installer`: think of it as a way to load our stuff to the RIO. Be sure to install all our packages (robotpy, robotpy-ctre, robotpy-navx, robotpy-cscore, robotpy-rev) to the RIO before testing code (download then install).
- `robotpy sync`: downloads reqs for RIO and installs them locally
- `robotpy sim`: test code on computer
- `robotpy deploy`: send code to robot! be sure to connect to its WiFi network.


#### To-Do:
Vision (est. time pending) - Lehansa, Santi?

Elevator movement ~2 days - Samuel

### Documentation for Code:

Currently None :pensive:
