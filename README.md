# Group 9

Tuesday Tutorial

Akshar Gajjar  
Devin Ramaswami  
Benjamin Fehr  
Travis Baldwin  
Yee Jing Shin  

# Compilation Instruction

Setup a virtual environment:
`python -m venv venv`

After creating the virtual environment the next step is to clone the repo:
`git clone https://git.cs.usask.ca/CMPT370-01-2020/group9.git`

once you have cloned the repo you can activate the virtual environment using:
`source venv/Scripts/activate`

after activating the virtual environment, please make sure you are in the group9 directory:
`cd group9/`

Install 3rd party libraries:
`pip install -r requirements.txt`

Run Program:
`python loginRegisterGUI.py`


How do we run tests?
At the moment none of our tests are runnable. This is because of the drastic changes we made to the code in order to implement a GUI. The main reason behind this error is the fact we didn’t update the tests as the code changed. In hindsight we should have written tests as we developed code instead of creating tests at an early stage. However, to show that the testing was working and the functions that were implemented prior to the GUI changes were successfully unit tested, we have included some test result log files showcasing successful testing.
