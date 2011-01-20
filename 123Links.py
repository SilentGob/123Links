#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By SilentGob
#
# Licensed under BSD

"""123Links

Get links from the 123people website
"""
import urllib, random
import HTMLParser, sys, getopt


# template strings for HTML output
HTMLSection = '<h2>%s</h2>'
HTMLLink = '<a href="%s">%s (%s)</a>'

# list of User Agen Strings to use for request
UAStrings = ["Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9",
							"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
							"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; fr-FR)",
							"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; fr-fr) AppleWebKit/534.15+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"]

# list of link we don't want to see in list
BlackList = [".1and1.", "wikipedia.org", "123people."]

class MyURLopener(urllib.FancyURLopener):
	version = random.choice(UAStrings)

class LinksParser(HTMLParser.HTMLParser):
  def __init__(self):
    HTMLParser.HTMLParser.__init__(self)
    self.recording = 0
    self.data = []

  def handle_starttag(self, tag, attributes):
		if self.recording:
			if tag == 'div':
				self.recording += 1
			if tag == 'a':
				if self.validLink(attributes[0][1]):
					self.data.append(attributes)
		else:
			if tag == 'div':
				for name, value in attributes:
					if name == 'class' and value == 'results':
						self.recording = 1
						break

  def handle_endtag(self, tag):
    if tag == 'div' and self.recording:
      self.recording -= 1
			
  def validLink(self, link):
		res = True
		if not link.startswith('http'):
			res = False
		else:
			for bl in BlackList:
				if link.find(bl) >= 0:
					res = False
					break
		return res

def usage():
	print """Usage:
123Links [-o outputMethod] 123PeopleURL

-o specifies the output method of the links (by default text)
	currently only 'html' is supported

Your 123PeopleURL must start with 'http://www.123people.'
"""

def textOutput(finalList):
	for section in finalList:
		print '\n',section
		for link in finalList[section]:
			print '%s (%s)' %(link[0], link[1])

def HTMLOutput(finalList):
	for section in finalList:
		print HTMLSection %section
		for link in finalList[section]:
			print HTMLLink %(link[0], link[0], link[1])

def getLinks(url123):
	# get links from web site
	urllib._urlopener = MyURLopener()
	opener = urllib.FancyURLopener({})
	f = opener.open(url123)
	page = f.read()
	parser = LinksParser()
	parser.feed(page)
	return parser.data

def sortLinks(data):
	# sort the links by section
	finalList = {}
	for d in data:
		tmp = {}
		for name, value in d:
			tmp[name] = value
		if not 'people_section' in tmp.keys():
			tmp['people_section'] = 'default'
		if not 'people_source' in tmp.keys():
			tmp['people_source'] = 'no source'
		section = tmp['people_section']
		if not section in finalList.keys():
			finalList[section] = []
		finalList[section].append([tmp['href'], tmp['people_source']])

	return finalList

def main():
    # parse command line options
    try:
			opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    output = 'text'
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
						if a == 'html':
							output = 'html'
        else:
						assert False, 'unhandled option'
		
    if len(args) != 1:
			usage()
			sys.exit(0)
    url123 = args[0]

    if not url123.startswith("http://www.123people."):
			print "Bad URL should start with: http://www.123people."
			exit(2)
		
    links = getLinks(url123)
    finalList = sortLinks(links)

    if output == 'html':
			HTMLOutput(finalList)
    else:
			textOutput(finalList)


if __name__ == "__main__":
    main()
