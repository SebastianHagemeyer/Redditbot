

import subprocess
import os
from PIL import Image
import shutil

import shlex
import json
import random
import ffmpeg


fsPATH = "E:/RedditBot"
normalPATH = "E:\\RedditBot"
musicPATH = "E:\\"
myPATH = normalPATH.replace("\\", "\\\\\\\\")

def findVideoResolution(pathToInputVideo):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(pathToInputVideo)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)

    # find height and width
    height = ffprobeOutput['streams'][0]['height']
    width = ffprobeOutput['streams'][0]['width']

    return height, width
#'''

vw, vh = 1280, 720

direcs = []

def comp():
     os.chdir(normalPATH) #navigate root in os

     os.system("ffmpeg -y -i pic.png -i pic.wav -acodec aac -vcodec mpeg4 pic.mp4") # compile intro view
     direcs.append(myPATH+'\\\\pic.mp4') #add intro to video order


     for i in range(0,5):#loop folder numbers
          os.chdir(normalPATH+'\\'+str(i)) #navigate folder in os
          os.system("ffmpeg -y -i p.png -i p.wav -acodec aac -vcodec mpeg4 p.mp4") # compile post view
          direcs.append(myPATH+'\\\\'+str(i)+'\\\\p.mp4') # add post view to video order

          #mdir = "./"+str(i)

          for fname in os.listdir("./"):
               print(fname)
               if fname.startswith("media"):
                    print("MEDIA")
                    
                    im = Image.open('p.png')
                    width, height = im.size

                    print(width, height)
                    
                    try:
                         
                         #### media view for image

                         orig = Image.open(fname)
                         x,y = orig.size
                         multi = float(height)/(y)
                         
                         redone = orig.resize((int(x*multi),int(y*multi)), Image.ANTIALIAS)
                         rwidth, rheight = redone.size

                         redone.save(fname)
                         ###

                         os.system("ffmpeg -y -i "+fname+" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=22050 -t 0:05 -acodec aac -vcodec copy mp.mp4") # compile media view
                         os.system('ffmpeg -y -i mp.mp4 -filter_complex "[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg]; \
                                        [bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" -qscale 0 -vcodec mpeg4 m.mp4') # compile media view
                         
                    except Exception as e: ## media view for video
                         #print(e)
                         if(os.path.isfile('m.mp4')):
                              os.remove('m.mp4')


                         h,w = findVideoResolution(fsPATH+'/'+str(i)+"/"+fname)

                         mult = float(height)/h
                         newW = int(w*mult)
                         if(newW > width):
                             newW = width

                         print("NEW AND OLD W" , newW,w)
                         newH = h*mult
                         print("NEW AND OLD H",newH,h)


                    
                         import subprocess
                         output = subprocess.getoutput("ffprobe -i "+fname+" -show_streams -select_streams a -loglevel error")
                         print(output)

                         # check if  clip has an audio stream
                         if output:
                              print('Video clip has audio')
                              os.system("ffmpeg -y -i "+fname+" -vf \"scale="+str(newW)+"x"+str(height)+"\" -ar 22050 -acodec aac -vcodec mpeg4 -qscale 10 -r 25 -t 60 m2.mp4")
                         else:
                              print("Video clip has no audio")
                              os.system("ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=22050 -i "+fname+" -vf \"scale="+str(newW)+"x"+str(height)+"\"  -shortest -acodec aac -vcodec mpeg4 -qscale 10 -r 25 -t 60 m2.mp4")

                         # re-encode and add padding
                         os.system('ffmpeg -y -i m2.mp4 -filter_complex "[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" -qscale 10 -r 25 -vcodec mpeg4 m.mp4') # compile media view

                         
                    direcs.append(myPATH+'\\\\'+str(i)+'\\\\m.mp4') # add media view to video order

          #raw_input()

          
          for ii in range(0,5): # loop comment numbers
             os.system("ffmpeg -y -i "+str(ii)+".png -i "+str(ii)+"a.wav -acodec aac -vcodec mpeg4 "+str(ii)+"f.mp4") #compile comment view
             direcs.append(myPATH+'\\\\'+str(i)+'\\\\'+str(ii)+'f.mp4') #add comment view to video order
          
          
     

     os.chdir(normalPATH) # navigate out of folder

     # outtro
     os.system("ffmpeg -y -i out.png -i out.wav -acodec aac -vcodec mpeg4 out.mp4") # compile outtro view
     os.system("ffmpeg -loop 1 -i out.png -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=22050 -t 5 -c:v copy -t 10 -y out2.mp4") # compile outtro view
     ## TRY 48000 samplerate
     direcs.append(myPATH+'\\\\out.mp4') #add outtro
     direcs.append(myPATH+'\\\\out2.mp4') #add outtro
     #

     print(direcs)

     file = open('directories.txt','w') #create directories text file
     end = len(direcs)
     for x in range(0,end):
          file.write("file "+ direcs[x] + "\n") # add file names/dirs
     file.close()

     
     os.chdir(normalPATH)

     #input()
     os.system('ffmpeg -y -f concat -safe 0 -i directories.txt -c copy output.mp4')# concat all videos into output
     ####
     
     os.chdir(musicPATH)
     ran = random.choice(os.listdir("./mus")) 
     os.system('ffmpeg -y -i '+"./mus/"+ran+' -ar 22050 '+fsPATH+'/ma.wav')
     os.chdir(normalPATH)

     
     os.system('ffmpeg -y -i output.mp4 -f wav -ar 22050 -vn outputwav.wav')
     os.system('ffmpeg -y -stream_loop 3 -i ma.wav -filter:a "volume=0.3" low.wav')
     os.system('ffmpeg -y -i low.wav -i outputwav.wav \
                         -filter_complex "[1:a]asplit=2[sc][mix];[0:a][sc]sidechaincompress=threshold=0.05:ratio=3[bg]; \
                         [bg][mix]amerge[merge]" \
                         -map [merge] merge.wav')
     os.system('ffmpeg -y -i output.mp4 -i merge.wav -map 0:v -map 1:a -c:a aac -vcodec copy withmusic.mp4')

     #get thumbnail
     import glob
     os.chdir(normalPATH+"\\0")
     for file in glob.glob("m.*"):
         print(file)
         os.system('ffmpeg -y -i '+"./"+file+' -vframes 1 thumb.png')
    

     basewidth = 1280
     img = Image.open('thumb.png')
     wpercent = (basewidth/float(img.size[0]))
     hsize = int((float(img.size[1])*float(wpercent)))
     img = img.resize((basewidth,hsize), Image.ANTIALIAS)
     # add logo
     til = Image.open("../logo.png")
     img.paste(til, (int(img.width/2 - til.width/2),int(img.height/2 - til.height/2)), til)

     img.save('thumb.png')
     
     os.chdir(normalPATH)
     ####
    
comp()

