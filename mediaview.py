import subprocess
import os
from PIL import Image
import shlex
import json
import random
import ffmpeg

fsPATH = "C:/Automate/RedditBot"
normalPATH = "C:\\Automate\\RedditBot"

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

vw, vh = 1280, 720

direcs = []

def comp():
    os.chdir(normalPATH)  # navigate root in os

    os.system("ffmpeg -y -i ./Out/pic.png -i ./Out/pic.wav -acodec aac -vcodec mpeg4 ./Out/pic.mp4")  # compile intro view
    direcs.append(myPATH + '\\\\Out\\\\pic.mp4')  # add intro to video order

    for i in range(0, 5):  # loop folder numbers
        os.chdir(normalPATH + '\\' + str(i))  # navigate folder in os
        os.system("ffmpeg -y -i p.png -i p.wav -acodec aac -vcodec mpeg4 p.mp4")  # compile post view
        direcs.append(myPATH + '\\\\' + str(i) + '\\\\p.mp4')  # add post view to video order

        for fname in os.listdir("./"):
            print(fname)
            if fname.startswith("media"):
                print("MEDIA")

                im = Image.open('p.png')
                width, height = im.size

                print(width, height)

                try:
                    # media view for image
                    orig = Image.open(fname)
                    x, y = orig.size
                    multi = float(height) / (y)

                    redone = orig.resize((int(x * multi), int(y * multi)), Image.ANTIALIAS)
                    rwidth, rheight = redone.size

                    redone.save(fname)

                    os.system(
                        "ffmpeg -y -i " + fname +
                        " -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=22050 -t 0:05 -acodec aac -vcodec copy mp.mp4"
                    )  # compile media view

                    os.system(
                        'ffmpeg -y -i mp.mp4 -filter_complex "[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" -qscale 0 -vcodec mpeg4 m.mp4'
                    )  # compile media view
                except Exception as e:  # media view for video
                    # print(e)
                    if os.path.isfile('m.mp4'):
                        os.remove('m.mp4')

                    h, w = findVideoResolution(fsPATH + '/' + str(i) + "/" + fname)

                    mult = float(height) / h
                    newW = int(w * mult)
                    if newW > width:
                        newW = width

                    print("NEW AND OLD W", newW, w)
                    newH = h * mult
                    print("NEW AND OLD H", newH, h)

                    import subprocess
                    output = subprocess.getoutput("ffprobe -i " + fname + " -show_streams -select_streams a -loglevel error")
                    print(output)

                    # check if clip has an audio stream
                    if output:
                        print('Video clip has audio')
                        os.system(
                            "ffmpeg -y -i " + fname +
                            " -vf \"scale=" + str(newW) + "x" + str(height) +
                            "\" -ar 22050 -acodec aac -vcodec mpeg4 -qscale 10 -r 25 -t 60 m2.mp4"
                        )
                    else:
                        print("Video clip has no audio")
                        os.system(
                            "ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=22050 -i " + fname +
                            " -vf \"scale=" + str(newW) + "x" + str(height) + "\"  -shortest -acodec aac -vcodec mpeg4 -qscale 10 -r 25 -t 60 m2.mp4"
                        )

                    # re-encode and add padding
                    os.system(
                        'ffmpeg -y -i m2.mp4 -filter_complex "[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" -qscale 10 -r 25 -vcodec mpeg4 m.mp4'
                    )  # compile media view

                direcs.append(myPATH + '\\\\' + str(i) + '\\\\m.mp4')  # add media view to video order
        # for each post
        
        for ii in range(0, 5):  # loop comment numbers
            os.system(
                "ffmpeg -y -i " + str(ii) + ".png -i " + str(ii) + "a.wav -acodec aac -vcodec mpeg4 " + str(ii) + "f.mp4"
            )  # compile comment view
            direcs.append(myPATH + '\\\\' + str(i) + '\\\\' + str(ii) + 'f.mp4')  # add comment view to video order
    
    # just comp
    #os.system("ffmpeg -y -i ./Out/pic.png -i ./Out/pic.wav -acodec aac -vcodec mpeg4 ./Out/pic.mp4")  # compile intro view
    #direcs.append(myPATH + '\\\\Out\\\\pic.mp4')  # add intro to video order
    
    os.chdir(normalPATH)  # navigate root in os
    
    os.system("ffmpeg -y -i ./Out/out.png -i ./Out/out.wav -acodec aac -vcodec mpeg4 ./Out/out.mp4") # compile outtro view
    direcs.append(myPATH+'\\\\Out\\\\out.mp4') #add outtro
    
    print(direcs)

    file = open('./Out/directories.txt','w') #create directories text file
    end = len(direcs)
    for x in range(0,end):
        file.write("file "+ direcs[x] + "\n") # add file names/dirs
    file.close()


comp()



