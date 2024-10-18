
# main.py


# imports
from chrome_driver_manager import manage_chrome_driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  
from selenium import webdriver
import random
import base64
from PIL import Image


from chrome_driver_manager import manage_chrome_driver

# Manage ChromeDriver
manage_chrome_driver()

# Provide the correct path to the ChromeDriver executable
myPATH = "C:/Automate/RedditBot"
chrome_driver_path = f"{myPATH}/chrome/chromedriver.exe"  # Chrome driver path
user_data_dir = f"{myPATH}/selenium"  # Path to store user profile data


# Initialize the Service object with the correct ChromeDriver path
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver with the Service object

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={user_data_dir}")  # Set custom user profile directory

# Initialize the WebDriver with the Service object and custom options
driver = webdriver.Chrome(service=service, options=chrome_options)

#Window size
driver.set_window_size(1280+16, 720+132)

# Functions

def paste_image(background_path, logo_path, output_path, position='center'):
    bg_img = Image.open(background_path)
    logo_img = Image.open(logo_path)

    if position == 'center':
        paste_position = (int(bg_img.width / 2 - logo_img.width / 2), int(bg_img.height / 2 - logo_img.height / 2))
    else:
        paste_position = (int(bg_img.width / 2 - logo_img.width / 2), 0)
    
    bg_img.paste(logo_img, paste_position, logo_img)
    bg_img.save(output_path)


#Pick sub
subname = random.choice(["gifs", "mildlyinteresting", "funny", "popular"])#"gifs" #gifs, popular, funny
url="https://old.reddit.com/r/"+subname+"/top"

viewers = ['bros', 'brothers', 'gals and pals', 'viewers', 'guys']


driver.get(url)

## Get intro and outro
driver.get_screenshot_as_file('./Out/pic.png')


paste_image('./Out/pic.png', './Resources/logo.png', './Out/pic.png', position='top')
paste_image('./Out/pic.png', './Resources/likesub.png', './Out/out.png')

## Lets get the content

links = []
allTopics = []

# Get all posts that are not promoted
x = driver.find_elements(By.XPATH, '//div[contains(@class,"thing") and not(contains(@class, "promoted"))]')

for sub in x:
    href = sub.get_attribute('data-context')
    if href == "listing":
        print(href)
        # Find the link to the comments
        acomment = sub.find_element(By.XPATH, './/a[contains(@class,"comments")]')
        link = acomment.get_attribute("href")
        links.append(link)

print(links)





driver.quit()


