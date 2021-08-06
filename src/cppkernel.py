import zipfile
import tqdm
import os  
import threading 
import utils

working_dir = os.getenv("HOME") + "/cppkernel"
fetch_dir = working_dir + "/cache"

try:
    os.mkdir(working_dir)
    os.mkdir(fetch_dir)
    os.rmdir("kernel")
    os.remove("kernel.zip")
except:
    pass

utils.download("https://registry-ppm.cf/archive/kernel.zip", "kernel.zip")


utils.extractall("kernel.zip", "kernel")