# Slot Checker

Automated appointment slot checking on the VFS Portal

If slots are available, will send an alert via phone call.

If not, will keep trying at regular intervals.

---

## Overview

Browser automation using Selenium.

Very narrow scope in this first prototype version.
- No incentive to generalize.
- If the project gains traction, then may start generalising few aspects for broader use cases.

Right now only works with Firefox;
- For Chrome, add the Chrome Driver to the path and update the initial driver instantion to webdriver.Chrome() from webdriver.Firefox().
	- Or something like that, verify the syntax yourself

Project requirement:
- Send alert if slot is available.

---

## Development Notes

Workflow:

1. Basic browser userflow automation, using selenium
2. Call trigger, using the twilio API
3. Cron Scheduler
4. Logging to file

---

## Usage Notes

### Basic Setup 

create conda env using local directory (conda create --prefix ./envs)

use the requirements files (either requirements.yml or requirements.txt) to create your environment

or finwhatever floats your boat, you know the drill

*NOTE:*

Could not resolve to a good clean solution/command for creating new conda env using the requirements files;

tread with caution; hacky solution will work;
- update README if solution is found

issue: twilio and a few other dependencies are not available on conda channels; need to install them with pip


### Selenium Setup 

https://www.selenium.dev/documentation/en/webdriver/driver_requirements/

install the web driver you need

and move it to the envs directory

quick reference from the selenium doc above

Chrome/Chromium -> https://chromedriver.storage.googleapis.com/index.html
Firefox	        -> https://github.com/mozilla/geckodriver/releases

and others are available in the documentation above

NOTE: Change the line in src/checker.py accordingly.

> self.driver = webdriver.Firefox()


### Twilio Console

https://www.twilio.com/blog/make-phone-call-python-twilio-programmable-voice

### Config

The config that is imported in `checker.py` is added to .gitignore for security reasons.

`config.py` contains a config dict which is imported.

Add the following dictionary to your config.py and update the values.


```
config_dict = {
	'username': 'email_id@email.com',
	'password': 'password',
	'call_origin': '+14XXXXXXXX5',
	'call_destination:' '+919XXXXXXXX3',
	'twiml_url': 'https://handler.twilio.com/twiml/EHxxxxa34wfds',
	'visa_application_center': "'Germany Visa Application Centre-Mumbai'",
	'appointment_category': "'Master student'",
	'login_url': "https://visa.vfsglobal.com/ind/en/deu/login"
}
```

Add these environment variables for twilio to work
get these from the twilio console
refer the tutorial below for reference

```
export TWILIO_ACCOUNT_SID=d718xxxxx70937073
export TWILIO_AUTH_TOKEN=7b6fbxxxxxxx2b
```


### Crontab Setup

#### Steps
using https://crontab.guru/ for the crontab formula

working solution for conda env
https://stackoverflow.com/a/60977676/11750716

1. Copy snippet appended by Anaconda in ~/.bashrc (at the end of the file) to a separate file ~/.bashrc_conda

2. In crontab -e add lines to run cronjobs on bash and to source ~/.bashrc_conda

	- Run "crontab -e" and insert the following before the cronjob:

```
SHELL=/bin/bash
BASH_ENV=~/.bashrc_conda
```

3. In crontab -e include at beginning of the cronjob conda activate my_env; as in example

	- Example of entry for a script that would execute at noon 12:30 each day on the Python interpreter within the conda environment:

	- At every 5th minute past every hour from 0800 through 1900 hrs.”

```
*/5 8-19 * * *  conda activate my_env; python /path/to/script.py; conda deactivate
```



---

## Reference

Useful links/reference used during development:

https://www.twilio.com/blog/make-phone-call-python-twilio-programmable-voice

https://towardsdatascience.com/how-to-schedule-python-scripts-with-cron-the-only-guide-youll-ever-need-deea2df63b4e
	
- https://unix.stackexchange.com/questions/454957/cron-job-to-run-under-conda-virtual-environment

https://docs.python.org/3/howto/logging.html
