# -*- coding: utf8 -*-
def create_index(params):
    plugintools.log("PalcoTV: Creating index file..." +repr(params))


    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    i = 0  # Control del número de listas
    for entry in ficheros:
        plugintools.log("entry= "+entry)        
        
        if entry.endswith("pbn") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
            entry = entry.replace(".plx", "")
            if new_entry.endswith("m3u") == True:
                plugintools.log("type=m3u")
                new_entry = new_entry.split("-")
                id_pbn = new_entry[0]
                title_pbn = new_entry[3]
                plugintools.log("id_pastebin= "+id_pbn)
                findex = open(tmp + 'index.txt', "a")
                findex.write("type=m3u" + '\n')
                findex.write('URL=http://pastebin.com/raw.php?i=/' + id_pbn + '/' + title_pbn + '.m3u\n')                
                i = i + 1
                continue

            if new_entry.endswith("plx") == True:
                plugintools.log("type=plx")
                new_entry = new_entry.split("-")
                id_pbn = new_entry[0]
                title_pbn = new_entry[3]
                plugintools.log("id_pastebin= "+id_pbn)
                findex = open(tmp + 'index.txt', "a")
                findex.write("type=plx" + '\n')
                findex.write('URL=http://pastebin.com/raw.php?i=/' + id_pbn + '/' + title_pbn + '.plx\n')             
                i = i + 1
                continue

            if new_entry.endswith("p2p") == True:
                plugintools.log("type=p2p")
                new_entry = new_entry.split("-")
                id_pbn = new_entry[0]
                title_pbn = new_entry[3]
                plugintools.log("id_pastebin= "+id_pbn)
                findex = open(tmp + 'index.txt', "a")
                findex.write("type=p2p" + '\n')
                findex.write('URL=http://pastebin.com/raw.php?i=/' + id_pbn + '/' + title_pbn + '.p2p\n')               
                i = i + 1
                continue

            if new_entry.endswith("xml") == True:
                plugintools.log("type=xml")
                new_entry = new_entry.split("-")
                id_pbn = new_entry[0]
                title_pbn = new_entry[3]
                plugintools.log("id_pastebin= "+id_pbn)
                findex = open(tmp + 'index.txt', "a")
                findex.write("type=xml" + '\n')
                findex.write('URL=http://pastebin.com/raw.php?i=/' + id_pbn + '/' + title_pbn + '.xml\n')             
                i = i + 1
                continue            
            
        else:
            
            entry.endswith("dbx") == True:
            entry = entry.split(".")
            new_entry = entry[0]
            
            if new_entry.endswith("m3u") == True:
                plugintools.log("type=m3u")
                new_entry = new_entry.split("-")
                id_dbx = new_entry[0]
                title_dbx = new_entry[3]
                plugintools.log("id_dropbox= "+id_dbx)
                findex = open(tmp + 'index.txt', "a")
                findex.write("type=m3u" + '\n')
                findex.write('URL=https://dl.dropboxusercontent.com/s/' + id_dbx + '/' + title_dbx + '.m3u\n')                
                i = i + 1
                continue

            if new_entry.endswith("plx") == True:
                plugintools.log("type=plx")
                new_entry = new_entry.split("-")
                id_dbx = new_entry[0]
                title_dbx = new_entry[3]
                plugintools.log("id_dropbox= "+id_dbx)
                findex = open(tmp + 'index.txt', "a")
                findex.write("type=plx" + '\n')
                findex.write('URL=https://dl.dropboxusercontent.com/s/' + id_dbx + '/' + title_dbx + '.plx\n')                
                i = i + 1
                continue

            if new_entry.endswith("p2p") == True:
                plugintools.log("type=p2p")
                new_entry = new_entry.split("-")
                id_dbx = new_entry[0]
                title_dbx = new_entry[3]
                plugintools.log("id_dropbox= "+id_dbx)
                findex = open(tmp + 'index.txt', "a")
                findex.write("type=p2p" + '\n')
                findex.write('URL=https://dl.dropboxusercontent.com/s/' + id_dbx + '/' + title_dbx + '.p2p\n')                
                i = i + 1
                continue

            if new_entry.endswith("xml") == True:
                plugintools.log("type=xml")
                new_entry = new_entry.split("-")
                id_dbx = new_entry[0]
                title_dbx = new_entry[3]
                plugintools.log("id_dropbox= "+id_dbx)
                findex = open(tmp + 'index.txt', "a")
                findex.write("type=xml" + '\n')
                findex.write('URL=https://dl.dropboxusercontent.com/s/' + id_dbx + '/' + title_dbx + '.xml\n')                
                i = i + 1
                continue




            
