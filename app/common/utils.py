# -*- coding: utf-8 -*-
import enum
import subprocess
from types import TracebackType
from typing import Type

from .logger import Logger

JBLLogger = Logger()


class ExceptionFilterMode(enum.Enum):
    RAISE_AND_PRINT = enum.auto()  # 过滤：弹框提示，也会抛出异常
    RAISE = enum.auto()  # 过滤：不弹框提示，但是会抛出异常
    PASS = enum.auto()  # 过滤：不弹框提示，也不抛出异常，就当做什么都没发生
    SILENT = enum.auto()  # 过滤：不弹框提示，也不抛出异常，就当做什么都没发生


def exceptionFilter(
        ty: Type[BaseException], value: BaseException, _traceback: TracebackType
) -> ExceptionFilterMode:
    """
    过滤异常
    """
    if isinstance(value, AttributeError) and "MessageBox" in str(value):
        return ExceptionFilterMode.SILENT
    if isinstance(value, RuntimeError) and "wrapped C/C++ object of type" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "raise test" in str(value):
        return ExceptionFilterMode.RAISE
    if isinstance(value, Exception) and "pass test" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "print test" in str(value):
        return ExceptionFilterMode.RAISE_AND_PRINT
    if isinstance(
            value, Exception
    ) and "RunningServerHeaderCardWidget cannot be converted to PyQt5.QtWidgets.QLayoutItem" in str(
        value
    ):
        return ExceptionFilterMode.SILENT
    if isinstance(value, Exception) and "sipBadCatcherResult" in str(value):
        return ExceptionFilterMode.SILENT

    return ExceptionFilterMode.RAISE_AND_PRINT


def svn_usd_update(svn_url, local_path):
    """
    检出USD仓库
    """
    try:
        cmd = ['svn', 'checkout', svn_url, local_path]
        r = subprocess.Popen(cmd, universal_newlines=True, bufsize=1, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        JBLLogger.info(r.stdout.read())
    except subprocess.CalledProcessError as e:
        JBLLogger.error(f"USD checkout error: {e}")
