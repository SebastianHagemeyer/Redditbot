import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json
import time
import subprocess
import aud
import random
import base64


import chromedriver_autoinstaller


chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path


myPATH = "E:\\RedditBot"

import pathlib
#save login
chrome_options = Options()
##temp
#chrome_options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"

scriptDirectory = pathlib.Path().absolute()
chrome_options.add_argument(f"user-data-dir={scriptDirectory}\\selenium") 
driver = webdriver.Chrome(options=chrome_options)

driver.set_window_size(1280+16, 720+132)

subname = random.choice(["gifs", "mildlyinteresting", "funny", "popular"])#"gifs" #gifs, popular, funny
url="https://old.reddit.com/r/"+subname+"/top"

viewers = ['bros', 'brothers', 'gals and pals', 'viewers', 'guys']


driver.get(url)
driver.get_screenshot_as_file('./pic.png')
#input()
### paste reddit logo onto landing page
from PIL import Image
til = Image.open("./logo.png")
im = Image.open("./pic.png") 
im.paste(til, (int(im.width/2 - til.width/2),0), til)

im.save("./pic.png")

### out page
til = Image.open("./likesub.png")
im = Image.open("./pic.png") 
im.paste(til, (int(im.width/2 - til.width/2),int(im.height/2 - til.height/2)), til)
im.save("./out.png")
###


firstTitle= "test"
links = []

allTopics = []

x = driver.find_elements_by_xpath('//div[ contains(@class,"thing") and not (contains(@class, "promoted")) ]') # create list with all visible posts that aren't ads

for sub in x:
    
    href = sub.get_attribute('data-context')
    if(href == "listing"):
        print(href)
        acomment = sub.find_element_by_xpath('.//a[contains(@class,"comments") ]')
        #and contains(@class ,"bylink")
        #bylink
        link = acomment.get_attribute("href")
        #print(link)
        #raw_input()
        links.append(link)
        
        

print(links)

from bs4 import BeautifulSoup

for i in range(0,5): 
    current =  links[i]
    print("page " + str(i))
   
    driver.get(current) # visit each page

    title = driver.find_element_by_xpath('//a[contains(@class,"title")]')
    
    driver.execute_script("arguments[0].style.fontSize = '40px' ;", title)

    try:
        driver.execute_script("document.getElementsByClassName('pinnable-content')[0].classList = ''; ") # remove video pin
    except: 
        pass
    
    titlelink = title.get_attribute("href")
    print("titlelink: ", titlelink)
    
    mdir = "./"+str(i)
    for fname in os.listdir(mdir):
        if fname.startswith("media"):
            os.remove(os.path.join(mdir, fname))
        
    link = titlelink
    print(link)
    
    import retrive
    
    retrive.retrive(link, "./"+str(i)+"/media") ############################# Get media

    
    driver.get_screenshot_as_file('./'+str(i)+'/p.png')

    print("Getting post screenshot")
    postElement = driver.find_element_by_xpath("//div[@class='entry unvoted']")
    screenshot_as_bytes = postElement.screenshot_as_png
    with open('postElement.png', 'wb') as f:
        f.write(screenshot_as_bytes)
        
    with open("postElement.png", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    b64_string = b64_string.decode('utf-8')
    #print(b64_string)
        
   
    
    titletext = title.get_attribute("innerHTML").encode('ascii', 'ignore')
    allTopics.append(str(titletext, "ascii"))
    if(i == 0 ):
        firstTitle = str(titletext, "ascii")
        if(len(firstTitle) > 70):
            firstTitle = ' '.join(firstTitle.split()[:9])
       
        print(firstTitle)
        #raw_input()
        
    aud.audio(titletext , './'+str(i)+'/p.wav')
    

    table = driver.find_element_by_xpath('//div[contains(@class,"nestedlisting") ]')
    
    # remove mod stuff
    try:
        stuck = table.find_element_by_xpath('//div[contains(@data-author,"AutoModerator") or (contains(@class, "stickied")) ]')
        driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, stuck)
    except:
        pass

        
    comments = table.find_elements_by_xpath('.//div[@class="md"]')
    #print(len(comments))

    
    
    for ii in range(0,5):

        if ii == 0:
            driver.execute_script("document.getElementsByClassName('commentarea')[0].style.background = '#e7e7e7';document.getElementsByTagName('body')[0].style.background = '#e7e7e7';var elemDiv = document.createElement('div');elemDiv.style.cssText = 'position: fixed;top: 30%;right: 45%';document.body.appendChild(elemDiv);elemDiv.innerHTML='<img style=\"display:block;max-width:400px;max-height:400px;width: auto;height: auto;\" class=\"preview\" src=\"data:image/png;base64,"+b64_string+"\">'") 
        
        #time.sleep(3)    # pause 5.5 seconds
        element = comments[ii]
        driver.execute_script("arguments[0].style.cssText = 'font-size:30px; position:relative;z-index:1; background-color:white;';", element) 
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.find_element_by_css_selector('body').send_keys(Keys.UP)
        driver.get_screenshot_as_file('./'+str(i)+'/'+str(ii)+'.png')
        
        text = element.get_attribute("innerHTML")
        text = re.sub('<blockquote.*?>(.|\n)*?</blockquote>', "Quote.", text )
        soup = BeautifulSoup(text, "html.parser")
        
        cleantext = soup.get_text() #get the raw comment weird symbols removed
        cleantext = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', 'Link.', cleantext)
        if(len(cleantext) > 300):
            print("LARGE TEXT")
            #dotpos = cleantext.replace('.', 'XXX', 0).find('.')
            dotpos = cleantext.find('.')
            #dotpos = cleantext.find('.')
            if(dotpos > 0 ):
                cleantext = cleantext[:dotpos]
        
        
        aud.audio(cleantext.encode('ascii', 'ignore') , './'+str(i)+'/'+str(ii)+'a.wav')
        
        print("COMMENT " + str(cleantext.encode('ascii', 'ignore')))


aud.audio(("Welcome to reddit, what's up today "+random.choice(viewers)+"?").encode('ascii', 'ignore') , './pic.wav')

aud.audio(("Thank you for watching "+random.choice(viewers)+"! Dont forget to smash like and subscribe. . .").encode('ascii', 'ignore') , './out.wav')


print("Ready to compile")
driver.quit()


#run next

#####
import compile ############################################ put video together
#####
#compile.comp()

print("upload")

import datetime

now = datetime.datetime.now()

counter = 1;
topicList = "";
for tt in allTopics:
    topicList = topicList + str(counter) + ". " + tt + "\n"
    counter += 1
# str(now.strftime("%A")
desc = "Join us for the latest scoop on the funniest and most talked-about memes and drama from the popular subreddit /r/" + subname  + ". \n" \
            + random.choice(["Today we're looking at:", "Today we're covering:", "In this episode, we're diving into the latest happenings, including:"]) \
            + "\n" + topicList + "\n Don't miss out on the laughs and join us for the latest memes and drama from the world of Reddit!"

f = open("desc.txt", "w", encoding = 'utf-8' )
f.write(desc)
f.close()
descfile = "desc.txt"

categ = "Entertainment"
tags = "reddit, news, " + subname

u= subprocess.call("youtube-upload --title=\" "+firstTitle+" \" --description-file=\"" + descfile +"\" --thumbnail \""+myPATH+"\\0\\thumb.png\" --category=\""+categ+"\" --tags=\""+tags+"\" withmusic.mp4",shell=True)
print(u)

input()

