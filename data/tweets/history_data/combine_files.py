import os

for dir in os.listdir("."):
    if os.path.isdir(dir):
        with open(dir+".txt", 'w') as outfile:
            for file in sorted(os.listdir(dir), reverse=True):
                with open(dir + "/" + file, 'r') as readfile:
                    outfile.write(readfile.read())