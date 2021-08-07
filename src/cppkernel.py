import zipfile
import tqdm
import os  
import threading 
import utils
import shutil

working_dir = ""
fetch_dir = ""
kernel_file = ""
kernel_dir = ""

if os.name == "nt":
    working_dir = os.getenv("USERPROFILE") + "\\cppkernel"
    fetch_dir = working_dir + "\\fetched"
    kernel_file = fetch_dir + "\\kernel.zip"
    kernel_dir = fetch_dir + "\\kernel"
else:
    working_dir = os.getenv("HOME") + "/cppkernel"
    fetch_dir = working_dir + "/fetched"
    kernel_file = fetch_dir + "/kernel.zip"

if not os.path.isdir(working_dir): os.mkdir(working_dir)
if not os.path.isdir(fetch_dir): os.mkdir(fetch_dir)
    

if not os.path.isfile(kernel_file):
    utils.download("https://registry-ppm.cf/archive/kernel.zip", kernel_file)

print("\x1b[1A")
print("\x1b[1A")

if not os.path.isdir("./kernel"):
    utils.extractall(kernel_file, kernel_dir)

source_target = str(input("C++ Source filename: "))
if not os.path.isfile(source_target):
    print("error: No such file")
    exit(1)
flags_target = str(input("Compiler Flags [press ENTER for no flags]: "))

if not os.path.isdir("build"):
    os.mkdir("build")

if not os.path.isdir("rootfs"):
    os.mkdir("rootfs")


if os.name == "nt":
    os.system("ubuntu run \"g++ -static " + source_target + flags_target + " -o build/init; cd build; find . | cpio -o -H newc | gzip > ../rootfs/rootfs.cpio.gz\"")
else:
    os.system("g++ -static " + source_target + flags_target + " -o build/init; cd build; find . | cpio -o -H newc | gzip > ../rootfs/rootfs.cpio.gz")

if os.path.isdir("build"):
    shutil.rmtree("build")

res = input("Execute OS? [y/n]: ")
rootfs = os.getcwd() + "/rootfs/rootfs.cpio.gz"
if res.lower().startswith("y"):
    os.system("qemu-system-x86_64 -kernel " + kernel_dir + "/arch/x86/boot/bzImage -initrd " + "rootfs/rootfs.cpio.gz")
else:
    res = input("Build iso? [y/n]: ")
    if(res.lower().startswith("y")):
        if os.name == "nt":
            os.system("ubuntu run \"cd " + kernel_dir + "; make isoimage FDINITRD=" + rootfs + "\"")
    else:
        shutil.rmtree("rootfs")