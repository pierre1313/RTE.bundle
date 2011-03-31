# -*- coding: utf-8 -*-
import re

####################################################################################################

VIDEO_PREFIX = "/video/rte"

NAME = L('RTE')

ART  = 'art-default.jpg'
ICON = 'icon-default.png'

FEEDBASE = "http://dj.rte.ie/vodfeeds/feedgenerator/"
LIVEURL = "http://www.rte.ie/player/#l=7"

MRSS  = {'media':'http://search.yahoo.com/mrss/'}
RTE   = {'rte':'http://www.rte.ie/schemas/vod'}

####################################################################################################
def Geo():
    country_code = HTML.ElementFromURL(FEEDBASE+'cl/').xpath("//geoinfo/country")[0]
    if country_code.text == "ie":
      return "#domestic"
    else:
      return "#international"

def Start():
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)
    WebVideoItem.thumb = R(ICON)

    HTTP.CacheTime = CACHE_1HOUR
    
    Dict['geo_code']=str(Geo())

def UpdateCache():
  HTTP.PreCache(FEEDBASE + "videos/live/?id=7")
  HTTP.PreCache(FEEDBASE + "latest/?limit=20")
  HTTP.PreCache(FEEDBASE + "lastchance/?limit=20")
  HTTP.PreCache(FEEDBASE + "genre/?id=Entertainment")
  HTTP.PreCache(FEEDBASE + "genre/?id=Drama")
  HTTP.PreCache(FEEDBASE + "genre/?id=News%20and%20Sport")
  HTTP.PreCache(FEEDBASE + "genre/?id=Factual")
  HTTP.PreCache(FEEDBASE + "genre/?id=Lifestyle")
  HTTP.PreCache(FEEDBASE + "genre/?id=Arts%20and%20Music")
  HTTP.PreCache(FEEDBASE + "genre/?id=Religious%20and%20Irish%20Language")
  HTTP.PreCache(FEEDBASE + "genre/?id=RT%C3%89jr%2C%20TRT%C3%89%2C%20Two%20Tube")

def VideoMainMenu():

    dir = MediaContainer(viewGroup="List")
    #Live Stream
    feed = (HTTP.Request(FEEDBASE + "videos/live/?id=7").content).encode("Latin1",'ignore').replace('media:','media')
    for entry in HTML.ElementFromString(feed).xpath("//feed/entry"):
      desc = entry.xpath("content")[0].text
      thumb = entry.xpath("mediathumbnail")[0].get('url')
      link = LIVEURL + Dict['geo_code']

      dir.Append(WebVideoItem(url=link,title="Live",summary=desc,thumb=thumb))

    dir.Append(Function(DirectoryItem(RSS_parser,"Latest"),pageurl = FEEDBASE + "latest/?limit=20"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Last Chance"),pageurl = FEEDBASE + "lastchance/?limit=20"))
    dir.Append(Function(DirectoryItem(CategoriesSubMenu,"Categories")))
    dir.Append(Function(DirectoryItem(AZSubMenu,"A to Z")))
    return dir

def CategoriesSubMenu (sender):
    dir = MediaContainer(title2="Categories", viewGroup="List")

    dir.Append(Function(DirectoryItem(RSS_parser,"Entertainment"),pageurl = FEEDBASE + "genre/?id=Entertainment"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Drama"),pageurl = FEEDBASE + "genre/?id=Drama"))
    dir.Append(Function(DirectoryItem(RSS_parser,"News and Sports"),pageurl = FEEDBASE + "genre/?id=News%20and%20Sport"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Factual"),pageurl = FEEDBASE + "genre/?id=Factual"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Lifestyle"),pageurl = FEEDBASE + "genre/?id=Lifestyle"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Arts and Music"),pageurl = FEEDBASE + "genre/?id=Arts%20and%20Music"))
    dir.Append(Function(DirectoryItem(RSS_parser,"Religious and Irish language"),pageurl = FEEDBASE + "genre/?id=Religious%20and%20Irish%20Language"))
    dir.Append(Function(DirectoryItem(RSS_parser,"RTÉjr, TRTÉ, Two Tube"),pageurl = FEEDBASE + "genre/?id=RT%C3%89jr%2C%20TRT%C3%89%2C%20Two%20Tube"))

    return dir

def AZSubMenu (sender):
    dir = MediaContainer(title2="A to Z", viewGroup="List")

    for entry in HTML.ElementFromURL(FEEDBASE+'azlist/').xpath("//entry"):
      if entry.xpath("title")[0].text == None:
        continue
      else:
        character = entry.xpath("title")[0].text
      dir.Append(Function(DirectoryItem(RSS_parser,character),pageurl = FEEDBASE + "az/?id="+character))
    return dir

def RSS_parser(sender, pageurl , replaceParent=False):
    dir = MediaContainer(title2=sender.itemTitle, viewGroup="InfoList", replaceParent=replaceParent)

    feed = (HTTP.Request(pageurl).content).encode("Latin1","ignore").replace('media:','media').replace('rte:','rte')
    for entry in HTML.ElementFromString(feed).xpath("//entry"):
      title = entry.xpath("title")[0].text
      desc = entry.xpath("content")[0].text
      duration = entry.xpath("rteduration")[0].get('ms')
      thumb = entry.xpath("mediathumbnail")[0].get('url')
      link = entry.xpath("link[@rel='alternate']")[0].get('href') + Dict['geo_code']

      dir.Append(WebVideoItem(url=link,title=title,summary=desc,thumb=thumb,duration=duration))

    return dir
