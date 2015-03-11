import sys
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
import re, os, time
import urllib, urllib2
import json

ROOTDIR = xbmcaddon.Addon(id='plugin.video.amaproracing').getAddonInfo('path')
FANART = ROOTDIR+'/images/fanart_supercross.jpg'
ICON = ROOTDIR+'/images/icon_supercross.png'
LIVE_FANART = 'http://www.supercrosslive.com/sites/default/files/Hero_slide_RDL.jpg'

class supercross():

    def CATEGORIES(self):        
        self.addDir('Race Day Live','/supercross/live',202,ICON,LIVE_FANART)        
        self.addDir('Race Day Archive','/supercross/archive',203,ICON)
        self.addDir('View Supercross Youtube Channel','/supercross/youtube',201,ICON)                


    def RACE_DAY_LIVE(self):                               

        #Attempt to get the Live Stream
        try:            
            json_source = self.GET_LIVESTREAM_INFO()
            self.LIVESTREAM_LINK(str(json_source['upcoming_events']['data'][0]['id']))
        except:
            #Get the next live stream date
            url = 'http://www.supercrosslive.com/race-day-live'
            req = urllib2.Request(url) 
            req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36') 
            #req.add_header('Referer', 'http://www.promotocross.com/motocross/live')
            response = urllib2.urlopen(req) 
            html = response.read()
            start = html.find('<h2> Race Day Live presented')
            end = html.find('</h2>', start)
            next_stream = html[start+5:end]
            
            self.addLink(next_stream,'',next_stream, LIVE_FANART)
            
        finally:
            pass
        
            
    def RACE_DAY_ARCHIVE(self):
        try:
            json_source = self.GET_LIVESTREAM_INFO()
            #Load all past events
            for past_event in json_source['past_events']['data']:            
                self.LIVESTREAM_LINK(str(past_event['id']))
        except:
            pass


    def GET_LIVESTREAM_INFO(self):
        #Get Supercross livestream.com info
        url = 'http://new.livestream.com/api/accounts/1543541'
        req = urllib2.Request(url) 
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36') 
        #req.add_header('Referer', 'http://www.promotocross.com/motocross/live')
        response = urllib2.urlopen(req)        
        #data_sources = response.read()
        json_source = json.load(response)
        response.close()  

        return json_source


    def LIVESTREAM_LINK(self,event_id):
        url = 'http://new.livestream.com/api/accounts/1543541/events/'+event_id+'/feed.json?&filter=video'
        #print url
        try:
            req = urllib2.Request(url) 
            req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36')             
            response = urllib2.urlopen(req)                    
            json_source = json.load(response)
            response.close()

            name = json_source['data'][0]['data']['caption']
            img_url = json_source['data'][0]['data']['thumbnail_url']

            #Attempt to get the HD feed, if not try for the SD
            try:
                live_url = json_source['data'][0]['data']['progressive_url_hd']
                self.addLink(name, live_url, name, img_url)
            except:
                live_url = json_source['data'][0]['data']['progressive_url']
                self.addLink(name, live_url, name, img_url)
            finally:
                pass
        except:
            pass


    def SUPERCROSS_YOUTUBE_CHANNEL(self):        
        win = str(xbmcgui.getCurrentWindowId())
        xbmc.executebuiltin('ActivateWindow('+win+',plugin://plugin.video.youtube/user/SupercrossLive/,return)')



    def addLink(self,name,url,title,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image',FANART)
        liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


    def addDir(self,name,url,mode,iconimage,fanart=None):       
        ok=True
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage=ICON, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if fanart != None:
            liz.setProperty('fanart_image', fanart)
        else:
            liz.setProperty('fanart_image', FANART)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)    
        return ok

