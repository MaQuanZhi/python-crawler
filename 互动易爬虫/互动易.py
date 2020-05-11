import requests
import re
import time
import random
from fake_useragent import UserAgent

class Cninfo(object):
    def __init__(self):
        self.base_url = 'http://irm.cninfo.com.cn/ircs/company/dynamic'
        self.stockcode = ''
        self.pub_count = [0]*11 #2010年到2020年
        self.reply_count = [0]*11
        self.ua = UserAgent()
    
    def get_ip(self):
        with open('f:\\data\\ip.txt','r') as f:
            ip_list = f.read().split('\n')
            return ip_list
        
    def prase_json(self,data):
        rows = data['rows']
        flag = 0
        for row in rows:
            if row['contentType'] != 3: # 3为公告
                pubYear = time.localtime(row['pubDate']//1000).tm_year
                if pubYear < 2010:
                    flag = 1
                    break
                if(row['attachedContent']): #有回复
                    replyYear = time.localtime(row['updateDate']//1000).tm_year
                    self.pub_count[pubYear-2010] += 1
                    self.reply_count[replyYear-2010] +=1
                else:
                    self.pub_count[pubYear-2010] += 1
        return flag
                    
    def get_data(self,stockcode):
        print(stockcode)
        ip_list = self.get_ip()
        url ='http://irm.cninfo.com.cn/ircs/company/companyDetail?stockcode={}'.format(stockcode)
        headers = {}
        headers['User-Agent'] = self.ua.random
        r = requests.get(url,headers=headers)
        orgId = re.findall('orgId = "(.*?)"',r.text)[0]
        form = {'stockcode': stockcode,
                'pageSize': 10,
                'orgId':orgId,
                'pageNum': 1}
        while(1):
            try:
                ip = random.choice(ip_list)
                resp = requests.post(self.base_url,data=form,headers=headers,proxies={'http':ip,'https':ip},timeout=1)
                page1 = resp.json()
                self.prase_json(page1)
                totalPage = page1['totalPage']
                break
            except:
                ip_list = self.get_ip()
        
        for pageNum in range(1,totalPage+1):
            print('\r{0}/{1}'.format(pageNum,totalPage),end='')
            form['pageNum'] = pageNum
            headers['User-Agent'] = self.ua.random
            while(1):
                try:
                    ip = random.choice(ip_list)
                    resp = requests.post(self.base_url,data=form,headers=headers,proxies={'http':ip,'https':ip},timeout=1)
                   
                    break
                except:
                    ip_list = self.get_ip()
            try:      
                data = resp.json()
                flag = self.prase_json(data)
                if flag:
                    break
            except:
                pass
        
        print('\n')
        pub_str = ','.join([str(_) for _ in self.pub_count])
        reply_str = ','.join([str(_) for _ in self.reply_count])
        self.pub_count = [0]*11
        self.reply_count = [0]*11
        with open('f:\\data\\cninfo.txt','a') as f:
            f.write(','.join([stockcode,pub_str,reply_str]))
            f.write('\n')
            
    def main(self):
        with open('f:\\data\\部分深证A股.txt','r') as f:
            code_list = f.read().split('\n')
        for code in code_list:
            self.get_data(code)
        
if __name__ == '__main__':
    cninfo = Cninfo()
    cninfo.main()
             
            
    
    