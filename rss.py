import globals

import urllib2

from xml.dom.minidom import parse, parseString



def getText(element):
    rc = []
    for node in element.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getEntries( blogurl=globals.BLOGURL , limit=3, label=None ):

	rssurl = globals.BLOGURL + "/rss"
	if label != None:
		rssurl = globals.BLOGURL + "/tagged/" + label + "/rss"
	
	request = urllib2.Request( rssurl )
	response = urllib2.urlopen(request)
	
	dom = parse( response )
	
	posts = []
	
	for item in dom.getElementsByTagName("item"):
		post = {}
		
		post['title'] =  getText( item.getElementsByTagName("title")[0]  )
		
		post['content'] =  getText( item.getElementsByTagName("description")[0]  )
		
		if len( item.getElementsByTagName("pubDate") ) > 0:
			post['pubDate'] = getText(  item.getElementsByTagName("pubDate")[0] )
			
		for link in item.getElementsByTagName("link"):
			post['url'] = getText( link )
			post['commenturl'] = post['url'] + "#disqus_thread"
		
		posts.append(post)
		
		if len(posts) >= limit:
			break
		
	return posts