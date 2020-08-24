# 라이브러리 imports
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient             # pymongo를 임포트 하기(패키지 설치 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)    # mongoDB는 27017 포트로 돌아갑니다.
db = client.wholesaleprice                  # 'wholesaleprice'라는 이름의 db를 사용합니다. 'wholesaleprice' db가 없다면 새로 만듭니다.


# 타겟 URL을 읽어서 HTML 받아옴
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://aglook.krei.re.kr/jsp/pc/front/trend/priceTrend17.jsp',headers=headers)

# HTML을 BeautifulSoup 라이브러리 활용 > 검색 용이한 상태
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')
# sdate = soup.select('body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > thead > tr > th')
wholesale = soup.select('body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table ')
#print(wholesale)

#############################
# 코딩 반복문 돌리기
#############################
for bprice in wholesale:
    salesdate = bprice.select_one('thead > tr').text
    salesvolumn = bprice.select_one('tbody > tr:nth-child(1) ').text
    wholesaleprice1 = bprice.select_one('tbody > tr:nth-child(2) ').text.strip()
    wholesaleprice2 = bprice.select_one('tbody > tr:nth-child(3) ').text.strip()
    wholesaleprice3 = bprice.select_one('tbody > tr:nth-child(4) ').text.strip()
    wholesaleprice4 = bprice.select_one('tbody > tr:nth-child(5) ').text.strip()

    doc = {
        'salesdate' :salesdate,
        'salesvolumn': salesvolumn,
        'wholesaleprice1' : wholesaleprice1,
        'wholesaleprice2': wholesaleprice2,
        'wholesaleprice3': wholesaleprice3,
        'wholesaleprice4': wholesaleprice4,
    }
    db.wholesaleprice.insert_one(doc)
    print(salesdate, salesvolumn, wholesaleprice1, wholesaleprice2, wholesaleprice3, wholesaleprice4)


#############################
# 사이트 분석 - copy selector
#############################
# web site address - 농업관측본부 바나나 도매가격
# http://aglook.krei.re.kr/jsp/pc/front/trend/priceTrend17.jsp
# salesdate
# body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > thead > tr > th:nth-child(2)
# wholesaleprice
# body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > tbody > tr:nth-child(2) > td:nth-child(2) > span


#############################
# body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > thead > tr > th:nth-child(2)
# body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > thead > tr > th:nth-child(3)
#.........................
# body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > thead > tr > th:nth-child(10)
#############################
#body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span


# body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > tbody > tr:nth-child(2) > td:nth-child(2) > span
# body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > tbody > tr:nth-child(2) > td:nth-child(3) > span
# body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > tbody > tr:nth-child(2) > td:nth-child(4) > span
#.........................
# body > section > article.content_right > article > article > article.sub_content > section:nth-child(12) > table > tbody > tr:nth-child(2) > td:nth-child(10) > span
#############################

