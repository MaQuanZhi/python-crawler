import requests
import re
import time

re_str = re.compile(r'<[^>]+>')

requests.adapters.DEFAULT_RETRIES = 5

ua = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
id = '1871802012' #深圳天气
containerid = '1076031871802012'
url='https://m.weibo.cn/api/container/getIndex?type=uid&value=1871802012&containerid=1076031871802012&page='
retweeted_url = 'https://m.weibo.cn/statuses/extend?id='
info_list = []

def get_weibo(page):
    global url,info_list
    resp = requests.get(url+str(page),headers = ua)
    json_data = resp.json()
    data = json_data['data']
    cards = data['cards']
    for card in cards:
        mblog = card['mblog']
        attitudes_count = str(mblog['attitudes_count']) #点赞
        created_at = mblog['created_at'] #时间
        reposts_count = str(mblog['reposts_count']) #转发
        comments_count = str(mblog['comments_count']) #评论
        text = mblog['text']
        text = re_str.sub('',text)
        text = text.replace('&quot;','"').replace('\n','').replace('\r','')
        try:
            textLength = str(mblog['textLength'])
        except:
            textLength = '0'
        if 'retweeted_status' in mblog.keys():
            retweeted_flag = '是'
            retweeted_status = mblog['retweeted_status']
            retweeted_id = retweeted_status['id']
            res = requests.get(retweeted_url+retweeted_id,headers = ua)
            retweeted_text = res.json()['data']['longTextContent']
            retweeted_text = re_str.sub('',retweeted_text) #去除html标记
            retweeted_text = retweeted_text.replace('&quot;','"').replace('\n','').replace('\r','') #替换引号，去掉换行
        else:
            retweeted_flag = '否'
            retweeted_text = ''
        format_str = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}'.format(created_at,
                      reposts_count,comments_count,attitudes_count,text,textLength,
                      retweeted_flag,retweeted_text) #时间，转发数，评论数，点赞数，内容，字数，转发，转发内容
#        print(format_str)
        info_list.append(format_str)
    
    
if __name__ == '__main__':
    with open('F:/1_3月微博.txt','w',encoding='utf8') as f:
        f.write('时间\t转发数\t评论数\t点赞数\t微博内容\t字数\t转发\t转发内容\n')
    for i in range(79,235): 
        time.sleep(1)
        get_weibo(i)
        print(i)
    with open('F:/1_3月微博.txt','a',encoding='utf8') as f:
        f.write('\n'.join(info_list))
    