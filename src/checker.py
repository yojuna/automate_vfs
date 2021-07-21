from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


from src.call_trigger import make_call

# import credentials from a config file
from src.config import config

import logging  
import time
import os


# # for adding Geckodriver to path
# os.environ["PATH"] += os.pathsep + '../envs'

class driverMan(object):
	def __init__(self):
		# options = Options()
		# # headless firefox
		# # Currently uncommented as going headless creates 
		# # breaking changes; defering for later
		# options.headless = True

		# # initialize the web driver; use Chrome() for chrome after downloading the relevant driver file
		# self.driver = webdriver.Firefox(options=options)

		# initialize the web driver; use Chrome() for chrome after downloading the relevant driver file
		self.driver = webdriver.Firefox()

		self.login_url = config['login_url']
		self.dashboard_url = "https://visa.vfsglobal.com/ind/en/deu/dashboard"
		# self.application_url = "https://visa.vfsglobal.com/ind/en/deu/application-detail"

		self.username = config['username']
		self.password = config['password']

		self.vac = config['visa_application_center']
		self.appointment_category = config['appointment_category']
		self.appointment_sub_category = config['appointment_sub_category']
		
		self.flag = 0

	# sleeper function required for letting the page to load
	# hard coded heuristic values used
	def sleeper(self, marker, sleep_time):
		logging.info('going to sleep for %s s >> %s', sleep_time, marker)
		time.sleep(sleep_time)
		logging.info('woke up')


	def login_process(self):
		self.driver.get(self.login_url) 

		# wait for DOM to load; JS to execute
		elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-placeholder="jane.doe@email.com"]')))

		logging.info('IN LOGIN | Current URL: %s', self.driver.current_url)

		self.sleeper('login creds', 5)

		username_field = self.driver.find_element_by_css_selector('input[formcontrolname="username"]')
		username_field.send_keys(self.username)

		password_field = self.driver.find_element_by_css_selector('input[formcontrolname="password"]')
		password_field.send_keys(self.password)

		self.sleeper('login submit button', 5)

		self.driver.find_element_by_class_name('mat-btn-lg').click()
		logging.info('login process complete. proceeding to booking page')

	def make_booking(self):
		self.sleeper('make booking', 5)

		logging.info('BOOKING | Current URL: %s', self.driver.current_url)

		# added handler for 'Multiple Attempts' error
		# clicks the link for Login Screen and
		# recursively calls the login_process() and make_booking() functions

		if self.driver.current_url == self.dashboard_url:
			self.sleeper('for button not in view error', 2)
			elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-brand-orange')))

			self.driver.find_element_by_class_name('btn-brand-orange').click()
			logging.info('booking page process complete. proceeding to selection page')
		else:
			self.sleeper('wait to resolve multiple attempts error', 5)
			# call handler()
			self.driver.find_element_by_link_text("Go back to home →").click()

			self.sleeper('back to LOGIN', 5)

			if self.driver.current_url == self.login_url:
				self.flag += 1
				if self.flag < config['retry_attempts']:
					logging.info('lets do this one more time; calling main() recursively')
					self.login_process()
					self.make_booking()
				else:
					logging.info('retry_attempts exhuasted')
					raise Exception('break out of the program | retries exhausted')
			else:
				logging.info('weird error; running away')
				raise Exception('break out of the program | going home')



	def selection(self):
		self.sleeper('selection', 5)
		logging.info('Current URL: %s', self.driver.current_url)

		self.driver.find_element_by_xpath("//span[contains(text(), 'Choose your Visa Application Centre')]").click()
		self.sleeper('Choose VAC', 2)
		self.driver.find_element_by_xpath("//span[contains(text(), "+ self.vac +")]").click()
		self.sleeper('VAC Chosen', 5)
		
		self.driver.find_element_by_xpath("//span[contains(text(), 'Select your appointment category')]").click()	
		self.sleeper('Choose appointment category', 2)
		self.driver.find_element_by_xpath("//span[contains(text(), "+ self.appointment_category +")]").click()
		self.sleeper('Appointment category selected', 5)

		## commenting out for speed, as the third option (appointment_sub_category) 
		## is automatically selected by the portal
		# self.driver.find_element_by_xpath("//span[contains(text(), 'Select your sub-category')]").click()	
		# self.sleeper('Choose appointment category', 2)
		# self.driver.find_element_by_xpath("//span[contains(text(), "+ self.appointment_sub_category +")]").click()
		# self.sleeper('Appointment category selected', 5)


		try: 
			alert = self.driver.find_element_by_class_name('alert')
			alert_text_ = alert.text
			logging.info('slots status: %s', alert_text_)
			# looking for a specific alert message
			# What I Want >> Earliest Available Slot : 23/07/2021 
			# What I Get  >> No appointment slots are currently available 
			if (alert_text_.find('Earliest Available Slot') == -1):
				logging.info('Slot not found. Trying Again')
			else:
				logging.info('initiating trigger for call')
				make_call()
				logging.info('call complete')				
		except:
			logging.info('ERROR: alert not found')
			logging.info('Current URL: %s', self.driver.current_url)

		logging.info('selection page process complete. proceeding to closing browser')
		# self.close_browser()

	def close_browser(self):
		self.driver.quit()
		logging.info('shutting down browser gracefully')
