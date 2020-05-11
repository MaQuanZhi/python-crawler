import requests
import re
import time
import random
import xlwt

requests.adapters.DEFAULT_RETRIES = 3

headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-HK;q=0.5',
            'cookie': 'sessid=C9046BC7-D214-02FE-FC9F-0C06FFF18147; aQQ_ajkguid=76BCC028-C9A2-82C7-15C0-A91E0027CB49; lps=http%3A%2F%2Fwww.anjuke.com%2F%7Chttps%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0v22y5tzjnKMNcnwKIMD2h7z3UgocrBZ-LHKh6Uh_e9WyTjAGC3PhCxyxo-Wy5NP%26wd%3D%26eqid%3Dd8b639d700031d4e000000065ea7bb72; twe=2; _ga=GA1.2.2067826780.1588050806; _gid=GA1.2.92057143.1588050806; 58tj_uuid=af973e09-648f-4eb3-9c82-bf1923a4c93d; als=0; wmda_uuid=9d2bf7390c4f0b6f9c74b40c8ab89d3d; wmda_new_uuid=1; wmda_visited_projects=%3B6145577459763; init_refer=; new_uv=3; ctid=31; wmda_session_id_6145577459763=1588085653964-8efa7f87-9daa-a1b6; new_session=0; xzfzqtoken=OLrjd7jAlPsch7ql7dfMk81cm5KF6uVzlxGYYL0Eb2bbDUx%2BMsOYx94XTUpg3v5zin35brBb%2F%2FeSODvMgkQULA%3D%3D',
            'referer': 'https://m.anjuke.com/xa/community/beilinqu/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

def to_string(mylist):
    mystr = '\t'.join([str(_) for _ in mylist])+'\n'
    return mystr

def get_info(page,txt_path="f:\\data\\anjuke.txt"):
    base_url = 'https://m.anjuke.com/xa/community/beilinqu/?p='+str(page)
    r = requests.get(base_url,headers=headers)
    time.sleep(random.randint(1, 3))
    data = r.json()['data']
    for i in range(len(data)):
        url = data[i]['url']
        print(i,url)
        resp = requests.get(url,headers=headers)
        all_num = re.findall('</i>([0-9]{1,5}户)',resp.text)
        data[i]['all_num'] = all_num[0] if all_num else '--'
        time.sleep(random.randint(1, 3))
    with open(txt_path,'a',encoding='utf8') as f:
        if page == 1:
            head = to_string(list(data[0].keys()))
            f.write(head)
        for i in range(len(data)):
            line = to_string(list(data[i].values()))
            f.write(line)
            
def write_excel(txt_path,xls_path):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet("sheet1")
    with open(txt_path,'r',encoding='utf8') as t:
        lines = t.read().split('\n')
        for row in range(len(lines)):
            line = lines[row].split('\t')
            for col in range(len(line)):
                sheet1.write(row,col,line[col])
    f.save(xls_path)
    
if __name__ == "__main__":       
    txt_path = "f:\\data\\anjuke.txt"
    xls_path = "f:\\data\\anjuke.xls"    
    for i in range(1,26):
        print(i)
        get_info(i,txt_path)
        time.sleep(random.randint(5, 15))
    write_excel(txt_path, xls_path)
