# -*- coding: utf-8 -*-
#------------------------------------------------------------
# palcoTV - XBMC Add-on by Juarrox (juarrox@gmail.com)
# Version 0.2.5 (15.05.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools



art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/playlists', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))
icon = art + 'icon.png'
fanart = 'fanart.jpg'


# Entry point
def run():
    
    plugintools.log("---> palcoTV.run <---")
    plugintools.set_view(plugintools.LIST)
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
       action = params.get("action")
       url = params.get("url")
       exec action+"(params)"

    plugintools.close_item_list()
       
  
# Main menu

def main_list(params):
    plugintools.log("palcoTV.main_list "+repr(params))
    data = plugintools.read("https://dl.dropboxusercontent.com/u/8036850/palcotv028.xml")

    matches = plugintools.find_multiple_matches(data,'<menu_info>(.*?)</menu_info>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        date = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        plugintools.add_item( action="" , title = title + date , fanart = art+'fanart.jpg' , thumbnail=art+'icon.png' , folder = False , isPlayable = False )

    data = plugintools.read("https://dl.dropboxusercontent.com/u/8036850/palcotv028.xml")
    
    matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        action = plugintools.find_single_match(entry,'<action>(.*?)</action>')
        last_update = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')
        url = plugintools.find_single_match(entry,'<url>(.*?)</url>')
        date = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')
      
        if thumbnail == 'new.png':
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'new.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'special.png':
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'special.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'm3u7.png':  # Control para listas M3U
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'm3u7.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'p2p.png':  # Control para listas P2P
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'p2p.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'xml.png':  # Control para listas XML
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'xml.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'plx3.png':  # Control para listas PLX
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'plx3.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'agenda2.png':  # Control para listas XML
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR yellowgreen]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'agenda2.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'splive.png':  # Control para listas SPlive
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'agenda2.png' , url = url , folder = True , isPlayable = False )

        else:
            fixed = title
            plugintools.add_item( action = action, plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'icon.png' , url = url , folder = True , isPlayable = False )
        
                
                         

def play(params):
    # plugintools.direct_play(params.get("url"))
    # xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(params.get("url"))
    plugintools.play_resolved_url( params.get("url") )  # Esta es la única línea de la función, por si falla el experimento
            
              
 
def runPlugin(url):
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')


def live_items_withlink(params):
    plugintools.log("palcoTV.live_items_withlink "+repr(params))
    data = plugintools.read(params.get("url"))

    # ToDo: Agregar función lectura de cabecera (fanart, thumbnail, título, últ. actualización)
    header_xml(params)

    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')  # Localizamos fanart de la lista
    if fanart == "":
        fanart = art + 'fanart.jpg'
        
    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')  # Localizamos autor de la lista (encabezado)
    
    matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        title = title.replace("<![CDATA[", "")
        title = title.replace("]]>", "")
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        url = plugintools.find_single_match(entry,'<link>(.*?)</link>')
        url = url.replace("<![CDATA[", "")
        url = url.replace("]]>", "")
        plugintools.add_item(action = "play" , title = title , url = url , fanart = fanart , folder = False , isPlayable = True )
        

  
def xml_lists(params):
    plugintools.log("palcoTV.xml_lists "+repr(params))
    data = plugintools.read( params.get("url") )
    name_channel = params.get("plot")
    plugintools.log("name_channel= "+name_channel)
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR]' , thumbnail= art + 'special.png' , fanart = art + fanart , folder = False , isPlayable = False )

    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<fanart>([^<]+)</fanart>([^<]+)<action>([^<]+)</action>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    for biny, ciny, diny, winy, pixy, dixy, boxy, susy, lexy, muny, kiny in subchannel:
        plugintools.add_item( action = susy , title = ciny , url= muny , thumbnail = winy , fanart = art + fanart , folder = True , isPlayable = False )
        plugintools.log("fanart= "+fanart)
        plugintools.log("thumbnail= "+winy)
        

       
def getstreams_now(params):
    plugintools.log("palcoTV.getstreams_now "+repr(params))
    
    data = plugintools.read( params.get("url") )
    poster = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    plugintools.add_item(action="" , title='[COLOR blue][B]'+poster+'[/B][/COLOR]', url="", folder =False, isPlayable=False)
    matches = plugintools.find_multiple_matches(data,'<title>(.*?)</link>')
    
    for entry in matches:
        title = plugintools.find_single_match(entry,'(.*?)</title>')
        url = plugintools.find_single_match(entry,'<link> ([^<]+)')
        plugintools.add_item( action="play" , title=title , url=url , folder = False , isPlayable = True )
        
      
def p2plinks(params):
    plugintools.log("palcoTV.livetv "+repr(params))
      
    data = plugintools.read( params.get("url") )
    matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        ace_url = plugintools.find_single_match(entry,'<link>(.*?)</link>')
        last_update = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        url = 'plugin://plugin.video.p2p-streams/?url=' + ace_url + '&mode=1&name=' + title + ')'
        plugintools.add_item( action="play" , title='[COLOR white]'+title+'[/COLOR]' , url=url , thumbnail=art + thumbnail , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
        

# Soporte de listas de canales por categorías (Livestreams, XBMC México, Motor SportsTV, etc.). 

def livestreams_channels(params):
    plugintools.log("palcoTV.livestreams_channels "+repr(params))
    data = plugintools.read( params.get("url") )
       
    # Extract directory list
    thumbnail = params.get("thumbnail")
    
    if thumbnail == "":
        thumbnail = 'icon.jpg'
        plugintools.log(thumbnail)
    else:
        plugintools.log(thumbnail)
    
    if thumbnail == art + 'icon.png':
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</items>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_subchannels" , title=title , url=params.get("url") , thumbnail=thumbnail , fanart=fanart , folder = True , isPlayable = False )

    else:
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</items>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_items" , title=title , url=params.get("url") , fanart=fanart , thumbnail=thumbnail , folder = True , isPlayable = False )
   
        
def livestreams_subchannels(params):
    plugintools.log("palcoTV.livestreams_subchannels "+repr(params))

    data = plugintools.read( params.get("url") )
    # title_channel = params.get("title")
    title_channel = params.get("title")
    name_subchannel = '<name>'+title_channel+'</name>'
    data = plugintools.find_single_match(data, name_subchannel+'(.*?)</channel>')
    info = plugintools.find_single_match(data, '<info>(.*?)</info>')
    title = params.get("title")
    plugintools.set_view(plugintools.LIST)
    plugintools.add_item( action="" , title='[B]'+title+'[/B] [COLOR yellow]'+info+'[/COLOR]' , folder = False , isPlayable = False )

    subchannel = plugintools.find_multiple_matches(data , '<name>(.*?)</name>')
    for entry in subchannel:
        plugintools.add_item( action="livestreams_subitems" , title=entry , url=params.get("url") , thumbnail=art+'motorsports-xbmc.jpg' , folder = True , isPlayable = False )


# Pendiente de cargar thumbnail personalizado y fanart...
def livestreams_subitems(params):
    plugintools.log("palcoTV.livestreams_subitems "+repr(params))

    title_subchannel = params.get("title")
    data = plugintools.read( params.get("url") )
    source = plugintools.find_single_match(data , title_subchannel+'(.*?)<subchannel>')

    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>').findall(source)
    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")
    
    for entry, quirry, winy in titles:
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = thumbnail , folder = False , isPlayable = True )


def livestreams_items(params):
    plugintools.log("palcoTV.livestreams_items "+repr(params))

    title_subchannel = params.get("title")
    plugintools.log("title= "+title_subchannel)    
    title_subchannel_fixed = title_subchannel.replace("Ã±", "ñ")
    title_subchannel_fixed = title_subchannel_fixed.replace("\\xc3\\xb1", "ñ")    
    title_subchannel_fixed = plugintools.find_single_match(title_subchannel_fixed, '([^[]+)')
    title_subchannel_fixed = title_subchannel_fixed.encode('utf-8', 'ignore')
    plugintools.log("subcanal= "+title_subchannel_fixed)
    if title_subchannel_fixed.find("+") >= 0:
        title_subchannel_fixed = title_subchannel_fixed.split("+")
        title_subchannel_fixed = title_subchannel_fixed[1]
        title_subchannel_fixxed = title_subchannel_fixed[0]
        if title_subchannel_fixed == "":
            title_subchannel_fixed = title_subchannel_fixxed
        
    data = plugintools.read( params.get("url") )
    source = plugintools.find_single_match(data , title_subchannel_fixed+'(.*?)</channel>')
    plugintools.log("source= "+source)
    fanart_channel = plugintools.find_single_match(source, '<fanart>(.*?)</fanart>')
    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>([^<]+)<thumbnail>([^<]+)</thumbnail>').findall(source)
       
    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")
    
    for entry, quirry, winy, xiry, miry in titles:
        plugintools.log("title= "+entry)
        plugintools.log("url= "+winy)
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = miry , fanart = fanart_channel , folder = False , isPlayable = True )


def xml_items(params):
    plugintools.log("palcoTV.xml_items "+repr(params))
    data = plugintools.read( params.get("url") )
    thumbnail = params.get("thumbnail")

    #Todo: Implementar una variable que permita seleccionar qué tipo de parseo hacer
    if thumbnail == "title_link.png":
        matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            url = plugintools.find_single_match(entry,'<link>([^<]+)</link>')
            fanart = plugintools.find_single_match(entry,'<fanart>([^<]+)</fanart>')
            plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )

    if thumbnail == "name_rtmp.png":
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            url = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
            plugintools.add_item( action = "play" , title = title , url = url , fanart = art + 'fanart.jpg' , plot = title , folder = False , isPlayable = True )

             
def simpletv_items(params):
    plugintools.log("palcoTV.simpletv_items "+repr(params))
    thumbnail = params.get("thumbnail")
    title = params.get("plot")    
    texto= params.get("texto")
    busqueda = ""
    if title == 'search':
        title = title + '.txt'
        plugintools.log("title= "+title)
    else:
        title = title + '.m3u'

    if title == 'search.txt':
        busqueda = 'search.txt'
        file = open(tmp + 'search.txt', "r")
        file.seek(0)
        data = file.readline()
        if data == "":
            ok = plugintools.message("palcoTV", "Sin resultados")
            return ok
    else:
        file = open(playlists + title, "r")
        file.seek(0)
        data = file.readline()
        plugintools.log("data= "+data)
      
    if data == "":
        print "No es posible leer el archivo!"
        data = file.readline()
        plugintools.log("data= "+data)
    else:
        file.seek(0)
        num_items = len(file.readlines())
        print num_items
        plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = False)
                           
    # Lectura de items en lista m3u. ToDo: Control de errores, implementar lectura de fanart y thumbnail
    tipo = ""
    i = -1
    file.seek(0)
    data = file.readline()
    while i <= num_items:
        if data.startswith("#EXTINF:-1") == True:
            if busqueda == 'search.txt':
                title = data.replace("#EXTINF:-1", "")
                title = title.replace(",", "")
                title = title.replace("-AZBOX *", "")
                title = title.replace("-AZBOX-*", "")
                title_search = title.split('"')
                titulo = title_search[0]
                origen = title_search[1]
                origen = origen.strip()
            else:
                origen = title.split(",")
                # origen = title[1]
                title = data.replace("#EXTINF:-1", "")
                title = title.replace(",", "")
                title = title.replace("-AZBOX *", "")
                title = title.replace("-AZBOX-*", "")
                title = title.strip()

            if title.startswith(' $ExtFilter="') == True:
                if busqueda == 'search.txt':
                    plugintools.log("lista tipo extfilters= "+title)
                    title = title.replace('$ExtFilter="', "")
                    title_search = title.split('"')
                    titulo = title_search[1]
                    origen = title_search[2]
                    origen = origen.strip()
                    i = i + 1

            if title.startswith('$ExtFilter="') == True:
                if busqueda == 'search.txt':
                    plugintools.log("lista tipo extfilters= "+title)
                    title = title.replace('$ExtFilter="', "")
                    title_search = title.split('"')
                    titulo = title_search[1]
                    origen = title_search[2]
                    origen = origen.strip()
                    i = i + 1
                else:
                    plugintools.log("lista tipo extfilters")
                    title = title.replace('$ExtFilter="', "")
                    category = title.split('"')
                    tipo = category[0]
                    tipo = tipo.strip()
                    title = category[1]
                    title = title.strip()
                    print title
                    plugintools.log("title_shannel= "+title)
                    data = file.readline()
                    i = i + 1
                       
            if title.startswith('group-title="') == True:
                if busqueda == 'search.txt':
                    plugintools.log("lista tipo group-title= "+title)
                    title = title.replace('group-title="', "")
                    title_search = title.split('"')
                    titulo = title_search[0]
                    origen = title_search[1]
                    origen = origen.strip()
                    i = i + 1
                    
                else:
                    plugintools.log("lista tipo group-title")
                    title = title.replace('group-title="', "")
                    category = title.split('"')
                    items = len(category)
                    print category
                    tipo = category[0]  # tipo= categoría o sección de canales
                    tipo = tipo.strip()
                    plugintools.log("tipo= "+tipo)
                    items = items - 1
                    title = category[items]
                    title = title.strip()
                    plugintools.log("title_vhannel= "+title)
                    data = file.readline()
                    i = i + 1

            if title.startswith(' tvg-name=') == True:
                if busqueda == 'search.txt':
                    plugintools.log("lista tipo tvg-name= "+title)
                    title = title.replace('tvg-name="', "")
                    title_search = title.split('"')
                    titulo = title_search[0]
                    titulo = titulo.strip()
                    origen = title_search[2]
                    origen = origen.strip()
                    i = i + 1
                    
                else:
                    plugintools.log("lista tipo tvg-name")
                    title = title.replace('tvg-name="', "")
                    category = title.split('"')
                    items = len(category)
                    print category
                    tipo = category[0]  # tipo= categoría o sección de canales
                    tipo = tipo.strip()
                    plugintools.log("tipo= "+tipo)
                    items = items - 1
                    title = category[items]
                    title = title.strip()
                    plugintools.log("title_vhannel= "+title)
                    data = file.readline()
                    i = i + 1
            
            if title.startswith('tvg-id=') == True:
                if busqueda == 'search.txt':
                    plugintools.log("lista tipo tvg-id= "+title)
                    title = title.replace('tvg-id="', "")
                    title_search = title.split('"')
                    titulo = title_search[0]
                    titulo = titulo.strip()
                    origen = title_search[2]
                    origen = origen.strip()
                    i = i + 1
                    
                else:
                    plugintools.log("lista tipo tvg-id")
                    title = title.replace('tvg-id="', "")
                    category = title.split('"')
                    items = len(category)
                    plugintools.log("número de comillas en titulo= "+str(items))
                    tipo = category[0]  # tipo= categoría o sección de canales
                    tipo = tipo.strip()
                    plugintools.log("tipo= "+tipo)
                    items = items - 1
                    title = category[items]
                    title = title.strip()
                    plugintools.log("title_vhannel= "+title)
                    data = file.readline()
                    i = i + 1    
                
        if data != "":
            data = data.strip()
            if data.startswith("http") == True:
                print "http"
                url = data.strip()
                if tipo != "":  # Controlamos el caso de subcategoría de canales
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + titulo + '[COLOR red] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        plugintools.add_item( action = "play" , title = '[COLOR red][I]' + tipo + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [HTTP][/COLOR]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                        
                else:
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + titulo + '[COLOR red] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        plugintools.add_item( action = "play" , title = '[COLOR red][I]' + '[/I][/COLOR][COLOR white] ' + title + '[COLOR red] [HTTP][/COLOR]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
          
            if data.startswith("rtmp") == True:
                print "rtmp"
                url = data
                url = parse_url(url)
                plugintools.log("url retornada= "+url)
                if tipo != "":  # Controlamos el caso de subcategoría de canales
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + titulo + '[COLOR green] [RTMP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        plugintools.add_item( action = "play" , title = '[COLOR red][I]' + tipo + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR green] [RTMP][/COLOR]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                        
                else:
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + titulo + '[COLOR green] [RTMP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR green] [RTMP][/COLOR]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue

            if data.startswith("plugin") == True:
                print "p2p"
                title = title.split('"')
                title = title[0]
                title = title.replace("#EXTINF:-1,", "")
                url = data
                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR blue] [P2P][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                data = file.readline()
                i = i + 1
                continue
            elif data.startswith("magnet") == True:
                print "p2p"
                title = title.split('"')
                title = title[0]
                title = title.replace("#EXTINF:-1,", "")
                url = data
                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR blue] [P2P][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                data = file.readline()
                i = i + 1
                continue                

            else:
                data = file.readline()
                i = i + 1

        else:
            data = file.readline()
            i = i + 1
            

    file.close()
    if title == 'search.txt':
            os.remove(tmp + title)


           
def myplaylists_m3u(params):  # Mis listas M3U
    plugintools.log("palcoTV.myplaylists_m3u "+repr(params))
    thumbnail = params.get("thumbnail")
    plugintools.add_item(action="play" , title = "[COLOR red][B][Tutorial][/B][COLOR lightyellow]: Importar listas M3U a mi biblioteca [/COLOR][COLOR blue][I][Youtube][/I][/COLOR]" , thumbnail = art + "icon.png" , url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=8i0KouM-4-U" , folder = False , isPlayable = True )
    plugintools.add_item(action="search_channel" , title = "[B][COLOR lightyellow]Buscador de canales[/COLOR][/B][COLOR lightblue][I] Nuevo![/I][/COLOR]" , thumbnail = art + "search.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
    
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    for entry in ficheros:
        plot = entry.split(".")        
        plot = plot[0]
        plugintools.log("entry= "+entry)
        
        if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
            entry = entry.replace(".plx", "")
            plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = playlists + entry , thumbnail = art + 'plx3.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            
        elif entry.endswith("p2p") == True:
            entry = entry.replace(".p2p", "")
            plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            
        else:
            entry = entry.replace(".m3u", "")
            plugintools.add_item(action="simpletv_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

            

def playlists_m3u(params):  # Biblioteca online
    plugintools.log("palcoTV.playlists_m3u "+repr(params))
    data = plugintools.read( params.get("url") )
    name_channel = params.get("plot")
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    online = '[COLOR yellowgreen][I][Auto][/I][/COLOR]'
    params["ext"] = 'm3u'
    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR] - [B][I][COLOR lightyellow]juarrox@gmail.com [/COLOR][/B][/I]' , thumbnail= art + 'icon.png' , folder = False , isPlayable = False )    
    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    # Sustituir por una lista!!!
    for biny, ciny, diny, winy, pixy, dixy, boxy in subchannel:
        if ciny == "Vcx7 IPTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            params["ext"] = "m3u"
            title = ciny
            params["title"]=title
        elif ciny == "Largo Barbate M3U":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "XBMC Mexico":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "allSat":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "AND Wonder":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "FenixTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        else:
            plot = ciny.split("[")
            plot = plot[0]
            plugintools.add_item( action="getfile_http" , plot = plot , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )



    plugintools.log("palcoTV.playlists_m3u "+repr(params))

    
        
def getfile_http(params):  # Descarga de lista M3U + llamada a simpletv_items para que liste los items
    plugintools.log("palcoTV.getfile_http "+repr(params))
    url = params.get("url")
    params["ext"] = "m3u"
    getfile_url(params)
    simpletv_items(params)
   
    
def parse_url(url):
    plugintools.log("url entrante= "+url)

    if url != "":
        url = url.strip()
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")
        # url = url.replace(" --live", "")
        # url = url.replace("conn=S:OK", "")
        # url = url.replace("Conn=S:OK", "")
        # url = url.replace("Conn=S:OK --live", "")
        # url = url.replace("conn=S:OK --live", "")
        # url = url.replace("-live", "")
        # url = url.strip()

        if url.startswith("rtsp") == True:
            url = url.replace("rtsp", "rtmp")
        
       # if url.find("timeout") > 0:
       #     url = url
       # else:
       #     url = url + ' timeout=15'  # En futuras versiones será modificable por el usuario
                    
                                    
        plugintools.log("url saliente= "+url)
        return url
    else:
        plugintools.log("error en url= ")  # Mostrar diálogo de error al parsear url (por no existir, por ejemplo)
        
                    
def getfile_url(params):
    plugintools.log("palcoTV.getfile_url " +repr(params))
    ext = params.get("ext")
    title = params.get("title")

    if ext == 'plx':
        filename = title + ".plx"  # El título del archivo con extensión (m3u, p2p, plx)
    elif ext == 'm3u':
        filename = params.get("plot")
        filename = filename + ".m3u"  # El título del archivo con extensión (m3u, p2p, plx)
    else:
        ext == 'p2p'
        filename = params.get("title")
        filename = filename + ".p2p"  # El título del archivo con extensión (m3u, p2p, plx)
        
    plugintools.log("filename= "+filename)
    url = params.get("url")
    plugintools.log("url= "+url)
    response = urllib2.urlopen(url)

    #open the file for writing
    fh = open(playlists + filename, "wb")

    # read from request while writing to file
    fh.write(response.read())

    fh.close()

    file = open(playlists + filename, "r")
    file.seek(0)
    data = file.readline()
    data = data.strip()

    lista_items = {'linea': data}
    file.seek(0)
    lista_items = {'plot': data}
    file.seek(0)
    


def header_xml(params):
    plugintools.log("palcoTV.header_xml "+repr(params))

    url = params.get("url")
    params.get("title")
    data = plugintools.read(url)
    # plugintools.log("data= "+data)
    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    author = author.strip()
    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')
    message = plugintools.find_single_match(data, '<message>(.*?)</message>')
    desc = plugintools.find_single_match(data, '<description>(.*?)</description>')
    thumbnail = plugintools.find_single_match(data, '<thumbnail>(.*?)</thumbnail>')
    
    if author != "":
        if message != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR][I] ' + message + '[/I]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
    else:
        if desc != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + desc + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            return fanart


def search_channel(params):
    plugintools.log("palcoTV.search " + repr(params))

    buscar = params.get("plot")
    plugintools.log("buscar texto: "+buscar)
    if buscar == "":
        last_search = plugintools.get_setting("last_search")
        texto = plugintools.keyboard_input(last_search)
        plugintools.set_setting("last_search",texto)
        params["texto"]=texto
        texto = texto.lower()
        tipo = ""
        if texto == "":
            errormsg = plugintools.message("palcoTV","Por favor, introduzca el canal a buscar")
            return errormsg
        
    else:
        texto = buscar
        texto = texto.lower()
        plugintools.log("texto a buscar= "+texto)
        tipo = ""
    
    results = open(tmp + 'search.txt', "wb")
    results.seek(0)
    results.close()
    print "Cerramos archivo de búsquedas"

    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    
    for entry in ficheros:
        if entry.endswith("m3u") == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            filename = plot + '.m3u'
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            plugintools.log("archivo= "+filename)
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)
            data = arch.readline()
            data = data.strip()
            texto = texto.strip()
            plugintools.log("data_antes= "+data)
            while i <= num_items:                                     
                data = arch.readline()
                i = i + 1
                            
                if data.startswith('#EXTINF:-1') == True:
                    data = data.replace('#EXTINF:-1,', "")  # Ignoramos la primera parte de la línea
                    data = data.replace(",", "")
                    title = data.strip()  # Ya tenemos el título
                    minus = title.lower()
                    title = title.replace("-AZBOX*", "")
                    title = title.replace("AZBOX *", "")
                                    
                    if data.startswith('$ExtFilter="') == True:
                        data = data.replace('$ExtFilter="', "")
                        data = data.replace(",", "")
                        data = data.split('"')
                        cat = data[0]
                        cat = cat.strip()
                        title = data[1]
                        title = title.strip()  # Ya tenemos el título
                        minus = title.lower()
                        data = arch.readline()
                        data = data.strip()
                        i = i + 1
                                
                    if title.find('group-title="') >= 0:
                        data = data.replace("group-title=", "")
                        data = data.split('"')
                        cat = data[0]
                        items = len(data)
                        print items
                        items = items - 1
                        title = data[items]
                        title = title.strip()  # Ya tenemos el título
                        minus = title.lower()
                        data = arch.readline()
                        data = data.strip()
                        i = i + 1
                    else:
                        data = arch.readline()
                        data = data.strip()
                        i = i + 1
                                   
                    if minus.find(texto) >= 0:
                    # if re.match(texto, title, re.IGNORECASE):
                        # plugintools.log("Concidencia hallada. Obtenemos url del canal: " + texto)
                        if data.startswith("http") == True:
                            print "URL de tipo 'http'"
                            url = data.strip()
                            if tipo != "":  # Controlamos el caso de subcategoría de canales
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()                            
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("rtmp") == True:
                            print "URL de tipo 'rtmp'"
                            url = data
                            url = parse_url(url)
                            if tipo != "":   # Controlamos el caso de subcategoría de canales
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:                            
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue                          
                else:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    #print i
                    


    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    
    for entry in ficheros:
        if entry.endswith('p2p') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.p2p'
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            plugintools.log("archivo= "+filename)
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)            
            while i <= num_items:
                data = arch.readline()
                data = data.strip()
                title = data
                texto = texto.strip()
                plugintools.log("linea a buscar title= "+data)                
                i = i + 1
                #print i
                if data != "":
                    title = data.strip()  # Ya tenemos el título
                    plugintools.log("title= "+title)
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        plugintools.log("title= "+title)
                        data = arch.readline()
                        i = i + 1
                        #print i
                        plugintools.log("linea a comprobar url= "+data)
                        if data.startswith("sop") == True:
                            # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                            title_fixed = title.replace(" " , "+")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name=' + title_fixed
                            plugintools.log("url sopcast= "+url)
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.startswith("magnet") == True:                            
                            # magnet:?xt=urn:btih:6CE983D676F2643430B177E2430042E4E65427...
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            plugintools.log("title magnet= "+title)
                            url = data
                            plugintools.log("url magnet= "+url)
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.find("://") == -1:
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            title_fixed = title.replace(" " , "+")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=1&name=' + title_fixed
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                    else:
                        plugintools.log("no coinciden titulo y texto a buscar")

                
    for entry in ficheros:
        if entry.endswith('plx') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.plx'
            plugintools.log("archivo PLX: "+filename)
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            print num_items
            i = 0
            arch.seek(0)
            while i <= num_items:
                data = arch.readline()
                data = data.strip()                
                i = i + 1
                #print i
                
                if data.startswith("#") == True:
                    continue

                if (data == 'type=video') or (data == 'type=audio') == True:
                    data = arch.readline()
                    i = i + 1
                    #print i
                    data = data.replace("name=", "")
                    data = data.strip()
                    title = data
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        plugintools.log("title= "+title)
                        data = arch.readline()
                        i = i + 1
                        #print i
                        print "Analizamos..."
                        if data.startswith("thumb") == True:
                            data = arch.readline()
                            i = i + 1
                            #print i
                            if data.startswith("date") == True:
                                data = arch.readline()
                                i = i + 1
                                #print i
                                if data.startswith("URL") == True:
                                    data = data.replace("URL=", "")
                                    data = data.strip()
                                    url = data
                                    if url == "":
                                        data = arch.readline()
                                        i = i + 1
                                        #print i
                                        continue
                                    else:
                                        parse_url(url)
                                        plugintools.log("URL= "+url)
                                        results = open(tmp + 'search.txt', "a")
                                        results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                        results.write(url + '\n\n')
                                        results.close()
                                        data = arch.readline()
                                        i = i + 1
                                        continue
                                
                        else:
                            if data.startswith("date") == True:
                                data = arch.readline()
                                i = i + 1
                                #print i
                                if data.startswith("URL=") == True:
                                    data = data.replace("URL=", "")
                                    data = data.strip()
                                    url = data
                                    if url == "":
                                        data = arch.readline()
                                        i = i + 1
                                        #print i
                                        continue
                                    else:
                                        parse_url(url)
                                        plugintools.log("URL= "+url)
                                        results = open(tmp + 'search.txt', "a")
                                        results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                        results.write(url + '\n\n')
                                        results.close()
                                        data = arch.readline()
                                        i = i + 1
                                        continue

                            else:
                                if data.startswith("URL=") == True:
                                    data = data.replace("URL=", "")
                                    data = data.strip()
                                    url = data
                                    if url == "":
                                        data = arch.readline()
                                        i = i + 1
                                        #print i
                                        continue
                                    else:
                                        parse_url(url)
                                        plugintools.log("URL= "+url)
                                        results = open(tmp + 'search.txt', "a")
                                        results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                        results.write(url + '\n\n')
                                        results.close()
                                        data = arch.readline()
                                        i = i + 1
                                        continue                            
                                
                                    
                    else:
                        data = arch.readline()
                        i = i + 1
                        #print i
                        continue

                      
    arch.close()
    results.close()
    params["plot"] = 'search'  # Pasamos a la lista de variables (params) el valor del archivo de resultados para que lo abra la función simpletv_items
    params['texto']= texto  # Agregamos al diccionario una nueva variable que contiene el texto a buscar
    simpletv_items(params)
    



def agendatv(params):
    plugintools.log("palcoTV.agendatv "+repr(params))

    hora_partidos = []
    lista_equipos=[]
    campeonato=[]
    canales=[]

    url = params.get("url")        
    data = plugintools.read(url)
    plugintools.log("data= "+data)
	    
    matches = plugintools.find_multiple_matches(data,'<tr>(.*?)</tr>')
    horas = plugintools.find_multiple_matches(data, 'color=#990000>(.*?)</td>')
    txt = plugintools.find_multiple_matches(data, 'color="#000099"><b>(.*?)</td>')
    tv = plugintools.find_multiple_matches(data, '<td align="left"><font face="Verdana, Arial, Helvetica, sans-serif" size="1" ><b>([^<]+)</b></font></td>')

    # <b><a href="indexf.php?comp=Súper Final Argentino">Súper Final Argentino&nbsp;&nbsp;</td>    
    for entry in matches:
        torneo = plugintools.find_single_match(entry, '<a href=(.*?)">')
        torneo = torneo.replace("&nbsp;&nbsp;", "")
        torneo = torneo.replace("indexf.php?comp=", "")
        torneo = torneo.replace('>', "")
        torneo = torneo.replace('"', "")
        torneo = torneo.replace("\n", "")
        torneo = torneo.strip()
        torneo = torneo.replace('\xfa', 'ú')
        torneo = torneo.replace('\xe9', 'é')
        torneo = torneo.replace('\xf3', 'ó')
        torneo = torneo.replace('\xfa', 'ú')
        torneo = torneo.replace('\xaa', 'ª')
        torneo = torneo.replace('\xe1', 'á')
        torneo = torneo.replace('\xf1', 'ñ')
        torneo = torneo.replace('indexuf.php?comp=', "")
        torneo = torneo.replace('indexfi.php?comp=', "")
        plugintools.log("string encoded= "+torneo)
        if torneo != "":
            plugintools.log("torneo= "+torneo)
            campeonato.append(torneo)                    

    # ERROR! Hay que añadir las jornadas, tal como estaba antes!!

    # Vamos a crear dos listas; una de los equipos que se enfrentan cada partido y otra de las horas de juego
    
    for dato in txt:
        lista_equipos.append(dato)
        
    for tiempo in horas:
        hora_partidos.append(tiempo)

    # <td align="left"><font face="Verdana, Arial, Helvetica, sans-serif" size="1" ><b>&nbsp;&nbsp; Canal + Fútbol</b></font></td>
    # <td align="left"><font face="Verdana, Arial, Helvetica, sans-serif" size="1" ><b>&nbsp;&nbsp; IB3</b></font></td>

    for kanal in tv:
        kanal = kanal.replace("&nbsp;&nbsp;", "")
        kanal = kanal.strip()
        kanal = kanal.replace('\xfa', 'ú')
        kanal = kanal.replace('\xe9', 'é')
        kanal = kanal.replace('\xf3', 'ó')
        kanal = kanal.replace('\xfa', 'ú')
        kanal = kanal.replace('\xaa', 'ª')
        kanal = kanal.replace('\xe1', 'á')
        kanal = kanal.replace('\xf1', 'ñ')
        canales.append(kanal)

        
    print lista_equipos
    print hora_partidos  # Casualmente en esta lista se nos ha añadido los días de partido
    print campeonato
    print canales
    
    i = 0       # Contador de equipos
    j = 0       # Contador de horas
    k = 0       # Contador de competición
    max_equipos = len(lista_equipos) - 2
    print max_equipos
    for entry in matches:
        while j <= max_equipos:
            # plugintools.log("entry= "+entry)
            fecha = plugintools.find_single_match(entry, 'color=#990000><b>(.*?)</b></td>')
            fecha = fecha.replace("&#225;", "á")
            fecha = fecha.strip()
            gametime = hora_partidos[i]
            gametime = gametime.replace("<b>", "")
            gametime = gametime.replace("</b>", "")
            gametime = gametime.strip()
            gametime = gametime.replace('&#233;', 'é')
            gametime = gametime.replace('&#225;', 'á')
            gametime = gametime.replace('&#233;', 'é')
            gametime = gametime.replace('&#225;', 'á')  
            print gametime.find(":")
            if gametime.find(":") == 2:
                i = i + 1
                #print i
                local = lista_equipos[j]
                local = local.strip()
                local = local.replace('\xfa', 'ú')
                local = local.replace('\xe9', 'é')
                local = local.replace('\xf3', 'ó')
                local = local.replace('\xfa', 'ú')
                local = local.replace('\xaa', 'ª')
                local = local.replace('\xe1', 'á')
                local = local.replace('\xf1', 'ñ')
                j = j + 1
                print j
                visitante = lista_equipos[j]
                visitante = visitante.strip()
                visitante = visitante.replace('\xfa', 'ú')
                visitante = visitante.replace('\xe9', 'é')
                visitante = visitante.replace('\xf3', 'ó')
                visitante = visitante.replace('\xfa', 'ú')
                visitante = visitante.replace('\xaa', 'ª')
                visitante = visitante.replace('\xe1', 'á')
                visitante = visitante.replace('\xf1', 'ñ')
                local = local.replace('&#233;', 'é')
                local = local.replace('&#225;', 'á')  
                j = j + 1
                print j
                tipo = campeonato[k]
                channel = canales[k]
                channel = channel.replace('\xfa', 'ú')
                channel = channel.replace('\xe9', 'é')
                channel = channel.replace('\xf3', 'ó')
                channel = channel.replace('\xfa', 'ú')
                channel = channel.replace('\xaa', 'ª')
                channel = channel.replace('\xe1', 'á')
                channel = channel.replace('\xf1', 'ñ')
                channel = channel.replace('\xc3\xba', 'ú')
                channel = channel.replace('Canal +', 'Canal+')
                title = '[B][COLOR khaki]' + tipo + ':[/B][/COLOR] ' + '[COLOR lightyellow]' + '(' + gametime + ')[COLOR white]  ' + local + ' vs ' + visitante + '[/COLOR][COLOR lightblue][I] (' + channel + ')[/I][/COLOR]'
                plugintools.add_item(plot = channel , action="contextMenu", title=title , url = "", fanart = art + 'agendatv.jpg', thumbnail = art + 'icon.png' , folder = True, isPlayable = False)
                # diccionario[clave] = valor
                plugintools.log("channel= "+channel)
                params["plot"] = channel
                # plugintools.add_item(plot = channel , action = "search_channel", title = '[COLOR lightblue]' + channel + '[/COLOR]', url= "", thumbnail = art + 'icon.png', fanart = fanart , folder = True, isPlayable = False)
                k = k + 1
                print k
                plugintools.log("title= "+title)
            else:
                plugintools.add_item(action="", title='[B][COLOR red]' + gametime + '[/B][/COLOR]', thumbnail = art + 'icon.png' , fanart = art + 'agendatv.jpg' , folder = True, isPlayable = False)
                i = i + 1
        


def encode_string(url):
    

    d = {    '\xc1':'A',
            '\xc9':'E',
            '\xcd':'I',
            '\xd3':'O',
            '\xda':'U',
            '\xdc':'U',
            '\xd1':'N',
            '\xc7':'C',
            '\xed':'i',
            '\xf3':'o',
            '\xf1':'n',
            '\xe7':'c',
            '\xba':'',
            '\xb0':'',
            '\x3a':'',
            '\xe1':'a',
            '\xe2':'a',
            '\xe3':'a',
            '\xe4':'a',
            '\xe5':'a',
            '\xe8':'e',
            '\xe9':'e',
            '\xea':'e',       
            '\xeb':'e',       
            '\xec':'i',
            '\xed':'i',
            '\xee':'i',
            '\xef':'i',
            '\xf2':'o',
            '\xf3':'o',
            '\xf4':'o',   
            '\xf5':'o',
            '\xf0':'o',
            '\xf9':'u',
            '\xfa':'u',
            '\xfb':'u',               
            '\xfc':'u',
            '\xe5':'a'       
    }
   
    nueva_cadena = url
    for c in d.keys():
        plugintools.log("caracter= "+c)
        nueva_cadena = nueva_cadena.replace(c,d[c])

    auxiliar = nueva_cadena.encode('utf-8')
    url = nueva_cadena
    return nueva_cadena



def plx_items(params):
    plugintools.log("palcoTV.plx_items" +repr(params))
    # filename = params.get("plot")
    fanart = ""
    thumbnail = ""

    # Control para elegir el título (plot, si formateamos el título / title , si no existe plot)
    if params.get("plot") == "":
        title = params.get("title") + '.plx'
        filename = title
        params["plot"]=filename
        params["ext"] = 'plx'
        getfile_url(params)
        title = params.get("title")
        title = title + '.plx'
    else:
        title = params.get("plot") + '.plx'
        plugintools.log("Lectura del archivo PLX")
      
    file = open(playlists + title, "r")
    file.seek(0)
    num_items = len(file.readlines())
    print num_items
        
    # Lectura del título y fanart de la lista
    file.seek(0)
    i = 0
    data = file.readline()
    while i <= 10:        
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            fanart = data.strip()
            plugintools.log("fanart= "+fanart)
            i = i + 1
            #print i
            data = file.readline()
            continue

        elif data.startswith("title=") == True:
            name = data.replace("title=", "")
            name = name.strip()
            plugintools.log("name= "+name)
            i = i + 1
            #print i
            data = file.readline()
            continue

        elif data.startswith("logo=") == True:
            data = data.replace("logo=", "")
            thumbnail = data.strip()
            plugintools.log("thumbnail= "+thumbnail)
            i = i + 1
            #print i
            data = file.readline()
            continue

        else:
            i = i + 1
            data = file.readline()
            #print i


    if fanart == "":
        fanart = art + 'fanart.jpg'

    if thumbnail == "":
        thumbnail = art + 'plx3.png'

    

    plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False)
    plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False)
            
    try:        
        data = file.readline()
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            data = data.strip()
            fanart = data
            plugintools.log("fanart= "+fanart)
        else:
            # data = file.readline()
            if data.startswith("background=") == True:
                print "Archivo plx!"
                data = data.replace("background=", "")
                fanart = data.strip()
                plugintools.log("fanart= "+fanart)
            else:
                if data.startswith("title=") == True:
                    name = data.replace("title=", "")
                    name = name.strip()
                    plugintools.log("name= "+name)
    except:
        plugintools.log("ERROR: Unable to load PLX file")


    data = file.readline()
    try:
        if data.startswith("title=") == True:
            data = data.replace("title=", "")
            name = data.strip()            
            plugintools.log("title= "+title)
            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , thumbnail = art + "icon.png" , fanart = fanart , folder = False , isPlayable = False)
            plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = art + "icon.png" , fanart = fanart , folder = False , isPlayable = False)
    except:
        plugintools.log("Unable to read PLX title")

    i = 0
    file.seek(0)
          
    # Lectura de items
    while i <= num_items:
        data = file.readline()
        data = data.strip()
        i = i + 1
        #print i
        if data.startswith("#") == True:
            continue
        
        if (data == 'type=video') or (data == 'type=audio') == True:
            data = file.readline()
            i = i + 1
            #print i
            data = data.replace("name=", "")
            data = data.strip()
            title = data
            plugintools.log("title= "+title)
            data = file.readline()
            i = i + 1
            #print i
            
            if data.startswith("thumb") == True:
                data = data.replace("thumb=", "")
                data = data.strip()
                thumbnail = data
                plugintools.log("thumbnail= "+thumbnail)
                data = file.readline()
                i = i + 1
                #print i
                if data.startswith("date") == True:
                    data = file.readline()
                    i = i + 1
                    #print i
                    
                data = data.replace("URL=", "")
                data = data.strip()
                url = data
                parse_url(url)
                plugintools.log("URL= "+url)
                data = file.readline()
                i = i + 1
                #print i
                plugintools.log("url= "+url)
                plugintools.add_item(action="play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                continue
                
            elif data.startswith("date") == True:
                data = file.readline()
                i = i + 1
                #print i
                if data.startswith("URL") == True:
                    data = data.replace("URL=", "")                    
                    url = data.strip()
                    parse_url(url)
                    plugintools.log("URL= "+url)
                    data = file.readline()
                    i = i + 1
                    #print i
                    plugintools.log("url= "+url)
                    if thumbnail == "":
                        thumbnail = art + 'plx3.png'
                        
                    plugintools.add_item(action="play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                    continue
                else:
                    if data.startswith("thumb") == True:
                        data = data.replace("thumb=", "")
                        data = data.strip()
                        thumb = data
                        data = file.readline()
                        i = i + 1
                        #print i
                        url = data.strip()
                        parse_url(url)
                        plugintools.log("URL= "+url)
                        data = file.readline()
                        i = i + 1
                        #print i
                        plugintools.add_item(action="play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        continue
                                        
            else:
                if data.startswith("URL") == True:
                    data = data.replace("URL=", "")
                    data = data.strip()
                    url = data
                    parse_url(url)
                    plugintools.log("URL= "+url)
                    data = file.readline()
                    i = i + 1
                    #print i
                    plugintools.log("url= "+url)
                    plugintools.add_item(action="play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                    continue

        else:
            i = i + 1
            #print i
            data = file.readline()
            plugintools.log("data= "+data)
           

    file.close()



def futbolenlatv(params):
    plugintools.log("palcoTV.futbolenlaTV "+repr(params))

    hora_partidos = []
    lista_equipos=[]
    campeonato=[]
    canales=[]

    url = params.get("url")
    print url
    fecha = get_fecha()
    dia_manana = params.get("plot")
    data = plugintools.read(url)
    
    if dia_manana == "":  # Control para si es agenda de hoy o mañana
        plugintools.add_item(action="", title = '[COLOR green][B]FutbolenlaTV.com[/B][/COLOR] - [COLOR lightblue][I]Agenda para el día '+ fecha + '[/I][/COLOR]', folder = False , isPlayable = False )
    else:
        dia_manana = dia_manana.split("-")
        dia_manana = dia_manana[2] + "/" + dia_manana[1] + "/" + dia_manana[0]
        plugintools.add_item(action="", title = '[COLOR green][B]FutbolenlaTV.com[/B][/COLOR] - [COLOR lightblue][I]Agenda para el día '+ dia_manana + '[/I][/COLOR]', folder = False , isPlayable = False )
        
	    
    bloque = plugintools.find_multiple_matches(data,'<span class="cuerpo-partido">(.*?)</div>')
    for entry in bloque:
        # plugintools.log("bloque= "+entry)
        # <span class="i-comp"><i class="ftvi-hockey-hierba comp"></i></span>


        category = plugintools.find_single_match(entry, '<i class=(.*?)</i>')
        category = category.replace("ftvi-", "")
        category = category.replace('comp">', '')
        category = category.replace('"', '')
        category = category.replace("-", " ")
        category = category.replace("Futbol", "Fútbol")
        category = category.strip()
        category = category.capitalize()
        plugintools.log("cat= "+category)
        champ = plugintools.find_single_match(entry, '<span class="com-detalle">(.*?)</span>')
        champ = encode_string(champ)
        champ = champ.strip()
        event = plugintools.find_single_match(entry, '<span class="bloque">(.*?)</span>')
        event = encode_string(event)
        event = event.strip()
        momentum = plugintools.find_single_match(entry, '<time itemprop="startDate" datetime=([^<]+)</time>')
        # plugintools.log("momentum= "+momentum)
        momentum = momentum.split(">")
        momentum = momentum[1]

        gametime = plugintools.find_multiple_matches(entry, '<span class="n">(.*?)</span>')
        for tiny in gametime:
            day = tiny
            month = tiny
            
        sport = plugintools.find_single_match(entry, '<meta itemprop="eventType" content=(.*?)/>')
        sport = sport.replace('"', '')
        sport = sport.strip()
        if sport == "Partido de fútbol":
            sport = "Fútbol"
            
        # plugintools.log("sport= "+sport)
        
        gameday = plugintools.find_single_match(entry, '<span class="dia">(.*?)</span>')

        rivals = plugintools.find_multiple_matches(entry, '<span>([^<]+)</span>([^<]+)<span>([^<]+)</span>')
        rivales = ""
        
        for diny in rivals:
            print diny
            items = len(diny)
            items = items - 1
            i = -1
            diny[i].strip()
            while i <= items:
                if diny[i] == "":
                    del diny[0]
                    i = i + 1
                else:
                    print diny[i]
                    rival = diny[i]                        
                    rival = encode_string(rival)
                    rival = rival.strip()
                    plugintools.log("rival= "+rival)
                    if rival == "-":
                        i = i + 1
                        continue
                    else:
                        if rivales != "":
                            rivales = rivales + " vs " + rival
                            plugintools.log("rivales= "+rivales)
                            break
                        else:
                            rivales = rival
                            plugintools.log("rival= "+rival)
                            i = i + 1


        tv = plugintools.find_single_match(entry, '<span class="hidden-phone hidden-tablet canales"([^<]+)</span>')
        tv = tv.replace(">", "")
        tv = encode_string(tv)                  
        if tv == "":
            continue
        else:
            tv = tv.replace("(Canal+, Astra", "")
            tv = tv.split(",")
            tv_a = tv[0]
            tv_a = tv_a.rstrip()
            tv_a = tv_a.lstrip()
            tv_a = tv_a.replace(")", "")
            plugintools.log("tv_a= "+tv_a)
            print len(tv)
            if len(tv) == 2:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                   
                tv = tv_a + " / " + tv_b
                plot = tv
                plugintools.log("plot= "+plot)
                
            elif len(tv) == 3:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                
                tv = tv_a + " / " + tv_b + " / " + tv_c
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 4:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                  
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                   
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")                  
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d            
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 5:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                 
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")                  
                tv_e = tv[4]
                tv_e = tv_e.lstrip()
                tv_e = tv_e.rstrip()
                tv_e = tv_e.replace(")", "")
                tv_e = tv_e.replace("(Bar+ dial 333-334", "")
                tv_e = tv_e.replace("(Canal+", "")                 
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d + " / " + tv_e
                # tv = tv.replace(")", "")                
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 6:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                 
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                  
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")                  
                tv_e = tv[4]
                tv_e = tv_e.lstrip()
                tv_e = tv_e.rstrip()
                tv_e = tv_e.replace(")", "")
                tv_e = tv_e.replace("(Bar+ dial 333-334", "")
                tv_e = tv_e.replace("(Canal+", "")                  
                tv_f = tv[5]
                tv_f = tv_f.lstrip()
                tv_f = tv_f.rstrip()
                tv_f = tv_f.replace(")", "")
                tv_f = tv_f.replace("(Bar+ dial 333-334", "")
                tv_f = tv_f.replace("(Canal+", "")                  
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d + " / " + tv_e + " / " + tv_f
                # tv = tv.replace(")", "")                
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 7:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                  
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                  
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")                  
                tv_e = tv[4]
                tv_e = tv_e.lstrip()
                tv_e = tv_e.rstrip()
                tv_e = tv_e.replace(")", "")
                tv_e = tv_e.replace("(Bar+ dial 333-334", "")
                tv_e = tv_e.replace("(Canal+", "")                  
                tv_f = tv[5]
                tv_f = tv_f.lstrip()
                tv_f = tv_f.rstrip()
                tv_f = tv_f.replace(")", "")
                tv_f = tv_f.replace("(Bar+ dial 333-334", "")
                tv_f = tv_f.replace("(Canal+", "")                
                tv_g = tv[6]
                tv_g = tv_g.lstrip()
                tv_g = tv_g.rstrip()
                tv_g = tv_g.replace(")", "")
                tv_g = tv_g.replace("(Bar+ dial 333-334", "")
                tv_g = tv_g.replace("(Canal+", "")                  
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d + " / " + tv_e + " / " + tv_f + " / " + tv_g
                plot = tv
                plugintools.log("plot= "+plot)                
            else:
                tv = tv_a
                plot = tv_a
                plugintools.log("plot= "+plot)
                

            plugintools.add_item(action="contextMenu", plot = plot , title = momentum + "h " + '[COLOR lightyellow][B]' + category + '[/B][/COLOR] ' + '[COLOR green]' + champ + '[/COLOR]' + " " + '[COLOR lightyellow][I]' + rivales + '[/I][/COLOR] [I][COLOR red]' + plot + '[/I][/COLOR]' , thumbnail  = 'http://i2.bssl.es/telelocura/2009/05/futbol-tv.jpg' , fanart = art + 'agenda2.jpg' , folder = True, isPlayable = False)
            # plugintools.add_item(action="contextMenu", title = '[COLOR yellow][I]' + tv + '[/I][/COLOR]', thumbnail = 'http://i2.bssl.es/telelocura/2009/05/futbol-tv.jpg' , fanart = art + 'agenda2.jpg' , plot = plot , folder = True, isPlayable = False)                
                
            # plugintools.add_item(action="contextMenu", title = gameday + '/' + day + "(" + momentum + ") " + '[COLOR lightyellow][B]' + category + '[/B][/COLOR] ' + champ + ": " + rivales , plot = plot , thumbnail = 'http://i2.bssl.es/telelocura/2009/05/futbol-tv.jpg' , fanart = art + 'agenda2.jpg' , folder = True, isPlayable = False)
            # plugintools.add_item(action="contextMenu", title = '[COLOR yellow][I]' + tv + '[/I][/COLOR]' , thumbnail = 'http://i2.bssl.es/telelocura/2009/05/futbol-tv.jpg' , fanart = art + 'agenda2.jpg' , plot = plot , folder = True, isPlayable = False)
               
         

def encode_string(txt):
    plugintools.log("palcoTV.encode_string: "+txt)
    
    txt = txt.replace("&#231;", "ç")
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#241;', 'ñ')
    txt = txt.replace('&#250;', 'ú')
    txt = txt.replace('&#237;', 'í')
    txt = txt.replace('&#243;', 'ó')    
    txt = txt.replace('&#39;', "'")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace('&#39;', "'")
    return txt



def splive_items(params):
    plugintools.log("palcoTV.SPlive_items "+repr(params))
    data = plugintools.read( params.get("url") )

    channel = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
    
    for entry in channel:
        # plugintools.log("channel= "+channel)
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        category = plugintools.find_single_match(entry,'<category>(.*?)</category>')
        thumbnail = plugintools.find_single_match(entry,'<link_logo>(.*?)</link_logo>')
        rtmp = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
        isIliveTo = plugintools.find_single_match(entry,'<isIliveTo>([^<]+)</isIliveTo>')
        rtmp = rtmp.strip()
        pageurl = plugintools.find_single_match(entry,'<url_html>([^<]+)</url_html>')
        link_logo = plugintools.find_single_match(entry,'<link_logo>([^<]+)</link_logo>')
        
        if pageurl == "SinProgramacion":
            pageurl = ""
            
        playpath = plugintools.find_single_match(entry, '<playpath>([^<]+)</playpath>')
        playpath = playpath.replace("Referer: ", "")
        token = plugintools.find_single_match(entry, '<token>([^<]+)</token>')

        iliveto = 'rtmp://188.122.91.73/edge'
        
        if isIliveTo == "0":
            if token == "0":
                url = rtmp
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)
            else:
                url = rtmp + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)

        if isIliveTo == "1":
            if token == "1":                                
                url = iliveto + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)
                
            else:
                url = iliveto + ' swfUrl=' + rtmp +  " playpath=" + playpath + " pageUrl=" + pageurl
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)
                


def get_fecha():

    from datetime import datetime

    ahora = datetime.now()
    anno_actual = ahora.year
    mes_actual = ahora.month
    dia_actual = ahora.day
    fecha = str(dia_actual) + "/" + str(mes_actual) + "/" + str(anno_actual)
    plugintools.log("fecha de hoy= "+fecha)
    return fecha




def p2p_items(params):
    plugintools.log("palcoTV.p2p_items" +repr(params))
    
    # Vamos a localizar el thumbnail 
    title = params.get("plot")
    if title == "":
        title = params.get("title")
        
    data = plugintools.read("https://dl.dropboxusercontent.com/u/8036850/palcotv028.xml")
    subcanal = plugintools.find_single_match(data,'<name>' + title + '(.*?)</subchannel>')
    thumbnail = plugintools.find_single_match(subcanal, '<thumbnail>(.*?)</thumbnail>')
    fanart = plugintools.find_single_match(subcanal, '<fanart>(.*?)</fanart>')
    plugintools.log("thumbnail= "+thumbnail)
    filename = title + '.p2p'    
    # Controlamos el caso en que no haya thumbnail
    if thumbnail == "":
        thumbnail = art + 'p2p.png'
    elif thumbnail == 'name_rtmp.png':
        thumbnail = art + 'p2p.png'          

    if fanart == "":
        fanart = art + 'p2p.png'

    # Comprobamos si la lista ha sido descargada o no
    plot = params.get("plot")
    if plot != "":
        print "Lista ya descargada (plot no vacío)"
        filename = params.get("plot")
        params["ext"] = 'p2p'
        params["plot"]=filename
        plugintools.log("Lectura del archivo P2P")
        title = title + '.p2p'
    else:
        getfile_url(params)
        title = params.get("title")
        title = title + '.p2p'

    # Abrimos el archivo P2P y calculamos número de líneas        
    file = open(playlists + title, "r")
    file.seek(0)
    data = file.readline()
    num_items = len(file.readlines())
    print num_items

    # Leemos entradas
    i = 0
    file.seek(0)
    data = file.readline()
    data = data.strip()
    while i <= num_items:        
        if data == "":
            data = file.readline()
            data = data.strip()
            plugintools.log("linea vacia= "+data)
            i = i + 1
            #print i
            continue
        else:
            title = data
            title = title.strip()
            plugintools.log("title= "+title)
            data = file.readline()
            data = data.strip()
            i = i + 1
            #print i
            plugintools.log("linea URL= "+data)
            if data.startswith("sop") == True:
                print "empieza el sopcast..."
                # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                title_fixed = title.replace(" " , "+")
                url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name=' + title_fixed
                plugintools.add_item(action="play" , title = title + ' [COLOR indianred][Sopcast][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i
                continue
                
            elif data.startswith("magnet") == True:
                print "empieza el torrent..."
                # plugin://plugin.video.xbmctorrent/play/ + <magnet_link>
                url_fixed = urllib.quote_plus(data)
                url = 'plugin://plugin.video.xbmctorrent/play/' + url_fixed
                plugintools.add_item(action="play" , title = title + ' [COLOR lightyellow][Torrent][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i
                continue
            else:
                print "empieza el acestream..."
                # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                title_fixed = title.replace(" " , "+")
                url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=1&name=' + title_fixed
                plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i
                
            


def contextMenu(params):
    plugintools.log("palcoTV.contextMenu " +repr(params))

    dialog = xbmcgui.Dialog()
    plot = params.get("plot")
    canales = plot.split("/")
    len_canales = len(canales)
    print len_canales
    plugintools.log("canales= "+repr(canales))

    if len_canales == 1:        
        tv_a = canales[0]
        tv_a = parse_channel(tv_a)
        search_channel(params)
        selector = ""        
    else:
        if len_canales == 2:
            print "len_2"
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            selector = dialog.select('palcoTV', [tv_a, tv_b])
                    
        elif len_canales == 3:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)        
            selector = dialog.select('palcoTV', [tv_a, tv_b, tv_c])
                    
        elif len_canales == 4:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)          
            selector = dialog.select('palcoTV', [tv_a, tv_b, tv_c, tv_d])
            
        elif len_canales == 5:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)         
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            selector = dialog.select('palcoTV', [tv_a, tv_b, tv_c, tv_d, tv_e])
            
        elif len_canales == 6:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)         
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)       
            selector = dialog.select('palcoTV', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f])
                      
        elif len_canales == 7:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)         
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)
            tv_g = canales[6]
            tv_g = parse_channel(tv_g)         
            selector = dialog.select('palcoTV', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f, tv_g])
            
    if selector == 0:
        print selector
        if tv_a.startswith("Gol") == True:
            tv_a = "Gol"
        params["plot"] = tv_a
        plugintools.log("tv= "+tv_a)
        search_channel(params)
    elif selector == 1:
        print selector
        if tv_b.startswith("Gol") == True:
            tv_b = "Gol"
        params["plot"] = tv_b
        plugintools.log("tv= "+tv_b)
        search_channel(params)            
    elif selector == 2:
        print selector      
        if tv_c.startswith("Gol") == True:
            tv_c = "Gol"
        params["plot"] = tv_c
        plugintools.log("tv= "+tv_c)
        search_channel(params)
    elif selector == 3:
        print selector       
        if tv_d.startswith("Gol") == True:
            tv_d = "Gol"
        params["plot"] = tv_d
        plugintools.log("tv= "+tv_d)
        search_channel(params)
    elif selector == 4:
        print selector       
        if tv_e.startswith("Gol") == True:
            tv_e = "Gol"
        params["plot"] = tv_e
        plugintools.log("tv= "+tv_e)
        search_channel(params)        
    elif selector == 5:
        print selector        
        if tv_f.startswith("Gol") == True:
            tv_f = "Gol"
        params["plot"] = tv_f
        plugintools.log("tv= "+tv_f)
        search_channel(params)
    elif selector == 6:
        print selector      
        if tv_g.startswith("Gol") == True:
            tv_g = "Gol"
        params["plot"] = tv_g
        plugintools.log("tv= "+tv_g)
        search_channel(params)
    else:
        pass



def magnet_items(params):
    plugintools.log("palcoTV.magnet_items" +repr(params))
    
    plot = params.get("plot")
    

    title = params.get("title")
    fanart = ""
    thumbnail = ""
    
    if plot != "":
        filename = params.get("plot")
        params["ext"] = 'p2p'
        params["plot"]=filename
        title = plot + '.p2p'
    else:
        getfile_url(params)
        title = params.get("title")
        title = title + '.p2p'

    # Abrimos el archivo P2P y calculamos número de líneas
    file = open(playlists + title, "r")
    file.seek(0)
    data = file.readline()
    num_items = len(file.readlines())

    # Leemos entradas
    file.seek(0)
    i = 0
    while i <= num_items:
        data = file.readline()
        i = i + 1
        #print i
        if data != "":
            data = data.strip()
            title = data
            data = file.readline()
            i = i + 1
            #print i
            data = data.strip()
            if data.startswith("magnet:") == True:
                # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                title_fixed = title.replace(" " , "+")
                url_fixed = urllib.quote_plus(link)
                url = 'plugin://plugin.video.xbmctorrent/play/' + url_fixed
                plugintools.add_item(action="play" , title = data + ' [COLOR indianred][Torrent][/COLOR]' , url = url, thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True)
            else:
                data = file.readline()
                i = i + 1
                #print i
        else:
            data = file.readline()
            i = i + 1
            #print i
            

def parse_channel(txt):
    plugintools.log("palcoTV.encode_string: "+txt)

    txt = txt.rstrip()
    txt = txt.lstrip() 
    return txt


def futbolenlatv_manana(params):
    plugintools.log("palcoTV.futbolenlatv " + repr(params))
    
    # Fecha de mañana
    import datetime

    today = datetime.date.today()
    manana = today + datetime.timedelta(days=1)
    anno_manana = manana.year
    mes_manana = manana.month
    if mes_manana == 1:
        mes_manana = "enero"
    elif mes_manana == 2:
        mes_manana = "febrero"
    elif mes_manana == 3:
        mes_manana = "marzo"
    elif mes_manana == 4:
        mes_manana = "abril"
    elif mes_manana == 5:
        mes_manana = "mayo"
    elif mes_manana == 6:
        mes_manana = "junio"
    elif mes_manana == 7:
        mes_manana = "julio"
    elif mes_manana == 8:
        mes_manana = "agosto"
    elif mes_manana == 9:
        mes_manana = "septiembre"
    elif mes_manana == 10:
        mes_manana = "octubre"
    elif mes_manana == 11:
        mes_manana = "noviembre"
    elif mes_manana == 12:
        mes_manana = "diciembre"
         
        
    dia_manana = manana.day
    plot = str(anno_manana) + "-" + str(mes_manana) + "-" + str(dia_manana)
    print manana

    url = 'http://agenda.futbolenlatv.com/m/Fecha/' + plot + '/agenda/false/false'
    plugintools.log("URL mañana= "+url)
    params["url"] = url
    params["plot"] = plot
    futbolenlatv(params)
    

                    
run()


