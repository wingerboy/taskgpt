from flask import Flask, jsonify, request
import markdown
import json
from bs4 import BeautifulSoup

from text_transfer_mind import *

import logging
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)

# jsonify({"code":"0", "msg":"操作成功", "data":data})
def app_log_debug(user, req=None, text=""):
    app.logger.debug(f"USER: {user}, REQ: {req}, info: {text}")

def app_log_info(user, req=None, text=""):
    app.logger.info(f"USER: {user}, REQ: {req}, info: {text}")

def app_log_error(user, req=None, text=""):
    app.logger.error(f"USER: {user}, REQ: {req}, info: {text}")
    

@app.route('/test')
def hello_world():
    return 'Hello, World!'

@app.route("/add_task", methods=["GET", "POST"])
def add_user_task():
    inp = request.get_json()
    app_log_info(inp["user"], inp, "request add_task")
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
    app_log_info(inp["user"], inp, "request gen_mind")
    try:
        token = inp["token"]
        user = inp["user"]
        text = inp["text"]
        task = inp["task"]
    except Exception as e:
        app_log_error(inp["user"], inp, f"Param Exception>>>{e}")
        return jsonify({"ret":"-1", "data":"", "msg": e})

    if token != "fighting":
        app_log_error(inp["user"], inp, "Error Auth")
        return jsonify({"ret":"-1", "data":"", "msg":"error auth!"})

    try:
        mind_txt, cost = text_to_mind(inp["text"])
        app_log_info(inp["user"], inp, f"cost: {cost}, output: {mind_txt}")
    except OpenAIException as e:
        app_log_error(inp["user"], inp, f"OpenAIException>>>{e}")

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
