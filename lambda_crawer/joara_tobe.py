import csv
import boto3
from datetime import datetime
from pytz import timezone 
import urllib.request 
from bs4 import BeautifulSoup 

s3 = boto3.resource('s3')
bucket = s3.Bucket('web-novel-db')
key = 'joara-tobe.csv'


def lambda_handler(event, context): 

    url = "http://www.joara.com/best/today_best_list.html?page_no=1&sl_subcategory=all" 
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser") 
    book_list = soup.find_all('td', class_='book_data_intro_form subject_long')
    
    local_file_name = '/tmp/joara-tobe.csv'
    bucket.download_file(key, local_file_name)
    
    date = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')

    for book in book_list:
        try:
            genre = book.strong.text
            title = book.a.text.replace(genre, '').strip()
            intro = book.span.text
        except:
            genre = 'failed'
            title = ''
            intro = book
        
        book_info = [date, genre,title, intro] 

        f = open(local_file_name, 'a',  encoding='utf-8-sig', newline='')
        wr = csv.writer(f)
        wr.writerow(book_info)
        f.close()
        
    bucket.upload_file(local_file_name, key)