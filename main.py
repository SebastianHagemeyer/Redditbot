
# main.py


# imports
from chrome_driver_manager import manage_chrome_driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import random
import base64
import os
import re
import aud
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



############## Unorganised shit

from bs4 import BeautifulSoup

for i in range(0, 0): 
    current = links[i]
    print("page " + str(i))
   
    driver.get(current)  # visit each page

    # Selenium 4: Use 'By.CLASS_NAME' instead of 'find_element_by_xpath'
    title = driver.find_element(By.XPATH, '//a[contains(@class,"title")]')
    
    driver.execute_script("arguments[0].style.fontSize = '40px' ;", title)

    try:
        driver.execute_script("document.getElementsByClassName('pinnable-content')[0].classList = ''; ")  # remove video pin
    except Exception as e: 
        print(f"Error removing video pin: {e}")
    
    titlelink = title.get_attribute("href")
    print("titlelink: ", titlelink)
    
    mdir = "./" + str(i)
    for fname in os.listdir(mdir):
        if fname.startswith("media"):
            os.remove(os.path.join(mdir, fname))
        
    link = titlelink
    print(link)
    
    import retrive  # Assuming retrive is a module for downloading media
    
    retrive.retrive(link, "./" + str(i) + "/media")  # Get media

    # Capture page screenshot
    driver.get_screenshot_as_file('./' + str(i) + '/p.png')
    print("Getting post screenshot")

    # Selenium 4: Use 'By.XPATH'
    postElement = driver.find_element(By.XPATH, "//div[@class='entry unvoted']")
    screenshot_as_bytes = postElement.screenshot_as_png
    with open('postElement.png', 'wb') as f:
        f.write(screenshot_as_bytes)

    with open("postElement.png", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')

    titletext = title.get_attribute("innerHTML").encode('ascii', 'ignore')
    allTopics.append(str(titletext, "ascii"))

    if i == 0:
        firstTitle = str(titletext, "ascii")
        if len(firstTitle) > 70:
            firstTitle = ' '.join(firstTitle.split()[:9])
        print(firstTitle)
        # raw_input() # Not used in Python 3

    aud.audio(titletext, './' + str(i) + '/p.wav')

    # Find the comments section
    table = driver.find_element(By.XPATH, '//div[contains(@class,"nestedlisting")]')
    
    # Remove mod stuff
    try:
        stuck = table.find_element(By.XPATH, '//div[contains(@data-author,"AutoModerator") or contains(@class, "stickied")]')
        driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
        """, stuck)
    except Exception as e:
        print(f"Error removing moderator/stickied posts: {e}")

    # Collect comments
    comments = table.find_elements(By.XPATH, './/div[@class="md"]')

    for ii in range(0, 5):
        if ii == 0:
            driver.execute_script("""
                document.getElementsByClassName('commentarea')[0].style.background = '#e7e7e7';
                document.getElementsByTagName('body')[0].style.background = '#e7e7e7';
                var elemDiv = document.createElement('div');
                elemDiv.style.cssText = 'position: fixed;top: 30%;right: 45%';
                document.body.appendChild(elemDiv);
                elemDiv.innerHTML='<img style="display:block;max-width:400px;max-height:400px;width: auto;height: auto;" class="preview" src="data:image/png;base64,""" + b64_string + """">';
            """)

        element = comments[ii]
        driver.execute_script("arguments[0].style.cssText = 'font-size:30px; position:relative;z-index:1; background-color:white;';", element) 
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.UP)
        driver.get_screenshot_as_file('./' + str(i) + '/' + str(ii) + '.png')

        text = element.get_attribute("innerHTML")
        text = re.sub('<blockquote.*?>(.|\n)*?</blockquote>', "Quote.", text)
        soup = BeautifulSoup(text, "html.parser")
        
        cleantext = soup.get_text()  # Get the raw comment without weird symbols
        cleantext = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', 'Link.', cleantext)
        if len(cleantext) > 300:
            print("LARGE TEXT")
            dotpos = cleantext.find('.')
            if dotpos > 0:
                cleantext = cleantext[:dotpos]
        
        aud.audio(cleantext.encode('ascii', 'ignore'), './' + str(i) + '/' + str(ii) + 'a.wav')

        print("COMMENT " + str(cleantext.encode('ascii', 'ignore')))

#aud.audio(("Welcome to reddit, what's up today " + random.choice(viewers) + "?").encode('ascii', 'ignore'), './pic.wav')

#aud.audio(("Thank you for watching " + random.choice(viewers) + "! Don't forget to smash like and subscribe."), './out.wav')

aud.audio(f"Welcome to reddit, what's up today {random.choice(viewers)}?".encode('ascii', 'ignore'), './Out/pic.wav')
aud.audio(f"Thank you for watching {random.choice(viewers)}! Don't forget to smash like and subscribe.".encode('ascii', 'ignore'), './Out/out.wav')

print("Ready to compile")


import compile ############################################ put video together


print("Upload")

driver.quit()






