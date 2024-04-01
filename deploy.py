# -*- coding: utf-8 -*-
import os

from app.common.setting import DEBUG

if not DEBUG:
    deploy_command = 'nuitka --standalone --enable-plugin=pyside6 '
    deploy_command += '--include-package=sqlite3,http.cookies '
    deploy_command += '--windows-disable-console '
    deploy_command += '--msvc=latest '
    # deploy_command += '--mingw64 '
    deploy_command += '--show-memory --show-progress '
    deploy_command += '--windows-icon-from-ico=app/resource/images/logo.ico '
    deploy_command += '--output-dir=build '
    deploy_command += '--report=build/report.xml '
    deploy_command += 'jumbla.py'

    os.system(deploy_command)
else:
    print('DEBUG模式下不进行打包')
