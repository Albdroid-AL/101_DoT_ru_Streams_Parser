# -*- coding: utf-8 -*-
#*-----------------------------------------------------------------------------------------------------------------*
#       _______ ___  ____  __  __   ________                           __        ____                              #
#      <  / __ <  / / __ \/ / / /  / ____/ /_  ____ _____  ____  ___  / /____   / __ \____ ______________  _____   #
#      / / / / / / / /_/ / / / /  / /   / __ \/ __ `/ __ \/ __ \/ _ \/ / ___/  / /_/ / __ `/ ___/ ___/ _ \/ ___/   #
#     / / /_/ / / / _, _/ /_/ /  / /___/ / / / /_/ / / / / / / /  __/ (__  )  / ____/ /_/ / /  (__  )  __/ /       #
#    /_/\____/_(_)_/ |_|\____/   \____/_/ /_/\__,_/_/ /_/_/ /_/\___/_/____/  /_/    \__,_/_/  /____/\___/_/        #
#                               _     _  _____  ______  _____   _______                                            #
#                               |____/  |     | |     \   |     |_____| |                                          #
#                               |    \_ |_____| |_____/ __|__ . |     | |_____                                     #
#                                                                                                                  #
#*-----------------------------------------------------------------------------------------------------------------*
# NOTE: JUST PRESS RUN AND SAVE 101_dot_RU_M3U_Radios_[NUMBER].m3u8 AND PLAY IT

import json

import requests

stations = set()
groups = {}

for station_id in range(1, 400):
    res = requests.get(
	# PERSHEMBULL http://101.ru/api/channel/AboutChannel/1/channel/?dataFormat=json
        'http://101.ru/api/channel/AboutChannel/{}/channel/?dataFormat=json'.
        format(station_id))
    data = res.json()
	# IF IS ACTIVE
    if data['status'] != 1:
        continue
    if data['result']['onAir'] is False and data['result']['visibility'] != 1:
        continue
    group_id = data['result']['group_id']
    try:
        groups[data['result']
               #['group_id']] = data['result']['group_info']['name'] # RUSSIAN GROUP NAMES
               ['group_id']] = data['result']['group_info']['name_eng'] # ENGLISH GROUP NAMES
    except TypeError:
        pass
   # NE GJUHEN E KETYRE CECENAVE TERHEQ ME SHUME KANALE 
   # title = data['result']['rus_name'] # Russian Lang Categoty Names
   # NE ENGLISH TERHEQ DIKU TEK 3-4 KANALE ME PAK
    title = data['result']['eng_name'] # English Lang Categoty Names
    res = requests.get(
	# PERSHEMBULL http://101.ru/api/channel/getServers/128/channel/5/128/?dataFormat=json
        'http://101.ru/api/channel/getServers/{}/channel/{}/128/?dataFormat=json'
        .format(station_id,
                'AAC' if data['result']['aac_format'] == 1 else 'MP3'))
    data2 = res.json()
    if data2['status'] != 1:
        continue
    print(station_id)
	# PERSHEMBULL http://101.ru/api/channel/getServers/128/channel/1/128/dataFormat/mobile
    url = 'http://101.ru/api/channel/getServers/{}/channel/{}/128/dataFormat/mobile'.format(
        station_id, 'AAC' if data['result']['aac_format'] == 1 else 'MP3')
    stations.add((group_id, title, url))

stations2 = []
for station in stations:
    stations2.append(('{} - {}'.format(
        groups.get(station[0]) or 'No Group', station[1]), station[2]))

# BUILD DATA

build_channels = sorted(stations2, key=lambda tup: tup[0].lower())
with open('101_Dot_RU_Radios_{}.m3u8'.format(len(build_channels)), 'w') as f:
    f.write('#EXTM3U Albdroid TV Streaming - 101.RU Radio Channels\r\n')
    # f.write('#PLAYLIST 101.RU Radio Channels\r\n')
    for title, url in build_channels:
        f.write('#EXTINF:-1,{}\r\n'.format(title))
        f.write('{}\r\n'.format(url))

print('Bulding', len(build_channels),'Channels')
