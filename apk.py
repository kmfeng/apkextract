#!/usr/bin/python

import os  # Folder creation, file handling, execution
import sys  # Handling file arguments
import platform  # Detect OS Types for different Java commands
import subprocess  # Detect Java version
import argparse

def javacheck():
	try:
		java = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
		javaversion = float(java.split('"')[1][0:3])

		if javaversion < 1.7:
			print(("[-] Java version", javaversion, "detected. Please install 1.7 or higher"))
			sys.exit()
		else:
			pass
	except:
		print(("Unexpected error:", sys.exc_info()[0]))
		pass

def filecheck(apk):
	try:
		filename, dotapk = os.path.splitext(apk)
		if os.path.isfile(apk):
			print(("[+] File", apk, "found!"))
			pass
		elif dotapk != ".apk":
			print(("[*] File", apk, "must have an apk file extension"))
			sys.exit(1)
		else:
			print(("[*] File", apk, "not found!"))
			sys.exit(1)
	except:
		sys.exit(1)

def foldercheck(recompfolder, ostype, cwd):
	if ostype == "Windows":
		outputfolder = recompfolder +  "\\apktool"
	else:
		outputfolder = recompfolder + "/apktool"

	if os.path.exists(outputfolder):
		print("[+] Detected previous apktool output folder.  Recompiling apk.")
		return True
	else:
		print("[*] No previous extracted APK folder found. Please extract APK first.")
		sys.exit(1)

def main():
	if len(sys.argv) == 1:
		print ("No arguments supplied. Type -h or --help")
		sys.exit(1)

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
			print("[*] Detected previous output folder.  Overwriting.")

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
		print("Not yet implemented")
		pass

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class Apk(object):
	def __init__(self, apk, dest, ostype, cwd):

		self.absapk = os.path.abspath(apk) # Absolute path to apk
		self.apk = apk # Apk file name
		self.dest = dest
		self.ostype = ostype
		self.cwfolder = cwd

	def apktool(self):
		try:
			if self.ostype == "Windows":
				self.apktool = self.cwfolder + "\\tools\\apktool2.0" + "\\apktool.jar"
			else:
				self.apktool = self.cwfolder + "/tools/apktool2.0" + "/apktool.jar"

			print(("[+] Extracting", self.apk, "to working folder", self.dest))

			if self.ostype == "darwin":
				os.system(
					"java -Xmx256M -Djava.awt.headless=true -jar " + self.apktool + " d -f " + self.apk + " -o " + self.dest + "/apktool")
			elif self.ostype == "Windows":
				os.system("java -jar -Duser.language=en " + self.apktool + " d -f " + self.apk + " -o " + self.dest + "\\apktool")
			else:
				os.system("java -Xmx256M -jar " + self.apktool + " d -f " + self.apk + " -o " + self.dest + "/apktool")

			self.enjarify()
		except Exception as e: print((str(e)))

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

	def enjarify(self):
		try:
			if self.ostype == "Windows":
				with cd("tools\\enjarify"):
					self.enjarifytool = self.cwfolder + "\\tools\\enjarify\\enjarify" + "\\enjarify.bat"
					self.enjararfile = self.cwfolder + "\\" + self.apk[:-4] + "-enjar.jar"
					print(("[+] Running Enjarify on", self.absapk))
					os.system(enjarifyrun)
			else:
				with cd("tools/enjarify"):
					self.enjarifytool = self.cwfolder + "/tools/enjarify" + "/enjarify.sh"
					self.enjararfile = self.cwfolder + "/" + self.apk[:-4] + "-enjar.jar"
					enjarifyrun = self.enjarifytool + " " + self.absapk + " -o " + self.enjararfile + " --force"
					print(("DEBUG", enjarifyrun))
					print(("[+] Running Enjarify on", self.absapk))
					os.system(enjarifyrun)

			# After running we pass over to jd-cli to extract jar file
			if os.path.isfile(self.enjararfile):
				print(("[+] Detected jar file: ", self.enjararfile))
				self.jd()
		except Exception as e: print((str(e)))

	def jd(self):
		try:
			if self.ostype == "Windows":
				jdfolder = self.dest + "\\jdtool"
				jdfmove = self.dest + "\\" + self.apk[:-4] + "-enjar.jar"
				jdargs = "java -jar " + self.cwfolder + "\\tools\\jd-cmd-0.9.1\\jd-cli.jar " + self.enjararfile + " -od " + jdfolder
			else:
				jdfolder = self.dest + "/jdtool"
				jdfmove = self.dest + "/" + self.apk[:-4] + "-enjar.jar"
				jdargs = "java -jar " + self.cwfolder + "/tools/jd-cmd-0.9.1/jd-cli.jar " + self.enjararfile + " -od " + jdfolder

			print(("[+] Decompiling: ", self.enjararfile, "\n[+] Output decompile:", jdfolder))
			os.makedirs(jdfolder)
			os.system(jdargs)
			os.rename(self.enjararfile, jdfmove)  # Move jar file into working folder

		except Exception as e: print((str(e)))

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