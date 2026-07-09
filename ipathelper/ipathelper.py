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
SHIKIBETSU_QUINELLA	= 4
SHIKIBETSU_QUINELLAPLACE = 5
SHIKIBETSU_EXACTA = 6
SHIKIBETSU_TRIO	= 7
SHIKIBETSU_TRIFECTA	= 8

ODDS_STATUS_NORMAL = 0
ODDS_STATUS_CANCEL = 1
ODDS_STATUS_UNACQUIRED = 2

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

class ST_ODDS_DATA:
    def __init__(self):
        self.Place = 0
        self.RaceNo = 0
        self.OddsTime = ""
        self.DetailCount = 0
        self.OddsDetail = []

class ST_RACECARD_DATA:
    def __init__(self):
        self.Place = 0
        self.RaceNo = 0
        self.OddsTime = ""
        self.EntryCount = 0
        self.EntryData = []

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

class ST_ODDS_DETAIL(Structure):
    _fields_ = [("Type", c_byte), ("Horse1", c_byte), ("Horse2", c_byte), ("Horse3", c_byte), \
        ("Status", c_byte), ("Odds", c_uint), ("OddsHigh", c_uint)]

class ST_ODDS_DATA_INTERNAL(Structure):
    _fields_ = [("Place", c_ushort), ("RaceNo", c_byte), ("OddsTime", c_char * 8), \
        ("DetailCount", c_uint), ("DetailData", c_void_p)]

class ST_ENTRY_DETAIL(Structure):
    # 文字列フィールド(HorseName/Sex/JockeyName/TrainerName)はUTF-8のbytes。
    # 利用時は .decode('utf-8') で文字列化する。
    _fields_ = [("Wakuban", c_byte), ("Umaban", c_byte), \
        ("HorseName", c_char * 64), ("Sex", c_char * 8), ("Age", c_byte), \
        ("WeightStatus", c_byte), ("Weight", c_ushort), \
        ("WeightDiffCode", c_byte), ("WeightDiff", c_ushort), ("Apprentice", c_byte), \
        ("JockeyName", c_char * 48), ("Burden", c_ushort), ("TrainerName", c_char * 48), \
        ("WinPopular", c_ushort), ("WinOddsStatus", c_byte), ("WinOdds", c_uint), \
        ("PlaceOddsStatus", c_byte), ("PlaceOddsLow", c_uint), ("PlaceOddsHigh", c_uint)]

class ST_RACECARD_DATA_INTERNAL(Structure):
    _fields_ = [("Place", c_ushort), ("RaceNo", c_byte), ("OddsTime", c_char * 8), \
        ("EntryCount", c_uint), ("EntryData", c_void_p)]


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

def get_odds(place : int, raceNo : int, shikibetsu : int, oddsData : ST_ODDS_DATA) -> int:
    '''
        オッズ取得処理実行(中央競馬・地方競馬に対応)
        単勝・複勝は基本オッズ、枠連〜三連単は全通りのオッズ表を取得する。
        ネイティブ側で確保されたメモリは本関数内で解放する。
    '''
    tempOddsData = ST_ODDS_DATA_INTERNAL()

    returnValue = lib.GetOdds(place, raceNo, shikibetsu, byref(tempOddsData))

    oddsData.Place = tempOddsData.Place
    oddsData.RaceNo = tempOddsData.RaceNo
    oddsData.OddsTime = tempOddsData.OddsTime.decode('ascii', errors='ignore')
    oddsData.DetailCount = tempOddsData.DetailCount

    # 取得失敗・明細なしはここで解放して戻る
    if (returnValue & 1) != 1 or tempOddsData.DetailCount <= 0 or not tempOddsData.DetailData:
        lib.ReleaseOddsData(byref(tempOddsData))
        return returnValue

    # ネイティブ側の明細配列をコピー(解放前に取り出す)
    allDetailBytes = bytearray(string_at(tempOddsData.DetailData, \
        sizeof(ST_ODDS_DETAIL) * tempOddsData.DetailCount))

    for i in range(tempOddsData.DetailCount):
        oneDetailBytes = bytearray(sizeof(ST_ODDS_DETAIL))
        for j in range(sizeof(ST_ODDS_DETAIL)):
            oneDetailBytes[j] = allDetailBytes[j + i * sizeof(ST_ODDS_DETAIL)]

        oddsData.OddsDetail.append(ST_ODDS_DETAIL.from_buffer(oneDetailBytes, 0))

    lib.ReleaseOddsData(byref(tempOddsData))

    return returnValue

def get_race_card(place : int, raceNo : int, raceCard : ST_RACECARD_DATA) -> int:
    '''
        出馬表取得処理実行(中央競馬・地方競馬に対応)
        各出走馬の枠番・馬番・馬名・性齢・馬体重・騎手・斤量・調教師・
        単勝人気・単勝/複勝オッズを取得する。
        ネイティブ側で確保されたメモリは本関数内で解放する。
        EntryData の各要素は ST_ENTRY_DETAIL で、馬名等の文字列フィールドは
        UTF-8 の bytes のため利用時に .decode('utf-8') する。
    '''
    tempRaceCardData = ST_RACECARD_DATA_INTERNAL()

    # 出馬表を取得する
    returnValue = lib.GetRaceCard(place, raceNo, byref(tempRaceCardData))

    # 返却用のデータに値を設定
    raceCard.Place = tempRaceCardData.Place
    raceCard.RaceNo = tempRaceCardData.RaceNo
    raceCard.OddsTime = tempRaceCardData.OddsTime.decode('ascii', errors='ignore')
    raceCard.EntryCount = tempRaceCardData.EntryCount

    # 取得失敗・明細なしはここで解放して戻る
    if (returnValue & 1) != 1 or tempRaceCardData.EntryCount <= 0 or not tempRaceCardData.EntryData:
        lib.ReleaseRaceCardData(byref(tempRaceCardData))
        return returnValue

    # 出走馬明細(全て)を格納するためのバッファを確保(解放前に取り出す)
    allEntryBytes = bytearray(string_at(tempRaceCardData.EntryData, \
        sizeof(ST_ENTRY_DETAIL) * tempRaceCardData.EntryCount))

    for i in range(tempRaceCardData.EntryCount):
        # 1つ分の構造体データを格納するバッファを確保して情報を格納する
        oneEntryBytes = bytearray(sizeof(ST_ENTRY_DETAIL))
        for j in range(sizeof(ST_ENTRY_DETAIL)):
            oneEntryBytes[j] = allEntryBytes[j + i * sizeof(ST_ENTRY_DETAIL)]

        # 出走馬明細(1個)をインスタンスに変換して追加する
        raceCard.EntryData.append(ST_ENTRY_DETAIL.from_buffer(oneEntryBytes, 0))

    lib.ReleaseRaceCardData(byref(tempRaceCardData))

    return returnValue
