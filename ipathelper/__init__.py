import os
import atexit
import importlib.resources as pkg_resources
from ctypes import windll, wintypes, POINTER, c_bool, c_uint, c_ushort, c_char_p, c_void_p, c_byte, c_long
from sys import maxsize

from .ipathelper import (
    # 定数: 開催場
    KAISAI_SAPPORO, KAISAI_HAKODATE, KAISAI_FUKUSHIMA, KAISAI_NIIGATA,
    KAISAI_TOKYO, KAISAI_NAKAYAMA, KAISAI_CHUKYO, KAISAI_KYOTO,
    KAISAI_HANSHIN, KAISAI_KOKURA, KAISAI_SONODA, KAISAI_HIMEJI,
    KAISAI_NAGOYA, KAISAI_MONBETSU, KAISAI_MORIOKA, KAISAI_MIZUSAWA,
    KAISAI_URAWA, KAISAI_FUNABASHI, KAISAI_OI, KAISAI_KAWASAKI,
    KAISAI_KASAMATSU, KAISAI_KANAZAWA, KAISAI_KOCHI, KAISAI_SAGA,
    KAISAI_LONGCHAMP, KAISAI_SHATIN, KAISAI_SANTAANITA, KAISAI_DEAUVILE,
    KAISAI_CHURCHILLDOWNS, KAISAI_ABDULAZIZ,
    # 定数: 方式
    HOUSHIKI_NORMAL, HOUSHIKI_FORMATION, HOUSHIKI_BOX,
    # 定数: 式別
    SHIKIBETSU_WIN, SHIKIBETSU_PLACE, SHIKIBETSU_BRACKETQUINELLA,
    SHIKIBETSU_QUINELLAPLACE, SHIKIBETSU_QUINELLA, SHIKIBETSU_EXACTA,
    SHIKIBETSU_TRIO, SHIKIBETSU_TRIFECTA,
    # 定数: その他
    DAYTYPE_TODAY, DAYTYPE_BEFORE,
    BETFLAG_NORMAL, BETFLAG_WIN5, BETFLAG_INTERNAL,
    DECISIONFLAG_DEFAULT, DECISIONFLAG_NORMAL, DECISIONFLAG_DEADLINE,
    DECISIONFLAG_CANCEL, DECISIONFLAG_FLATMATESCANCEL, DECISIONFLAG_HIT,
    DECISIONFLAG_MISS, DECISIONFLAG_BACK, DECISIONFLAG_PARTCANCEL,
    DECISIONFLAG_INVALID, DECISIONFLAG_SALECANCEL,
    WEEKDAY_SUNDAY, WEEKDAY_MONDAY, WEEKDAY_TUESDAY, WEEKDAY_WEDNESDAY,
    WEEKDAY_THURSDAY, WEEKDAY_FRIDAY, WEEKDAY_SATURDAY,
    SUCCESS, UNSUCCESS, FAILED_CHUOU, FAILED_CHIHOU,
    FAILED_COMMUNICATE_CHUOU, FAILED_COMMUNICATE_CHIHOU,
    DEFAULT_RETRY_COUNT,
    # クラス
    ST_TICKET_DATA, ST_PURCHASE_DATA,
    ST_TICKET_DATA_DETAIL, ST_TICKET_DATA_INTERNAL,
    ST_PURCHASE_DATA_INTERNAL, ST_BET_DATA, ST_BET_DATA_WIN5,
    # 関数
    login, logout, deposit, withdraw, get_purchase_data,
    get_bet_instance, get_bet_instance_win5, bet, bet_win5,
    set_auto_deposit_flag,
)
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
