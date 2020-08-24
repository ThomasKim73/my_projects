from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbmarket  # 'dbmarket'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('market.html')


## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    # salesdate_receive로 클라이언트가 준 title 가져오기
    salesdate_receive = request.form['salesdate_give']
    # soldto_receive로 클라이언트가 준 author 가져오기
    soldto_receive = request.form['soldto_give']
    # review_receive로 클라이언트가 준 review 가져오기
    type_receive = request.form['type_give']
    # review_receive로 클라이언트가 준 review 가져오기
    price_receive = request.form['price_give']
    # review_receive로 클라이언트가 준 review 가져오기
    comments_receive = request.form['comments_give']

    # DB에 삽입할 review 만들기
    review = {
        'salesdate': salesdate_receive,
        'soldto': soldto_receive,
        'type': type_receive,
        'price': price_receive,
        'comments': comments_receive
    }
    # reviews에 review 저장하기
    db.reviews.insert_one(review)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '시장조사가 성공적으로 작성되었습니다.'})


@app.route('/review', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.reviews.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews})


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)