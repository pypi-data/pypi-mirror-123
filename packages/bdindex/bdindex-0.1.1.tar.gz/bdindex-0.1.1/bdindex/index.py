from datetime import datetime
from datetime import timedelta
import json
import requests


class index():
    def __init__(self, word, cookie):
        self.keyword = word
        self.cookie = cookie
        #self.cj = browsercookie.chrome()
        self.today = datetime.strftime(datetime.today(), '%Y-%m-%d')

    def get_max(self, key, data):
        a = key
        i = data
        n = {}
        s = []
        rn = []
        for o in range(len(a)//2):
            n[a[o]] = a[len(a)//2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        res = ''.join(s).split(',')
        for j in res:
            try:
                rn.append(int(j))
            except:
                rn.append(0)
        return rn

    def get_baidu_index(self, start = '2011-01-01', end = datetime.strftime(datetime.today(), '%Y-%m-%d')):
        try:
            header = {
            'Host': 'zhishu.baidu.com',
            #'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Connection': 'keep-alive',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cookie': self.cookie
            }
            url = f'http://zhishu.baidu.com/api/SearchApi/index?area=0&word=[[{{"name":"{self.keyword}","wordType":1}}]]&startDate={start}&endDate={end}'
            wbdata = requests.get(url, headers=header)
            time_type = json.loads(wbdata.text)['data']['userIndexes'][0]['type']
            data = json.loads(wbdata.text)['data']['userIndexes'][0]['all']['data']
            uniqid = json.loads(wbdata.text)['data']['uniqid']
            url_key = 'http://zhishu.baidu.com/Interface/ptbk?uniqid=' + uniqid
            kdata = requests.get(url_key, headers=header)
            key = json.loads(kdata.text)['data']
            record =  self.get_max(key,data)
            if time_type == 'week':
                dic = {}
                sd = datetime.strptime(start, '%Y-%m-%d')
                ed = datetime.strptime(end, '%Y-%m-%d')
                sdw = sd.weekday()
                sd0 = sd-timedelta(sdw)
                ticks = []
                time = sd0
                while time <= ed:
                    ticks.append(datetime.strftime(time, '%Y%m%d') + '-' + datetime.strftime(time+timedelta(6), '%Y%m%d'))
                    time = time+timedelta(7)
                for i in range(len(record)):
                    dic[ticks[i]] = record[i]
            elif time_type == 'day':
                sd = datetime.strptime(start, '%Y-%m-%d')
                date = []
                while len(date) < len(record):
                    date.append(datetime.strftime(sd, '%Y-%m-%d'))
                    sd = sd + timedelta(1)
                dic = {}
                for i in range(len(record)):
                    dic[date[i]] = record[i]
            return dic
        except:
            return None
    
    def get_age(self):
        record1 = []
        record2 = []
        url = 'http://zhishu.baidu.com/api/SocialApi/baseAttributes?wordlist[]={}'.format(self.keyword)
        data = json.loads(requests.get(url).text)['data']
        if data == '':
            record1 = record1 + [None for n in range(7)]
            record2 = record2 + [None for n in range(7)]
        else:
            for li in range(2):
                record1 = record1 + [data['result'][0]['gender'][li]['tgi']]
            for li in range(5):
                record1 = record1 + [data['result'][0]['age'][li]['tgi']]
            for li in range(2):
                record2 = record2 + [data['result'][0]['gender'][li]['rate']]
            for li in range(5):
                record2 = record2 + [data['result'][0]['age'][li]['rate']]
        return record1,record2
