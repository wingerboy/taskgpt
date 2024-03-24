from flask import Flask, jsonify, request

app = Flask(__name__)

# jsonify({"code":"0", "msg":"操作成功", "data":data})

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/test", methods=["GET"])
def get_all_users():
    """获取所有用户信息"""
    return jsonify({"ret":"0", "data":data, "msg":"测试test成功"})

@app.route('/process', methods=["GET", "POST"])
def process_data():
  # 请求方式为post时，可以使用 request.get_json()接收到JSON数据
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    resp = {"ret":"0", "data":data, "msg":"测试process成功"}

    # 请求方得到处理后的数据
    return jsonify(resp)


if __name__ == '__main__':
    app.run()
