# joi-skill-mainmenu

## Managing Skill Installations
All of these Mycroft Skills Manager (mycroft-msm) commands are executed on the Raspberry Pi

### Install Skill
    cd ~/mycroft-core/bin
    ./mycroft-msm install https://github.com/TySeddon/joi-skill-mainmenu.git

### Remove Skill    
    cd ~/mycroft-core/bin
    ./mycroft-msm remove joi-skill-mainmenu.tyseddon

### Bash Script to automate updating of skills
In home director create file called update-skills.sh
    #!/bin/bash

    echo "----Updating joi-skill-utils----"
    cd ~/mycroft-core
    source ./venv-activate.sh
    pip install git+https://github.com/TySeddon/joi-skill-utils -q

    cd ~/mycroft-core/bin

    echo "----Uninstalling joi-skill-mainmenu----"
    ./mycroft-msm remove joi-skill-mainmenu.tyseddon
    echo "----Uninstalling skill-homeassistant----"
    ./mycroft-msm remove skill-homeassistant
    ./mycroft-msm remove skill-homeassistant.tyseddon
    echo "----Uninstalling joi-skill-music----"
    ./mycroft-msm remove joi-skill-music.tyseddon
    echo "----Uninstalling joi-skill-photo----"
    ./mycroft-msm remove joi-skill-photo.tyseddon

    echo "----Installing joi-skill-mainmenu----"
    ./mycroft-msm install https://github.com/TySeddon/joi-skill-mainmenu.git
    echo "----Installing skill-homeassistant----"
    ./mycroft-msm install https://github.com/TySeddon/skill-homeassistant.git
    echo "----Installing joi-skill-music----"
    ./mycroft-msm install https://github.com/TySeddon/joi-skill-music.git
    echo "----Installing joi-skill-photo----"
    ./mycroft-msm install https://github.com/TySeddon/joi-skill-photo.git

    echo "Clearing pycache"
    py3clean /opt/mycroft
    py3clean ~/mycroft-core

    echo "Restarting Skills"
    cd ~/mycroft-core
    ./start-mycroft.sh skills restart    

## Virtual Environment Setup

### Install Virtual Environment
    pip install virtualenv

### Creating 
    python -m venv venv

### Activate Virtual Environment
    .\venv\Scripts\activate

# Required Packages
    pip install msk
    pip install adapt-parser
    pip install git+https://github.com/TySeddon/joi-skill-utils

## Mycroft 
NOTE: It is recommended that you install the Mycroft package into your virtual environment.  However, this package does not exist on your computer, unless you have mycroft installed.  On Windows, this is not possible.  The simplest workaround is to clone the git hub repository to somewhere on your computer's harddrive, then copy the "mycroft" folder to .venv/Lib/site-packages.
Repo is here: https://github.com/MycroftAI/mycroft-core

## Update requirements.txt
    pip freeze > requirements.txt

