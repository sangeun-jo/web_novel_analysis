from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import csv, boto3
import time
from datetime import datetime
from pytz import timezone 
from bs4 import BeautifulSoup 
import re


s3 = boto3.resource('s3')
bucket = s3.Bucket('web-novel-db')

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = "/opt/python/bin/headless-chromium"
    
    driver = webdriver.Chrome('/opt/python/bin/chromedriver', chrome_options=chrome_options)
    return driver

def tocsoda_tobe(category):
    
    driver = get_driver()
    driver.get('http://www.tocsoda.co.kr/totalBestView/' + category)
    
    time.sleep(1)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.select_one('#TOTAL_PRODUCT_LIST')
    
    titles = data.find_all('span', class_='txt')
    genres = data.find_all('span', class_='total')
    introes = data.find_all('p', class_='desc')
    
    if category == '00023':
        key = 'tocsoda-tobe-web.csv'
        local_file_name = '/tmp/tocsoda-tobe-web.csv'
    else:
        key = 'tocsoda-tobe-free.csv'
        local_file_name = '/tmp/tocsoda-tobe-free.csv'
    bucket.download_file(key, local_file_name)
    date = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
    
    for title, genre,intro  in zip(titles, genres, introes):
        title = title.text.strip()
        genre = re.search(r'\[(.*?)\]', genre.text).group() 
        intro = intro.text
        
        book_info = [date, title, genre, intro]

        f = open(local_file_name, 'a',  encoding='utf-8-sig', newline='')
        wr = csv.writer(f)
        wr.writerow(book_info)
        f.close()
        
    bucket.upload_file(local_file_name, key)
    
    driver.close()

def lambda_handler(event, context): 
    tocsoda_tobe('00023')
    tocsoda_tobe('00024')