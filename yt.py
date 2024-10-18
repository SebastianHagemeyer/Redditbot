import subprocess
from subprocess import check_output


def getLength(name):
    a = str(check_output('ffprobe -i  "'+name+'" 2>&1 |findstr "Duration"',shell=True)) 
    a = a.split(",")[0].split("Duration:")[1].strip()

    h, m, s = a.split(':')
    duration = int(h) * 3600 + int(m) * 60 + float(s)
    return(duration)


print (getLength("output.mp4"))
