import os
import atexit
import importlib.resources as pkg_resources
from ctypes import windll, wintypes, POINTER, c_bool, c_uint, c_ushort, c_char_p, c_void_p, c_byte
from sys import maxsize

from .ipathelper import *
from .ipathelper import ST_PURCHASE_DATA_INTERNAL
import ipathelper.ipathelper as _core


def _get_dll_path():
    '''
        アーキテクチャに応じたDLLのパスを取得する。
        インストール済み環境・ソースからの実行どちらでも動作する。
    '''
    arch = "x64" if maxsize > 2 ** 32 else "x86"
    dll_name = "IpatHelper.dll"

    try:
        ref = pkg_resources.files("ipathelper") / arch / dll_name
        with pkg_resources.as_file(ref) as dll_path:
            return str(dll_path)
    except (TypeError, FileNotFoundError, ModuleNotFoundError):
        pass

    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, arch, dll_name)


def _init():
    '''
        モジュールのイニシャライズ（import時に自動実行）
    '''
    dll_path = _get_dll_path()

    if not os.path.exists(dll_path):
        return False

    _core.lib = windll.LoadLibrary(dll_path)

    _core.lib.Login.restype = c_uint
    _core.lib.Login.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]

    _core.lib.Logout.restype = c_uint
    _core.lib.Logout.argtypes = []

    _core.lib.Deposit.restype = c_uint
    _core.lib.Deposit.argtypes = [c_uint, c_ushort]

    _core.lib.Withdraw.restype = c_uint
    _core.lib.Withdraw.argtypes = [c_ushort]

    _core.lib.GetPurchaseData.restype = c_uint
    _core.lib.GetPurchaseData.argtypes = [c_void_p]

    _core.lib.ReleasePurchaseData.restype = None
    _core.lib.ReleasePurchaseData.argtypes = [POINTER(ST_PURCHASE_DATA_INTERNAL)]

    _core.lib.GetBetInstance.restype = c_uint
    _core.lib.GetBetInstance.argtypes = [c_byte, c_byte, c_ushort, c_byte, c_byte, c_byte, c_byte, c_uint, c_char_p, c_void_p]

    _core.lib.Bet.restype = c_uint
    _core.lib.Bet.argtypes = [c_void_p, c_ushort, c_ushort]

    _core.lib.GetBetInstanceWin5.restype = c_uint
    _core.lib.GetBetInstanceWin5.argtypes = [c_uint, c_ushort, c_byte, c_byte, c_char_p, c_void_p]

    _core.lib.BetWin5.restype = c_uint
    _core.lib.BetWin5.argtypes = [c_void_p, c_ushort]

    _core.lib.SetAutoDepositFlag.restype = c_uint
    _core.lib.SetAutoDepositFlag.argtypes = [c_bool, c_ushort, c_ushort]

    if maxsize > 2 ** 32:
        windll.kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]

    return True


def _uninit():
    '''
        モジュールのファイナライズ（プログラム終了時に自動実行）
    '''
    if _core.lib is None:
        return

    libraryHandle = _core.lib._handle
    del _core.lib
    _core.lib = None

    windll.kernel32.FreeLibrary(libraryHandle)


# import時にDLLを自動ロード
_init()

# プログラム終了時にDLLを自動アンロード
atexit.register(_uninit)
