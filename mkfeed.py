import twitter, re, datetime, PyRSS2Gen

file = "/var/www/timsaylor.com/twitterlinkfeed.xml"
url = unicode(r"(?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~/|/)?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?")

def getURLs(text):
   #url=unicode(r"((http|ftp)://)?(((([\d]+\.)+){3}[\d]+(/[\w./]+)?)|([a-z]\w*((\.\w+)+){2,})([/][\w.~]*)*)")
   return [a.group() for a in re.finditer(url,text)]

def hasURLs(text):
    return ( re.search(url, text) != None )

def convertLinks(text):
    return text

def mkFeedItem(status):
   return PyRSS2Gen.RSSItem(
            title = status.user.name,
            link = convertLinks(status.user.url),
            description = status.text,
#            guid = PyRSS2Gen.Guid(status.text),
            pubDate = status.created_at #datetime.datetime(2003, 9, 6, 21, 31) # get the right date/time from python-twitter
          )

def mkFeed(statuses):
   rss = PyRSS2Gen.RSS2(
       title = "Twitter Links",
       link = "www.twitter.com",
       description = "Your friends' stupid links",
       items = [mkFeedItem(status) for status in statuses],
       lastBuildDate = datetime.datetime.now()   )

   rss.write_xml(open(file, "w"))



api = twitter.Api(username="", password="") # XXX your user/pass

allstatuses = api.GetFriendsTimeline("") #  XXX your username
#alltext = [(s.user.name, s.text, s.created_at) for s in statuses]

# get one list of URLs, even if there are multiple URLs in some posts
urlstatuses = []
for status in allstatuses:
    if hasURLs(status.text):
       urlstatuses.append (status)

mkFeed(urlstatuses)
