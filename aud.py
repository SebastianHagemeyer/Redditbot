import subprocess
from subprocess import Popen, PIPE, STDOUT

def audio(text,path):
    p = Popen(['balcon', '-i', '-w', path, '-n', 'ScanSoft Daniel_Full_22kHz'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = p.communicate(input=text)[0]
    print(stdout_data)


#audio("hello, test", './test.wav')
