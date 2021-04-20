import pathlib  
  
# Replace input() with your email
EMAIL = input('enter email: ') #'employee@chapman.edu'
 
 # Replace input() with your pass
PASSWORD = input('enter pass: ')

# executable path for chrome driver  
DRIVER_EXECUTABLE_PATH = pathlib.Path(__file__).parent.absolute().joinpath("chromedriver.exe")  
#DRIVER_EXECUTABLE_PATH = "/mnt/c/Python/chromedrivery.exe"
 
SKIP_LOGIN = False # Skin login on saved profiles