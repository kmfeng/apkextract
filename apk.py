#!/usr/bin/python

import os # Folder creation, file handling, execution
import sys # Handling file arguments
import platform # Detect OS Types for different Java commands
import subprocess # Detect Java version
from os.path import join as path_join # For lib folder with dex2jar

def main():
    javacheck() # Check for Java 1.7+

    # Check for arguments
    if len(sys.argv) == 1:
        print "Usage:", sys.argv[0], "[filename.apk]"
        sys.exit(1)

    # Check for APK file and if found create working folder, otherwise exit
    if os.path.isfile(sys.argv[1]):
        apk = sys.argv[1].strip()
        outputfolder = "OUTPUT-" + apk[:-4] # Folder created with filename minus extension
    else:
        print "File", sys.argv[1], "not found!"
        sys.exit(1)

    extract = Apk(apk, outputfolder)
    extract.apktool()

class Apk(object):
    def __init__(self, apk, dest):

        self.apk = apk
        self.dest = dest
        self.cwfolder = os.path.dirname(os.path.abspath(__file__))
        self.ostype = platform.system()

    def apktool(self):
        apktool = self.cwfolder + '/tools/apktool2.0' + "/apktool.jar"

        print "[+] Extracting", self.apk, "to working folder", self.dest

        if self.ostype == "darwin":
            os.system("java -Xmx256M -Djava.awt.headless=true -jar " + apktool + " d -f " + self.apk + " -o " + self.dest +"/apktool")
        elif self.ostype == "Windows":
            os.system("java -jar -Duser.language=en " + apktool + " d -f " + self.apk + " -o " + self.dest +"/apktool")
        else:
            os.system("java -Xmx256M -jar " + apktool + " d -f " + self.apk + " -o " + self.dest +"/apktool")

        self.dex2jar()

    def dex2jar(self):
        jars = (
            'asm-all-3.3.1.jar',
            'commons-lite-1.15.jar',
            'dex-ir-1.12.jar',
            'dex-reader-1.15.jar',
            'dex-tools-0.0.9.15.jar',
            'dex-translator-0.0.9.15.jar',
            'dx.jar',
            'jar-rename-1.6.jar',
            'jasmin-p2.5.jar',
        )
        libdir = self.cwfolder + '/tools/dex2jar-0.0.9.15'
        classpath = ':'.join([path_join(libdir, x) for x in jars])
        dexarg = "java -Xms512m -Xmx1024m -classpath " + classpath + " com.googlecode.dex2jar.tools.Dex2jarCmd " + self.apk

        print "[+] Running dex2jar on", self.apk
        os.system(dexarg)

        # After running dex2jar we pass over to jd-cli to extract jar file
        self.dex2jarfile = self.cwfolder + "/" + self.apk[:-4] + "-dex2jar.jar"
        if os.path.isfile(self.dex2jarfile):
            print "[+] Detected dex2jar file: ", self.dex2jarfile
            self.jd()

    def jd(self):
        try:
            jdfolder = self.dest + "/jdtool"
            jdfmove = self.dest + "/" + self.apk[:-4] + "-dex2jar.jar"
            print "JDFMOVE:", jdfmove

            jdargs = "java -jar " + self.cwfolder + "/tools/jd-cmd-0.9.1/jd-cli.jar " + self.dex2jarfile + " -od " + jdfolder

            print "[+] Decompiling ", self.dex2jarfile, "into folder ", jdfolder
            os.makedirs(jdfolder)
            os.system(jdargs)
            os.rename(self.dex2jarfile, jdfmove) # Move jar file into working folder
        except:
            pass

def javacheck():
    try:
        java = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
        javaversion = float(java.split('"')[1][0:3])

        if javaversion < 1.7:
            print "[-] Java version", javaversion, "detected. Please install 1.8 +"
            sys.exit()
        else:
            pass
    except:
        print "Unexpected error:", sys.exc_info()[0]
        pass

if __name__ == "__main__":
	main()