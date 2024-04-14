from flask import Flask, jsonify, request
import markdown
import json
from bs4 import BeautifulSoup

from .text_transfer_mind import *

app = Flask(__name__)

# jsonify({"code":"0", "msg":"操作成功", "data":data})

@app.route('/test')
def hello_world():
    return 'Hello, World!'

@app.route("/add_task", methods=["GET", "POST"])
def add_user_task():
    inp = request.get_json()
    try:
        token = inp["token"]
        user = inp["user"]
        text = inp["text"]
        task = inp["task"]
    except Exception as e:
        return jsonify({"ret":"-1", "data":"", "msg": e})

    if token != "fighting":
        return jsonify({"ret":"-1", "data":"", "msg":"error auth!"})
    
    return jsonify({"ret":"0", "data": inp, "msg":"test success!"})

@app.route('/gen_mind', methods=["GET", "POST"])
def gen_text_mind():
    inp = request.get_json()
    try:
        token = inp["token"]
        user = inp["user"]
        text = inp["text"]
        task = inp["task"]
    except Exception as e:
        return jsonify({"ret":"-1", "data":"", "msg": e})

    if token != "fighting":
        return jsonify({"ret":"-1", "data":"", "msg":"error auth!"})
    
    mind_txt, cost = text_to_mind(inp["text"])

    # 将Markdown文本转换为HTML
    html = markdown.markdown(mind_txt)

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 将HTML解析为JSON
    json_data = []
    for tag in soup.find_all():
        json_data.append({
            'tag': tag.name,
            'text': tag.text,
            'attrs': tag.attrs,
        })

    # 将JSON数据转换为字符串
    json_str = json.dumps(json_data, indent=4)

    return jsonify({"ret":"0", "data": json_str, f"msg":"gen success! cost: {cost}"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8501")
