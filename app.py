from src.main import main
import os

# for adding Selenium Geckodriver to path
os.environ["PATH"] += os.pathsep + 'envs'

if __name__ == "__main__":
	main()