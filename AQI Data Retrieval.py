from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import datetime
import sys

ts = time.time()
current_time_dt = datetime.datetime.fromtimestamp(ts)
current_time = current_time_dt.strftime('%d-%m-%Y %H:%M:%S')
last_update = datetime.datetime.strptime(pd.read_csv('./data/aqi-data.csv').iloc[0]['Timestamp'],'%d-%m-%Y %H:%M:%S')
if (current_time_dt-last_update) >= datetime.timedelta(hours = 1):
    df = pd.DataFrame()

    l = ['https://www.aqi.in/dashboard/india/andhra-pradesh',
     'https://www.aqi.in/dashboard/india/arunachal-pradesh',
     'https://www.aqi.in/dashboard/india/assam',
     'https://www.aqi.in/dashboard/india/bihar',
     'https://www.aqi.in/dashboard/india/chandigarh',
     'https://www.aqi.in/dashboard/india/chhattisgarh',
     'https://www.aqi.in/dashboard/india/dadra-and-nagar-haveli',
     'https://www.aqi.in/dashboard/india/daman-and-diu',
     'https://www.aqi.in/dashboard/india/delhi',
     'https://www.aqi.in/dashboard/india/goa',
     'https://www.aqi.in/dashboard/india/gujarat',
     'https://www.aqi.in/dashboard/india/haryana',
     'https://www.aqi.in/dashboard/india/himachal-pradesh',
     'https://www.aqi.in/dashboard/india/jammu-and-kashmir',
     'https://www.aqi.in/dashboard/india/jharkhand',
     'https://www.aqi.in/dashboard/india/karnataka',
     'https://www.aqi.in/dashboard/india/kerala',
     'https://www.aqi.in/dashboard/india/madhya-pradesh',
     'https://www.aqi.in/dashboard/india/maharashtra',
     'https://www.aqi.in/dashboard/india/manipur',
     'https://www.aqi.in/dashboard/india/meghalaya',
     'https://www.aqi.in/dashboard/india/mizoram',
     'https://www.aqi.in/dashboard/india/nagaland',
     'https://www.aqi.in/dashboard/india/odisha',
     'https://www.aqi.in/dashboard/india/puducherry',
     'https://www.aqi.in/dashboard/india/punjab',
     'https://www.aqi.in/dashboard/india/rajasthan',
     'https://www.aqi.in/dashboard/india/sikkim',
     'https://www.aqi.in/dashboard/india/tamil-nadu',
     'https://www.aqi.in/dashboard/india/telangana',
     'https://www.aqi.in/dashboard/india/tripura',
     'https://www.aqi.in/dashboard/india/uttar-pradesh',
     'https://www.aqi.in/dashboard/india/uttarakhand',
     'https://www.aqi.in/dashboard/india/west-bengal']

    for link in l:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, features="html.parser")
        state = r.url[35:]
        content = soup.find_all('table')[0]
        count = 0
        for i in content.find_all('td'):
            if count == 0:
                place = i.text
                count+=1
            elif count == 1:
                condition = i.text
                count+=1
            elif count == 2:
                aqi = i.text
                count+=1
            elif count == 3:
                pm25 = i.text
                count+=1
            elif count == 4:
                pm10 = i.text
                count+=1
            elif count == 5:
                temp = i.text
                count+=1
            elif count == 6:
                humid = i.text
                place_dict = {
                    'Timestamp':current_time,
                    'State':state,
                    'City':place,
                    'Condition':condition,
                    'AQI':aqi,
                    'PM 2.5':pm25,
                    'PM 10':pm10,
                    'Temperature':temp,
                    'Humidity':humid
                }
                df = df.append(place_dict,ignore_index=True)
                count = 0

    def state_name(name):
        split_list = name.split('-')
        if len(split_list) == 4:
            return split_list[0].capitalize() + " " + split_list[1].capitalize() + " " + split_list[2].capitalize() + " " + split_list[3].capitalize()
        elif len(split_list) == 3:
            return split_list[0].capitalize() + " " + split_list[1].capitalize() + " " + split_list[2].capitalize()
        elif len(split_list) == 2:
            return split_list[0].capitalize() + " " + split_list[1].capitalize()
        else:
            return split_list[0].capitalize()

    df['State'] = df['State'].apply(state_name)
    print('Updated Realtime Data')
    df.to_csv('./data/aqi-data.csv')
