import os
import sys
import requests
from xml.etree import ElementTree as ET

maildom = sys.argv[1]

folder_zero = sys.argv[2]

final_lst = []

srclst = ["baidu", "bing", "censys", "crtsh", "google", "google-certificates", "googleplus", "google-profiles", "linkedin", "netcraft", "pgp", "threatcrowd", "twitter", "vhost", "virustotal", "yahoo"]

def chkfold():
	folder_exists = os.path.isdir(folder_zero)
	if folder_exists:
		print("-----------------COOL, We are good to go-------------------")
	else:
		print("-----------------The folder does not exists----------------")
		exit(0)

def chkmdom():
	if '.' in maildom:
		pass
	else:
		print("----------------The domain name is not correct...----------------")
		exit(0)

def mkcmd(src):
		chkmdom()
		chkfold()
		cmd1 = "theharvester -d " + maildom + " -b " + src + " -f " + folder_zero + "/" + src + "/" + src + ".html"
		return cmd1

def getharvest(src):
	os.system("mkdir " + folder_zero + "/" + src)
	realcmd = mkcmd(src)
	print("=============== Harvesting From " + src + " ================")
	os.system(realcmd)

def save_in_list(src):
	xmlpath = folder_zero + "/" + src + "/" + src + ".xml"
	file_exists = os.path.isfile(xmlpath)
	if file_exists:
		tree = ET.parse(xmlpath)
		root = tree.getroot()
		for email in root.findall("./email"):
			final_lst.append(email.text)
			print(email.text)
	else:
		print("------------------- " + src + " --- XML file does not exist... --------------------")

def saveres(email_lst):
	result_file = folder_zero + "/res.lst"
	file_res = open(result_file, "a")
	for mail_name in email_lst:
		file_res.write(mail_name + "\n")
	file_res.close()

def fullprocess():
	for src in srclst:
		getharvest(src)
		save_in_list(src)
	saveres(final_lst)

fullprocess()

cwdir = os.getcwd()
os.system("mv " + cwdir + "/report.html " + folder_zero + "/report.html")
os.system("mv " + cwdir + "/stash.sqlite " + folder_zero + "/stash.sqlite")
