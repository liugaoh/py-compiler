import os

import app
from src.to_asm import to_asm


def run(show=True):
    if show:
        try:
            to_asm('code/upload.c')
            os.system("gcc " + 'code/upload.s ' + "-o " + 'code/upload')
            result = "编译成功，执行结果：\n"
            result += os.popen("code/upload").read()
            # print(result)
            return result
        except BaseException:
            return "\t编译失败！！！"
    else:
        try:
            to_asm('code/upload.c')
            os.system("gcc " + 'code/upload.s ' + "-o " + 'code/upload')
        except BaseException:
            pass


def zipfiles():
    run(show=False)
    import tarfile
    if os.path.exists("code/download.tar"):
        os.remove("code/download.tar")
    with tarfile.open('code/download.tar', 'w') as tar:
        tar.add('code/upload.c', arcname='upload.c')
        tar.add('code/upload.s', arcname='upload.s')
        tar.add('code/upload', arcname='upload')


def download():
    zipfiles()
    dirpath = 'code/'  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    from flask import send_from_directory
    # as_attachment=True 一定要写，不然会变成打开，而不是下载
    return send_from_directory(dirpath, 'download.tar', as_attachment=True)
