import os

from flask import Flask, render_template, request

app = Flask(__name__, static_folder='')


def save_file(text):
    with open('code/upload.c', 'w', encoding='UTF-8') as f:
        f.write(text)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/get_table', methods=["GET"])
def get_table():
    from src.get_predict_table import show_tables
    result = show_tables()
    return result


# @app.route('/get_generate', methods=["GET"])
# def get_generate():
#     from src.generate import get_generate
#     text = request.args.get('message')
#     save_file(text)
#     result = get_generate()
#     return result


@app.route('/get_lexer', methods=["GET"])
def get_lexer():
    text = request.args.get('message')
    save_file(text)
    from src.lexer import get_lexer
    result = get_lexer()
    return result


@app.route('/get_lr', methods=["GET"])
def get_lr_index():
    text = request.args.get('message')
    save_file(text)
    from src.LR import get_lr
    result = get_lr()
    return result


@app.route('/get_asm', methods=["GET"])
def get_asm_index():
    text = request.args.get('message')
    save_file(text)
    from src.to_asm import get_asm
    result = get_asm()
    return result


@app.route('/run', methods=["GET"])
def run_index():
    text = request.args.get('message')
    save_file(text)
    from src.main import run
    result = run()
    return result


@app.route('/download_url', methods=["GET"])
def download_url_index():
    text = request.args.get('message')
    save_file(text)
    from src.main import zipfiles
    zipfiles()
    return '/code/download.tar'


@app.route('/download', methods=["GET"])
def download_index():
    text = request.args.get('message')
    save_file(text)
    from src.main import zipfiles
    zipfiles()
    dirpath = 'code'
    from flask import send_from_directory
    return send_from_directory(dirpath, 'download.tar', as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
