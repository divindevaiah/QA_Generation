# QA_Generation

This tool generates questions and provides corresponding answers from a paragraph given to the algorithm.

## Prerequisites

Software needed to run this repository:

- [Ubuntu 16.04](https://ubuntu.com/download/desktop)
- Python 2.7 / 3.6

## Installation

**Note 1:** If you have a default Anaconda environment sourced when opening a terminal, you must deactivate it by doing ```conda deactivate``` in terminal. 


### Python virtual environment

Open terminal to install pip and virtual environment

```
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv (outdated)
sudo apt-get install python3-venv
```

### Clone repository and install requirements

Clone this repository in your computer

```
git clone https://github.com/divindevaiah/QA_Generation.git
```

Create a python environment in main folder

```
cd QA_Generation/
python3 -m venv env
```

This will create a folder called ```env``` where all the packages required to run this software will be stored.

Now activate python environment 

```
source env/bin/activate
```

Install requirements in python environment

```
pip install -r requirements.txt
```

## Run

Open a terminal and do

cd QA_generation/
source env/bin/activate
cd src/
python3 app.py
```

A local host has been created at ```http://127.0.0.1:5000/```. Go to that page in your browser and start using the application.


## Built With

* [Flask](https://www.palletsprojects.com/p/flask/) - Web framework

##  Authors 

- [Ragith Ayyappan Kutty](https://github.com/rkutty1)
- [Devaiah Ulliyada Arun](https://github.com/divindevaiah)

# QA_Generation
# QA_Generation
# QA_Generation
