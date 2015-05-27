#!/usr/bin/python

import os  # Folder creation, file handling, execution
import sys  # Handling file arguments
import platform  # Detect OS Types for different Java commands
import subprocess  # Detect Java version
from os.path import join as path_join  # For lib folder with dex2jar
import argparse

def javacheck():
	try:
		java = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
		javaversion = float(java.split('"')[1][0:3])

		if javaversion < 1.7:
			print "[-] Java version", javaversion, "detected. Please install 1.7 or higher"
			sys.exit()
		else:
			pass
	except:
		print "Unexpected error:", sys.exc_info()[0]
		pass

def filecheck(apk):
	filename, dotapk = os.path.splitext(apk)

	if os.path.isfile(apk):
		print "[+] File", apk, "found!"
		pass
	elif dotapk != ".apk":
		print "[*] File", apk, "must have an apk file extension"
		sys.exit(1)
	else:
		print "[*] File", apk, "not found!"
		sys.exit(1)

def foldercheck(recompfolder, ostype, cwd):
	if ostype == "Windows":
		outputfolder = recompfolder +  "\\apktool"
	else:
		outputfolder = recompfolder + "/apktool"

	if os.path.exists(outputfolder):
		print "[+] Detected previous apktool output folder.  Recompiling apk."
		return True
	else:
		print "[*] No previous extracted APK folder found. Please extract APK first."
		sys.exit(1)

def main():
	parser = argparse.ArgumentParser(
		description='APKextract is a python wrapper for Android APK extraction tools')
	parser.add_argument(
		'-e', '--extract', type=str, help='Extract apk file', dest="extract")
	parser.add_argument(
		'-r', '--recompile', type=str, help='Recompile apk from extracted folder path', dest="recompile")
	parser.add_argument(
		'-s', '--sign', type=str, help='Sign APK file', dest="sign")
	parser.add_argument(
		'-o', '--output', type=str, help='Specify an output folder for extraction', dest="output")

	args = parser.parse_args()

	javacheck()  # Check for Java 1.7+
	ostype = platform.system() # Check for OS type
	cwd = os.getcwd() # Get current working folder

	if args.output:
		if not args.extract:
			parser.error("--output can only be used with extract option")

	if args.extract:
		apk = args.extract.strip()
		filecheck(apk)
		if args.output:
			outputfolder = args.output
		else:
			outputfolder = "OUTPUT-" + apk[:-4]
		if os.path.exists(outputfolder):
			print "[*] Detected previous output folder.  Overwriting."

		apk = Apk(apk, outputfolder, ostype, cwd)
		apk.apktool()

	if args.recompile:
		apk = ""
		recompfolder = args.recompile
		check = foldercheck(recompfolder, ostype, cwd)
		if check:
			apk = Apk(apk, recompfolder, ostype, cwd)
			apk.recompile()

	if args.sign:
		print "Not yet implemented"
		pass

class Apk(object):
	def __init__(self, apk, dest, ostype, cwd):

		self.apk = apk
		self.dest = dest
		self.ostype = ostype
		self.cwfolder = cwd

	def apktool(self):
		try:
			if self.ostype == "Windows":
				self.apktool = self.cwfolder + "\\tools\\apktool2.0" + "\\apktool.jar"
			else:
				self.apktool = self.cwfolder + "/tools/apktool2.0" + "/apktool.jar"

			print "[+] Extracting", self.apk, "to working folder", self.dest

			if self.ostype == "darwin":
				os.system(
					"java -Xmx256M -Djava.awt.headless=true -jar " + self.apktool + " d -f " + self.apk + " -o " + self.dest + "/apktool")
			elif self.ostype == "Windows":
				os.system("java -jar -Duser.language=en " + self.apktool + " d -f " + self.apk + " -o " + self.dest + "\\apktool")
			else:
				os.system("java -Xmx256M -jar " + self.apktool + " d -f " + self.apk + " -o " + self.dest + "/apktool")

			self.dex2jar()
		except Exception,e: print str(e)

		try:
			if self.ostype == "Windows":
				filename = self.dest + "\\" + self.apk + "_certificate.txt"
			else:
				filename = self.dest + "/" + self.apk + "_certificate.txt"

			certificate = subprocess.check_output(["keytool", "-list", "-printcert", "-jarfile", self.apk], stderr=subprocess.STDOUT)
			f = open(filename,"w")
			f.write(certificate)
			f.close()
		except:
			pass

	def dex2jar(self):
		try:
			if self.ostype == "Windows":
				libdir = self.cwfolder + '\\tools\\dex2jar-0.0.9.15'
				self.dex2jarfile = self.cwfolder + "\\" + self.apk[:-4] + "-dex2jar.jar"
			else:
				libdir = self.cwfolder + '/tools/dex2jar-0.0.9.15'
				self.dex2jarfile = self.cwfolder + "/" + self.apk[:-4] + "-dex2jar.jar"

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

			if self.ostype == "Windows":
				classpath = ';'.join([path_join(libdir, x) for x in jars])
				dexarg = "java -Xms512m -Xmx1024m -cp " + classpath + " com.googlecode.dex2jar.tools.Dex2jarCmd " + self.apk
			else:
				classpath = ':'.join([path_join(libdir, x) for x in jars])
				dexarg = "java -Xms512m -Xmx1024m -classpath " + classpath + " com.googlecode.dex2jar.tools.Dex2jarCmd " + self.apk


			print "[+] Running dex2jar on", self.apk
			os.system(dexarg)

			# After running dex2jar we pass over to jd-cli to extract jar file
			if os.path.isfile(self.dex2jarfile):
				print "[+] Detected dex2jar file: ", self.dex2jarfile
				self.jd()
		except Exception,e: print str(e)

	def jd(self):
		try:
			if self.ostype == "Windows":
				jdfolder = self.dest + "\\jdtool"
				jdfmove = self.dest + "\\" + self.apk[:-4] + "-dex2jar.jar"
				jdargs = "java -jar " + self.cwfolder + "\\tools\\jd-cmd-0.9.1\\jd-cli.jar " + self.dex2jarfile + " -od " + jdfolder
			else:
				jdfolder = self.dest + "/jdtool"
				jdfmove = self.dest + "/" + self.apk[:-4] + "-dex2jar.jar"
				jdargs = "java -jar " + self.cwfolder + "/tools/jd-cmd-0.9.1/jd-cli.jar " + self.dex2jarfile + " -od " + jdfolder

			print "[+] Decompiling: ", self.dex2jarfile, "\n[+] Output decompile:", jdfolder
			os.makedirs(jdfolder)
			os.system(jdargs)
			os.rename(self.dex2jarfile, jdfmove)  # Move jar file into working folder
		except Exception,e: print str(e)

	def recompile(self):
		if self.ostype == "Windows":
			self.apktool = self.cwfolder + "\\tools\\apktool2.0" + "\\apktool.jar"
		else:
			self.apktool = self.cwfolder + "/tools/apktool2.0" + "/apktool.jar"

		if self.ostype == "darwin":
			os.system(
				"java -Xmx256M -Djava.awt.headless=true -jar " + self.apktool + " b " + self.dest + "/apktool")
		elif self.ostype == "Windows":
			os.system("java -jar -Duser.language=en " + self.apktool + " b " + self.dest + "\\apktool")
		else:
			os.system("java -Xmx256M -jar " + self.apktool + " b " + self.dest + "/apktool")

if __name__ == "__main__":
	main()