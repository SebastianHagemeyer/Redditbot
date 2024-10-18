import subprocess
from subprocess import Popen, PIPE, STDOUT

def audio(text,path):
    try:
        p = Popen(['balcon', '-i', '-w', path, '-n', 'ScanSoft Daniel_Full_22kHz'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout_data = p.communicate(input=text)[0]
        print(stdout_data)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

#audio("hello, test", './test.wav')
