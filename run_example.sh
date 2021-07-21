#!/bin/bash


# cd to working directory
cd to/path/automate_vfs


# add the conda initialize from ~/.bashrc

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/$USER/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/$USER/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/$USER/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/$USER/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<


conda activate ./envs

# add the twilio credentials
export TWILIO_ACCOUNT_SID=d718xxxxx70937073
export TWILIO_AUTH_TOKEN=7b6fbxxxxxxx2b

python app.py