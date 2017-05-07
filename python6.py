import requests

#request module allows us to get stuff from the internet

#part one - data collection - aka the getting stuff phase.

def getPageSource(url):
	page, link = getPageOne(url)
	p = 2
	listofurl = [link]
	total = ""
	nPages = pagetotal(url)
	while p <= nPages:
		page2url = url + "&page=" + str(p)
		listofurl.append(page2url)
		p = p + 1
	for i in listofurl:
		pagei, linki = getPageOne(i)
		total = total + pagei
	return total

#pretty simple function. it gets the full thread into python. For that it calls on 2 functions.
#first function below is the start of the whole script. It takes a given thread url and saves the first page, 
#it returns two things. 1, first page source in string, 2, the url - thread link. 

def getPageOne(link):
	url = link
	source = requests.get(url)
	page = source.content
	return str(page), url

#the function below uses the first page, and finds out how many pages there are in the whole thread

def pagetotal(link):
	pageOne, url = getPageOne(link)
	str1 = "Page 1 of "
	if str1 in pageOne:
		string = pageOne[pageOne.find(str1):pageOne.find(str1)+13]
		if string[-1] == '\r':
			return int(string[-3:-1])
		if string[-1] == '\n':
			return int(string[-3:-1])
		return int(string[-3:])
	else:
		string = 1
	return string


#put simply: we take a given thread url [no defensive programming!], then find out how many pages there are 
#in the thread, and then collect all the pages
#at this stage, its all quite hard to read. instead of using something like beautiful soup, I just did my own thing

#part 2 - parse content - clean house basically.
#there's only a few things we really need such as username, post url, and story title. 
#And that's mostly determined from the desired output - the entry. 
#knowing that, I set up splitting the page into the obvious posts.

def getNextTarget(p):
	postStart = p.find("<!-- / post")
	if postStart == -1:
		return None, 0
	postEnd = p.find("<!-- / post", postStart + 1)
	post = p[postStart:postEnd]
	return post, postEnd

#this finds the start of a post. And the end of a post. So naturally it knows the start of the next post.

def postUrl(p):
	UrlP1 = "http://www.neogaf.com/forum/showpost.php?p="
	check1 = p.find("postbit-post")
	showpostStart = p.find("showpost", check1)
	showpostEnd = p.find("amp", showpostStart + 1)
	start = p.find('div id="edit') + 12
	UrlP2 = p[start:p.find('"', start)]
	postStart = p.find("post", showpostEnd + 1)
	postEnd = p.find('"',postStart+1)
	UrlP3 = p[postStart:postEnd]
	return UrlP1+ UrlP2 + '&' + UrlP3

def getTitle(p):
	titleClass = p.find("post-meta post-meta-border")
	if titleClass == -1:
		return "untitled"
	else:
		titleStart = p.find("<strong>",titleClass + 1)
		titleEnd = p.find("</strong>",titleStart + 1)
		title = p[titleStart + 8:titleEnd]
		return title

#simple enough. getTitle gets whatever is in the title box [we need this to know the story title]
#returns untitled if nothing is put in there
# and post url, gets the url of the post - this is so if we add the post in the entry list, we'd know the post url

def extractName(p):
# find the username class
	postStart = p.find('<div class="postbit-details-username"')
	postEnd = p.find("</a>", postStart+1)
#create smaller target area
	post = p[postStart:postEnd]
#get rid of data that isn't needed
	post = post.replace('</span>', '')
#usernamer should be here:
	name = post.rfind('>')
	return post[name+1:]

#gets username. harder than you think. still some errors come up when I test for threads with a thousand posts. 
#still working on it. but anyways, since we know quite a bit about each post: start, end, posturl, title, we can
#make finally make it presentable. by that I mean, how it ought to look like in a line in the entry list

def cleanUpPost(p):
	post, postEnd = getNextTarget(p)
	userName = extractName(post)
	link = postUrl(post)
	title = getTitle(post)
	entryLine = userName + " - [url=" + link + "]" + title + "[/url]"
	return entryLine

# cleanup done, the following function finds href in each post, just so we can print out every post. Good diagnostic test. 
# script won't need this of course, but it does goes to show it's not a great leap to the finale.

def printAllhref(page):
	print """Entries:\n"""
	while True:
		post, postEnd = getNextTarget(page)
		if post:
			if "href" in post:
				print cleanUpPost(post) 
			page = page[postEnd:]
		else:
			break
		
#final functon searches posts for keyword and returns that in entry list format.

def printAllEntries(page):
	print """Entries:\n"""
	while True:
		post, postEnd = getNextTarget(page)
		if post:
			if "#entry" in post:
				print cleanUpPost(post) 
			page = page[postEnd:]
		else:
			break

#user input - lets the user enter a url.

print 'Hi... how are ya?'		
import requests
url = raw_input("Thread url? : ")
printAllEntries(getPageSource(url))
print """
""" 
 

