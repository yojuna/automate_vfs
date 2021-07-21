import time
import sys
import logging

from checker import driverMan

def main():
	logging.basicConfig(
		filename='debug_log.log', 
		encoding='utf-8', 
		level=logging.DEBUG,
		format='%(asctime)s %(levelname)-8s %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S'
		)
	# to print to stdout
	logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
	
	starttime = time.time()
	doer = driverMan()
	try:
		logging.info('Logging in')
		doer.login_process()
		doer.make_booking()
		doer.selection()
		logging.info('Elapsed time: %s seconds', time.time() - starttime)
	except:
		logging.info('ERROR. closing browser')
		logging.info('Current URL: %s', doer.driver.current_url)

	doer.close_browser()
	logging.info('xxxxxxxxxxxxxxxxxxxxxx  fin  xxxxxxxxxxxxxxxxxxxxxx')


if __name__ == "__main__":
	main()