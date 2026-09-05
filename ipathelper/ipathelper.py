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
KAISAI_DEAUVILLE = 27
KAISAI_DEAUVILE = KAISAI_DEAUVILLE  # 綴りを誤った旧名。値は同じ。新規コードでは KAISAI_DEAUVILLE を使うこと
KAISAI_CHURCHILLDOWNS = 28
KAISAI_ABDULAZIZ = 29
KAISAI_ASCOT = 30

HOUSHIKI_NORMAL = 0
HOUSHIKI_FORMATION = 1
HOUSHIKI_BOX = 2
HOUSHIKI_WHEEL_1ST = 3          # 軸1頭ながし(1着流し)/馬連・ワイド・枠連/三連複軸1頭/三連単1着。買い目「軸-相手」
HOUSHIKI_WHEEL_2ND = 4          # 2着ながし(馬単・三連単)。買い目「軸-相手」
HOUSHIKI_WHEEL_3RD = 5          # 3着ながし(三連単)。買い目「軸-相手」
HOUSHIKI_WHEEL_1ST_2ND = 6      # 軸2頭ながし(三連複)/1・2着ながし(三連単)
HOUSHIKI_WHEEL_1ST_3RD = 7      # 1・3着ながし(三連単)。買い目「1着軸-相手-3着軸」
HOUSHIKI_WHEEL_2ND_3RD = 8      # 2・3着ながし(三連単)。買い目「相手-2着軸-3着軸」
HOUSHIKI_WHEEL_MULTI_AXIS1 = 9  # 軸1頭ながしマルチ(馬単・三連単)。買い目「軸-相手」
HOUSHIKI_WHEEL_MULTI_AXIS2 = 10 # 軸2頭ながしマルチ(三連単)。買い目「軸-軸-相手」

SHIKIBETSU_WIN = 1
SHIKIBETSU_PLACE = 	2
SHIKIBETSU_BRACKETQUINELLA = 3
SHIKIBETSU_QUINELLA	= 4
SHIKIBETSU_QUINELLAPLACE = 5
SHIKIBETSU_EXACTA = 6
SHIKIBETSU_TRIO	= 7
SHIKIBETSU_TRIFECTA	= 8
# 応援馬券(同一馬の単勝＋複勝のセット)。方式は通常のみ・馬番1頭のみ。
# 合計金額は指定額の2倍になり、購入履歴には単勝と複勝が別々の馬券として現れる。
# get_odds にこの式別は指定できない(UNSUCCESS)。
SHIKIBETSU_WINPLACE = 9

ODDS_STATUS_NORMAL = 0
ODDS_STATUS_CANCEL = 1
ODDS_STATUS_UNACQUIRED = 2

# ST_RACECARD_DATA.RaceStatus の値
RACE_STATUS_ON_SALE = 0         # 発売中
RACE_STATUS_CLOSED = 1          # 発売終了
RACE_STATUS_CANCELED = 2        # 発売中止
RACE_STATUS_BEFORE_SALE = 3     # 発売前
RACE_STATUS_UNKNOWN = 0xFF      # 取得できなかった

DAYTYPE_TODAY = 1
DAYTYPE_BEFORE = 2

# ST_TICKET_DATA_DETAIL.BetFlag の値(券種)
BETFLAG_NORMAL = 0
BETFLAG_WIN5 = 1
BETFLAG_INTERNATIONAL = 2       # 海外。中央の購入履歴に混在する
BETFLAG_INTERNAL = BETFLAG_INTERNATIONAL  # 旧名。値は同じ

# ST_TICKET_DATA_DETAIL.DecisionFlag の値(確定フラグ)
# PARSE_FAILED(0) はその明細を解析できなかったことを表す。
# DECISIONFLAG_* は 1 始まりのため、正常な確定フラグと衝突しない。
DECISIONFLAG_PARSE_FAILED = 0
DECISIONFLAG_DEFAULT = 1
DECISIONFLAG_NORMAL = 2
DECISIONFLAG_DEADLINE = 3
DECISIONFLAG_CANCEL = 4
DECISIONFLAG_FLATMATESCANCEL = 5
DECISIONFLAG_HIT = 6
DECISIONFLAG_MISS = 7
DECISIONFLAG_BACK = 8
DECISIONFLAG_PARTCANCEL = 9
DECISIONFLAG_INVALID = 10
DECISIONFLAG_SALECANCEL = 11

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
# サービス時間外(ログインフォームが提供されていない)。login() でのみ立ち、
# FAILED_CHUOU / FAILED_CHIHOU と併せて立つ。最も多い原因は投票受付時間外で、
# 特に地方競馬は営業時間外に必ずこの状態になる(メンテナンス中も同じ状態になり区別できない)。
# このフラグが立った場合、即座のリトライは必ず失敗する。時間をおいて再試行すること。
FAILED_OUT_OF_SERVICE = 64

# 買い目の列数
UMABAN_COLUMN_COUNT = 3         # ST_BET_DATA.Umaban の要素数
UMABAN_TICKET_COLUMN_COUNT = 5  # 購入明細 HorseNo1〜HorseNo5(WIN5 の5レース分を含む)
WIN5_RACE_COUNT = 5             # WIN5 のレース数

# 1回の送信あたりの合計購入金額の上限(円)。1点でもこの上限が効くため、
# 1点あたりの金額の上限も同じ値になる。
MAX_TOTAL_AMOUNT_PER_SEND = 1000000

MAX_WIN5_AUTO_BET_COUNT = 50    # bet_win5_auto() で生成させられる点数の上限

DEFAULT_RETRY_COUNT = 10
DEPOSIT_DEFAULT_VALUE = 1000    # set_auto_deposit_flag() の既定入金額(円)
DEFAULT_CONFIRM_TIMEOUT = 10000 # 残高反映を待つ既定のタイムアウト(ms)

# 分割送信の間隔(ms)。タイムアウトではない。
# DEFAULT_BET_INTERVAL は DLL 側の既定値。本モジュールの bet()/bet_win5() は
# より余裕を持たせた DEFAULT_WAIT_TIME を既定で渡す。
DEFAULT_BET_INTERVAL = 500
DEFAULT_WAIT_TIME = 1000

WIN5_AUTO_SELECT = 2    # WIN5 セレクト: 軸馬を指定し、残りはサーバが選ぶ
WIN5_AUTO_RANDOM = 3    # WIN5 ランダム: すべてサーバが選ぶ

LOG_LEVEL_TRACE = 0     # 詳細トレース。入出金失敗時の応答本文の抜粋はこのレベルのみ
LOG_LEVEL_INFO = 1      # 情報(既定)
LOG_LEVEL_WARN = 2      # 警告
LOG_LEVEL_ERROR = 3     # エラー。失敗した段階・画面ID・タイトルはこのレベル

# ログコールバックの型。DLL側は __cdecl のため CFUNCTYPE(WINFUNCTYPE ではない)。
LOG_CALLBACK = CFUNCTYPE(None, c_int, c_char_p)

# ネイティブへ渡したコールバックはGCされるとクラッシュするため参照を保持する
_log_callback_ref = None
_log_handler = None

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
        self.RaceName = ""                       # レース名(取得できない場合は空文字。海外開催でも取得できる)
        self.Deadline = ""                       # 発売締切時刻 "HH:MM"(取得できない場合は空文字)
        self.RaceStatus = RACE_STATUS_UNKNOWN    # 発売状態(RACE_STATUS_*)

class ST_NOTICE_DATA:
    def __init__(self):
        self.Message = ""       # 強制表示お知らせ本文。無い場合は空文字
        self.NoticeNo = ""      # お知らせ番号
        self.NoticeType = ""    # お知らせ種別
        self.ItemCount = 0      # お知らせ一覧の件数
        self.ItemData = []      # お知らせ一覧(ST_NOTICE_ITEM のリスト)

#構造体マーシャリング用クラス
# ネイティブ側は unsigned char のため c_ubyte を使う。
# c_byte(符号付き)にすると WIN5 明細の 0xFF が -1 として読めてしまう。
class ST_TICKET_DATA_DETAIL(Structure):
    '''
        馬券1点分の詳細情報。

        購入時の指定そのものではなく、投票内容から復元した値。
        HorseNo1〜HorseNo5 の各列が何を指すかは Method(方式)と Type(式別)の
        組み合わせで変わる。列を機械的に "-" で連結すると誤った買い目になる
        (README「購入明細の読み方」を参照)。

        馬番の判定は (HorseNo1 & (1 << (馬番 - 1))) != 0。枠連だけは馬番ではなく枠番。
        マルチの判定は必ず Multi で行うこと(Method では判定できない)。
        WIN5 の明細では HorseNo1〜HorseNo5 が第1〜第5レースに対応し、
        Kaisai / RaceNo / Week / Method / Type は 0xFF(255)になる。
    '''
    _fields_ = [("DecisionFlag", c_ubyte), ("BetFlag", c_ubyte), ("Kaisai", c_ushort), ("RaceNo", c_ubyte), \
        ("Week", c_ubyte), ("Method", c_ubyte), ("Type", c_ubyte), ("HorseNo1", c_uint), \
        ("HorseNo2", c_uint), ("HorseNo3", c_uint), ("HorseNo4", c_uint), ("HorseNo5", c_uint), ("Multi", c_ubyte)]

class ST_TICKET_DATA_INTERNAL(Structure):
    _fields_ = [("DayFlag", c_ubyte), ("ReceiptNo", c_ubyte), ("Hour", c_ubyte), ("Minute", c_ubyte), \
        ("Kingaku", c_uint), ("Payout", c_uint), ("DetailCount", c_uint), ("DetailData", c_void_p)]

class ST_PURCHASE_DATA_INTERNAL(Structure):
    _fields_ = [("AvailableBetCount", c_ushort), ("Balance", c_uint), ("DayPurchase", c_uint),\
         ("DayHaraimodosi", c_uint), ("TotalPurchase", c_uint), ("TotalHaraimodosi", c_uint), ("TicketCount", c_uint), ("TicketData", c_void_p)]

class ST_BET_DATA(Structure):
    _fields_ = [("Place", c_ushort), ("RaceNo", c_ubyte), ("Youbi", c_ubyte), ("Kaikata", c_ubyte),\
         ("Shikibetsu", c_ubyte), ("Kingaku", c_uint), ("Umaban", c_uint * UMABAN_COLUMN_COUNT), \
         ("TotalAmount", c_uint), ("Multi", c_ubyte)]  # Multi: マルチかどうか(0:通常 1:マルチ)

class ST_BET_DATA_WIN5(Structure):
    _fields_ = [("Kingaku", c_uint), ("Youbi", c_ubyte), ("Umaban", c_uint * WIN5_RACE_COUNT)]

class ST_ODDS_DETAIL(Structure):
    _fields_ = [("Type", c_ubyte), ("Horse1", c_ubyte), ("Horse2", c_ubyte), ("Horse3", c_ubyte), \
        ("Status", c_ubyte), ("Odds", c_uint), ("OddsHigh", c_uint)]

class ST_ODDS_DATA_INTERNAL(Structure):
    _fields_ = [("Place", c_ushort), ("RaceNo", c_ubyte), ("OddsTime", c_char * 8), \
        ("DetailCount", c_uint), ("DetailData", c_void_p)]

class ST_ENTRY_DETAIL(Structure):
    # 文字列フィールド(HorseName/Sex/JockeyName/TrainerName)はUTF-8のbytes。
    # 利用時は .decode('utf-8') で文字列化する。
    _fields_ = [("Wakuban", c_ubyte), ("Umaban", c_ubyte), \
        ("HorseName", c_char * 64), ("Sex", c_char * 8), ("Age", c_ubyte), \
        ("WeightStatus", c_ubyte), ("Weight", c_ushort), \
        ("WeightDiffCode", c_ubyte), ("WeightDiff", c_ushort), ("Apprentice", c_ubyte), \
        ("JockeyName", c_char * 48), ("Burden", c_ushort), ("TrainerName", c_char * 48), \
        ("WinPopular", c_ushort), ("WinOddsStatus", c_ubyte), ("WinOdds", c_uint), \
        ("PlaceOddsStatus", c_ubyte), ("PlaceOddsLow", c_uint), ("PlaceOddsHigh", c_uint)]

class ST_RACECARD_DATA_INTERNAL(Structure):
    # RaceName はレース名(UTF-8のbytes)。ネイティブ側構造体の末尾に追加されたため、
    # EntryData(ポインタ)の後ろに配置する。
    # Deadline(発売締切時刻)/RaceStatus(発売状態) も同様に末尾へ追加されている。
    # ネイティブ側は呼び出し元が確保したこの領域へ書き込むため、
    # フィールドの順序・型が DLL の ST_RACECARD_DATA と一致していないとメモリ破壊になる。
    # 末尾へ勝手にフィールドを足さないこと(DLL が書かない領域を読むだけになる)。
    _fields_ = [("Place", c_ushort), ("RaceNo", c_ubyte), ("OddsTime", c_char * 8), \
        ("EntryCount", c_uint), ("EntryData", c_void_p), ("RaceName", c_char * 128), \
        ("Deadline", c_char * 8), ("RaceStatus", c_ubyte)]

class ST_NOTICE_ITEM(Structure):
    # 文字列フィールド(Title/Date/Url/Icon/Color)はUTF-8のbytes。
    # 利用時は .decode('utf-8') で文字列化する。
    _fields_ = [("Title", c_char * 512), ("Date", c_char * 64), \
        ("Url", c_char * 1024), ("Icon", c_char * 128), ("Color", c_char * 32)]

class ST_NOTICE_DATA_INTERNAL(Structure):
    _fields_ = [("Message", c_char * 2048), ("NoticeNo", c_char * 16), \
        ("NoticeType", c_char * 8), ("ItemCount", c_uint), ("ItemData", c_void_p)]


def set_log_callback(handler, minLevel : int = LOG_LEVEL_INFO) -> None:
    '''
        DLL内部のログを受け取るハンドラを登録する(Noneで解除)

        handler は handler(level: int, message: str) の形で呼ばれる。
        入出金は機械可読なエラーコードを返さないため、失敗の原因を知るには
        このログが唯一の手掛かりになる。失敗した段階・画面ID・タイトルは
        LOG_LEVEL_ERROR で通知されるが、サーバ側の拒否理由が載る応答本文の抜粋は
        LOG_LEVEL_TRACE を指定したときのみ通知される(口座番号や残高を含み得る)。

        注意: ハンドラはDLL内部ロックを保持したまま呼ばれるため、
        ハンドラ内から本モジュールのAPIを呼び返さないこと(デッドロックする)。
        またログイン中は中央・地方の2スレッドから同時に呼ばれる。
    '''
    global _log_callback_ref, _log_handler

    _log_handler = handler

    if handler is None:
        # 解除時はDLL側が排他ロックを取るため、戻った時点で実行中の呼び出しは無い
        lib.SetLogCallback(None, minLevel)
        _log_callback_ref = None
        return

    def _on_log(level, message):
        # message は UTF-8 の null 終端文字列
        try:
            text = message.decode('utf-8', 'replace') if message else ''
            _log_handler(level, text)
        except Exception:
            pass    # ハンドラ側の例外をネイティブへ伝播させない

    _log_callback_ref = LOG_CALLBACK(_on_log)
    lib.SetLogCallback(_log_callback_ref, minLevel)

def login(iNetId : str, id : str, password : str, pars : str) -> int:
    '''
        ログイン処理実行

        中央競馬と地方競馬へ並列でログインを試み、どちらか一方でも成功すれば
        SUCCESS が立つ。失敗した系統は FAILED_CHUOU / FAILED_CHIHOU で判別する。

        受付時間外・メンテナンス中は、それらと併せて FAILED_OUT_OF_SERVICE が立つ。
        この場合の即時リトライは必ず失敗するため、時間をおいて再試行すること。
    '''
    return lib.Login(iNetId.encode('utf-8'), id.encode('utf-8'), password.encode('utf-8'), pars.encode('utf-8'))

def logout() -> int:
    '''
        ログアウト処理実行

        セッション情報と自動入金設定を初期化する。
        サーバへの通知に失敗しても後始末は必ず行われ、本関数自体は成功を返す。
    '''
    return lib.Logout()

def deposit(depositValue : int, retryCount : int = DEFAULT_RETRY_COUNT) -> int:
    '''
        入金処理実行

        depositValue は100円以上かつ100円単位で指定する。
        入金後、入金額が残高へ加算されたことを確認できるまで待機し、
        反映を確認できた場合のみ成功を返す(待機時間の上限は
        set_auto_deposit_flag の confirmTimeout)。

        retryCount が適用されるのは入金実行前の準備段階のみ。入金の実行そのものは、
        応答を受信できなくてもサーバ側で成立している可能性があるため再送しない
        (二重入金の防止)。成否は残高への反映で判定する。

        即PAT(ネットバンク)会員専用。A-PAT 会員は UNSUCCESS を返す。
        登録口座が PayPay(コード決済アプリ)の場合も利用できず、通信を行わず
        UNSUCCESS を返す(PayPay 銀行は従来どおり利用できる。両者は別物)。
    '''
    return lib.Deposit(depositValue, retryCount)

def withdraw(retryCount : int = DEFAULT_RETRY_COUNT) -> int:
    '''
        出金処理実行(全額出金。出金額の指定は不要)

        出金後、残高が0になったことを確認できるまで待機し、
        反映を確認できた場合のみ成功を返す。

        retryCount の適用範囲は deposit と同じで、出金の実行そのものは再送しない
        (二重出金の防止)。deposit と同じく即PAT 会員専用で、
        登録口座が PayPay(コード決済アプリ)の場合は UNSUCCESS を返す。
    '''
    return lib.Withdraw(retryCount)

def get_purchase_data(purchaseData : ST_PURCHASE_DATA) -> int:
    '''
        購入状況取得処理実行

        購入履歴は会場ごとに別々に保持されているため、ログイン済みの会場すべてから
        取得して連結する(中央 → 地方の順)。海外の馬券は中央の履歴に含まれる。
        残高・購入可能件数・当日/累計の金額は合算しない(中央・地方は同じ即PAT 口座を
        共有するため、どちらか一方の値をそのまま返す)。

        片方の会場だけ取得に失敗した場合は、取得できた分を返したうえで
        FAILED_CHUOU / FAILED_CHIHOU を立てる(SUCCESS と同時に立つ)。
        履歴の欠けを検出したい場合はこれらのフラグも確認すること。

        明細(ST_TICKET_DATA_DETAIL)から買い目を復元する方法は
        README「購入明細の読み方」を参照。列を機械的に連結すると誤った買い目になる。

        ネイティブ側で確保されたメモリは本関数内で解放する。
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

    if tempPurchaseData.TicketCount <= 0 or not tempPurchaseData.TicketData:
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

        # 明細を持たない受付があっても、後続の受付は正常に返される。
        # ここで打ち切ると以降の馬券をすべて取りこぼすため次の受付へ進む。
        if oneTicketData.DetailCount <= 0 or not oneTicketData.DetailData:
            tempTicketData.DetailCount = 0
            purchaseData.TicketData.append(tempTicketData)
            continue

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

        raceNo は 1〜14、kingaku は100円以上 MAX_TOTAL_AMOUNT_PER_SEND 円以下・100円単位。
        馬番は 1〜18(海外開催は 1〜24)で指定する。範囲外の馬番が含まれる場合は、
        その馬番を無視するのではなく UNSUCCESS を返す
        (指定より少ない点数で購入されるのを防ぐため)。

        合計購入金額は betData.TotalAmount に自動計算されて格納される。
        マルチ(HOUSHIKI_WHEEL_MULTI_*)を指定すると Kaikata は基底のながし方式に
        正規化され、betData.Multi が 1 になる。

        海外開催では枠連(SHIKIBETSU_BRACKETQUINELLA)を購入できない(UNSUCCESS)。
        本関数は通信を行わないため、他のAPIの実行中でも並行して呼び出せる。
    '''
    return lib.GetBetInstance(kaisai, raceNo, year, month, day, houshiki, shikibetsu, kingaku, kaime.encode('utf-8'), byref(betData))

def get_bet_instance_win5(kingaku : int, year : int, month : int, day : int, kaime : str, betData : ST_BET_DATA_WIN5) -> int:
    '''
        馬券購入用インスタンス取得処理(WIN5)

        金額の上限は get_bet_instance と同じ MAX_TOTAL_AMOUNT_PER_SEND 円。
        馬番は 1〜18 で指定する。get_bet_instance と同じく通信を行わない。
    '''
    return lib.GetBetInstanceWin5(kingaku, year, month, day, kaime.encode('utf-8'), byref(betData))

def bet(betDataList : list, listCount : int, waitMiliSeconds : int = DEFAULT_WAIT_TIME) -> int:
    '''
        馬券購入処理実行

        購入件数が1回の送信上限(中央255件・地方50件)を超える場合は自動的に分割送信する。
        waitMiliSeconds はそのときの間隔(ms)で、タイムアウトではない。
        間隔が短いと購入に失敗することがあるため、ネットワーク環境に応じて調整する。

        DLL 側の既定値は DEFAULT_BET_INTERVAL(500ms)だが、本モジュールは
        より余裕を持たせた DEFAULT_WAIT_TIME(1000ms)を既定で渡す。

        応援馬券(SHIKIBETSU_WINPLACE)は送信時に単勝と複勝の2点へ展開される。
        件数・金額の上限は展開後の値で判定される。
    '''
    return lib.Bet(betDataList, listCount, waitMiliSeconds)

def bet_win5(betData : ST_BET_DATA_WIN5, waitMiliSeconds : int = DEFAULT_WAIT_TIME) -> int:
    '''
        馬券購入処理実行(WIN5。中央競馬のみ)

        1回の購入上限(50組み合わせ)を超える場合は自動的に分割送信する。
        waitMiliSeconds は bet と同じく分割送信の間隔(ms)。
    '''
    return lib.BetWin5(betData, waitMiliSeconds)

def bet_win5_auto(mode : int, axisUmaban : str, betCount : int, kingaku : int,
                  year : int, month : int, day : int) -> int:
    '''
        WIN5を「セレクト」または「ランダム」で購入する(中央競馬のみ)

        買い目を指定する bet_win5 と違い、買い目はサーバが生成する。
        生成された買い目はそのまま購入されるため、内容を事前に確認する手段は無い。
        実際に購入が行われるため、呼び出す前に必ず利用者の確認を取ること。

        mode        : WIN5_AUTO_SELECT(2) / WIN5_AUTO_RANDOM(3)
        axisUmaban  : セレクト時の軸馬番。5レース分をカンマ区切りで指定する(例 "3,0,7,0,0")。
                      0のレースはサーバが選ぶ。ランダム時は None 可。

                      0(おまかせ)にできるのは 1〜4 レース。次の2つは送信せずに
                      UNSUCCESS を返す。
                        ・すべて0 ("0,0,0,0,0")  ランダムと同じ指定になる。
                          WIN5_AUTO_RANDOM を使うこと
                        ・0が1つも無い ("3,7,1,5,2")  買い目が1通りに決まり、
                          依頼した点数を生成できない。bet_win5 で直接指定すること
        betCount    : 生成させる点数(1〜MAX_WIN5_AUTO_BET_COUNT)。分割送信は行わない
        kingaku     : 1点あたりの購入金額(円。100円単位)。合計が
                      MAX_TOTAL_AMOUNT_PER_SEND 円を超える場合は UNSUCCESS を返す
    '''
    axis = axisUmaban.encode('utf-8') if axisUmaban else None
    return lib.BetWin5Auto(mode, axis, betCount, kingaku, year, month, day)

def set_auto_deposit_flag(enable : bool, depositValue : int = DEPOSIT_DEFAULT_VALUE, \
                          confirmTimeout : int = DEFAULT_CONFIRM_TIMEOUT) -> int:
    '''
        自動入金機能フラグ設定

        有効にすると bet / bet_win5 実行時に残高不足を検出した場合、
        自動的に depositValue 円を入金してから購入に移る。
        入金後、残高への反映を最大 confirmTimeout ミリ秒待機し、
        タイムアウトした場合は購入を中止する。
        入金しても残高が購入金額に満たない場合は入金を行わず UNSUCCESS を返す。

        depositValue は100円単位(enable が False の場合は検証しない)。
        confirmTimeout は deposit / withdraw の反映待機にも使われる。
        自動入金は deposit と同じ経路のため、即PAT 会員専用という制約も同じ。
    '''
    return lib.SetAutoDepositFlag(enable, depositValue, confirmTimeout)

def get_odds(place : int, raceNo : int, shikibetsu : int, oddsData : ST_ODDS_DATA) -> int:
    '''
        オッズ取得処理実行(中央競馬・地方競馬・海外競馬に対応)

        単勝・複勝は基本オッズ、枠連〜三連単は全通りのオッズ表を取得する。
        オッズは10倍の整数(例: 12.3倍 → 123)。複勝・ワイドは下限を Odds、
        上限を OddsHigh に格納する。

        海外開催は中央競馬へのログインが必要で、枠が無いため枠連
        (SHIKIBETSU_BRACKETQUINELLA)を指定すると UNSUCCESS を返す。
        応援馬券(SHIKIBETSU_WINPLACE)はオッズの式別ではないため指定できない。
        指定した開催場がその日開催されていない場合も UNSUCCESS を返す。

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
        出馬表取得処理実行(中央競馬・地方競馬・海外競馬に対応)

        各出走馬の枠番・馬番・馬名・性齢・馬体重・騎手・斤量・調教師・
        単勝人気・単勝/複勝オッズを取得する。斤量・オッズは10倍の整数。
        あわせて RaceName(レース名)、Deadline(発売締切時刻 "HH:MM")、
        RaceStatus(発売状態 RACE_STATUS_*)を取得する(追加の通信は発生しない)。
        締切時刻だけでは購入可否が判断できないため RaceStatus も参照すること。

        海外開催は中央競馬へのログインが必要で、I-PAT が返す項目が国内より少ない。
        取得できるのは Umaban / HorseName / WinPopular / 単勝・複勝オッズ と
        RaceName / Deadline / RaceStatus のみで、Wakuban / Sex / Age / Weight /
        JockeyName / Burden / TrainerName は 0 または空文字になる。
        指定した開催場がその日開催されていない場合は UNSUCCESS を返す。

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
    # レース名はUTF-8のbytesのためutf-8でデコードする(OddsTimeはascii)
    raceCard.RaceName = tempRaceCardData.RaceName.decode('utf-8', errors='ignore')
    # 発売締切時刻("HH:MM")と発売状態。海外開催でも取得できる
    raceCard.Deadline = tempRaceCardData.Deadline.decode('ascii', errors='ignore')
    raceCard.RaceStatus = tempRaceCardData.RaceStatus

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

def get_notice(notice : ST_NOTICE_DATA) -> int:
    '''
        お知らせ取得処理実行(中央競馬・地方競馬に対応)
        強制表示お知らせ本文(Message)と、お知らせ一覧(ItemData)を取得する。
        ネイティブ側で確保されたメモリは本関数内で解放する。
        ItemData の各要素は ST_NOTICE_ITEM で、Title 等の文字列フィールドは
        UTF-8 の bytes のため利用時に .decode('utf-8') する。
    '''
    tempNoticeData = ST_NOTICE_DATA_INTERNAL()

    # お知らせを取得する
    returnValue = lib.GetNotice(byref(tempNoticeData))

    # 返却用のデータに値を設定
    notice.Message = tempNoticeData.Message.decode('utf-8', errors='ignore')
    notice.NoticeNo = tempNoticeData.NoticeNo.decode('utf-8', errors='ignore')
    notice.NoticeType = tempNoticeData.NoticeType.decode('utf-8', errors='ignore')
    notice.ItemCount = tempNoticeData.ItemCount

    # 取得失敗・一覧なしはここで解放して戻る
    if (returnValue & 1) != 1 or tempNoticeData.ItemCount <= 0 or not tempNoticeData.ItemData:
        lib.ReleaseNoticeData(byref(tempNoticeData))
        return returnValue

    # お知らせ一覧(全て)を格納するためのバッファを確保(解放前に取り出す)
    allItemBytes = bytearray(string_at(tempNoticeData.ItemData, \
        sizeof(ST_NOTICE_ITEM) * tempNoticeData.ItemCount))

    for i in range(tempNoticeData.ItemCount):
        # 1つ分の構造体データを格納するバッファを確保して情報を格納する
        oneItemBytes = bytearray(sizeof(ST_NOTICE_ITEM))
        for j in range(sizeof(ST_NOTICE_ITEM)):
            oneItemBytes[j] = allItemBytes[j + i * sizeof(ST_NOTICE_ITEM)]

        # お知らせ一覧(1個)をインスタンスに変換して追加する
        notice.ItemData.append(ST_NOTICE_ITEM.from_buffer(oneItemBytes, 0))

    lib.ReleaseNoticeData(byref(tempNoticeData))

    return returnValue
