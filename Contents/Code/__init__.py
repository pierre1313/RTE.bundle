# PMS plugin framework
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
import re

####################################################################################################

VIDEO_PREFIX = "/video/rte"

NAME = L('RTE')

# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART           = 'art-default.jpg'
ICON          = 'icon-default.png'

FEEDBASE = "http://dj.rte.ie/vodfeeds/feedgenerator/"

MRSS  = {'media':'http://search.yahoo.com/mrss/'}
RTE   = {'rte':'http://www.rte.ie/schemas/vod'}

CACHE_TIME = 3600

####################################################################################################

def Start():

    ## make this plugin show up in the 'Video' section
    ## in Plex. The L() function pulls the string out of the strings
    ## file in the Contents/Strings/ folder in the bundle
    ## see also:
    ##  http://dev.plexapp.com/docs/mod_Plugin.html
    ##  http://dev.plexapp.com/docs/Bundle.html#the-strings-directory
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, L('VideoTitle'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    ## see also:
    ##  http://dev.plexapp.com/docs/Objects.html
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

def UpdateCache():
  HTTP.PreCache(FEEDBASE + "videos/live/?id=7", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "latest/?limit=20", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "lastchance/?limit=20", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "genre/?id=Entertainment", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "genre/?id=Drama", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "genre/?id=News%20and%20Sport", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "genre/?id=Factual", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "genre/?id=Lifestyle", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "genre/?id=Arts%20and%20Music", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "genre/?id=Religious%20and%20Irish%20Language", CACHE_TIME)
  HTTP.PreCache(FEEDBASE + "genre/?id=The%20Den%2C%20Den%20Tots%2C%20Two%20Tube", CACHE_TIME)
  GetCollectionsMenu(ItemInfoRecord())

def VideoMainMenu():

    dir = MediaContainer(viewGroup="List")
    #Live Stream
    feed = HTTP.Request(FEEDBASE + "videos/live/?id=7").replace('media:','media')
    for entry in XML.ElementFromString(feed, True).xpath("//feed/entry"):
      desc = entry.xpath("content")[0].text
#      duration = 0
      thumb = entry.xpath("mediathumbnail")[0].get('url')
      link = 'http://www.rte.ie/player/#l=7'#entry.xpath("link[@rel='alternate']")[0].get('href')
#      Log(link)
      dir.Append(WebVideoItem(url=link,title="Live",summary=desc,thumb=thumb))

    #dir.Append(Function(DirectoryItem(RSS_parser,"Live"),pageurl = FEEDBASE + "videos/live/?id=7"))
    #Other streams 
    dir.Append(Function(DirectoryItem(RSS_parser,"Latest"),pageurl = FEEDBASE + "latest/?limit=20"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Last Chance"),pageurl = FEEDBASE + "lastchance/?limit=20"))
    dir.Append(Function(DirectoryItem(CategoriesSubMenu,"Categories")))
    dir.Append(Function(DirectoryItem(AZSubMenu,"A to Z")))
    return dir

def CategoriesSubMenu (sender):
    dir = MediaContainer(title2="Live", viewGroup="List")

    dir.Append(Function(DirectoryItem(RSS_parser,"Entertainment"),pageurl = FEEDBASE + "genre/?id=Entertainment"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Drama"),pageurl = FEEDBASE + "genre/?id=Drama"))
    dir.Append(Function(DirectoryItem(RSS_parser,"News and Sports"),pageurl = FEEDBASE + "genre/?id=News%20and%20Sport"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Factual"),pageurl = FEEDBASE + "genre/?id=Factual"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Lifestyle"),pageurl = FEEDBASE + "genre/?id=Lifestyle"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Arts and Music"),pageurl = FEEDBASE + "genre/?id=Arts%20and%20Music"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Religious and Irish language"),pageurl = FEEDBASE + "genre/?id=Religious%20and%20Irish%20Language"))
    dir.Append(Function(DirectoryItem(RSS_parser,"The Den Den Tots Two Tube"),pageurl = FEEDBASE + "genre/?id=The%20Den%2C%20Den%20Tots%2C%20Two%20Tube"))

    return dir

def AZSubMenu (sender):
    dir = MediaContainer(title2="A to Z", viewGroup="List")

    for entry in XML.ElementFromURL('http://dj.rte.ie/vodfeeds/feedgenerator/azlist/', True).xpath("//feed/entry"):
        character = entry.xpath("title")[0].text
        dir.Append(Function(DirectoryItem(RSS_parser,character),pageurl = FEEDBASE + "az/?id="+character))
    return dir

def RSS_parser(sender, pageurl , replaceParent=False):
#    tags = RSS.FeedFromURL(pageurl)
    dir = MediaContainer(title2=sender.itemTitle, viewGroup="List", replaceParent=replaceParent)
    #Log(
    feed = HTTP.Request(pageurl).replace('media:','media').replace('rte:','rte')
    #Log(feed)
    for entry in XML.ElementFromString(feed, True).xpath("//feed/entry"):
      title = entry.xpath("title")[0].text
      desc = entry.xpath("content")[0].text
      duration = entry.xpath("rteduration")[0].get('ms')
      thumb = entry.xpath("mediathumbnail")[0].get('url')
      #Log(thumb)
      link = entry.xpath("link[@rel='alternate']")[0].get('href')
#      Log(link)
#      feed = HTTP.Request(link).replace('media:','media').replace('rte:','rte')
      #Log(feed)
#      xml = XML.ElementFromString(feed, True)
      #Log(xml.xpath('//title')[0].text)
    # video_pattern = re.compile('url=\"rtmpte([^"]+).mp4')
#      Log(XML.StringFromElement(xml))
    #video = video_pattern.search(XML.StringFromElement(xml))
      #content = xml.xpath("//mediacontent")
#      for c in xml.xpath("//mediacontent"):
#        video = c.get('url')
#        Log(video)
#        if c.get('type') == 'video/mp4':
     #     video = c.get('url')
     #     Log(video)
#          video = video.replace('rtmpte','http').replace('rtmpe','http').replace('mp4:/','')
#          break
#      else:
#        duration = 0
#        content = entry.xpath('//mediacontent[@type=video/mp4]')[0].get('url').replace('rtmpe','http')
      #video_pattern = re.compile('url=\"rtmpe([^"]+)"')
      #Log(XML.StringFromElement(entry))
      #video = video_pattern.search(XML.StringFromElement(entry))
      #  if video != None:
      #    video = 'http'+video.group(1)
      #video = xml.xpath('//media:group/media:content[@type=video/mp4]', namespaces = MRSS)[0].get('url')
     # Log(link)
      dir.Append(WebVideoItem(url=link,title=title,summary=desc,thumb=thumb,duration=duration))
#   for tag in tags["entries"]:
#      (stream , vignette) = get_stream(tag["link"])
#      if stream != None:
#        dir.Append(WebVideoItem(stream,width=384,height=216,title=tag["title"],summary='',thumb=vignette))
    return dir
