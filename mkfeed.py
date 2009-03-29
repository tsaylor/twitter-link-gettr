import twitter, re, datetime, PyRSS2Gen, urllib2, settings, sys

url = unicode(r"(?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~/|/)?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?")

def getURLs(text):
   # url=unicode(r"((http|ftp)://)?(((([\d]+\.)+){3}[\d]+(/[\w./]+)?)|([a-z]\w*((\.\w+)+){2,})([/][\w.~]*)*)")
   return [a.group() for a in re.finditer(url,text)]

def hasURLs(text):
    return ( re.search(url, text) != None )

def convertLinks(text):
    links = [a.group() for a in re.finditer(url,text)]
    # swap links found in above for actual links
    for link in links:
        text = re.sub(link, "<a href='%s' target='_blank'>%s</a>" % (link,link), text)
    return text

def mkFeedItem(status):
   return PyRSS2Gen.RSSItem(
            title = status.user.name,
            link = status.user.url,
            description = convertLinks(status.text),
            # guid = PyRSS2Gen.Guid(status.text),
            pubDate = status.created_at #datetime.datetime(2003, 9, 6, 21, 31) # get the right date/time from python-twitter
          )

def mkFeed(statuses):
   rss = PyRSS2Gen.RSS2(
       title = "Twitter Links",
       link = "www.twitter.com",
       description = "Your friends' stupid links",
       items = [mkFeedItem(status) for status in statuses],
       lastBuildDate = datetime.datetime.now()   )

   rss.write_xml(open(settings.FILE, "w"))


try:
    api = twitter.Api(username=settings.USERNAME, password=settings.PASSWORD)

    allstatuses = api.GetFriendsTimeline(settings.USERNAME)
except urllib2.HTTPError:
    sys.exit()

# get one list of URLs, even if there are multiple URLs in some posts
urlstatuses = []
for status in allstatuses:
    if hasURLs(status.text):
       urlstatuses.append (status)

mkFeed(urlstatuses)
