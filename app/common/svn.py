# -*- coding: utf-8 -*-
import os
import subprocess
from PySide6.QtCore import QThread, Signal
from app.common.utils import JBLLogger
from app.common.setting import SVN_SETTINGS


class SVN:
    @staticmethod
    def checkout(url, path):
        cmd = f'svn checkout {url} {path}'
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        JBLLogger.info(result.stdout)
        if result.stderr:
            JBLLogger.error(result.stderr)

    @staticmethod
    def update(path):
        if not os.path.isdir(path):
            print(f'路径 {path} 不存在，无法更新，请检出')
            return
        cmd = f'svn update {path}'
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        JBLLogger.info(result.stdout)
        if result.stderr:
            JBLLogger.error(result.stderr)


if __name__ == '__main__':
    # for setting in SVN_SETTINGS:
    #     function_name = setting[0]
    #     args = setting[1:]
    #     getattr(SVN, function_name)(*args)
    # print('IT' in SVN_SETTINGS['department'])
    SVN.update('d:/1123')
