from ctypes import *

lib = None

KAISAI_SAPPORO = 0
KAISAI_HAKODATE = 1
KAISAI_FUKUSHIMA = 2
KAISAI_NIIGATA = 3
KAISAI_TOKYO = 4
KAISAI_NAKAYAMA = 5
KAISAI_CHUKYO = 6
KAISAI_KYOTO = 7
KAISAI_HANSHIN = 8
KAISAI_KOKURA = 9

KAISAI_SONODA = 10
KAISAI_HIMEJI = 11
KAISAI_NAGOYA = 12
KAISAI_MONBETSU	= 13
KAISAI_MORIOKA = 14
KAISAI_MIZUSAWA	= 15
KAISAI_URAWA = 16
KAISAI_FUNABASHI = 17
KAISAI_OI = 18
KAISAI_KAWASAKI	= 19
KAISAI_KASAMATSU = 20
KAISAI_KANAZAWA	= 21
KAISAI_KOCHI = 22
KAISAI_SAGA = 23
KAISAI_LONGCHAMP = 24
KAISAI_SHATIN = 25
KAISAI_SANTAANITA = 26
KAISAI_DEAUVILE = 27
KAISAI_CHURCHILLDOWNS = 28
KAISAI_ABDULAZIZ = 29

HOUSHIKI_NORMAL = 0
HOUSHIKI_FORMATION = 1
HOUSHIKI_BOX = 2

SHIKIBETSU_WIN = 1
SHIKIBETSU_PLACE = 	2
SHIKIBETSU_BRACKETQUINELLA = 3
SHIKIBETSU_QUINELLAPLACE = 4
SHIKIBETSU_QUINELLA	= 5
SHIKIBETSU_EXACTA = 6
SHIKIBETSU_TRIO	= 7
SHIKIBETSU_TRIFECTA	= 8

DAYTYPE_TODAY = 1
DAYTYPE_BEFORE = 2

BETFLAG_NORMAL = 1
BETFLAG_WIN5 = 2
BETFLAG_INTERNAL = 3

DECISIONFLAG_DEFAULT = 1
DECISIONFLAG_NORMAL = 2
DECISIONFLAG_DEADLINE = 3
DECISIONFLAG_CANCEL = 4
DECISIONFLAG_FLATMATESCANCEL = 5
DECISIONFLAG_HIT = 6
DECISIONFLAG_MISS = 7
DECISIONFLAG_BACK = 8
DECISIONFLAG_PARTCANCEL = 10
DECISIONFLAG_INVALID = 11
DECISIONFLAG_SALECANCEL = 12

WEEKDAY_SUNDAY = 1
WEEKDAY_MONDAY = 2
WEEKDAY_TUESDAY = 3
WEEKDAY_WEDNESDAY = 4
WEEKDAY_THURSDAY = 5
WEEKDAY_FRIDAY = 6
WEEKDAY_SATURDAY = 7

SUCCESS = 1
UNSUCCESS = 2
FAILED_CHUOU = 4
FAILED_CHIHOU = 8
FAILED_COMMUNICATE_CHUOU = 16
FAILED_COMMUNICATE_CHIHOU = 32

DEFAULT_RETRY_COUNT = 10
DEFAULT_WAIT_TIME = 1000
DEFAULT_CONFIRM_TIMEOUT = 10000

class ST_TICKET_DATA:
    def __init__(self):
        self.DayFlag = 0
        self.ReceiptNo = 0
        self.Hour = 0
        self.Minute = 0
        self.Kingaku = 0
        self.Payout = 0
        self.DetailCount = 0
        self.DetailData = []

class ST_PURCHASE_DATA:
    def __init__(self):
        self.AvailableBetCount = 0
        self.Balance = 0
        self.DayPurchase = 0
        self.DayHaraimodosi = 0
        self.TotalPurchase = 0
        self.TotalHaraimodosi = 0
        self.TicketCount = 0
        self.TicketData = []

#構造体マーシャリング用クラス
class ST_TICKET_DATA_DETAIL(Structure):
    _fields_ = [("DecisionFlag", c_byte), ("BetFlag", c_byte), ("Kaisai", c_ushort), ("RaceNo", c_byte), \
        ("Week", c_byte), ("Method", c_byte), ("Type", c_byte), ("HorseNo1", c_uint), \
        ("HorseNo2", c_uint), ("HorseNo3", c_uint), ("HorseNo4", c_uint), ("HorseNo5", c_uint), ("Multi", c_byte)]

class ST_TICKET_DATA_INTERNAL(Structure):
    _fields_ = [("DayFlag", c_byte), ("ReceiptNo", c_byte), ("Hour", c_byte), ("Minute", c_byte), \
        ("Kingaku", c_uint), ("Payout", c_uint), ("DetailCount", c_uint), ("DetailData", c_void_p)]

class ST_PURCHASE_DATA_INTERNAL(Structure):
    _fields_ = [("AvailableBetCount", c_ushort), ("Balance", c_uint), ("DayPurchase", c_uint),\
         ("DayHaraimodosi", c_uint), ("TotalPurchase", c_uint), ("TotalHaraimodosi", c_uint), ("TicketCount", c_uint), ("TicketData", c_void_p)]

class ST_BET_DATA(Structure):
    _fields_ = [("Place", c_ushort), ("RaceNo", c_byte), ("Youbi", c_byte), ("Kaikata", c_byte),\
         ("Shikibetsu", c_byte), ("Kingaku", c_uint), ("Umaban", c_uint * 3), ("TotalAmount", c_long)]

class ST_BET_DATA_WIN5(Structure):
    _fields_ = [("Kingaku", c_uint), ("Youbi", c_byte), ("Umaban", c_uint * 5)]


def login(iNetId : str, id : str, password : str, pars : str) -> int:
    '''
        ログイン処理実行
    '''
    return lib.Login(iNetId.encode('utf-8'), id.encode('utf-8'), password.encode('utf-8'), pars.encode('utf-8'))

def logout() -> int:
    '''
        ログアウト処理実行
    '''
    return lib.Logout()

def deposit(depositValue : int, retryCount : int = DEFAULT_RETRY_COUNT) -> int:
    '''
        入金処理実行
    '''
    return lib.Deposit(depositValue, retryCount)

def withdraw(retryCount : int = DEFAULT_RETRY_COUNT) -> int:
    '''
        出金処理実行
    '''
    return lib.Withdraw(retryCount)

def get_purchase_data(purchaseData : ST_PURCHASE_DATA) -> int:
    '''
        購入状況取得処理実行
    '''
    tempPurchaseData = ST_PURCHASE_DATA_INTERNAL()

    returnValue = lib.GetPurchaseData(byref(tempPurchaseData))
    if (returnValue & 1) != 1:
        return returnValue
    
    purchaseData.TicketCount = tempPurchaseData.TicketCount
    purchaseData.AvailableBetCount = tempPurchaseData.AvailableBetCount
    purchaseData.Balance = tempPurchaseData.Balance
    purchaseData.DayPurchase = tempPurchaseData.DayPurchase
    purchaseData.DayHaraimodosi = tempPurchaseData.DayHaraimodosi
    purchaseData.TotalPurchase = tempPurchaseData.TotalPurchase
    purchaseData.TotalHaraimodosi = tempPurchaseData.TotalHaraimodosi
    purchaseData.TicketCount = tempPurchaseData.TicketCount

    if tempPurchaseData.TicketCount <= 0:
        lib.ReleasePurchaseData(byref(tempPurchaseData))
        return returnValue

    allTicketBytes = bytearray(string_at(tempPurchaseData.TicketData, \
        sizeof(ST_TICKET_DATA_INTERNAL) * tempPurchaseData.TicketCount))
    
    for i in range(tempPurchaseData.TicketCount):
        oneTicketBytes = bytearray(sizeof(ST_TICKET_DATA_INTERNAL))
        for j in range(sizeof(ST_TICKET_DATA_INTERNAL)):   
            oneTicketBytes[j] = allTicketBytes[j + i * sizeof(ST_TICKET_DATA_INTERNAL)]

        oneTicketData = ST_TICKET_DATA_INTERNAL.from_buffer(oneTicketBytes, 0)
        tempTicketData = ST_TICKET_DATA()

        tempTicketData.DayFlag = oneTicketData.DayFlag
        tempTicketData.DetailCount = oneTicketData.DetailCount
        tempTicketData.Hour = oneTicketData.Hour
        tempTicketData.Minute = oneTicketData.Minute
        tempTicketData.Kingaku = oneTicketData.Kingaku
        tempTicketData.Payout = oneTicketData.Payout
        tempTicketData.ReceiptNo = oneTicketData.ReceiptNo

        if oneTicketData.DetailCount <= 0:
            lib.ReleasePurchaseData(byref(tempPurchaseData))
            return returnValue

        allDetailBytes = bytearray(string_at(oneTicketData.DetailData, \
            sizeof(ST_TICKET_DATA_DETAIL) * oneTicketData.DetailCount))

        for j in range(oneTicketData.DetailCount):
            oneDetailBytes = bytearray(sizeof(ST_TICKET_DATA_DETAIL))
            for k in range(sizeof(ST_TICKET_DATA_DETAIL)):
                oneDetailBytes[k] = allDetailBytes[k + j * sizeof(ST_TICKET_DATA_DETAIL)]

            tempTicketData.DetailData.append(ST_TICKET_DATA_DETAIL.from_buffer(oneDetailBytes, 0))
        
        purchaseData.TicketData.append(tempTicketData)
    
    lib.ReleasePurchaseData(byref(tempPurchaseData))

    return returnValue

def get_bet_instance(kaisai : int, raceNo : int, year : int, month : int, day : int, \
                    houshiki : int, shikibetsu : int, kingaku : int, kaime : str, betData : ST_BET_DATA) -> int:
    '''
        馬券購入用インスタンス取得処理
    '''
    return lib.GetBetInstance(kaisai, raceNo, year, month, day, houshiki, shikibetsu, kingaku, kaime.encode('utf-8'), byref(betData))

def get_bet_instance_win5(kingaku : int, year : int, month : int, day : int, kaime : str, betData : ST_BET_DATA_WIN5) -> int:
    '''
        馬券購入用インスタンス取得処理(WIN5)
    '''
    return lib.GetBetInstanceWin5(kingaku, year, month, day, kaime.encode('utf-8'), byref(betData))

def bet(betDataList : list, listCount : int, waitMiliSeconds : int = DEFAULT_WAIT_TIME) -> int:
    '''
        馬券購入処理実行
    '''
    return lib.Bet(betDataList, listCount, waitMiliSeconds)

def bet_win5(betData : ST_BET_DATA_WIN5, waitMiliSeconds : int = DEFAULT_WAIT_TIME) -> int:
    '''
        馬券購入処理実行(WIN5)
    '''
    return lib.BetWin5(betData, waitMiliSeconds)

def set_auto_deposit_flag(enable : bool, depositValue : int, confirmTimeout : int = DEFAULT_CONFIRM_TIMEOUT) -> int:
    '''
        自動入金機能フラグ設定
    '''
    return lib.SetAutoDepositFlag(enable, depositValue, confirmTimeout)
