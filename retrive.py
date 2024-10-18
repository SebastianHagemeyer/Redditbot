import requests
import re
import subprocess
def retrive(url , name):
    ext = re.findall('.+(\.\w{3})\?*.*',url)[0]
    r=requests.get(url)
    headers = r.headers['content-type']
    if("html" not in headers):
        
        f=open(name+ext,'wb');
        print ("Downloading.....")
        for chunk in r.iter_content(chunk_size=255): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        print ("Done")
        f.close()
    else:
        u= subprocess.call(["youtube-dl",url, "-o", name+".mp4"],shell=True)
        print(u)

