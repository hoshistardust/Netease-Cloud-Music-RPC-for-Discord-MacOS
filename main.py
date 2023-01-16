import os
import time
import re
from pypresence import Presence
import json
import datetime as dt

def follow(thefile):
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)
    
    # start infinite loop
    while True:
        # read last line of file
        line = thefile.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue

        yield line

# for calculating elapsed time - WIP, replacable with int(time.time()) for the current application
def epoch_convert(human_time):
    pattern = '%Y-%m-%d %H:%M:%S'
    epoch_time = int(time.mktime(time.strptime(human_time,pattern)))
    return epoch_time

if __name__ == '__main__':
    # Input your discord application client ID here
    client_id = 'Your Client ID here'
    RPC = Presence(client_id)
    RPC.connect()
    path = os.path.join(os.path.expanduser('~'),r'Library/Containers/com.netease.163music/Data/Documents/storage/Logs/music.163.log')
    current_song = ""
    current_artist = ""
    current_album = ""
    current_image = ""
    current_duration = ""
    reg_newsong = re.compile(r'songName')
    #reg_status = re.compile(r'(?<=player\._\$).+(?<!\sdo)$')
    reg_time = re.compile(r'(?<=\[).+?(?=\])')  
    logfile = open(path,"r")
    loglines = follow(logfile)
    # iterate over the generator  
    for line in loglines:
        if reg_newsong.search(line):
            # extract song info from netease log file
            result = re.findall(r'({"playId".+)',line)[0]
            current_info = json.loads(result)
            current_song = current_info['songName']
            current_album = current_info['albumName']
            current_artist = current_info['artistName']
            current_image = current_info['url']
            current_duration = str(dt.timedelta(seconds=round(float(current_info['duration']))))
            #song_elapsed = 0
            song_start = epoch_convert(reg_time.search(line).group(0))
            # update relevant song data to discord RPC
            RPC.update(details = current_song + " (" + current_duration + ")", 
            state = current_artist + " | " + current_album, 
            large_image= current_image, start = song_start)
"""
        if reg_status.search(line):
            if reg_status.search(line).group(0) == "pause":
                paused_time = epoch_convert(reg_time.search(line).group(0))
                RPC.update(small_image='pause',end = int(time.time()))
            elif reg_status.search(line).group(0) == "resume":
                RPC.update(small_image='play')
"""