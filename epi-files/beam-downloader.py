#!/usr/bin/python3
import sys
import requests
from packaging import version
import xml.etree.ElementTree as ET
import time

def extractRelease(f):
    parts = f.split('_')
    if len(parts) >= 3:
        return parts[1]
    return "0.0.0"  # fallback if no version found
#def extractRelease

def getXml(awsUrl):
	response = requests.get(awsUrl)
	response.raise_for_status() 

	root = ET.fromstring(response.content)
	releaseArray=[]
	for elem in root.iter():
		if elem.text!=None:
			if elem.text.endswith(".deb"): 
				release=elem.text.split("/")[-1]
				if release.count("-")==1:
					releaseArray.append(elem.text)
	releases = sorted(releaseArray, key=lambda f: version.parse(extractRelease(f)))
	return releases[-1]
#def getXml

if __name__ == "__main__":
	output="{}.deb".format(sys.argv[1])
	awsUrl = "https://beamstudio.s3-ap-northeast-1.amazonaws.com/"
	lastRelease = getXml(awsUrl)
	if lastRelease.endswith(".deb"):
		url="{}{}".format(awsUrl,lastRelease)
		print("Downloading {}".format(url))
		content=requests.get(url,stream=True)
		progressA="Downloading "
		progress=["|","/","-","\\"]
		cont=0
		otime=time.time()
		with open(output,"wb") as f:
			for fchunk in content.iter_content(chunk_size=9082):
				if fchunk!=None:
					f.write(fchunk)
					if time.time()-otime>=0.2:
						out=progressA+progress[int(cont)]
						print(out,end="\r")
						cont+=1
						if cont>=len(progress):
							cont=0
						otime=time.time()
		print("")
