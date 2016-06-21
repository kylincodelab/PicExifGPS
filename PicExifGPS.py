#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-22 00:08:37
# @Author  : 14zyn0s noemail@h4ck.com
# @Link    : 
# @Version : $1$

import os
import urllib2
import optparse
from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS

#find the images in url
def findImages(url):
	print "[+] Finding images on "+url
	urlContent=urllib2.urlopen(url).read()
	soup=BeautifulSoup(urlContent,'html.parser')
	imgTags=soup.findAll('img')
	return imgTags
	
#try to download the image
def donwloadImage(imagTag):
	try:
		
		imgSrc=imagTag['src']
		print "[+] Downloading image-->"+imgSrc
		imgContent=urllib2.urlopen(imgSrc).read()
		imgFilName=basename(urlsplit(imgSrc)[2])
		imgFile=open(imgFilName,"wb")
		imgFile.write(imgContent)
		imgFile.close()
		return imgFilName
	except Exception, e:
		return ''

def testForExif(imgFilName):
	try:
		exifData={}
		imgFile=Image.open(imgFilName)
		info=imgFile._getexif()
		if info:
			for (tag,value) in info.items():
				decoded=TAGS.get(tag,tag)
				exifData[decoded]=value
				exifGPS=exifData['GPSINFO']
				if exifGPS:
					print "[*] "+imgFilName+"Contain GPS MetaData"
	except Exception, e:
		pass
def main():
	parser=optparse.OptionParser("usage%prog "+"-u <target url>")
	parser.add_option("-u",dest="url",type="string",help="specify a target url")
	
	(options,args)=parser.parse_args()

	url=options.url

	if url==None:
		print "[-] "+parser.usage
		exit(0)
	else:
		print "[+] Proccessing..."
		imgTags=findImages(url)
		for imgTag in imgTags:
			imgFilName=donwloadImage(imgTag)
			testForExif(imgFilName)
	print "[+] Handling Successfully..."

if __name__ == '__main__':
	main()
