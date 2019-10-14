# -*- coding: utf-8 -*-
import requests
import zipfile
import os
from parse_pdf import parse_pdf
from flask import Flask, abort, request, jsonify

app = Flask(__name__)


def get_report(sid):
    ''' 解析准考证文件 pdf，提取准考证号码 '''
    res = requests.session().get(f"http://cet-bm.neea.edu.cn/Home/DownTestTicket?SID={sid}")
    with open(sid, "wb") as f:
        f.write(res.content)

    with zipfile.ZipFile(sid, "r") as zipf:
        for names in zipf.namelist():
            # print(names.encode('cp437').decode('gbk'))
            pdf_file = f"./data_file/{names.encode('cp437').decode('gbk')}"
            data = zipf.read(names)
            with open(pdf_file, "wb") as f:
                f.write(data)

            return parse_pdf(pdf_file)


@app.errorhandler(400)
def error(e):
    return jsonify({'status': 0, 'msg': str(e)})


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'status': 0, 'msg': str(e)})


@app.route('/<sid>')
def index(sid):
    data = get_report(sid)
    if (os.path.exists(sid)):
        os.remove(sid)

    return jsonify({'status': 1, 'msg': 'success', 'data': data})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8890)
    app.debug = True
