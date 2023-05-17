import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
ca = certifi.where()

client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.1v14zkv.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/members", methods=["POST"])
def members_post():
    name_receive = request.form['name_give']
    image_receive = request.form['image_give']
    blog_receive = request.form['blog_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name': name_receive,
        'image': image_receive,
        'blog': blog_receive,
        'comment': comment_receive
    }
    db.members.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/members", methods=["GET"])
def member_get():
    all_members = list(db.members.find({},{'_id':False}))
    return jsonify({'result': all_members})

@app.route('/members/memberid', methods=['POST'])
def delete_member():
    data = request.json
    name_receive = data['name_give']
    db.members.delete_one({'name': name_receive})
    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
