from flask import Flask, jsonify, request

from backend_algo import *

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
    return jsonify({"ret":"0", "data": mind_txt, f"msg":"gen success! cost: {cost}"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8501")
