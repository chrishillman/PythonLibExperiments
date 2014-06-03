from subprocess import PIPE, Popen
from sys import exit, exc_info, argv

from socket import *

def hostToIP(host):
    try:
        ip = gethostbyname(host)
        return ip
    except:
        return None

def connectTo(host, port):
    try:
        s=socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        return s
    except:
        s.close()
        return None

def bannerGrabber(sock):
    try:
        sock.send("0000000000000000000000\r\n")
        banner=sock.recv(1024)
        return banner
    except:
        return None

def scan(host, port):
    sock=connectTo(host, port)
    setdefaulttimeout(5)
    if sock:
        banner=bannerGrabber(sock)
        if banner:
            return True
        else:
            return False
        sock.close()
    else:
        return False

def pingHost(host):
    pingout,pingerr=Popen(["ping.exe", line, "-n", "1"], stdout=PIPE, shell=True).communicate()
    print "Pingout: " + pingout + " :|: "
    if pingout.find(" ms") > 0:
        return True
    else:
        return False


if __name__=="__main__":



    lines=[]

    if len(argv)<2:

        try:
                with open("spider.ini", "r") as f:
                        for line in f:
                                lines.append(line)
        except:
                print("spider.ini not found!")
                print("Create the file with the following format: (For one IP Address)")
                print("FIRST IP ADDRESS")
                exit()
    else:
        for arg in argv:
            lines.append(arg)

    for line in lines:
        try:
            ip=hostToIP(line)
            if ip:
                if scan(line, 135) or scan(line, 445):
                    print("%s : Windows"%(line))
                if scan(line, 22) or scan(line, 23):
                    print("%s : Cisco or Linux"%(line))
            else:
                print("invalid host")
        except:
            print("error")

