from threading import Thread, Lock
import socket

PORT = 80
StringToDetect='<script src="js/sha256.min.js" type="text/javascript"></script>'

class Threader:
    def __init__(self, threads=30):
        self.thread_lock = Lock()
        self.functions_lock = Lock()
        self.functions = []
        self.threads = []
        self.nthreads = threads
        self.running = True
        self.print_lock = Lock()

    def stop(self) -> None:
        self.running = False

    def append(self, function, *args) -> None:
        self.functions.append((function, args))

    def start(self) -> None:
        for i in range(self.nthreads):
            thread = Thread(target=self.worker, daemon=True)
            thread._args = (thread, )
            self.threads.append(thread)
            thread.start()

    def join(self) -> None:
        for thread in self.threads:
            thread.join()

    def worker(self, thread:Thread) -> None:
        while self.running and (len(self.functions) > 0):
            with self.functions_lock:
                function, args = self.functions.pop(0)
            function(*args)
        with self.thread_lock:
            self.threads.remove(thread)

def GetLANInfo():
    import platform
    Interface=''
    Mask=''
    if platform.system() == "Windows":
        import subprocess
        for Line in str(subprocess.run(["route", "print"], capture_output=True).stdout.decode()).split('\n'):
            if '0.0.0.0' in Line:
                LineParts=" ".join(Line.split()).split(' ')
                if LineParts[0]=='0.0.0.0' and LineParts[1]=='0.0.0.0':
                    Interface=LineParts[3]
                    break
        print('Interface='+str(Interface))

        for Line in str(subprocess.run(["ipconfig"], capture_output=True).stdout.decode()).split('\n'):
            if Interface in Line:
                Mask='NextLine'
            elif Mask=='NextLine' :
                Mask=Line.split(':')[1].replace(' ','').rstrip()
        print('Mask='+str(Mask))
    else:
        pass
    return Interface, Mask

def GetLANIps(Interface, Mask):
    import ipaddress
    IpRange=str(Interface)+'/'+str(Mask)
    Ips=[]
    for ip in ipaddress.ip_network(IpRange, False).hosts():
        Ips.append(str(ip))
    print('Ips='+str(len(Ips))+' elements')
    return Ips

def ConnectToPort(hostname, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((hostname, port))
    with threader.print_lock:
        if result == 0:
            print("Found open port in "+str(hostname))
            IpsWithPortOpen.append(hostname)

def ScanIpRange(Ips):
    socket.setdefaulttimeout(0.1)
    global threader
    threader = Threader(10)
    for Ip in Ips:
        threader.append(ConnectToPort, Ip, PORT)
    threader.start()
    threader.join()
    print("Done scanning ip range")

def DetectWebContent(IpsWithPortOpen):
    import requests
    Targets=[]
    for Ip in IpsWithPortOpen:
        Url = 'http://'+str(Ip)
        Response=False
        try:
            Response = requests.get(Url, stream=True)
        except:
            pass
        if Response:
            print ('There is someone behind '+str(Ip))
            if StringToDetect in str(Response.content):
                print ('SHE IS THE ONE!')
                Targets.append(Ip)
        return Targets

Interface, Mask = GetLANInfo()
Ips = GetLANIps(Interface, Mask)
IpsWithPortOpen=[]
ScanIpRange(Ips)
Targets=DetectWebContent(IpsWithPortOpen)

print('Targets='+str(Targets))