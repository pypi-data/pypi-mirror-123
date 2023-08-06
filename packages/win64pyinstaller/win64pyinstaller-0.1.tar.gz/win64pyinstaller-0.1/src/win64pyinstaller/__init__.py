from time import sleep
from os import path, startfile, remove
from pymyfile import file
from tempfile import gettempdir
from urllib.request import urlopen
from time import time
from sys import stdout
def __restart_line():
    stdout.write('\r')
    stdout.flush()

def install(url, destination_path, auto_open=False):
    start = time()
    powershell = f"$url = '{url}' \n$output = '{destination_path}'\nInvoke-WebRequest -Uri $url -OutFile $output"
    install_file = open(f"{gettempdir()}\\install.ps1", "a")
    install_file.write(f"{powershell}")
    u = urlopen(url)
    meta = u.info()
    file_size = int(meta.get("Content-Length"))
    install_file.close()
    from subprocess import Popen, SW_HIDE
    Popen(["powershell",f'{gettempdir()}\\install.ps1'], creationflags=SW_HIDE)
    sleep(2)
    stdout.write('starting...')
    stdout.flush()
    __restart_line()
    def _download_info():
        n = 1
        while True:
            sleep(1)
            b = path.getsize(f"{destination_path}") / 1000000
            temp_file = open(f"{gettempdir()}\\temp.txt", "a")
            temp_file.write(f"\n{b:.2f}")
            if not(n == 1):
                myfile = file(f"{gettempdir()}\\temp.txt")
                f = myfile.readline(line_num = n)
                distance = float(f) - b
                t = 1
                speed = distance / t
                stdout.write(f'done - {b:.2f}/{(file_size/1000000):.2f}MB, speed - {0 - speed:.2f}MB/S')
                stdout.flush()
                __restart_line()
                if (b*1000000) == file_size:
                    break
            n += 1
    _download_info()
    remove(f"{gettempdir()}\\temp.txt")
    remove(f"{gettempdir()}\\install.ps1")
    if auto_open == True:
        print("opening file...")
        startfile(f"{destination_path}")
    stop = time()
    print(f"completed in {float(stop-start):.2f} sec") # total time taken