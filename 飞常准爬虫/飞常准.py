import requests
import re
from bs4 import BeautifulSoup as bs
import time
import random
from fake_useragent import UserAgent

requests.adapters.DEFAULT_RETRIES = 5

class Variflight(object):
    def __init__(self):
        self.url_base = 'http://www.variflight.com'
        self.ua = UserAgent()
        self.headers = {}
        
    def get_ip(self):
        with open('f:\\data\\ip.txt','r') as f:
            ip_list = f.read().split('\n')
            return ip_list
    
    def get_fnums(self): #航班列表
        ip_list = self.get_ip()
        url_fnum_list = 'http://www.variflight.com/sitemap.html?AE71649A58c77='
        while(1):
            try:
                self.headers['User-Agent'] = self.ua.random
                ip = random.choice(ip_list)
                r = requests.get(url_fnum_list,headers=self.headers,proxies={'http':ip,'https':ip},timeout=1)
                break
            except:
                ip_list = self.get_ip()
        soup = bs(r.text,'lxml')
        list_a = soup.find(class_='list').find_all('a')
        list_url_fnum = [self.url_base + a.attrs['href'] for a in list_a]
#        print('get_fums')
        return list_url_fnum
    
    def get_fnums_from_txt(self,fname='所有航班号'):
        url = 'http://www.variflight.com/flight/fnum/{}.html?AE71649A58c77='
        with open('f:\\data\\{}.txt'.format(fname),'r') as f:
            fnums = f.read().split(' ')
            url_fnums = [url.format(fnum) for fnum in fnums]
            return url_fnums
    
    def get_url_details(self,url_fnum,fdate): 
        
        try:#fdate=20200101
            url = url_fnum + '&fdate={}'.format(fdate)
#            print(url)
            ip_list = self.get_ip()
            while(1):
                try:
                    ip = random.choice(ip_list)
                    self.headers['User-Agent'] = self.ua.random
                    r = requests.get(url,headers=self.headers,proxies={'http':ip,'https':ip},timeout=1)
    #                   print(r.text)
                    break
                except:
                    ip_list = self.get_ip()
            soup = bs(r.text,'lxml')
            list_a = soup.find_all(class_="searchlist_innerli")
            list_url = [self.url_base + a.attrs['href'] for a in list_a]
            
            return list_url
        
        except:
#            print(e)
            return []
    def timeformat(self,timestamp):
        timestr = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(timestamp)) if timestamp else '--'
        return timestr
    
    def get_url_data(self,url_detail):
        while(1):
            ip_list = self.get_ip()
            try:
                self.headers['User-Agent'] = self.ua.random
                ip = random.choice(ip_list)
                r = requests.get(url_detail,headers=self.headers,proxies={'http':ip,'https':ip},timeout=1)
                url_str = re.findall('https://flightadsb.variflight.com/flight-playback/(.*?)"',r.text)[0]
                values = url_str.split('/')
                fnum = values[0]
                forg = values[1]
                fdst = values[2]
                ftime = values[3]
                url_data = 'https://adsbapi.variflight.com/adsb/index/flight?lang=zh_CN&fnum={fnum}&time={time}&forg={forg}&fdst={fdst}'.format(fnum=fnum,time=ftime,forg=forg,fdst=fdst)
                break
            except:
#                print(e)
                ip_list = self.get_ip()
       
#        print('get_url_data')
        return url_data
    
    def parse_data(self,url_data,fdata):
        ip_list = self.get_ip()
        while(1):
            try:
                self.headers['User-Agent'] = self.ua.random
                ip = random.choice(ip_list)
                r = requests.get(url_data,headers=self.headers,proxies={'http':ip,'https':ip},timeout=1)
                json= r.json()
                data = json.get('data',{})
                break
            except:
                ip_list = self.get_ip()
        
        fnum = data.get('fnum','--') #航班号
        airCName = data.get('airCName','--') # 航空公司
        scheduledDeptime = self.timeformat(data.get('scheduledDeptime',0)) # 计划出发
        actualDeptime = self.timeformat(data.get('actualDeptime',0)) # 实际出发
        forgAptCname = data.get('forgAptCname','--') # 出发地
        scheduledArrtime = self.timeformat(data.get('scheduledArrtime',0)) # 计划到达
        actualArrtime = self.timeformat(data.get('actualArrtime',0)) # 实际到达
        fdstAptCname = data.get('fdstAptCname','--') # 到达地
        status = '取消' if actualArrtime == '--' else '到达' # 状态
        value = ','.join([fnum,airCName,scheduledDeptime,actualDeptime,forgAptCname,scheduledArrtime,actualArrtime,fdstAptCname,status])
#        print(value)
        with open('f:\\data\\{0}.csv'.format(fdata),'a') as f:
            f.write(value + '\n')
            
    def main(self):
#        fnums = self.get_fnums()
        fnums = self.get_fnums_from_txt('所有航班号')
        n = len(fnums)
        fdata_list = [_ for _ in range(20200102,20200132)] + [_ for _ in range(20200201,20200229)]
        for fdata in fdata_list:
            print(fdata)
            for i in range(n):
                print('\r{}/{}'.format(i+1,n),end='')
                fnum = fnums[i]
                url_details = self.get_url_details(fnum,fdata)
                for url_detail in url_details:
                    url_data = self.get_url_data(url_detail)
                    self.parse_data(url_data,fdata)
                
if __name__ == "__main__":  
    flight = Variflight()
    flight.main()

