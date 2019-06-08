#!/usr/bin/python 
# -*- coding: utf-8 -*-

import csv
import requests
# 之後可用bs()來表示BeautifulSoup()
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import chardet
import random

import gmaps
import gmaps.datasets
from geopy.geocoders import GoogleV3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def print_area_num():
    dic = {1: '台北市', 2: '新北市', 3: '宜蘭縣', 4: '基隆市',
           5: '桃園市', 6: '新竹縣市', 7: '苗栗縣', 8: '台中市',
           9: '台中市(原台中縣)', 10: '彰化縣', 11: '南投縣',
           12: '雲林縣', 13: '嘉義縣市', 14: '台南市',
           15: '台南市(原台南縣)', 16: '高雄市', 17: '高雄市(原高雄縣)',
           18: '屏東縣', 19: '台東縣', 20: '花蓮縣', 21: '澎湖縣',
           22: '金門縣', 23: '連江縣'}

    for item, value in dic.items():
        print(item, value)


def print_job_num():
    job_num = {'經營／人資類': '1',
               '行政／總務／法務類': '2',
               '財會／金融專業類': '3',
               '行銷／企劃／專案管理類': '4',
               '客服／門市／業務／貿易類': '5',
               '餐飲／旅遊 ／美容美髮類': '6',
               '資訊軟體系統類': '7',
               '研發相關類': '8',
               '生產製造／品管／環衛類': '9',
               '操作／技術／維修類': '10',
               '資材／物流／運輸類': '11',
               '營建／製圖類': '12',
               '傳播藝術／設計類': '13',
               '文字／傳媒工作類': '14',
               '醫療／保健服務類': '15',
               '學術／教育／輔導類': '16',
               '軍警消／保全類': '17',
               '其他職類': '18'}

    for item, value in job_num.items():
        print(value, item)


def print_job7_num():
    # if input include 7
    job7_num = {
        '全部': '7.0.0',
        '軟體╱工程類人員': '7.1.0',
        '軟體專案主管': '7.1.1',
        '電子商務技術主管': '7.1.2',
        '通訊軟體工程師': '7.1.3',
        '軟體設計工程師': '7.1.4',
        '韌體設計工程師': '7.1.5',
        'Internet程式設計師': '7.1.6',
        '電腦系統分析師': '7.1.7',
        '電玩程式設計師': '7.1.8',
        '其他資訊專業人員': '7.1.9',
        '資訊助理人員': '7.1.10',
        'BIOS工程師': '7.1.11',
        '演算法開發工程師': '7.1.12',

        'MIS╱網管類人員': '7.2.0',
        'MIS╱網管主管': '7.2.1',
        '資料庫管理人員': '7.2.2',
        'MIS程式設計師': '7.2.3',
        'MES工程師': '7.2.4',
        '網路管理工程師': '7.2.5',
        '系統維護╱操作人員': '7.2.6',
        '資訊設備管制人員': '7.2.7',
        '網路安全分析師': '7.2.8',
    }  # 空字串不可以
    for item, value in job7_num.items():
        print(value, item)


def get_input_value():
    global Action
    Action = [i for i in input('請輸入欲執行的動作(1=搜尋職缺, 2=在地圖上顯示職缺, 3=自動投遞, 4=搜尋職缺+自動投遞):').split(",")]

    if ("1" in Action) or ("4" in Action):
        # 104網址新鮮人網填入的選項
        global keyword_input, area_input, jobcategory_input, job7_input, job7_or_not
        keyword_input = input('請輸入關鍵字:')
        print_area_num()
        area_input = input('請輸入縣市(依上表代碼)')
        print()
        print_job_num()
        jobcategory_input = input('請輸入職務類別(依上表代碼)')
        print()

        # 判斷是否 7
        job7_input = ''
        job7_or_not = 0
        if '7' in jobcategory_input.split(','):
            job7_or_not = 1
            print('====資訊軟體系統類====')
            print_job7_num()
            job7_input = input('請輸入職務類別(資訊軟體系統類):(依上表代碼)')
        print()

        # 選擇輸出的欄位,Default或All
        global column
        column = "1"
        # column = input("請輸入欄位(1=Default, 2=All):")

        # 選擇輸出的職務欄位
        global job_Default, job_All, job_head_dic
        job_Default = [2, 4, 12, 16, 17]
        job_All = [i for i in range(1, 19)]
        job_head_dic = {1: '職務類別', 2: '工作待遇', 3: '工作性質', 4: '上班地點', 5: '管理責任', 6: '出差外派', 7: '上班時段',
                        8: '休假制度', 9: '可上班日', 10: '需求人數', 11: '接受身份', 12: '工作經歷', 13: '學歷要求', 14: '科系要求',
                        15: '語文條件', 16: '擅長工具', 17: '工作技能', 18: '其他條件'}

        # 選擇輸出的公司欄位
        global com_Default, com_All, com_head_dic
        com_Default = [1, 3, 4]
        com_All = [i for i in range(1, 10)]
        com_head_dic = {1: '產業類別', 2: '產業描述', 3: '員工', 4: '資\xa0本\xa0額', 5: '聯\xa0絡\xa0人', 6: '公司地址',
                        7: '電話', 8: '傳真', 9: '公司網址'}

    if ("3" in Action) or ("4" in Action):
        global job_submit_username, job_submit_password
        job_submit_username = 'A106592535'
        job_submit_password = 'test1234'

    if ("2" in Action) or ("3" in Action):
        global job_seq_method, job_seq
        job_seq_method = input('請選擇"職務編號"(1=全部, 2=自行輸入需要的編號, 3=自行輸入不需要的編號):')
        if job_seq_method != "1":
            job_seq = input('請輸入:')


def get_area():
    area_lib = {'1': '6001001000',
                '2': '6001002000',
                '3': '6001003000',
                '4': '6001004000',
                '5': '6001005000',
                '6': '6001006000',
                '7': '6001007000',
                '8': '6001008000',
                '9': '6001009000',
                '10': '6001010000',
                '11': '6001011000',
                '12': '6001012000',
                '13': '6001013000',
                '14': '6001014000',
                '15': '6001015000',
                '16': '6001016000',
                '17': '6001017000',
                '18': '6001018000',
                '19': '6001019000',
                '20': '6001020000',
                '21': '6001021000',
                '22': '6001022000',
                '23': '6001023000'}

    area_mid_index = [area_lib[i] for i in area_input.split(',') if i in area_lib]  # 任何輸入皆可符合
    area_output = '%2C'.join(area_mid_index)
    return area_output


def get_jobcategory():
    jobcategory_lib = {'1': '2001000000',
                       '2': '2002000000',
                       '3': '2003000000',
                       '4': '2004000000',
                       '5': '2005000000',
                       '6': '2006000000',
                       '7': '2007000000',
                       '8': '2008000000',
                       '9': '2009000000',
                       '10': '2010000000',
                       '11': '2011000000',
                       '12': '2012000000',
                       '13': '2013000000',
                       '14': '2014000000',
                       '15': '2015000000',  # python output no job
                       '16': '2016000000',
                       '17': '2017000000',
                       '18': '2018000000',
                       '': ''}  # 單輸入空字串可

    jobcategory_mid_index = [jobcategory_lib[i] for i in jobcategory_input.split(',') if
                             i in jobcategory_lib and i != '7']

    job7_lib = {
        '7.0.0': '2007000000',  # shift tab
        '7.1.0': '2007001000',
        '7.1.1': '2007001001',
        '7.1.2': '2007001002',
        '7.1.3': '2007001003',
        '7.1.4': '2007001004',
        '7.1.5': '2007001005',
        '7.1.6': '2007001006',
        '7.1.7': '2007001007',
        '7.1.8': '2007001008',
        '7.1.9': '2007001009',
        '7.1.10': '2007001010',
        '7.1.11': '2007001011',
        '7.1.12': '2007001012',
        '7.2.0': '2007002000',
        '7.2.1': '2007002001',
        '7.2.2': '2007002002',
        '7.2.3': '2007002003',
        '7.2.4': '2007002004',
        '7.2.5': '2007002005',
        '7.2.6': '2007002006',
        '7.2.7': '2007002007',
        '7.2.8': '2007002008',  # 空字串不可
    }

    if job7_or_not == 1:
        job7_mid_index = [job7_lib[i] for i in job7_input.split(',') if i in job7_lib]  # 至少不會噴error
        jobcategory_mid_index.extend(job7_mid_index)
    jobcategory_output = '%2C'.join(jobcategory_mid_index)

    return jobcategory_output


def get_head_list(Default, All, head_dic):
    if column == "1":
        output_column = Default
    else:
        output_column = All

    head_list = []
    for i in output_column:
        head_list.append(head_dic[i])

    return head_list


# 利用url取得網頁原始碼,並用beautiful soup進行解析
def load_web(url, head):
    # 增加sleep time防止被ban的機率
    time.sleep(random.uniform(0, 2))
    # 送出request取得網頁原始碼
    web_res = requests.get(url, headers=head)
    web_res.encoding = 'utf8'
    # 將網頁原始碼用beautiful soup進行解析
    web_bs = bs(web_res.text, 'html.parser')
    return web_bs


def writeline(array):
    def transfer(array):
        t1 = '"' + array[0] + '"'
        for i in range(1, len(array)):
            t1 = t1 + ',"' + array[i] + '"'
        return t1

    t2 = transfer(array)
    for i in range(len(t2)):
        try:
            t2[i].encode('cp950').decode('cp950')
        except:
            tmp = list(t2)
            tmp[i] = " "
            t2 = ''.join(tmp)
    return t2


def get_all_page(beautifulsoup_text):
    page = beautifulsoup_text.select('.next_page')[0]
    tt = page.text.replace('\t', '').split('\n')
    num = tt[1].split()
    allpage = int(num[3])
    return allpage


class job_class(object):

    def __init__(self, joblist):
        # 抓出'職務名稱'欄位的文字內容(做法是搜尋全部欄位中,第0個具有超連結的欄位,並抓出該欄位的內容)
        self.job_name = joblist.select('a')[0]['title']
        # 抓出'公司名稱'欄位的文字內容(做法是搜尋全部欄位中,第1個具有超連結的欄位,並抓出該欄位的內容)
        self.com_name = joblist.select('a')[1]['title']
        # 抓出'學歷'欄位的文字內容
        self.edu = joblist.select('.edu')[0].text.replace('\t', '').replace('\r\n', '')
        # 抓出'地區'欄位的文字內容
        # self.area = joblist.select('.area')[0].text.replace('\t','').replace('\r\n','')
        # 抓出'應徵人數'欄位的文字內容
        self.num = joblist.select('.candidates')[0].select('a')[0]['title'][8:]
        # 取得'職務名稱'欄位的url
        self.job_url = "https://www.104.com.tw" + joblist.select('a')[0]['href']
        # 取得'公司名稱'欄位的url
        self.com_url = "https://www.104.com.tw" + joblist.select('a')[1]['href']

        self.ban1 = 0
        self.ban2 = 0

    def load_job_info(self):

        # 將每列"職務名稱"的url丟進BeautifulSoup做解析
        job_web_bs = load_web(self.job_url, "")

        # 判斷是否被ban(被ban後會被導向有"modal-body"元素的網頁),若是則重送request
        if (len(job_web_bs.select('.modal-body')) != 0):
            self.ban1 = "False"
            # print("ban")
            time.sleep(10)
            return self.load_job_info()

        else:
            # job_info的架構{職務類別:xx工程師}
            job_info = {}
            # 抓出第i個section:'工作內容','條件要求'
            for i in range(2):
                main_info = job_web_bs.select('section')[i]

                # 抓出第j個dt:'工作說明','職務類別'...
                for j in range(len(main_info.select('dt'))):
                    title = main_info.select('dt')[j].text.replace('\r', '').replace('\t', '').replace('：', '')
                    explanation = main_info.select('dd')[j].text.replace(' ', '').replace('\n', '')

                    # 公司地址去掉"地圖找工作"
                    if '地圖找工作' in explanation:
                        explanation = explanation[0:-5]
                    # 工作待遇若有出現"待遇面議"的字眼,僅保留這四個字
                    if '待遇面議' in explanation:
                        explanation = explanation[0:4]

                    job_info[title] = explanation

            self.ban1 = "True"
            return job_info

    def load_com_info(self):

        # 將每列"公司名稱"的url丟進BeautifulSoup做解析
        com_web_bs = load_web(self.com_url, "")

        if (len(com_web_bs.select('.modal-body')) != 0):
            self.ban2 = "False"
            # print("ban")
            time.sleep(10)
            return self.load_com_info()

        else:
            # com_info的架構{產業類別:軟體}
            com_info = {}
            # 抓出第0個intro:'公司介紹'
            main_info = com_web_bs.select('#cont_main')[0].select('.intro')[0]

            # 抓出第j個dt:'產業類別','產業描述'...
            for j in range(len(main_info.select('dt'))):
                title = main_info.select('dt')[j].text.replace('\u3000', '').replace('：', '')
                explanation = main_info.select('dd')[j].text.replace('\r', '').replace('\n', '')
                com_info[title] = explanation

            self.ban2 = "True"
            return com_info


def load_104_newpeople_main(search_url, filename='./crawler.csv'):
    print('write to file ', filename)

    # 輸出之職務欄位
    job_head_list = get_head_list(job_Default, job_All, job_head_dic)
    # 輸出之公司欄位
    com_head_list = get_head_list(com_Default, com_All, com_head_dic)
    # 輸出之104新鮮人網頁的欄位+職務欄位+公司欄位
    all_head_list = ['編號', '職務名稱', '公司名稱', '學歷', '兩週內應徵人數']

    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'}

    # 職務編號
    seq = 1

    for i in job_head_list:
        all_head_list.append(i)
    for i in com_head_list:
        all_head_list.append(i)

    all_head_list.append("職務連結")

    # 將上面自己定義(all_head)的標題匯入excel
    fw = open(filename, 'w')
    t2 = writeline(all_head_list)
    fw.writelines(t2 + '\n')

    # 下載104新鮮人網頁,第1頁的資料
    soup = load_web(search_url, head)
    # 取得104新鮮人網頁的總頁數
    allpage = get_all_page(soup) + 1

    # 印出104新鮮人網頁,每一頁的url
    for page in range(1, allpage):

        if page == 1:
            print('page:', page)
            print(search_url)

        else:
            # 將第1頁的url,修改page="_"的部分,取得第2~n頁的url
            search_url = (
                        "https://www.104.com.tw/area/freshman/search?area=" + area_output + "&jobcategory=" + jobcategory_output +
                        "&keyword=" + keyword_input + "&page=" + str(page) + "&sortField=APPEAR_DATE&sortMode=DESC")

            # 下載104新鮮人網頁,第2~n頁的資料
            soup = load_web(search_url, "")
            print('page:', page)
            print(search_url)

        # 抓出第1~n頁,職務列表的內容
        job_box = soup.select(".job_box")[0]

        # 抓出第1~20列的內容
        for joblis in job_box.select('.joblist_cont'):
            job = job_class(joblis)
            print(job.job_name)

            # 搜尋每列"職務名稱"的url中,職務內容
            job_info = job.load_job_info()
            # 搜尋每列"公司名稱"的url中,公司內容
            com_info = job.load_com_info()

            once_data = []
            once_data.append(str(seq))
            once_data.append(job.job_name)
            once_data.append(job.com_name)
            once_data.append(job.edu)
            # once_data.append(job.area)
            once_data.append(job.num)
            # print(job.num)

            # job
            for i in job_head_list:
                try:
                    once_data.append(job_info[i])

                except:
                    once_data.append('')

            # company
            for i in com_head_list:
                try:
                    once_data.append(com_info[i])
                except:
                    once_data.append('')

            once_data.append(job.job_url)

            # do wl
            t2 = writeline(once_data)
            fw.writelines(t2 + '\n')

            seq += 1
            # break

    fw.close()
    print('output file succesful')
    return 'succesful'


def gmap():
    gmaps.configure(api_key="AIzaSyABbkTh3c7pQEVIIaLRHdLPtkuVjeWU9Oc")
    geolocator = GoogleV3(api_key="AIzaSyABbkTh3c7pQEVIIaLRHdLPtkuVjeWU9Oc")

    # 開啟CSV讀首行參數
    with open(selection_file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, rows in enumerate(reader):
            if i == 0:
                row = rows

    # 開啟CSV 讀編號
    with open(selection_file_name, newline='') as csvFile:
        reader = csv.reader(csvFile)
        number_index = row.index('編號')
        cloumn_number = [row[number_index] for row in reader]

    # 開啟CSV 讀地址
    with open(selection_file_name, newline='') as csvFile:
        reader = csv.reader(csvFile)
        address_index = row.index('上班地點')
        cloumn_address = [row[address_index] for row in reader]

    # 開啟CSV讀職務名稱
    with open(selection_file_name, newline='') as csvFile:
        reader = csv.reader(csvFile)
        jobname_index = row.index('職務名稱')
        cloumn_jobname = [row[jobname_index] for row in reader]

    # 開啟CSV讀公司名稱
    with open(selection_file_name, newline='') as csvFile:
        reader = csv.reader(csvFile)
        comname_index = row.index('公司名稱')
        cloumn_jobcompany = [row[comname_index] for row in reader]

        # 開啟CSV讀職務連結
    with open(selection_file_name, newline='') as csvFile:
        reader = csv.reader(csvFile)
        joburl_index = row.index('職務連結')
        cloumn_joburl = [row[joburl_index] for row in reader]

        # 住家地址轉經緯度
    print('住家地址')
    home = geolocator.geocode(str(input()))
    home_lat, home_lon = home.latitude, home.longitude
    home_address = []
    home_address.append((home_lat, home_lon))

    # 將地址轉成經緯度
    locations = []
    loc_lon_lis = []
    for i in range(1, len(cloumn_address)):
        location = geolocator.geocode(cloumn_address[i])
        loc_lat, loc_lon = location.latitude, location.longitude
        if loc_lon in loc_lon_lis:
            while loc_lon in loc_lon_lis:
                loc_lon = loc_lon * 1.0000015
            loc_lon_lis.append(loc_lon)
        else:
            loc_lon_lis.append(loc_lon)
        locations.append([loc_lat, loc_lon])

    # 創立joblist存marker資訊
    joblist = []
    dict1 = {}
    for i in range(1, len(cloumn_address)):
        dict1['編號'] = cloumn_number[i]
        dict1['職務名稱'] = cloumn_jobname[i]
        dict1['地址'] = cloumn_address[i]
        dict1['公司名稱'] = cloumn_jobcompany[i]
        dict1['職務連結'] = cloumn_joburl[i]
        joblist.append(dict1)
        dict1 = {}

    # 將資訊轉成html格式
    info_box_template = """
    <dl>
    <dt>編號</dt><dd>{編號}</dd>
    <dt>職務名稱</dt><dd>{職務名稱}</dd>
    <dt>公司名稱</dt><dd>{公司名稱}</dd>
    <dt>地址</dt><dd>{地址}</dd>
    <a href="{職務連結}"target="_blank">職務連結</a>
    </dl>
    """
    # 建立hover text
    job_all_info = []
    jobname = '職缺名稱：'
    jobcompany = ' \n公司名稱：'
    for i in range(1, len(cloumn_address)):
        jobname += cloumn_jobname[i]
        jobcompany += cloumn_jobcompany[i]
        result = jobname + jobcompany
        job_all_info.append(result)
        jobname = '職缺名稱：'
        jobcompany = ' \n公司名稱：'
        result = ''

    # 將html分別放入每個職缺
    job_infobox = [info_box_template.format(**job) for job in joblist]

    # 畫座標資訊
    marker_layer = gmaps.marker_layer(locations, hover_text=job_all_info, info_box_content=job_infobox)
    global fig
    fig = gmaps.figure()
    fig.add_layer(marker_layer)
    symbols = gmaps.symbol_layer(home_address, fill_color='yellow', stroke_color='blue', scale=10)
    fig.add_layer(symbols)


def self_job_submit():
    def job_submit(i):
        driver = webdriver.Chrome()
        # 要投遞工作的網址
        driver.get(i)
        # 點投遞按鈕
        driver.find_element_by_id('applyJobBtn').click()
        # 輸入帳密
        driver.find_element_by_id('username').send_keys(job_submit_username)
        driver.find_element_by_id('password').send_keys(job_submit_password)
        # 登入
        driver.find_element_by_id('submitBtn').click()
        # 等待頁面加載完成
        driver.implicitly_wait(2)
        # 　改COVER LETTER
        driver.find_element_by_id('job_com_content').clear()
        driver.find_element_by_id('job_com_content').send_keys('拜託讓我進去QQQQQ')
        # 送出履歷
        driver.find_element_by_id('btSend').click()
        driver.close()

    if ("4" in Action):
        job_submit_file = crawler_file_name

    if ("3" in Action):
        job_submit_file = selection_file_name

    # 開啟CSV讀首行參數
    with open(job_submit_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, rows in enumerate(reader):
            if i == 0:
                row = rows
    with open(job_submit_file, newline='') as csvFile:
        reader = csv.reader(csvFile)
        joburl_index = row.index('職務連結')
        cloumn_joburl = [row[joburl_index] for row in reader]
    for i in cloumn_joburl[1:]:
        job_submit(i)


if __name__ == '__main__':
    global crawler_file_name, selection_file_name

    crawler_file_name = './crawler1.csv'
    selection_file_name = './selection1.csv'

    filename = crawler_file_name

    get_input_value()

    if ("1" in Action) or ("4" in Action):

        area_output = get_area()
        jobcategory_output = get_jobcategory()

        search_url = (
                    "https://www.104.com.tw/area/freshman/search?area=" + area_output + "&jobcategory=" + jobcategory_output +
                    "&keyword=" + keyword_input + "&page=1&sortField=APPEAR_DATE&sortMode=DESC")

        load_104_newpeople_main(search_url, filename)

        if ("4" in Action):
            self_job_submit()

    if ("2" in Action) or ("3" in Action):

        with open(crawler_file_name, newline='') as csvFile:  # 讀檔時會有編碼問題，要加encoding='big5'

            global csv_all
            reader = csv.reader(csvFile)
            # csv_all = [row for row in reader]
            # print(csv_all)

            csv_all = []
            job_column_list = []
            job_column_name = []

            i = 0
            for csv_row in reader:
                if i == 0:
                    job_column_name = csv_row
                    i += 1
                break

            job_column_list.append(job_column_name.index('編號'))
            job_column_list.append(job_column_name.index('職務名稱'))
            job_column_list.append(job_column_name.index('公司名稱'))
            job_column_list.append(job_column_name.index('上班地點'))
            job_column_list.append(job_column_name.index('職務連結'))
            csv_all.append(['編號', '職務名稱', '公司名稱', '上班地點', '職務連結'])

            if job_seq_method == "1":
                # csv_all = [csv_row for csv_row in reader]

                for csv_row in reader:
                    csv_all_column = []
                    for csv_column in job_column_list:
                        csv_all_column.append(csv_row[csv_column])
                    csv_all.append(csv_all_column)

            else:

                job_seq_list = [i for i in job_seq.split(",")]

                if job_seq_method == "2":
                    for csv_row in reader:
                        if (csv_row[0] in job_seq_list):
                            csv_all_column = []
                            for csv_column in job_column_list:
                                csv_all_column.append(csv_row[csv_column])
                            csv_all.append(csv_all_column)

                if job_seq_method == "3":
                    for csv_row in reader:
                        if (csv_row[0] not in job_seq_list):
                            csv_all_column = []
                            for csv_column in job_column_list:
                                csv_all_column.append(csv_row[csv_column])
                            csv_all.append(csv_all_column)

            # print(csv_all)

        with open(selection_file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in csv_all:
                writer.writerow(row)

        if "2" in Action:
            gmap()

        if "3" in Action:
            self_job_submit()

fig