from pexel import *
import subprocess
import shutil

# Config.read('/home/wolfmeist/.config/plasma-org.kde.plasma.desktop-appletsrc')
# get the image file name
image_location = resize_image()
filename = '/home/wolfmeist/.config/plasma-org.kde.plasma.desktop-appletsrc'
# temporary file to store the edits
outputfile = 'plasma-org.kde.plasma.desktop-appletsrc'
Edited = False
with open(filename) as fin, open(outputfile, 'w+') as out:
    flag = False
    for line in fin:
        out.write(line)
        # if group wallpaper found
        if 'Wallpaper' in line:
            # second line is the image file name
            new_line = 'Image=file://' + image_location + '\n'
            out.write(new_line)
            Edited = True
            # skip the next line to read
            line = next(fin)
            continue

outputfile = os.getcwd() + "/" + outputfile
# move the temporary file with the orignal appletrc file
if Edited:
    shutil.move(outputfile, filename)

# restart the plasma shell
kill = "killall plasmashell"
start = "kstart plasmashell"

subprocess.call(kill, shell=True)
subprocess.call(start, shell=True)
