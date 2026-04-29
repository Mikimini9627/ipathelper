=====================
ipathelper
=====================

.. contents:: 目次
   :depth: 2
   :local:
   :backlinks: none

--------
概要
--------

**ipathelper** は、JRA（日本中央競馬会）のインターネット投票サービス「I-PAT」および地方競馬の投票システムに対して、
ログイン・入出金・馬券購入・購入履歴取得などを Python から行うためのラッパーライブラリです。

- 中央競馬・地方競馬・海外競馬・WIN5 に対応
- Windows 32bit / 64bit 環境で動作

`GitHub <https://github.com/Mikimini9627/ipathelper_dll>`__ では Python 以外の利用例も公開しています。
詳細な関数仕様については `関数仕様書 <https://github.com/Mikimini9627/ipathelper_dll/blob/main/builds/%E9%96%A2%E6%95%B0%E4%BB%95%E6%A7%98%E6%9B%B8.md>`__ を参照してください。

.. note::

   本ライブラリを使用した馬券購入は実際の金銭を伴います。
   認証情報（ID・パスワード・P-ARS 番号）はメモリ上にのみ保持され、ファイルへの保存は行いません。

----------------
インストール方法
----------------

.. code-block:: console

   $ pip install ipathelper

--------
動作環境
--------

- OS: Windows 10 以降（32bit / 64bit）
- Python: 3.x

--------
共通仕様
--------

戻り値
======

全関数（``None`` を返すものを除く）は``int`` をビットフラグとして返します。
複数のフラグが同時に立つ場合があります。判定には AND 演算を使用してください。

.. code-block:: python

   ret = bet(bet_data_list, 1, 0)

   if (ret & 1) == 1:    # SUCCESS
       print("成功")
   if (ret & 4) == 4:    # FAILED_CHUOU
       print("中央競馬で失敗")

戻り値ビットフラグ一覧:

.. list-table::
   :header-rows: 1
   :widths: 35 10 55

   * - 定数名
     - ビット
     - 意味
   * - ``RETURN_SUCCESS``
     - 1
     - 処理に成功
   * - ``RETURN_UNSUCCESS``
     - 2
     - 処理に失敗（パラメータ不正・残高不足等）
   * - ``RETURN_FAILED_CHUOU``
     - 4
     - 中央競馬での処理に失敗
   * - ``RETURN_FAILED_CHIHOU``
     - 8
     - 地方競馬での処理に失敗
   * - ``RETURN_FAILED_COM_CHUOU``
     - 16
     - 中央競馬との通信に失敗
   * - ``RETURN_FAILED_COM_CHIHOU``
     - 32
     - 地方競馬との通信に失敗

スレッドセーフ
==============

全関数は内部で排他制御されています。複数スレッドからの同時呼び出しは安全ですが、
関数はブロッキング動作となります。

前提条件
========

``bet``・``deposit``・``withdraw``・``get_purchase_data`` などの関数は、
事前に``login()`` が成功している必要があります。
未ログイン状態での呼び出しは``RETURN_UNSUCCESS`` を返します。

--------
定数一覧
--------

開催場（KAISAI）
================

中央競馬:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 定数名
     - 開催場
   * - ``KAISAI_SAPPORO``
     - 札幌
   * - ``KAISAI_HAKODATE``
     - 函館
   * - ``KAISAI_FUKUSHIMA``
     - 福島
   * - ``KAISAI_NIIGATA``
     - 新潟
   * - ``KAISAI_TOKYO``
     - 東京
   * - ``KAISAI_NAKAYAMA``
     - 中山
   * - ``KAISAI_CHUKYO``
     - 中京
   * - ``KAISAI_KYOTO``
     - 京都
   * - ``KAISAI_HANSHIN``
     - 阪神
   * - ``KAISAI_KOKURA``
     - 小倉

地方競馬:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 定数名
     - 開催場
   * - ``KAISAI_SONODA``
     - 園田
   * - ``KAISAI_HIMEJI``
     - 姫路
   * - ``KAISAI_NAGOYA``
     - 名古屋
   * - ``KAISAI_MONBETSU``
     - 門別
   * - ``KAISAI_MORIOKA``
     - 盛岡
   * - ``KAISAI_MIZUSAWA``
     - 水沢
   * - ``KAISAI_URAWA``
     - 浦和
   * - ``KAISAI_FUNABASHI``
     - 船橋
   * - ``KAISAI_OI``
     - 大井
   * - ``KAISAI_KAWASAKI``
     - 川崎
   * - ``KAISAI_KASAMATSU``
     - 笠松
   * - ``KAISAI_KANAZAWA``
     - 金沢
   * - ``KAISAI_KOCHI``
     - 高知
   * - ``KAISAI_SAGA``
     - 佐賀

海外競馬:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 定数名
     - 開催場
   * - ``KAISAI_LONGCHAMP``
     - ロンシャン（フランス）
   * - ``KAISAI_SHATIN``
     - シャティン（香港）
   * - ``KAISAI_SANTAANITA``
     - サンタアニタ（アメリカ）
   * - ``KAISAI_DEAUVILLE``
     - ドーヴィル（フランス）
   * - ``KAISAI_CHURCHILLDOWNS``
     - チャーチルダウンズ（アメリカ）
   * - ``KAISAI_ABDULAZIZ``
     - キングアブドゥルアジーズ（サウジアラビア）

式別（SHIKIBETSU）
==================

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 定数名
     - 式別
   * - ``SHIKIBETSU_WIN``
     - 単勝
   * - ``SHIKIBETSU_PLACE``
     - 複勝
   * - ``SHIKIBETSU_BRACKETQUINELLA``
     - 枠連
   * - ``SHIKIBETSU_QUINELLAPLACE``
     - ワイド
   * - ``SHIKIBETSU_QUINELLA``
     - 馬連
   * - ``SHIKIBETSU_EXACTA``
     - 馬単
   * - ``SHIKIBETSU_TRIO``
     - 三連複
   * - ``SHIKIBETSU_TRIFECTA``
     - 三連単

方式（HOUSHIKI）
================

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 定数名
     - 方式
   * - ``HOUSHIKI_NORMAL``
     - 通常
   * - ``HOUSHIKI_FORMATION``
     - フォーメーション
   * - ``HOUSHIKI_BOX``
     - ボックス

確定フラグ（DECISIONFLAG）
==========================

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - 定数名
     - 意味
   * - ``DECISIONFLAG_DEFAULT``
     - デフォルト
   * - ``DECISIONFLAG_NORMAL``
     - 通常確定
   * - ``DECISIONFLAG_DEADLINE``
     - 発売締切
   * - ``DECISIONFLAG_CANCEL``
     - キャンセル
   * - ``DECISIONFLAG_FLATMATESCANCEL``
     - 仲間入力取消
   * - ``DECISIONFLAG_HIT``
     - 的中
   * - ``DECISIONFLAG_MISS``
     - 外れ
   * - ``DECISIONFLAG_BACK``
     - 返還
   * - ``DECISIONFLAG_PARTCANCEL``
     - 一部取消
   * - ``DECISIONFLAG_INVALID``
     - 無効
   * - ``DECISIONFLAG_SALECANCEL``
     - 発売取消

----------
データ構造
----------

ST_BET_DATA
===========

``get_bet_instance()`` で設定し、``bet()`` に渡す購入情報です。
フィールドを直接参照することで購入内容を確認できます。

.. code-block:: python

   betData = ST_BET_DATA()
   get_bet_instance(KAISAI_TOKYO, 11, 2026, 4, 5,
                    HOUSHIKI_NORMAL, SHIKIBETSU_WIN, 100, "1", betData)

   print(betData.unTotalAmount)  # 合計購入金額（円）

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - フィールド名
     - 型
     - 説明
   * - ``unTotalAmount``
     - int
     - 合計購入金額（``get_bet_instance`` が自動計算）

ST_BET_DATA_WIN5
================

``get_bet_instance_win5()`` で設定し、``bet_win5()`` に渡す WIN5 専用の購入情報です。

ST_PURCHASE_DATA
================

``get_purchase_data()`` が設定するルート構造体です。
使用後は必ず``release_purchase_data()`` で解放してください。

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - フィールド名
     - 型
     - 説明
   * - ``usRemainBetCount``
     - int
     - 残購入可能件数
   * - ``unBalance``
     - int
     - 現在残高（円）
   * - ``unDayPurchase``
     - int
     - 当日累計購入金額（円）
   * - ``unDayPayout``
     - int
     - 当日累計払戻金額（円）
   * - ``unTotalPurchase``
     - int
     - 合計購入金額（円）
   * - ``unTotalPayout``
     - int
     - 合計払戻金額（円）
   * - ``unTicketCount``
     - int
     - 馬券情報の件数
   * - ``pobjTicketData``
     - array
     - 馬券情報の配列（下記参照）

``pobjTicketData`` の各要素（ST_TICKET_DATA）:

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - フィールド名
     - 型
     - 説明
   * - ``ucDayFlag``
     - int
     - 購入日（1:当日 / 2:前日）
   * - ``ucReceiptNo``
     - int
     - 受付番号
   * - ``ucHour``
     - int
     - 購入時刻（時）
   * - ``ucMinute``
     - int
     - 購入時刻（分）
   * - ``unKingaku``
     - int
     - 購入金額（円）
   * - ``unPayout``
     - int
     - 払戻金額（円）
   * - ``unDetailCount``
     - int
     - 詳細情報の件数
   * - ``pobjDetail``
     - array
     - 詳細情報の配列（下記参照）

``pobjDetail`` の各要素（ST_TICKET_DATA_DETAIL）:

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - フィールド名
     - 型
     - 説明
   * - ``ucDecisionFlag``
     - int
     - 確定フラグ（DECISIONFLAG 定数）
   * - ``usKaisai``
     - int
     - 開催場（KAISAI 定数）
   * - ``ucRaceNo``
     - int
     - レース番号
   * - ``ucMethod``
     - int
     - 方式（HOUSHIKI 定数）
   * - ``ucType``
     - int
     - 式別（SHIKIBETSU 定数）
   * - ``ucMulti``
     - int
     - マルチ購入フラグ（1: マルチあり）

----------------
関数リファレンス
----------------

init
====

モジュールを初期化します。全ての関数を呼び出す前に必ず実行してください。

.. code-block:: python

   result = init()  # -> bool

戻り値は``True`` /``False`` です（ビットフラグではありません）。

uninit
======

モジュールを終了処理します。プログラム終了時に必ず``finally`` ブロック内で呼び出してください。

.. code-block:: python

   uninit()  # -> None

login
=====

I-PAT へログインします。中央競馬と地方競馬の両方へログインを試みます。

.. code-block:: python

   ret = login(inet_id, id, password, pars)

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 引数
     - 型
     - 説明
   * - ``inet_id``
     - str
     - I-NET ID
   * - ``id``
     - str
     - ログイン ID
   * - ``password``
     - str
     - パスワード
   * - ``pars``
     - str
     - P-ARS 番号

戻り値パターン:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 状態
     - 返るフラグ
   * - 両方成功
     - ``SUCCESS``
   * - 中央のみ失敗
     - ``SUCCESS | FAILED_CHUOU``
   * - 地方のみ失敗
     - ``SUCCESS | FAILED_CHIHOU``
   * - 両方失敗
     - ``FAILED_CHUOU | FAILED_CHIHOU``
   * - 既ログイン
     - ``UNSUCCESS``

logout
======

I-PAT からログアウトします。自動入金設定もリセットされます。

.. code-block:: python

   ret = logout()  # -> int

- ログアウト後、再度``login()`` を呼び出すまで他の関数は使用できません。

deposit
=======

登録口座から I-PAT 残高へ入金します。

.. code-block:: python

   ret = deposit(amount, retry_count=10)

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 引数
     - 型
     - 説明
   * - ``amount``
     - int
     - 入金額（円）。100円以上かつ100円単位。
   * - ``retry_count``
     - int
     - 通信失敗時のリトライ回数。デフォルト: 10回。

.. note::

   金額は **100円以上かつ100円単位** で指定してください。
   条件を満たさない場合は``UNSUCCESS`` を返します。

withdraw
========

I-PAT 残高を登録口座へ全額出金します。

.. code-block:: python

   ret = withdraw(retry_count=10)

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 引数
     - 型
     - 説明
   * - ``retry_count``
     - int
     - 通信失敗時のリトライ回数。デフォルト: 10回。

- 出金額の指定は不要です。残高の全額が出金対象となります。

set_auto_deposit_flag
=====================

馬券購入前の残高不足時に自動で入金を行う機能を設定します。
有効化すると``bet()`` /``bet_win5()`` 実行時に残高不足が検出された場合、自動的に入金してから購入を行います。

.. code-block:: python

   ret = set_auto_deposit_flag(enable, deposit_value=1000, confirm_timeout=10000)

.. list-table::
   :header-rows: 1
   :widths: 25 10 65

   * - 引数
     - 型
     - 説明
   * - ``enable``
     - bool
     - ``True`` で有効化、``False`` で無効化
   * - ``deposit_value``
     - int
     - 自動入金額（円）。デフォルト: 1,000円
   * - ``confirm_timeout``
     - int
     - 入金反映確認タイムアウト（ms）。デフォルト: 10秒

-``logout()`` を呼び出すと設定はリセットされます。

get_bet_instance
================

買い目文字列を解析し、``bet()`` に渡す``ST_BET_DATA`` を構築します。

.. code-block:: python

   betData = ST_BET_DATA()
   ret = get_bet_instance(place, race_no, year, month, day,
                          houshiki, shikibetsu, kingaku, kaime, betData)

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 引数
     - 型
     - 説明
   * - ``place``
     - int
     - 開催場（KAISAI 定数）
   * - ``race_no``
     - int
     - レース番号
   * - ``year``
     - int
     - 開催年（西暦 4桁）
   * - ``month``
     - int
     - 開催月（1〜12）
   * - ``day``
     - int
     - 開催日（1〜31）
   * - ``houshiki``
     - int
     - 方式（HOUSHIKI 定数）
   * - ``shikibetsu``
     - int
     - 式別（SHIKIBETSU 定数）
   * - ``kingaku``
     - int
     - 1点あたりの購入金額（円、100円単位）
   * - ``kaime``
     - str
     - 買い目文字列（書式は後述）
   * - ``betData``
     - 
     - [out] ST_BET_DATA インスタンス

成功すると``betData.unTotalAmount`` に合計購入金額が格納されます。

買い目文字列の書式
------------------

- 列の区切り:``-`` （ハイフン）
- 同一列内の複数馬番の区切り:``,`` （カンマ）

.. code-block:: text

   単勝 1番               -> "1"
   馬連 通常 1-5          -> "1-5"
   馬単 通常 3-7          -> "3-7"
   三連複 通常 2-5-8      -> "2-5-8"
   三連単 通常 1-3-5      -> "1-3-5"

   馬連 フォーメーション 1・2番 vs 3・4・5番                  -> "1,2-3,4,5"
   三連複 フォーメーション 軸1番/相手A2・3番/相手B4・5・6番    -> "1-2,3-4,5,6"
   三連単 フォーメーション 1着1番/2着2・3番/3着4・5番          -> "1-2,3-4,5"

   馬連 ボックス 1・2・3・4番（6点）  -> "1,2,3,4"
   三連単 ボックス 1・2・3番（6点）   -> "1,2,3"

bet
===

``get_bet_instance()`` で構築した``ST_BET_DATA`` の配列を一括購入します。
開催場に応じて中央・地方・海外に自動で振り分けられます。

.. code-block:: python

   betDataList = (ST_BET_DATA * n)()
   betDataList[0] = betData
   ret = bet(betDataList, n, wait_ms=500)

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 引数
     - 型
     - 説明
   * - ``betDataList``
     - 
     - ST_BET_DATA の配列（``(ST_BET_DATA * n)()`` で作成）
   * - ``n``
     - int
     - 配列の要素数
   * - ``wait_ms``
     - int
     - 購入リクエスト間隔（ms）。デフォルト: 500ms

.. note::

  ``wait_ms`` が短すぎると購入に失敗する場合があります。
   ネットワーク環境に応じて調整してください。

get_bet_instance_win5
=====================

WIN5 の買い目文字列を解析し、``bet_win5()`` に渡す``ST_BET_DATA_WIN5`` を構築します。

.. code-block:: python

   betDataWin5 = ST_BET_DATA_WIN5()
   ret = get_bet_instance_win5(kingaku, year, month, day, kaime, betDataWin5)

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 引数
     - 型
     - 説明
   * - ``kingaku``
     - int
     - 1組み合わせあたりの購入金額（円、100円単位）
   * - ``year``
     - int
     - 開催年（西暦 4桁）
   * - ``month``
     - int
     - 開催月（1〜12）
   * - ``day``
     - int
     - 開催日（1〜31）
   * - ``kaime``
     - str
     - 5レース分の買い目（``-`` でレース区切り）
   * - ``betDataWin5``
     - 
     - [out] ST_BET_DATA_WIN5 インスタンス

WIN5 の買い目文字列は必ず **5レース分** を``-`` で区切って指定してください。

.. code-block:: text

   各レース1頭ずつ              -> "1-2-3-4-5"
   一部のレースで複数頭指定     -> "1,2-3-4,5-6-7,8"

bet_win5
========

``get_bet_instance_win5()`` で構築した``ST_BET_DATA_WIN5`` を使って WIN5 を購入します。

.. code-block:: python

   ret = bet_win5(betDataWin5, wait_ms=500)

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 引数
     - 型
     - 説明
   * - ``betDataWin5``
     - 
     - ST_BET_DATA_WIN5 インスタンス
   * - ``wait_ms``
     - int
     - 購入リクエスト間隔（ms）。デフォルト: 500ms

.. note::

   WIN5 は **中央競馬でのみ購入可能** です。
   地方競馬のみにログインしている場合は``UNSUCCESS`` を返します。

get_purchase_data
=================

当日・前日の馬券購入履歴（残高・累計金額・購入済み馬券一覧）を取得します。

.. code-block:: python

   purchaseData = ST_PURCHASE_DATA()
   ret = get_purchase_data(purchaseData)
   if (ret & 1) == 1:
       print(f"残高: {purchaseData.unBalance} 円")
   release_purchase_data(purchaseData)

.. warning::

   取得した``ST_PURCHASE_DATA`` は使用後に必ず``release_purchase_data()`` で解放してください。
   解放を忘れるとメモリリークが発生します。

release_purchase_data
=====================

``get_purchase_data()`` が内部で確保したメモリを解放します。

.. code-block:: python

   release_purchase_data(purchaseData)

-``get_purchase_data()`` の成否にかかわらず **必ず呼び出してください** 。
-``None`` を渡しても安全に動作します。

--------
使用例
--------

基本フロー（ログイン〜単勝購入〜ログアウト）
============================================

.. code-block:: python

   from ipathelper import *

   def main():
       try:
           # 初期化
           if not init():
               return

           # ログイン
           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           if (ret & 1) != 1:
               print("ログインに失敗しました。")
               return

           # 購入情報の構築（東京 11R、単勝、1番、100円）
           betData = ST_BET_DATA()
           ret = get_bet_instance(
               KAISAI_TOKYO, 11,
               2026, 4, 5,
               HOUSHIKI_NORMAL, SHIKIBETSU_WIN,
               100, "1",
               betData
           )
           if (ret & 1) != 1:
               print("購入情報の構築に失敗しました。")
               return

           print(f"合計購入金額: {betData.unTotalAmount} 円")

           # 馬券購入
           betDataList = (ST_BET_DATA * 1)()
           betDataList[0] = betData
           ret = bet(betDataList, 1)
           if (ret & 1) != 1:
               print("馬券購入に失敗しました。")
               return

           print("購入成功")

       finally:
           logout()
           uninit()

   if __name__ == '__main__':
       main()

複数買い目の一括購入
====================

.. code-block:: python

   from ipathelper import *

   def main():
       try:
           if not init():
               return

           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           if (ret & 1) != 1:
               return

           bet_list = [
               # (開催場, R, 年, 月, 日, 方式, 式別, 金額, 買い目)
               (KAISAI_TOKYO,    11, 2026, 4, 5, HOUSHIKI_NORMAL,    SHIKIBETSU_WIN,      100, "3"),
               (KAISAI_HANSHIN,  10, 2026, 4, 5, HOUSHIKI_BOX,       SHIKIBETSU_QUINELLA, 200, "1,3,5,7"),
               (KAISAI_NAKAYAMA,  9, 2026, 4, 5, HOUSHIKI_FORMATION, SHIKIBETSU_TRIFECTA, 100, "1-2,3-4,5"),
               # 地方競馬も同じ配列に混在させることができる
               (KAISAI_OI,        8, 2026, 4, 5, HOUSHIKI_NORMAL,    SHIKIBETSU_EXACTA,   100, "5-8"),
           ]

           n = len(bet_list)
           betDataList = (ST_BET_DATA * n)()

           for i, (place, r, y, m, d, houshiki, shikibetsu, kingaku, kaime) in enumerate(bet_list):
               tmp = ST_BET_DATA()
               ret = get_bet_instance(place, r, y, m, d, houshiki, shikibetsu, kingaku, kaime, tmp)
               if (ret & 1) != 1:
                   print(f"[{i}] 購入情報の構築に失敗しました。")
                   return
               betDataList[i] = tmp

           # 4件を一括購入（中央・地方は自動振り分け）
           ret = bet(betDataList, n)
           if (ret & 1) == 1:
               print("全件購入成功")
           if (ret & 4) == 4:
               print("中央競馬の一部または全部が失敗")
           if (ret & 8) == 8:
               print("地方競馬の一部または全部が失敗")

       finally:
           logout()
           uninit()

   if __name__ == '__main__':
       main()

WIN5 の購入
===========

.. code-block:: python

   from ipathelper import *

   def main():
       try:
           if not init():
               return

           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           if (ret & 1) != 1:
               return

           betDataWin5 = ST_BET_DATA_WIN5()

           # レース1: 1・2番 / レース2: 3番 / レース3: 4・5番 / レース4: 6番 / レース5: 7・8番
           # -> 2x1x2x1x2 = 8通り、計 800円
           ret = get_bet_instance_win5(100, 2026, 4, 5, "1,2-3-4,5-6-7,8", betDataWin5)
           if (ret & 1) != 1:
               print("WIN5 購入情報の構築に失敗しました。")
               return

           ret = bet_win5(betDataWin5)
           if (ret & 1) == 1:
               print("WIN5 購入成功")
           else:
               print("WIN5 購入失敗")

       finally:
           logout()
           uninit()

   if __name__ == '__main__':
       main()

入金・出金
==========

.. code-block:: python

   from ipathelper import *

   def main():
       try:
           if not init():
               return

           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           if (ret & 1) != 1:
               return

           # 入金（2,000円）
           ret = deposit(2000)
           if (ret & 1) == 1:
               print("入金成功")

           # 入金（ネットワーク不安定時に最大 3 回だけリトライ）
           ret = deposit(1000, retry_count=3)
           if (ret & 1) != 1:
               print("3回試みても入金できませんでした。")

           # 全額出金
           ret = withdraw()
           if (ret & 1) == 1:
               print("出金成功")

       finally:
           logout()
           uninit()

   if __name__ == '__main__':
       main()

自動入金を有効にして購入
========================

.. code-block:: python

   from ipathelper import *

   def main():
       try:
           if not init():
               return

           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           if (ret & 1) != 1:
               return

           # 残高不足時に 3,000円 自動入金、反映確認タイムアウト 15秒
           set_auto_deposit_flag(True, deposit_value=3000, confirm_timeout=15000)

           betData = ST_BET_DATA()
           ret = get_bet_instance(
               KAISAI_TOKYO, 11, 2026, 4, 5,
               HOUSHIKI_FORMATION, SHIKIBETSU_TRIFECTA,
               100, "1-2,3,4-5,6,7", betData
           )
           if (ret & 1) != 1:
               return

           betDataList = (ST_BET_DATA * 1)()
           betDataList[0] = betData

           # 残高不足なら自動的に 3,000円 入金してから購入
           ret = bet(betDataList, 1)
           if (ret & 1) == 1:
               print("購入成功")
           else:
               print("購入失敗（残高不足またはタイムアウト）")

       finally:
           logout()
           uninit()

   if __name__ == '__main__':
       main()

購入履歴の取得
==============

.. code-block:: python

   from ipathelper import *

   def main():
       try:
           if not init():
               return

           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           if (ret & 1) != 1:
               return

           purchaseData = ST_PURCHASE_DATA()
           ret = get_purchase_data(purchaseData)

           if (ret & 1) == 1:
               print(f"残高          : {purchaseData.unBalance} 円")
               print(f"残購入可能数  : {purchaseData.usRemainBetCount} 件")
               print(f"当日購入金額  : {purchaseData.unDayPurchase} 円")
               print(f"当日払戻金額  : {purchaseData.unDayPayout} 円")
               print(f"累計購入金額  : {purchaseData.unTotalPurchase} 円")
               print(f"累計払戻金額  : {purchaseData.unTotalPayout} 円")
               print(f"馬券件数      : {purchaseData.unTicketCount} 件")
               print("--------------------------------")

               for i in range(purchaseData.unTicketCount):
                   ticket = purchaseData.pobjTicketData[i]
                   day_label = "当日" if ticket.ucDayFlag == 1 else "前日"
                   print(f"[受付No.{ticket.ucReceiptNo:02d}] "
                         f"{day_label} "
                         f"{ticket.ucHour:02d}:{ticket.ucMinute:02d}購入 "
                         f"{ticket.unKingaku}円 "
                         f"(払戻: {ticket.unPayout}円) "
                         f"詳細{ticket.unDetailCount}点")

                   for j in range(ticket.unDetailCount):
                       detail = ticket.pobjDetail[j]
                       status_map = {
                           DECISIONFLAG_HIT:      "的中",
                           DECISIONFLAG_MISS:     "外れ",
                           DECISIONFLAG_BACK:     "返還",
                           DECISIONFLAG_CANCEL:   "取消",
                           DECISIONFLAG_NORMAL:   "確定",
                           DECISIONFLAG_DEADLINE: "締切",
                       }
                       status = status_map.get(detail.ucDecisionFlag, "不明")
                       multi  = "[マルチ]" if detail.ucMulti else ""
                       print(f"  詳細[{j}]: {status} {multi} "
                             f"R{detail.ucRaceNo} 方式:{detail.ucMethod} 式別:{detail.ucType}")

           # 必ず解放する
           release_purchase_data(purchaseData)

       finally:
           logout()
           uninit()

   if __name__ == '__main__':
       main()

エラーハンドリング
==================

.. code-block:: python

   from ipathelper import *

   # 戻り値のビットフラグを一括確認するユーティリティ関数
   def print_return_value(func_name: str, ret: int):
       flags = []
       if (ret &  1): flags.append("SUCCESS")
       if (ret &  2): flags.append("UNSUCCESS")
       if (ret &  4): flags.append("FAILED_CHUOU")
       if (ret &  8): flags.append("FAILED_CHIHOU")
       if (ret & 16): flags.append("FAILED_COM_CHUOU")
       if (ret & 32): flags.append("FAILED_COM_CHIHOU")
       print(f"[{func_name}] {' | '.join(flags)}")

   def main():
       try:
           if not init():
               return

           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           print_return_value("login", ret)

           if (ret & 1) != 1:
               print("ログインに失敗しました。処理を中止します。")
               return

           # 中央・地方のログイン状態を個別確認
           if (ret & 4) == 4:
               print("警告: 中央競馬ログイン失敗。中央競馬の馬券は購入できません。")
           if (ret & 8) == 8:
               print("警告: 地方競馬ログイン失敗。地方競馬の馬券は購入できません。")

           betData = ST_BET_DATA()
           ret = get_bet_instance(KAISAI_TOKYO, 11, 2026, 4, 5,
                                  HOUSHIKI_NORMAL, SHIKIBETSU_WIN, 100, "5", betData)
           print_return_value("get_bet_instance", ret)

           if (ret & 1) == 1:
               betDataList = (ST_BET_DATA * 1)()
               betDataList[0] = betData
               ret = bet(betDataList, 1)
               print_return_value("bet", ret)

               # 通信エラー時は再ログインを試みる
               if (ret & 1) != 1 and (ret & 16) == 16:
                   print("通信エラー。再ログインを試みます。")
                   logout()
                   login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')

       finally:
           logout()
           uninit()

   if __name__ == '__main__':
       main()

--------------------
対応金融機関
--------------------

入出金に使用できる金融機関は以下の通りです。

- PayPay 銀行
- 楽天銀行
- 三井住友銀行
- 三菱 UFJ 銀行
- 住信 SBI ネット銀行
- ゆうちょ銀行
- りそな銀行
- 埼玉りそな銀行
- au じぶん銀行
