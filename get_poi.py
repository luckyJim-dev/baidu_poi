# -*- coding: UTF-8 -*-

from mapapi import baidu
import json
import logging
import re
from xpinyin import Pinyin
import lnglatTransfer as Transfer
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

def get_file_name_by_city(city):
    piny = Pinyin()
    cittyName = piny.get_pinyin(city,'')
    return ('data/{0}.csv'.format(cittyName))

def get_kml_file_by_city(city):
    piny = Pinyin()
    cittyName = piny.get_pinyin(city,'')
    return ('data/{0}.kml'.format(cittyName))

def get_tags_by_city(tags,city):
    map_api = baidu.MapApi()
    file_name = get_file_name_by_city(city)
    kml_name = get_kml_file_by_city(city)
    fold = KML.Folder()
    with open(kml_name,'w',encoding = 'utf-8') as kml_f:
        with open(file_name,'w',encoding = 'utf-8') as f:
            print("Start...")
            f.write("{},{},{}".format('name','lat','lng'))
            for tag in tags:
                data = map_api.place_api.get_place_all(tag,city)
                for item in data:
                    try:
                        name = item['name']
                        lng = float(item['location']['lng'])
                        lat = float(item['location']['lat'])
                        [g_lng,g_lat] = Transfer.bd09_to_wgs84(lng,lat)
                        # Write data in CSV
                        f.write("{},{},{}".format(name,g_lng,g_lat))
                        # Write data in kml
                        fold.append(
                            KML.Placemark(
                                KML.name(name),
                                KML.Point(KML.coordinates(str(g_lng)+","+str(g_lat)))
                            ))
                    except:
                        logging.exception('Error: Parsing json file ')
            f.close()
        output = etree.tostring(fold,pretty_print=True)
        kml_f.write(output.decode('utf-8'))
        kml_f.close()
    print("sucess")
    pass

if __name__ == '__main__':

    tags = input("请输入你所需要查询的场景,多个场景以逗号隔开:").split(',')
    city = input("请输入你所需要查询的城市:")
    get_tags_by_city(tags,city)