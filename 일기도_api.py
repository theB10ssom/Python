# -*- coding: utf-8 -*-
"""일기도_API.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RuXaemmXpRK_XGWhJYUD80x5XrZH8Glh
"""

!pip install xmltodict
import pandas as pd
import urllib.request
import urllib.parse as urlparse
import requests
import xmltodict
from pandas import json_normalize 
#from pandas.io.json import json_normalize #use if pandas version is low (about 0.25?)
from IPython.display import Image, display



class Weather_map_api():
    def __init__(self, url,serviceKey):
        self.url = url
        self.serviceKey = serviceKey

    def get_request_query(self, operation, params):
        params = urlparse.urlencode(params)
        request_query = f'{self.url}/{operation}?serviceKey={self.serviceKey}&{params}'
        req = requests.get(url = request_query)
        self.response = req
        return req
    
    def parse_response(self):
        df_temp = pd.DataFrame()
        if True == self.response.ok:
            content = self.response.content
            box = xmltodict.parse(content)
            temp = json_normalize(box['response']['body'])
            df_temp = pd.concat([df_temp, temp])
            return df_temp
        else:
            return print("Error Occured")
        
    def show_image(self, img_url):
        image_url = img_url
        return Image(url = image_url)

if __name__ == '__main__':

    url = 'http://apis.data.go.kr/1360000/WthrChartInfoService'
    serviceKey = 'your servicekey'
    weathermap = Weather_map_api(url, serviceKey)

    operation = 'getSurfaceChart'
    params = {'code' : 12, 'time' : '20210121'} 
    response = weathermap.get_request_query(operation, params)
    api_out = weathermap.parse_response()

    img_url = api_out.iloc[0,-1]
    display(weathermap.show_image(img_url))
    
    #save option
    #urllib.request.urlretrieve(img_url, "test.png")

