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
ログイン・入出金・馬券購入・購入履歴取得・オッズ取得・出馬表取得・お知らせ取得を Python から行うためのラッパーライブラリです。

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
- Python: 3.12 以上

.. note::

   ネイティブ DLL（``IpatHelper.dll``）は 32bit / 64bit の両方がパッケージに同梱され、
   実行中の Python のビット数に応じて自動で読み込まれます。個別のインストールは不要です。

--------
共通仕様
--------

戻り値
======

全関数（``None`` を返すものを除く）は ``int`` をビットフラグとして返します。
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
   * - ``SUCCESS``
     - 1
     - 処理に成功
   * - ``UNSUCCESS``
     - 2
     - 処理に失敗（パラメータ不正・残高不足等）
   * - ``FAILED_CHUOU``
     - 4
     - 中央競馬での処理に失敗
   * - ``FAILED_CHIHOU``
     - 8
     - 地方競馬での処理に失敗
   * - ``FAILED_COMMUNICATE_CHUOU``
     - 16
     - 中央競馬との通信に失敗
   * - ``FAILED_COMMUNICATE_CHIHOU``
     - 32
     - 地方競馬との通信に失敗
   * - ``FAILED_OUT_OF_SERVICE``
     - 64
     - サービス時間外（``login()`` のみ。下記参照）

``FAILED_OUT_OF_SERVICE`` は ``login()`` でのみ立ち、``FAILED_CHUOU`` / ``FAILED_CHIHOU`` と
**併せて**\ 立ちます（どちらの会場かはそちらで判別してください）。
ログインページ自体は受信できたのに、ログインに必要な要素が含まれていなかったことを意味します。

- 最も多い原因は **投票受付時間外**\ です。特に地方競馬は営業時間外に必ずこの状態になります（不具合ではありません）。
- **メンテナンス中も同じ状態**\ になるため、両者は区別できません。
- このフラグが立った場合、**即座のリトライは必ず失敗します**\ 。時間をおいて再試行してください。
  ID・パスワード誤りや一時的な通信障害とは扱いを分けてください。

スレッドセーフ
==============

通信を伴う関数は DLL 内部の単一ロックで直列化されます。複数スレッドから同時に呼び出しても
壊れませんが、先行する呼び出しが完了するまでブロックします
（購入・入出金は通信と残高反映待ちを含むため、数分に及ぶことがあります）。

``get_bet_instance`` / ``get_bet_instance_win5`` は通信もグローバル状態の参照も行わない
純粋な入力変換のためロックを取りません。他の関数の通信中でも並行して呼び出せます。

DLL 内部で発生した例外は境界を越えず、すべて捕捉されて ``UNSUCCESS`` として返ります。

購入金額の上限
==============

1回の送信あたりの合計購入金額は **1,000,000円**\ （``MAX_TOTAL_AMOUNT_PER_SEND``）が上限です。
I-PAT 側でも同じ上限が課されており、
``bet`` / ``bet_win5`` / ``bet_win5_auto`` は送信前に検査し、超過する場合は
送信せずに ``UNSUCCESS`` を返します。

送信は **中央 255点／地方・WIN5 50点** ずつに自動分割され、上限はこの分割単位ごとに効きます。
1点だけでもこの上限が効くため、1点あたりの金額も実質 1,000,000円 が上限です。

前提条件
========

``bet`` ・ ``deposit`` ・ ``withdraw`` ・ ``get_purchase_data`` などの関数は、
事前に ``login()`` が成功している必要があります。
未ログイン状態での呼び出しは ``UNSUCCESS`` を返します。

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
   * - ``KAISAI_ASCOT``
     - アスコット（イギリス）

.. note::
   ``KAISAI_DEAUVILE``\ （``L`` が1つ）は綴りを誤った旧名です。
   ``KAISAI_DEAUVILLE`` と同じ値の別名として残していますが、新しいコードでは
   ``KAISAI_DEAUVILLE`` を使ってください。

   開催場の値は固定されており、開催場が追加される場合は必ず末尾へ追加されます。
   既存の値がずれることはありません。

式別（SHIKIBETSU）
==================

.. list-table::
   :header-rows: 1
   :widths: 34 16 50

   * - 定数名
     - 値
     - 式別
   * - ``SHIKIBETSU_WIN``
     - 1
     - 単勝
   * - ``SHIKIBETSU_PLACE``
     - 2
     - 複勝
   * - ``SHIKIBETSU_BRACKETQUINELLA``
     - 3
     - 枠連（買い目は馬番ではなく **枠番 1〜8**\ 。海外開催では購入不可）
   * - ``SHIKIBETSU_QUINELLA``
     - 4
     - 馬連
   * - ``SHIKIBETSU_QUINELLAPLACE``
     - 5
     - ワイド
   * - ``SHIKIBETSU_EXACTA``
     - 6
     - 馬単
   * - ``SHIKIBETSU_TRIO``
     - 7
     - 三連複
   * - ``SHIKIBETSU_TRIFECTA``
     - 8
     - 三連単
   * - ``SHIKIBETSU_WINPLACE``
     - 9
     - 応援馬券（同一馬の単勝＋複勝のセット）

**枠連（SHIKIBETSU_BRACKETQUINELLA）の注意点**

- 買い目は馬番ではなく **枠番（1〜8）** で指定します。9以上を指定すると ``UNSUCCESS`` で失敗します。
- **ゾロ目（同枠の2頭による決着）は同じ枠を2つ指定します**\ （``"3-3"``\ ）。
  通常方式で枠を1つだけ指定した ``"3"`` も同じ意味です。
- **ゾロ目が成立する枠かどうかは検証しません。** その枠に2頭以上いるかは出馬表を見ないと
  分からないためです。同枠のない枠でゾロ目を指定すると、購入時にサーバ側で失敗します。
- 海外開催では購入できません（``UNSUCCESS``\ ）。

**応援馬券（SHIKIBETSU_WINPLACE）の注意点**

- 方式は ``HOUSHIKI_NORMAL``\ （通常）\ **のみ**\ 、買い目は **1頭のみ**\ 指定できます（``"7"`` のように馬番ひとつ）。
  ボックス・フォーメーション・ながしは指定できません。
- **合計購入金額は指定金額の2倍**\ になります（100円指定 = 単勝100円 + 複勝100円）。点数も2点として数えます。
- 単勝と複勝の2点として購入されるため、**購入履歴には単勝と複勝が別々の馬券として現れます**\ 。
- 独立した2点として扱われるため、分割送信の境界で単勝と複勝が別チャンクに分かれ、
  通信失敗時に **片方だけが成立する可能性**\ があります。
- ``get_odds()`` にこの式別は指定できません（``UNSUCCESS``\ ）。単勝・複勝を個別に取得してください。

方式（HOUSHIKI）
================

.. list-table::
   :header-rows: 1
   :widths: 34 30 36

   * - 定数名
     - 方式
     - 買い目の指定
   * - ``HOUSHIKI_NORMAL``
     - 通常
     - 1点を指定
   * - ``HOUSHIKI_FORMATION``
     - フォーメーション
     - 各列に複数馬番
   * - ``HOUSHIKI_BOX``
     - ボックス
     - 1列に複数馬番（全組み合わせ）
   * - ``HOUSHIKI_WHEEL_1ST``
     - 軸1頭ながし（1着流し）
     - ``"軸-相手"``
   * - ``HOUSHIKI_WHEEL_2ND``
     - 2着ながし（馬単・三連単）
     - ``"軸-相手"``
   * - ``HOUSHIKI_WHEEL_3RD``
     - 3着ながし（三連単）
     - ``"軸-相手"``
   * - ``HOUSHIKI_WHEEL_1ST_2ND``
     - 軸2頭ながし（三連複）／1・2着ながし（三連単）
     - 三連複 ``"軸,軸-相手"`` ／三連単 ``"1着軸-2着軸-相手"``
   * - ``HOUSHIKI_WHEEL_1ST_3RD``
     - 1・3着ながし（三連単）
     - ``"1着軸-相手-3着軸"``
   * - ``HOUSHIKI_WHEEL_2ND_3RD``
     - 2・3着ながし（三連単）
     - ``"相手-2着軸-3着軸"``
   * - ``HOUSHIKI_WHEEL_MULTI_AXIS1``
     - 軸1頭ながしマルチ（馬単・三連単）
     - ``"軸-相手"``\ （全着順）
   * - ``HOUSHIKI_WHEEL_MULTI_AXIS2``
     - 軸2頭ながしマルチ（三連単のみ）
     - ``"軸-軸-相手"``\ （全着順）

.. note::

   ながし（``WHEEL_*``）／マルチ（``WHEEL_MULTI_*``）は「軸」と「相手」を列（``-`` 区切り）で指定します。
   列の意味は式別・方式によって変わります。マルチは馬単・三連単でのみ指定でき、購入すると
   ``ST_BET_DATA.Multi`` が ``1`` になります。中央・地方・海外すべての開催場で指定できます。

確定フラグ（DECISIONFLAG）
==========================

.. list-table::
   :header-rows: 1
   :widths: 45 10 45

   * - 定数名
     - 値
     - 意味
   * - ``DECISIONFLAG_PARSE_FAILED``
     - 0
     - **その明細を解析できなかった**\ （下記参照）
   * - ``DECISIONFLAG_DEFAULT``
     - 1
     - デフォルト
   * - ``DECISIONFLAG_NORMAL``
     - 2
     - 通常確定
   * - ``DECISIONFLAG_DEADLINE``
     - 3
     - 発売締切
   * - ``DECISIONFLAG_CANCEL``
     - 4
     - キャンセル
   * - ``DECISIONFLAG_FLATMATESCANCEL``
     - 5
     - 仲間入力取消
   * - ``DECISIONFLAG_HIT``
     - 6
     - 的中
   * - ``DECISIONFLAG_MISS``
     - 7
     - 外れ
   * - ``DECISIONFLAG_BACK``
     - 8
     - 返還
   * - ``DECISIONFLAG_PARTCANCEL``
     - 9
     - 一部取消
   * - ``DECISIONFLAG_INVALID``
     - 10
     - 無効
   * - ``DECISIONFLAG_SALECANCEL``
     - 11
     - 発売取消

``DECISIONFLAG_PARSE_FAILED``\ （0）は、その明細を解析できなかったことを表します。
通常の確定フラグは1始まりのため、この値が正常なフラグと衝突することはありません。
詳細は `購入明細の読み方`_ を参照してください。

券種（BETFLAG）
===============

``ST_TICKET_DATA_DETAIL.BetFlag`` の値です。

.. list-table::
   :header-rows: 1
   :widths: 45 10 45

   * - 定数名
     - 値
     - 意味
   * - ``BETFLAG_NORMAL``
     - 0
     - 通常
   * - ``BETFLAG_WIN5``
     - 1
     - WIN5
   * - ``BETFLAG_INTERNATIONAL``
     - 2
     - 海外（中央の購入履歴に混在します）

.. note::
   ``BETFLAG_INTERNAL`` は ``BETFLAG_INTERNATIONAL`` の旧名で、同じ値の別名として残しています。

その他の定数
============

購入日種類（DAYTYPE）は ``get_purchase_data()`` の結果に現れます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 定数名
     - 意味
   * - ``DAYTYPE_TODAY`` / ``DAYTYPE_BEFORE``
     - 購入日（当日 / 前日）
   * - ``WEEKDAY_SUNDAY`` 〜 ``WEEKDAY_SATURDAY``
     - 曜日（日曜=1 〜 土曜=7）
   * - ``ODDS_STATUS_NORMAL`` / ``ODDS_STATUS_CANCEL`` / ``ODDS_STATUS_UNACQUIRED``
     - オッズ状態（通常=0 / 発売中止=1 / オッズ未取得=2）
   * - ``RACE_STATUS_ON_SALE`` 〜 ``RACE_STATUS_UNKNOWN``
     - 発売状態（発売中=0 / 発売終了=1 / 発売中止=2 / 発売前=3 / 取得できなかった=0xFF）
   * - ``WIN5_AUTO_SELECT`` / ``WIN5_AUTO_RANDOM``
     - ``bet_win5_auto()`` の購入方式（セレクト=2 / ランダム=3）
   * - ``LOG_LEVEL_TRACE`` 〜 ``LOG_LEVEL_ERROR``
     - ``set_log_callback()`` のログレベル（0〜3）

上限・列数・既定値の定数:

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - 定数名
     - 値
     - 用途
   * - ``MAX_TOTAL_AMOUNT_PER_SEND``
     - 1000000
     - 1回の送信あたりの合計購入金額の上限（円）。1点あたりの上限も同じ値
   * - ``MAX_WIN5_AUTO_BET_COUNT``
     - 50
     - ``bet_win5_auto()`` で生成させられる点数の上限
   * - ``UMABAN_COLUMN_COUNT``
     - 3
     - ``ST_BET_DATA.Umaban`` の要素数
   * - ``UMABAN_TICKET_COLUMN_COUNT``
     - 5
     - 購入明細の ``HorseNo1`` 〜 ``HorseNo5``\ （WIN5 の5レース分を含む）
   * - ``WIN5_RACE_COUNT``
     - 5
     - WIN5 のレース数
   * - ``DEFAULT_RETRY_COUNT``
     - 10
     - ``deposit()`` / ``withdraw()`` のリトライ回数の既定値
   * - ``DEPOSIT_DEFAULT_VALUE``
     - 1000
     - ``set_auto_deposit_flag()`` の入金額（円）の既定値
   * - ``DEFAULT_CONFIRM_TIMEOUT``
     - 10000
     - 残高反映の確認タイムアウト（ms）の既定値
   * - ``DEFAULT_BET_INTERVAL``
     - 500
     - DLL 側の分割送信間隔（ms）の既定値
   * - ``DEFAULT_WAIT_TIME``
     - 1000
     - ``bet()`` / ``bet_win5()`` が既定で渡す分割送信間隔（ms）

.. note::
   分割送信の間隔は **タイムアウトではありません**\ 。
   DLL 側の既定値は ``DEFAULT_BET_INTERVAL``\ （500ms）ですが、本モジュールは
   より余裕を持たせた ``DEFAULT_WAIT_TIME``\ （1000ms）を既定で渡します。
   DLL と同じ値にしたい場合は ``DEFAULT_BET_INTERVAL`` を明示的に渡してください。

----------
データ構造
----------

ST_BET_DATA
===========

``get_bet_instance()`` で設定し、 ``bet()`` に渡す購入情報です。
フィールドを直接参照することで購入内容を確認できます。

.. code-block:: python

   betData = ST_BET_DATA()
   get_bet_instance(KAISAI_TOKYO, 11, 2026, 4, 5,
                    HOUSHIKI_NORMAL, SHIKIBETSU_WIN, 100, "1", betData)

   print(betData.TotalAmount)  # 合計購入金額（円）

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - フィールド名
     - 型
     - 説明
   * - ``Place``
     - int
     - 開催場（KAISAI 定数）
   * - ``RaceNo``
     - int
     - レース番号
   * - ``Youbi``
     - int
     - 曜日（WEEKDAY 定数。年月日から自動判定）
   * - ``Kaikata``
     - int
     - 方式（HOUSHIKI 定数。マルチ指定時は基底のながし方式へ変換される）
   * - ``Shikibetsu``
     - int
     - 式別（SHIKIBETSU 定数）
   * - ``Kingaku``
     - int
     - 1点あたりの購入金額（円）
   * - ``Umaban``
     - array
     - 買い目の各列を表すビットデータ（3列分）
   * - ``TotalAmount``
     - int
     - 合計購入金額（``get_bet_instance`` が自動計算）
   * - ``Multi``
     - int
     - マルチかどうか（0:通常 / 1:マルチ）。``HOUSHIKI_WHEEL_MULTI_*`` 指定時に 1 になる

ST_BET_DATA_WIN5
================

``get_bet_instance_win5()`` で設定し、 ``bet_win5()`` に渡す WIN5 専用の購入情報です。

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - フィールド名
     - 型
     - 説明
   * - ``Kingaku``
     - int
     - 1組み合わせあたりの購入金額（円）
   * - ``Youbi``
     - int
     - 曜日（WEEKDAY 定数）
   * - ``Umaban``
     - array
     - 5レース分の買い目を表すビットデータ

ST_PURCHASE_DATA
================

``get_purchase_data()`` が設定するルート構造体です。
ネイティブ側のメモリ解放は ``get_purchase_data()`` 内部で自動的に行われるため、
利用者側での解放処理は不要です（返却されるデータは Python 側にコピー済みです）。

``TicketData`` にはログイン済みの会場すべての馬券が **中央 → 地方の順に連結**\ されます。
残高・購入可能件数・当日/累計の金額は **合算しません**\ （中央・地方は同じ即PAT 口座を
共有するため、どちらか一方の値をそのまま返します）。詳細は `get_purchase_data`_ を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - フィールド名
     - 型
     - 説明
   * - ``AvailableBetCount``
     - int
     - 残購入可能件数
   * - ``Balance``
     - int
     - 現在残高（円）
   * - ``DayPurchase``
     - int
     - 当日累計購入金額（円）
   * - ``DayHaraimodosi``
     - int
     - 当日累計払戻金額（円）
   * - ``TotalPurchase``
     - int
     - 合計購入金額（円）
   * - ``TotalHaraimodosi``
     - int
     - 合計払戻金額（円）
   * - ``TicketCount``
     - int
     - 馬券情報の件数
   * - ``TicketData``
     - array
     - 馬券情報の配列（下記参照）

``TicketData`` の各要素（ST_TICKET_DATA）:

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - フィールド名
     - 型
     - 説明
   * - ``DayFlag``
     - int
     - 購入日（1:当日 / 2:前日）
   * - ``ReceiptNo``
     - int
     - 受付番号
   * - ``Hour``
     - int
     - 購入時刻（時）。時刻を読み取れなかった受付では 0
   * - ``Minute``
     - int
     - 購入時刻（分）。時刻を読み取れなかった受付では 0
   * - ``Kingaku``
     - int
     - 購入金額（円）
   * - ``Payout``
     - int
     - 払戻金額（円）
   * - ``DetailCount``
     - int
     - 詳細情報の件数
   * - ``DetailData``
     - array
     - 詳細情報の配列（下記参照）

``DetailData`` の各要素（ST_TICKET_DATA_DETAIL）:

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - フィールド名
     - 型
     - 説明
   * - ``DecisionFlag``
     - int
     - 確定フラグ（DECISIONFLAG 定数）。0 は **その明細を解析できなかった**
   * - ``BetFlag``
     - int
     - 券種（BETFLAG 定数。通常=0 / WIN5=1 / 海外=2）
   * - ``Kaisai``
     - int
     - 開催場（KAISAI 定数）。WIN5 の明細では 0xFF
   * - ``RaceNo``
     - int
     - レース番号。WIN5 の明細では 0xFF
   * - ``Week``
     - int
     - 開催週。WIN5 の明細では 0xFF
   * - ``Method``
     - int
     - 方式（HOUSHIKI 定数）。WIN5 の明細では 0xFF
   * - ``Type``
     - int
     - 式別（SHIKIBETSU 定数）。WIN5 の明細では 0xFF
   * - ``HorseNo1`` 〜 ``HorseNo5``
     - int
     - 買い目の各列を表すビットデータ（WIN5 を含めるため 5 列分）
   * - ``Multi``
     - int
     - マルチ購入フラグ（1: マルチあり）

.. warning::
   ``HorseNo1`` 〜 ``HorseNo5`` の各列が何を指すかは ``Method``\ （方式）と ``Type``\ （式別）の
   組み合わせで変わります。**列を機械的に "-" で連結すると誤った買い目になります。**
   `購入明細の読み方`_ の対応表に従ってください。

----------------
関数リファレンス
----------------

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
   * - 受付時間外・メンテナンス中
     - 上記に加えて ``FAILED_OUT_OF_SERVICE``
   * - 既ログイン
     - ``UNSUCCESS``

.. code-block:: python

   ret = login(inet_id, id, password, pars)

   if (ret & SUCCESS) == 0:
       if (ret & FAILED_OUT_OF_SERVICE) != 0:
           # 受付時間外・メンテナンス中。即時リトライは必ず失敗する
           print("サービス時間外です。時間をおいて再試行してください")
       else:
           print("ログイン失敗")

.. note::
   ``FAILED_OUT_OF_SERVICE`` は ``FAILED_CHUOU`` / ``FAILED_CHIHOU`` と併せて立ちます。
   **地方競馬は営業時間外に必ずこの状態になります**\ （不具合ではありません）。
   即座のリトライは必ず失敗するため、ID・パスワード誤りや通信障害とは扱いを分けてください。

logout
======

I-PAT からログアウトします。自動入金設定もリセットされます。

.. code-block:: python

   ret = logout()  # -> int

- ログアウト後、再度 ``login()`` を呼び出すまで他の関数は使用できません。

deposit
=======

登録口座から I-PAT 残高へ入金します。

.. code-block:: python

   ret = deposit(depositValue, retryCount=DEFAULT_RETRY_COUNT)

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 引数
     - 型
     - 説明
   * - ``depositValue``
     - int
     - 入金額（円）。100円以上かつ100円単位。
   * - ``retryCount``
     - int
     - **準備段階のみ** のリトライ回数。デフォルト: 10回（``DEFAULT_RETRY_COUNT``）。

- 入金指示の完了後、入金額が残高へ加算されたことを確認できるまで待機し、
  **反映を確認できた場合のみ成功** を返します。
  ``set_auto_deposit_flag()`` の ``confirmTimeout``\ （既定 10 秒）以内に反映されない場合は失敗です。
- 中央競馬へのログインが有効な場合は中央を優先し、失敗時は地方へフォールバックします。
  ただし入金の実行に進んだ後は、その系統で失敗しても地方へフォールバックしません。
- 登録口座の金融機関は自動的に判定します
  （取得できない場合のみ、対応金融機関のコードを順に試行します）。

.. note::

   金額は **100円以上かつ100円単位** で指定してください。
   条件を満たさない場合は ``UNSUCCESS`` を返します。

.. warning::

   ``retryCount`` が適用されるのは **入金の実行前の準備段階**
   のみです。
   入金実行そのものは、応答を受信できなかった場合でもサーバ側で成立している可能性があるため
   **再送しません**\ （二重入金の防止）。この場合は残高への反映で成否を判定します。

.. warning::

   入出金は **即PAT（ネットバンク）会員専用** です。
   A-PAT 会員は入金 URL が存在しないため
   ``UNSUCCESS`` を返します。会員種別は自動判定されます。

.. warning::

   **登録口座が PayPay（コード決済アプリ）の場合は利用できません。**
   通信を行わず ``UNSUCCESS`` を返します。入金は PayPay アプリ側で操作してください。

   **PayPay** *銀行* **は従来どおり利用できます。** 拒否されるのは PayPay *アプリ* を
   登録口座にしている会員だけです（両者は別物です）。

withdraw
========

I-PAT 残高を登録口座へ全額出金します。

.. code-block:: python

   ret = withdraw(retryCount=DEFAULT_RETRY_COUNT)

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 引数
     - 型
     - 説明
   * - ``retryCount``
     - int
     - **準備段階のみ** のリトライ回数。デフォルト: 10回（``DEFAULT_RETRY_COUNT``）。

- 出金額の指定は不要です。残高の全額が出金対象となります。
- 出金指示の完了後、**残高が 0 になったことを確認できた場合のみ成功** を返します。
  ``confirmTimeout`` 以内に反映されない場合は失敗です。
- リトライの適用範囲・二重出金の防止・即PAT 会員専用・PayPay（アプリ）非対応である点は
  ``deposit()`` と同じです。

.. note::

   入出金は機械可読なエラーコードを返しません。**失敗の原因を知るには**
   ``set_log_callback()`` **が必須です。**

   ``LOG_LEVEL_ERROR`` を指定すると、どの段階で失敗したか（入金ページの取得 / 確認 /
   実行 / 実行後の完了画面確認）、応答を受信できたかどうか、着地した画面の ID とタイトル、
   残高反映待機の実測値（経過時間・確認回数・タイムアウト設定値）が通知されます。
   タイムアウトしていた場合は「反映が遅いだけ」の可能性があるため、
   ``confirmTimeout`` を延ばして解消するか確認できます。

   さらに ``LOG_LEVEL_TRACE`` を指定すると、サーバ側の拒否理由（時間外・パスワード誤り・
   メンテナンス等）を含む **応答本文の抜粋** も通知されます。
   ただし抜粋には **口座番号や残高が含まれることがあります**\ 。
   調査時のみ指定し、ログの取り扱いにご注意ください。

set_auto_deposit_flag
=====================

馬券購入前の残高不足時に自動で入金を行う機能を設定します。
有効化すると ``bet()`` / ``bet_win5()`` 実行時に残高不足が検出された場合、自動的に入金してから購入を行います。

.. code-block:: python

   ret = set_auto_deposit_flag(enable, depositValue=DEPOSIT_DEFAULT_VALUE,
                               confirmTimeout=DEFAULT_CONFIRM_TIMEOUT)

.. list-table::
   :header-rows: 1
   :widths: 25 10 65

   * - 引数
     - 型
     - 説明
   * - ``enable``
     - bool
     - ``True`` で有効化、``False`` で無効化
   * - ``depositValue``
     - int
     - 自動入金額（円、100円単位）。デフォルト: 1,000（``DEPOSIT_DEFAULT_VALUE``）
   * - ``confirmTimeout``
     - int
     - 残高反映の確認タイムアウト（ms）。デフォルト: 10,000（``DEFAULT_CONFIRM_TIMEOUT``）

- 入金後、残高への反映を最大 ``confirmTimeout`` ms 待機します。タイムアウトした場合は購入を中止します。
- 入金しても残高が購入金額に満たない場合は、入金を行わず ``UNSUCCESS`` を返します。
- ``depositValue`` は ``enable=False`` の場合は検証されません。
- ``confirmTimeout`` は自動入金だけでなく、``deposit()`` / ``withdraw()`` の
  **残高反映待ちにも使用されます**\ 。反映が遅い環境では延長してください。
- 自動入金は ``deposit()`` と同じ経路を使うため、**即PAT 会員専用**\ ・
  **PayPay（アプリ）非対応** という制約もそのまま当てはまります。
- ``logout()`` を呼び出すと設定はリセットされます。

get_bet_instance
================

買い目文字列を解析し、 ``bet()`` に渡す``ST_BET_DATA`` を構築します。

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
     - 1点あたりの購入金額（円、100円単位）。100円以上 1,000,000円以下
   * - ``kaime``
     - str
     - 買い目文字列（書式は後述）
   * - ``betData``
     -
     - [out] ST_BET_DATA インスタンス

成功すると ``betData.TotalAmount`` に合計購入金額が格納されます。

- 馬番は **1〜18**\ （海外開催は 1〜24）の範囲で指定してください。
  範囲外の馬番が含まれる場合、その馬番を無視するのではなく ``UNSUCCESS`` を返します
  （指定より少ない点数で購入されるのを防ぐためです）。
- **海外開催では枠連（**\ ``SHIKIBETSU_BRACKETQUINELLA``\ **）を購入できません。**
  海外競馬に枠の概念が無いため、指定すると ``UNSUCCESS`` を返します。
- 合計購入金額の上限については「`購入金額の上限`_」を参照してください。
- 本関数は通信もグローバル状態の参照も行わないため内部ロックを取りません。
  ``bet()`` などの通信中でも並行して呼び出せます。

買い目文字列の書式
------------------

- 列の区切り: ``-`` （ハイフン）
- 同一列内の複数馬番の区切り: ``,`` （カンマ）

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

ながし・マルチは ``houshiki`` に ``HOUSHIKI_WHEEL_*`` / ``HOUSHIKI_WHEEL_MULTI_*`` を指定します。

.. code-block:: text

   三連単 1着ながし    軸=1 / 相手=2,3,4    HOUSHIKI_WHEEL_1ST         -> "1-2,3,4"   （6点）
   三連単 1・2着ながし 1着軸=1 / 2着軸=2 / 相手=3,4  HOUSHIKI_WHEEL_1ST_2ND -> "1-2-3,4"
   馬連 ながし         軸=1 / 相手=2,3,4    HOUSHIKI_WHEEL_1ST         -> "1-2,3,4"
   三連単 軸1頭マルチ  軸=1 / 相手=2,3,4    HOUSHIKI_WHEEL_MULTI_AXIS1 -> "1-2,3,4"   （全着順18点）
   三連単 軸2頭マルチ  軸=1,2 / 相手=3,4    HOUSHIKI_WHEEL_MULTI_AXIS2 -> "1-2-3,4"

枠連は馬番ではなく **枠番（1〜8）** で指定します。ゾロ目は同じ枠を2つ（``"3-3"``\ ）。
応援馬券は **通常方式・1頭のみ**\ （``"7"``\ ）です。詳細は
`式別（SHIKIBETSU）`_ を参照してください。

bet
===

``get_bet_instance()`` で構築した ``ST_BET_DATA`` の配列を一括購入します。
開催場に応じて中央・地方・海外に自動で振り分けられます。

.. code-block:: python

   betDataList = (ST_BET_DATA * n)()
   betDataList[0] = betData
   ret = bet(betDataList, n, waitMiliSeconds=DEFAULT_WAIT_TIME)

.. list-table::
   :header-rows: 1
   :widths: 25 10 65

   * - 引数
     - 型
     - 説明
   * - ``betDataList``
     -
     - ST_BET_DATA の配列（``(ST_BET_DATA * n)()`` で作成）
   * - ``listCount``
     - int
     - 配列の要素数
   * - ``waitMiliSeconds``
     - int
     - 分割購入時のリクエスト間隔（ms）。デフォルト: 1,000（``DEFAULT_WAIT_TIME``）

- 購入件数が1回の上限（**中央 255件 / 地方 50件**\ ）を超える場合、自動的に分割して購入します。
  ``waitMiliSeconds`` はこの分割送信の間隔です。
- 開催場に応じて中央・地方・海外の適切なエンドポイントへ自動的に振り分けます。
- 購入前に残高と購入可能件数を確認します。自動入金が有効な場合は残高不足時に自動入金します。
- 1回の送信あたりの合計購入金額が 1,000,000円 を超える場合は、送信せずに ``UNSUCCESS`` を返します。

.. note::

   ``waitMiliSeconds`` が短すぎると購入に失敗する場合があります。
   ネットワーク環境に応じて調整してください。

get_bet_instance_win5
=====================

WIN5 の買い目文字列を解析し、 ``bet_win5()`` に渡す``ST_BET_DATA_WIN5`` を構築します。

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
     - 1組み合わせあたりの購入金額（円、100円単位）。100円以上 1,000,000円以下
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

WIN5 の買い目文字列は必ず **5レース分** を ``-`` で区切って指定してください。
馬番は 1〜18 の範囲です。

.. code-block:: text

   各レース1頭ずつ              -> "1-2-3-4-5"
   一部のレースで複数頭指定     -> "1,2-3-4,5-6-7,8"

- ``get_bet_instance()`` と同じく内部ロックを取りません。

bet_win5
========

``get_bet_instance_win5()`` で構築した ``ST_BET_DATA_WIN5`` を使って WIN5 を購入します。

.. code-block:: python

   ret = bet_win5(betDataWin5, waitMiliSeconds=DEFAULT_WAIT_TIME)

.. list-table::
   :header-rows: 1
   :widths: 25 10 65

   * - 引数
     - 型
     - 説明
   * - ``betDataWin5``
     -
     - ST_BET_DATA_WIN5 インスタンス
   * - ``waitMiliSeconds``
     - int
     - 分割購入時のリクエスト間隔（ms）。デフォルト: 1,000（``DEFAULT_WAIT_TIME``）

- 1回の購入上限（**50 組み合わせ**\ ）を超える場合は自動的に分割購入します。

.. note::

   WIN5 は **中央競馬でのみ購入可能** です。
   地方競馬のみにログインしている場合は ``UNSUCCESS`` を返します。

get_purchase_data
=================

当日・前日の馬券購入履歴（残高・累計金額・購入済み馬券一覧）を取得します。

.. code-block:: python

   purchaseData = ST_PURCHASE_DATA()
   ret = get_purchase_data(purchaseData)
   if (ret & 1) == 1:
       print(f"残高: {purchaseData.Balance} 円")
       for i in range(purchaseData.TicketCount):
           ticket = purchaseData.TicketData[i]
           print(f"受付No.{ticket.ReceiptNo} {ticket.Hour:02d}:{ticket.Minute:02d} {ticket.Kingaku}円")

       # 履歴の欠けを検出したい場合は、SUCCESS と同時に立つ失敗フラグも見る
       if (ret & FAILED_CHUOU) != 0:
           print("※中央の履歴が欠けています")
       if (ret & FAILED_CHIHOU) != 0:
           print("※地方の履歴が欠けています")

**中央と地方の両方に投票した場合**

購入履歴は会場ごとに別々に保持されているため、**ログイン済みの会場すべてから取得して連結**\ します。
中央と地方の両方へ投票した購入も、1回の ``get_purchase_data()`` で両方の馬券が得られます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 項目
     - 扱い
   * - 馬券（``TicketData``\ ）
     - 中央 → 地方の順に連結（各会場内は前日 → 当日）
   * - 残高・購入可能件数・当日/累計の金額
     - **合算しません。** 中央・地方は同じ即PAT 口座を共有するため、どちらか一方の値をそのまま返します
   * - 海外の馬券
     - 中央の履歴に含まれます（明細の ``BetFlag`` が ``BETFLAG_INTERNATIONAL``\ ）

- **片方の会場だけ取得に失敗した場合は、取得できた分を返したうえで** ``FAILED_CHUOU`` /
  ``FAILED_CHIHOU`` を立てます。この場合 ``SUCCESS`` と **同時に**\ 立つため、
  履歴の欠けを検出したいときはこれらのフラグも確認してください。
  両方失敗した場合のみ ``SUCCESS`` は立ちません。
- 受付時刻を読み取れなかった受付は、その受付を捨てるのではなく ``Hour`` / ``Minute`` が
  ``0`` のまま返されます。金額・明細は正常です。

.. warning::

   明細（``ST_TICKET_DATA_DETAIL``\ ）から買い目を復元する方法は `購入明細の読み方`_ を
   参照してください。**列を機械的に "-" で連結すると誤った買い目になります。**

.. note::

   ネイティブ側で確保されたメモリは ``get_purchase_data()`` 内部で自動的に解放されます。
   利用者側での解放処理は不要です（返却される ``ST_PURCHASE_DATA`` は Python 側にコピー済みです）。

get_odds
========

指定レース・式別のオッズを取得します（**中央競馬・地方競馬・海外競馬に対応**）。
単勝・複勝は基本オッズ、枠連〜三連単は全通りのオッズ表を取得します
（三連単18頭なら 4,896 点）。

.. code-block:: python

   oddsData = ST_ODDS_DATA()
   ret = get_odds(place, race_no, shikibetsu, oddsData)

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
   * - ``shikibetsu``
     - int
     - 式別（SHIKIBETSU 定数）
   * - ``oddsData``
     -
     - [out] ST_ODDS_DATA インスタンス

- ネイティブ側のメモリは関数内部で自動解放されます。利用者側での解放は不要です。
- オッズは 10 倍の整数（``Odds``）で格納されます。実際の倍率は ``Odds / 10.0``。
- 複勝・ワイドは下限を ``Odds``、上限を ``OddsHigh`` に格納します。
- ``Status`` が 1（発売中止）／2（オッズ未取得）の場合、``Odds`` / ``OddsHigh`` は 0 です。
- 全式別に対応します。開催場によって発売のない式別（地方の枠連等）は、
  サーバ側のエラーまたは明細 0 件になります。
- **応援馬券（**\ ``SHIKIBETSU_WINPLACE``\ **）はオッズの式別ではないため指定できません**\ （``UNSUCCESS``\ ）。
  単勝・複勝を個別に取得してください。
- **海外開催にも対応しています。** ただし **中央競馬へのログインが必要** で、
  海外競馬に枠は無いため **枠連を指定すると** ``UNSUCCESS`` **を返します**\ 。
  取得できるオッズの内容は中央・地方と同じです。
- 指定した開催場が **その日開催されていない場合は** ``UNSUCCESS`` を返します。

``oddsData.OddsDetail`` の各要素（ST_ODDS_DETAIL）:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド名
     - 説明
   * - ``Type``
     - 式別（SHIKIBETSU 定数）
   * - ``Horse1`` / ``Horse2`` / ``Horse3``
     - 馬番/枠番（単複は1頭、馬連・ワイド・馬単・枠連は2頭、三連系は3頭）
   * - ``Status``
     - 0:通常 1:発売中止 2:オッズ未取得
   * - ``Odds`` / ``OddsHigh``
     - オッズ×10（複勝・ワイドは下限/上限）

.. code-block:: python

   oddsData = ST_ODDS_DATA()
   ret = get_odds(KAISAI_TOKYO, 11, SHIKIBETSU_QUINELLA, oddsData)
   if (ret & 1) == 1:
       print(f"オッズ更新時刻: {oddsData.OddsTime} / 明細数: {oddsData.DetailCount}")
       for d in oddsData.OddsDetail:
           kaime = str(d.Horse1)
           if d.Horse2:
               kaime += "-" + str(d.Horse2)
           if d.Horse3:
               kaime += "-" + str(d.Horse3)
           odds = f"{d.Odds / 10.0:.1f}" if d.Status == 0 else "-"
           print(f"  {kaime} : {odds}")

get_race_card
=============

指定レースの出馬表（出走馬一覧）を取得します（**中央競馬・地方競馬・海外競馬に対応**）。
各出走馬の枠番・馬番・馬名・性齢・馬体重・騎手・斤量・調教師・単勝人気・単勝/複勝オッズを取得します。

.. code-block:: python

   raceCard = ST_RACECARD_DATA()
   ret = get_race_card(place, race_no, raceCard)

- ネイティブ側のメモリは関数内部で自動解放されます。利用者側での解放は不要です。
- ``raceCard.EntryData`` の各要素は ``ST_ENTRY_DETAIL`` です。
- ``raceCard.RaceName`` はレース名（**UTF-8 の文字列**）です。取得できない場合は空文字です。
- ``raceCard.Deadline`` は**発売締切時刻**（``"HH:MM"``）です。取得できない場合は空文字です。
- ``raceCard.RaceStatus`` はそのレースの**発売状態**です（``RACE_STATUS_ON_SALE`` =0 発売中 / ``RACE_STATUS_CLOSED`` =1 発売終了 / ``RACE_STATUS_CANCELED`` =2 発売中止 / ``RACE_STATUS_BEFORE_SALE`` =3 発売前 / ``RACE_STATUS_UNKNOWN`` =0xFF 取得できなかった）。締切時刻だけでは購入可否が判断できないため併せて参照してください。
- ``RaceName`` ・ ``Deadline`` ・ ``RaceStatus`` の取得に **追加の通信は発生しません**\ 。
- 馬名・騎手名・調教師名などの文字列フィールドは **UTF-8 の bytes** です。利用時は ``.decode('utf-8')`` してください。
- 斤量・オッズは 10 倍の整数で格納されます。実際の値は ``/ 10.0``。
- 指定した開催場が **その日開催されていない場合は** ``UNSUCCESS`` を返します。

.. note::

   **海外開催について** — I-PAT が返す項目が国内より少なく、取得できるのは
   ``Umaban`` ・ ``HorseName`` ・ ``WinPopular`` ・単勝/複勝オッズと、
   ``RaceName`` ・ ``Deadline`` ・ ``RaceStatus`` です。
   海外競馬には枠・性齢・馬体重・斤量・調教師などの概念が無いため、
   ``Wakuban`` ・ ``Sex`` ・ ``Age`` ・ ``Weight`` ・ ``JockeyName`` ・ ``Burden`` ・
   ``TrainerName`` は **0 または空 bytes** になります。
   また海外開催は **中央競馬へのログインが必要** です。

``raceCard.EntryData`` の各要素（ST_ENTRY_DETAIL）:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド名
     - 説明
   * - ``Wakuban`` / ``Umaban``
     - 枠番 / 馬番
   * - ``HorseName`` / ``Sex`` / ``Age``
     - 馬名(bytes) / 性別(bytes) / 年齢
   * - ``WeightStatus`` / ``Weight`` / ``WeightDiffCode`` / ``WeightDiff``
     - 馬体重の状態(0:通常 1:未発表 2:出走取消 3:計量不能) / 重量(kg) / 増減符号 / 増減量
   * - ``Apprentice``
     - 見習騎手コード(0:なし 1〜5:減量 9:女性騎手2kg減)
   * - ``JockeyName`` / ``Burden`` / ``TrainerName``
     - 騎手名(bytes) / 斤量×10 / 調教師名(bytes)
   * - ``WinPopular``
     - 単勝人気(0:データなし)
   * - ``WinOddsStatus`` / ``WinOdds``
     - 単勝オッズの状態(0:通常 1:発売中止 2:未取得) / オッズ×10
   * - ``PlaceOddsStatus`` / ``PlaceOddsLow`` / ``PlaceOddsHigh``
     - 複勝オッズの状態 / 下限×10 / 上限×10

.. code-block:: python

   raceCard = ST_RACECARD_DATA()
   ret = get_race_card(KAISAI_TOKYO, 11, raceCard)
   if (ret & 1) == 1:
       print(f"レース名: {raceCard.RaceName}")
       print(f"締切: {raceCard.Deadline} / 発売状態: {raceCard.RaceStatus}")
       print(f"オッズ更新時刻: {raceCard.OddsTime} / 出走頭数: {raceCard.EntryCount}")
       for e in raceCard.EntryData:
           name = e.HorseName.decode('utf-8')
           sex = e.Sex.decode('utf-8')
           jockey = e.JockeyName.decode('utf-8')
           win = f"{e.WinOdds / 10.0:.1f}" if e.WinOddsStatus == 0 else "-"
           print(f"  {e.Umaban:2d}番 {name} {sex}{e.Age} "
                 f"斤量{e.Burden / 10.0:.1f} 騎手:{jockey} 単勝:{win} 人気:{e.WinPopular}")

get_notice
==========

現在有効なお知らせを取得します（**中央競馬・地方競馬に対応**）。
強制表示お知らせ本文（``Message``）に加え、お知らせ一覧（``ItemData``）を全件取得します。

.. code-block:: python

   notice = ST_NOTICE_DATA()
   ret = get_notice(notice)

- ログイン済みのセッションが必要です（**中央を優先し、失敗時は地方へフォールバック**\ します）。
- ネイティブ側のメモリは関数内部で自動解放されます。利用者側での解放は不要です。
- ``notice.ItemData`` の各要素は ``ST_NOTICE_ITEM`` です。
- ``Title`` / ``Date`` / ``Url`` などの文字列フィールドは **UTF-8 の bytes** です。利用時は ``.decode('utf-8')`` してください。
- お知らせが無い場合は ``Message`` が空文字・``ItemCount`` が 0 で成功します。
- ``Message`` は HTML を含むことがあり、**2048 バイトで打ち切られます**\ （``Title`` は 512 バイト、``Url`` は 1024 バイト）。
  古い版の DLL では打ち切り位置が文字の途中になることがあり、``.decode('utf-8')`` が
  ``UnicodeDecodeError`` になる場合があります。最新版へ更新するか、
  ``.decode('utf-8', errors='replace')`` で安全に読み取ってください。

``notice.ItemData`` の各要素（ST_NOTICE_ITEM）:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド名
     - 説明
   * - ``Title`` / ``Date``
     - タイトル(bytes) / 日付テキスト(bytes)
   * - ``Url`` / ``Icon`` / ``Color``
     - リンクURL(bytes) / アイコン(bytes) / 日付表示色(bytes)

.. code-block:: python

   notice = ST_NOTICE_DATA()
   ret = get_notice(notice)
   if (ret & 1) == 1:
       if notice.Message:
           print(f"強制表示: {notice.Message}")
       print(f"お知らせ {notice.ItemCount} 件")
       for item in notice.ItemData:
           title = item.Title.decode('utf-8')
           date = item.Date.decode('utf-8')
           url = item.Url.decode('utf-8')
           print(f"  [{date}] {title}  {url}")

bet_win5_auto
=============

WIN5 を「セレクト」または「ランダム」で購入します。買い目を指定する ``bet_win5`` と違い、
**買い目はサーバが生成**\ します。

.. code-block:: python

   bet_win5_auto(mode, axisUmaban, betCount, kingaku, year, month, day)

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 方式
     - 動作
   * - ``WIN5_AUTO_SELECT`` (2)
     - ``axisUmaban`` で軸馬を指定し、``0`` にしたレースはサーバが選ぶ
       （``0`` **にできるのは 1〜4 レース**\ ）
   * - ``WIN5_AUTO_RANDOM`` (3)
     - 5 レースすべてサーバが選ぶ（``axisUmaban`` は ``None`` で可）

- **生成された買い目はそのまま購入されます。** 内容を事前に確認する手段はないため、
  呼び出す前に必ず利用者の確認を取ってください。
- **セレクトは「一部のレースだけ軸を決めて、残りをサーバに選ばせる」方式です。**
  ``0``\ （おまかせ）にするレース数は **1〜4** でなければならず、
  次の 2 つは送信せずに ``UNSUCCESS`` を返します。

  .. list-table::
     :header-rows: 1
     :widths: 25 20 55

     * - 指定
       - 例
       - 理由
     * - 全レース ``0``
       - ``"0,0,0,0,0"``
       - ランダムと同じになりセレクトの意味がありません。``WIN5_AUTO_RANDOM`` を使ってください
     * - ``0`` が1つも無い
       - ``"3,7,1,5,2"``
       - 買い目が1通りに決まり、依頼した点数を生成できません。``bet_win5`` で直接指定してください

- 点数の上限は 50 点（``MAX_WIN5_AUTO_BET_COUNT``）で、``bet_win5`` と違い **分割送信は行いません**\ 。
- 合計金額はサーバが生成した買い目から算出され、1,000,000 円（``MAX_TOTAL_AMOUNT_PER_SEND``）を
  超える場合は送信せずに ``UNSUCCESS`` を返します。
- WIN5 は中央競馬のみ対応です。

.. code-block:: python

   from ipathelper import bet_win5_auto, WIN5_AUTO_SELECT, WIN5_AUTO_RANDOM

   # ランダムで 10 点 × 100円
   ret = bet_win5_auto(WIN5_AUTO_RANDOM, None, 10, 100, 2026, 8, 9)

   # セレクト: 1R の軸だけ決めて 20 点 × 100円
   ret = bet_win5_auto(WIN5_AUTO_SELECT, "6,0,0,0,0", 20, 100, 2026, 8, 9)

set_log_callback
================

DLL 内部のログを受け取るハンドラを登録します（``None`` で解除）。
**Release ビルドの DLL でも取得できます。**

.. code-block:: python

   set_log_callback(handler, minLevel=LOG_LEVEL_INFO)

**入出金の失敗調査にはこの API が必須です。** 入出金はサーバレンダリングの HTML フォームで、
``erc`` / ``erm`` のような機械可読なエラーコードを返しません。失敗した段階・画面 ID・
画面タイトルは ``LOG_LEVEL_ERROR`` で通知されますが、**サーバ側の拒否理由が載る
応答本文の抜粋は** ``LOG_LEVEL_TRACE`` **を指定したときのみ**\ 通知されます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ログレベル
     - 説明
   * - ``LOG_LEVEL_TRACE``
     - 詳細トレース。**入出金失敗時の応答本文の抜粋はこのレベルのみ**
   * - ``LOG_LEVEL_INFO``
     - 情報（既定）
   * - ``LOG_LEVEL_WARN``
     - 警告
   * - ``LOG_LEVEL_ERROR``
     - エラー。失敗した段階・画面 ID・タイトルはこのレベル

- ハンドラは ``handler(level: int, message: str)`` の形で呼ばれます。
  ``message`` は UTF-8 からデコード済みの ``str`` です（他の API の bytes と異なります）。
- ハンドラは **DLL 内部ロックを保持したまま**\ 呼ばれます。
  **ハンドラ内から本モジュールの API を呼び返さないでください**\ （デッドロックします）。
- ``login`` 実行中は中央・地方の **2 スレッドから同時に**\ 呼ばれます。
- ``None`` を渡して戻った時点で実行中のハンドラは存在しないため、対象を安全に破棄できます。
- 応答本文の抜粋には\ **口座番号や残高が含まれ得ます**\ 。``LOG_LEVEL_TRACE`` は調査時のみ指定し、
  ログの取り扱いに注意してください。

.. code-block:: python

   from ipathelper import set_log_callback, LOG_LEVEL_INFO, LOG_LEVEL_TRACE

   def on_log(level, message):
       print(f"[{level}] {message}")

   set_log_callback(on_log, LOG_LEVEL_INFO)   # 調査時は LOG_LEVEL_TRACE

   # ... 各 API を実行 ...

   set_log_callback(None)                      # 解除してからハンドラの対象を破棄する

------------------
購入明細の読み方
------------------

``get_purchase_data()`` が返す ``ST_TICKET_DATA_DETAIL`` は、
**購入時の指定そのものではなく、投票内容から復元した値**\ です。
``HorseNo1`` 〜 ``HorseNo5`` の各列が何を指すかは ``Method``\ （方式）と ``Type``\ （式別）の
**組み合わせで変わります。** 列を機械的に ``-`` で連結すると誤った買い目になります。

HorseNo のビット表現
====================

- **bit 0 が馬番 1**\ 、bit 1 が馬番 2 … と続きます。判定は
  ``(horse_no & (1 << (馬番 - 1))) != 0`` です。
- **枠連（**\ ``SHIKIBETSU_BRACKETQUINELLA``\ **）だけは馬番ではなく枠番**\ で、
  bit 0 が枠 1、bit 7 が枠 8 です。
- 有効なビットの範囲は **国内 18 頭 / 海外 24 頭 / 枠連 8 枠**\ 。範囲外のビットは立ちません。
- **使わない列は 0** です。``0`` は「指定なし」ではなく「その方式・式別には存在しない列」を
  意味します。列がいくつあるかは必ず下表で判断してください。
- ``HorseNo4`` と ``HorseNo5`` は **WIN5 専用**\ です。WIN5 以外の明細では常に 0 で、
  使うのは ``HorseNo1`` 〜 ``HorseNo3`` だけです。

.. code-block:: python

   def umaban(mask, max_no=18):
       '''1つの列から馬番の一覧を取り出す'''
       return [n for n in range(1, max_no + 1) if mask & (1 << (n - 1))]

Method / Type とマルチ
======================

``Method`` は HOUSHIKI、``Type`` は SHIKIBETSU と同じ数値です。

.. warning::

   **マルチの判定は必ず** ``Multi`` **で行ってください。** ``Method`` **では判定できません。**
   マルチは基底のながし方式（軸1頭 = 3 / 軸2頭 = 6）のまま記録されることがあるため、
   購入明細では **方式が 3 / 6 のまま** ``Multi = 1`` という形と、
   **方式が 9 / 10** という形の **両方があり得ます**\ 。どちらも同じ買い目です。

**応援馬券（**\ ``SHIKIBETSU_WINPLACE`` **= 9）は** ``Type`` **に現れません。**
単勝＋複勝の2点として購入されるため、履歴には ``Type`` が 1（単勝）と 2（複勝）の
別々の馬券として並びます。

HorseNo の列の意味（方式 × 式別）
=================================

``—`` は使用しない列（常に 0）です。

**通常（Method = 0）**

.. list-table::
   :header-rows: 1
   :widths: 34 22 22 22

   * - 式別
     - ``HorseNo1``
     - ``HorseNo2``
     - ``HorseNo3``
   * - 単勝(1) / 複勝(2)
     - 馬 1 頭
     - —
     - —
   * - 枠連(3)
     - 枠 2 つ（**ゾロ目は 1 つだけ**\ ）
     - —
     - —
   * - 馬連(4) / ワイド(5)
     - 馬 2 頭（順不同なので同じ列）
     - —
     - —
   * - 馬単(6)
     - 1 着馬
     - 2 着馬
     - —
   * - 三連複(7)
     - 馬 3 頭（順不同なので同じ列）
     - —
     - —
   * - 三連単(8)
     - 1 着馬
     - 2 着馬
     - 3 着馬

**フォーメーション（Method = 1）**

.. list-table::
   :header-rows: 1
   :widths: 34 22 22 22

   * - 式別
     - ``HorseNo1``
     - ``HorseNo2``
     - ``HorseNo3``
   * - 枠連(3)
     - 1 枠目群
     - 2 枠目群
     - **同枠（ゾロ目）群** ← 枠の選択ではない
   * - 馬連(4) / ワイド(5) / 馬単(6)
     - 1 列目
     - 2 列目
     - —
   * - 三連複(7) / 三連単(8)
     - 1 列目
     - 2 列目
     - 3 列目

**ボックス（Method = 2）**

枠連(3)〜三連単(8) のいずれも、選択した馬（枠）すべてが ``HorseNo1`` に入ります
（``HorseNo2`` / ``HorseNo3`` は 0）。

**軸1頭系のながし（Method = 3 / 4 / 5 / 9）** — 列は「軸」と「相手」です。

.. list-table::
   :header-rows: 1
   :widths: 14 30 20 20 16

   * - ``Method``
     - 式別
     - ``HorseNo1``
     - ``HorseNo2``
     - ``HorseNo3``
   * - 3
     - 枠連(3) / 馬連(4) / ワイド(5)
     - 軸
     - 相手
     - —
   * - 3
     - 馬単(6) / 三連単(8)
     - 軸（1 着）
     - 相手
     - —
   * - 3
     - 三連複(7)
     - 軸 1 頭
     - 相手
     - —
   * - 4
     - 馬単(6) / 三連単(8)
     - 軸（2 着）
     - 相手
     - —
   * - 5
     - 三連単(8)
     - 軸（3 着）
     - 相手
     - —
   * - 9
     - 馬単(6) / 三連単(8)
     - 軸
     - 相手
     - —

**軸2頭系のながし（Method = 6 / 7 / 8 / 10）**

三連複（式別 7・``Method`` = 6）は順不同のため着順の意味を持たず、
``HorseNo1`` に軸 2 頭がまとめて入り、``HorseNo2`` が相手です（``HorseNo3`` は 0）。

三連単（式別 8）は **列がそのまま着順** になります。
軸 2 頭が入る列を方式が表し、残り 1 列が相手です。

.. list-table::
   :header-rows: 1
   :widths: 28 24 24 24

   * - ``Method``
     - ``HorseNo1``\ （1 着）
     - ``HorseNo2``\ （2 着）
     - ``HorseNo3``\ （3 着）
   * - 6（1・2着ながし）
     - 軸
     - 軸
     - 相手
   * - 7（1・3着ながし）
     - 軸
     - 相手
     - 軸
   * - 8（2・3着ながし）
     - 相手
     - 軸
     - 軸
   * - 10（軸2頭ながしマルチ）
     - 軸
     - 軸
     - 相手

枠連の表示に関する注意
======================

枠連は **列の数が他の式別と違う**\ ため、三連単などと同じ描画処理を通すと誤った表示になります。

- **通常方式**: 買い目は ``HorseNo1`` の枠だけで表せます。
  **ゾロ目のときは枠が 1 つしか立ちません。**
  1 つしか立っていない場合は同じ枠を 2 回並べて ``8-8`` と表示してください。
- **フォーメーション**: 表示に使うのは ``HorseNo1``\ （1 枠目群）と ``HorseNo2``\ （2 枠目群）\ **だけ**\ です。
  ``HorseNo3`` は「1 枠目群と 2 枠目群の両方に現れた枠 ＝ その枠をゾロ目としても買っている」ことを
  示す印で、**3 つ目の枠の選択ではありません。**

.. list-table::
   :header-rows: 1
   :widths: 20 16 16 16 10 22

   * - 買い目
     - ``HorseNo1``
     - ``HorseNo2``
     - ``HorseNo3``
     - 点数
     - 正しい表示
   * - 1,2,3 → 4,5
     - ``1,2,3``
     - ``4,5``
     - （なし）
     - 6
     - ``1,2,3 - 4,5``
   * - 1,2,3 → 2,3,4
     - ``1,2,3``
     - ``2,3,4``
     - ``2,3``
     - 8
     - ``1,2,3 - 2,3,4``\ （うち 2-2, 3-3 はゾロ目）
   * - 8 → 8
     - ``8``
     - ``8``
     - ``8``
     - 1
     - ``8-8``\ （ゾロ目 1 点）

**3 行目を** ``8-8-8`` **と表示するのは誤りです。**

WIN5 の明細
===========

``BetFlag`` が ``BETFLAG_WIN5`` の明細では、``HorseNo1`` 〜 ``HorseNo5`` が**
第 1〜第 5 レースの馬番**\ に対応します。
レース単位の情報を持たないため、``Kaisai`` ・ ``RaceNo`` ・ ``Week`` ・ ``Method`` ・ ``Type``
には **意味のある値が入りません**\ （すべて ``0xFF`` = 255）。

WIN5 の判定は ``BetFlag`` で行うのが確実です。

解析できなかった明細
====================

**1 件の明細を解析できなかった場合**\ 、その明細は ``DecisionFlag`` が
``DECISIONFLAG_PARSE_FAILED``\ （0）になります。
通常の確定フラグは 1 始まりのため、この値が正常なフラグと衝突することはありません。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - フィールド
     - 解析できなかった明細の値
   * - ``DecisionFlag``
     - ``DECISIONFLAG_PARSE_FAILED``\ （0）
   * - ``BetFlag``
     - その受付の券種（どの種別の明細が壊れたか分かるように残ります）
   * - ``Kaisai`` / ``RaceNo`` / ``Week`` / ``Method`` / ``Type`` / ``HorseNo1``〜``HorseNo5`` / ``Multi``
     - すべて 0

- **他の明細・他の受付は正常に返されます。** 1 件の破損で購入履歴全体を失わないための仕様です。
- ``Method`` / ``Type`` に **0xFF は入りません**\ （WIN5 の判定と衝突させないため）。
- **1 件も解析できなかった場合は** ``get_purchase_data()`` **自体が失敗します。**
  空の履歴として黙って返さないためです。
- 金額は明細ではなく ``ST_TICKET_DATA`` の ``Kingaku`` / ``Payout`` に入っているため、
  **金額の集計はこの状況でも正しく行えます。**

海外開催の明細
==============

``BetFlag`` が ``BETFLAG_INTERNATIONAL`` の明細も、列の意味は上表と **完全に同じ**\ です。
違いは次の 2 点だけです。

- 馬番の上限が **24**\ （国内は 18）。
- **枠連が存在しません**\ （``Type`` に 3 は現れません）。

買い目を復元できない場合
========================

方式と式別の組み合わせが I-PAT に存在しないものだった場合、``HorseNo1`` 〜 ``HorseNo5`` は
**5 列すべて 0** になります（``Method`` / ``Type`` / ``Multi`` にはそのままの値が入ります）。
正常な購入履歴では発生しませんが、サーバの仕様変更で未知の方式が返った場合にこの形になります。
**列がすべて 0 の明細は「買い目なし」として扱ってください。** 金額の集計には影響しません。

--------
使用例
--------

基本フロー（ログイン〜単勝購入〜ログアウト）
============================================

.. code-block:: python

   from ipathelper import *

   def main():
       try:
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

           print(f"合計購入金額: {betData.TotalAmount} 円")

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

   if __name__ == '__main__':
       main()

複数買い目の一括購入
====================

.. code-block:: python

   from ipathelper import *

   def main():
       try:
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

   if __name__ == '__main__':
       main()

WIN5 の購入
===========

.. code-block:: python

   from ipathelper import *

   def main():
       try:
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

   if __name__ == '__main__':
       main()

入金・出金
==========

.. code-block:: python

   from ipathelper import *

   def main():
       try:
           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           if (ret & 1) != 1:
               return

           # 入金（2,000円）
           ret = deposit(2000)
           if (ret & 1) == 1:
               print("入金成功")

           # 入金（準備段階のリトライを最大 3 回に制限）
           ret = deposit(1000, retryCount=3)
           if (ret & 1) != 1:
               print("入金できませんでした。原因は set_log_callback のログで確認する。")

           # 全額出金
           ret = withdraw()
           if (ret & 1) == 1:
               print("出金成功")

       finally:
           logout()

   if __name__ == '__main__':
       main()

自動入金を有効にして購入
========================

.. code-block:: python

   from ipathelper import *

   def main():
       try:
           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           if (ret & 1) != 1:
               return

           # 残高不足時に 3,000円 自動入金、反映確認タイムアウト 15秒
           set_auto_deposit_flag(True, 3000, confirmTimeout=15000)

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

   if __name__ == '__main__':
       main()

購入履歴の取得
==============

.. code-block:: python

   from ipathelper import *

   def main():
       try:
           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           if (ret & 1) != 1:
               return

           purchaseData = ST_PURCHASE_DATA()
           ret = get_purchase_data(purchaseData)

           if (ret & 1) == 1:
               print(f"残高          : {purchaseData.Balance} 円")
               print(f"残購入可能数  : {purchaseData.AvailableBetCount} 件")
               print(f"当日購入金額  : {purchaseData.DayPurchase} 円")
               print(f"当日払戻金額  : {purchaseData.DayHaraimodosi} 円")
               print(f"累計購入金額  : {purchaseData.TotalPurchase} 円")
               print(f"累計払戻金額  : {purchaseData.TotalHaraimodosi} 円")
               print(f"馬券件数      : {purchaseData.TicketCount} 件")
               print("--------------------------------")

               for i in range(purchaseData.TicketCount):
                   ticket = purchaseData.TicketData[i]
                   day_label = "当日" if ticket.DayFlag == 1 else "前日"
                   print(f"[受付No.{ticket.ReceiptNo:02d}] "
                         f"{day_label} "
                         f"{ticket.Hour:02d}:{ticket.Minute:02d}購入 "
                         f"{ticket.Kingaku}円 "
                         f"(払戻: {ticket.Payout}円) "
                         f"詳細{ticket.DetailCount}点")

                   for j in range(ticket.DetailCount):
                       detail = ticket.DetailData[j]

                       # 解析できなかった明細は買い目が入っていないので飛ばす
                       if detail.DecisionFlag == DECISIONFLAG_PARSE_FAILED:
                           print(f"  詳細[{j}]: 解析できませんでした")
                           continue

                       status_map = {
                           DECISIONFLAG_HIT:      "的中",
                           DECISIONFLAG_MISS:     "外れ",
                           DECISIONFLAG_BACK:     "返還",
                           DECISIONFLAG_CANCEL:   "取消",
                           DECISIONFLAG_NORMAL:   "確定",
                           DECISIONFLAG_DEADLINE: "締切",
                       }
                       status = status_map.get(detail.DecisionFlag, "不明")
                       multi  = "[マルチ]" if detail.Multi else ""

                       # WIN5 は Kaisai / RaceNo / Method / Type に意味のある値が入らない
                       if detail.BetFlag == BETFLAG_WIN5:
                           print(f"  詳細[{j}]: {status} WIN5")
                           continue

                       # 買い目の復元は「購入明細の読み方」を参照
                       # （列の意味が方式・式別で変わる）
                       print(f"  詳細[{j}]: {status} {multi} "
                             f"R{detail.RaceNo} 方式:{detail.Method} 式別:{detail.Type}")

           # 履歴の欠けを検出したい場合は、SUCCESS と同時に立つ失敗フラグも見る
           if (ret & FAILED_CHUOU) != 0:
               print("※中央の履歴が欠けています")
           if (ret & FAILED_CHIHOU) != 0:
               print("※地方の履歴が欠けています")

           # メモリ解放は get_purchase_data 内部で自動実行される

       finally:
           logout()

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
       if (ret & 16): flags.append("FAILED_COMMUNICATE_CHUOU")
       if (ret & 32): flags.append("FAILED_COMMUNICATE_CHIHOU")
       if (ret & 64): flags.append("FAILED_OUT_OF_SERVICE")
       print(f"[{func_name}] {' | '.join(flags)}")

   def main():
       try:
           ret = login('INET-ID', 'LOGIN-ID', 'PASSWORD', 'PARS')
           print_return_value("login", ret)

           if (ret & 1) != 1:
               if (ret & 64) == 64:
                   # 受付時間外・メンテナンス中。即時リトライは必ず失敗する
                   print("サービス時間外です。時間をおいて再試行してください。")
               else:
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

   if __name__ == '__main__':
       main()

--------------------
対応金融機関
--------------------

入出金に使用できる金融機関は以下の通りです。

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - 金融機関名
     - コード
   * - PayPay 銀行
     - 2033
   * - 楽天銀行
     - 2036
   * - 三井住友銀行
     - 2009
   * - 三菱 UFJ 銀行
     - 2005
   * - 住信 SBI ネット銀行
     - 2038
   * - ゆうちょ銀行
     - 2900
   * - りそな銀行
     - 2010
   * - 埼玉りそな銀行
     - 2017
   * - au じぶん銀行
     - 2039

登録口座の金融機関は自動的に判定します。判定できない場合のみ、上記のコードを
先頭から順に試行し、登録されている口座が見つかった時点でその口座を使用します。

.. warning::

   入出金を利用できるのは **即PAT（ネットバンク）会員** のみです。
   A-PAT 会員は ``deposit()`` / ``withdraw()`` が ``UNSUCCESS`` を返します。

.. warning::

   **登録口座が PayPay（コード決済アプリ）の場合は入出金を利用できません。**
   上の表の **PayPay 銀行（2033）とは別物**\ で、そちらは従来どおり利用できます。

--------------------
DLL のアンロード
--------------------

DLL は ``import ipathelper`` 時に自動ロードされ、プログラム終了時に自動解放されます。
通常は利用者が意識する必要はありません。

明示的に解放したい場合は、次の順序を守ってください。

1. **すべての API 呼び出しが戻っていること**\ を確認する（他スレッドで実行中の呼び出しが1つも無い状態にする）
2. ``logout()`` を呼ぶ
3. ``set_log_callback(None)`` を呼んでコールバックを解除する
4. 解放する

- 実行中の呼び出しが残ったまま解放すると動作は未定義です。
- ``set_log_callback(None)`` から戻った時点で実行中のハンドラは存在しないことが保証されます。
  解除せずに解放すると、DLL 内から既に無効なコールバックを呼ぶ可能性があります。
- ``logout()`` を省略してもローカルの後始末は行われますが、
  サーバ側のセッションはログアウトされないまま残ります。

.. note::

   自動解放処理はコールバックの解除だけを行い、``logout()`` は呼びません。
   終了処理で通信を始めるとプロセスの終了が長時間ブロックされ得るためです。
   サーバ側のセッションを確実に閉じたい場合は、終了前に ``logout()`` を呼んでください。

------------------------------
開発者向け: リリース手順
------------------------------

公開は GitHub Actions が自動で行います。**手元での公開作業は不要**\ です
（``deploy_prd.bat`` などのバッチは廃止しました）。

リポジトリ構成
==============

.. code-block:: text

   ipathelper/
   ├── .github/workflows/release.yml  ... バージョン更新・ビルド・PyPI 公開を行う
   ├── pyproject.toml                 ... [project] の version を release.yml が自動更新する
   └── ipathelper/
       ├── __init__.py     ... DLL の読み込み・解放
       ├── ipathelper.py   ... 各 API のラッパー
       ├── x64/IpatHelper.dll
       └── x86/IpatHelper.dll

自動公開の流れ
==============

``IpatHelperNative`` の CI がビルドした ``IpatHelper.dll`` を
``ipathelper/x64/`` と ``ipathelper/x86/`` へ push してくると、それを合図に
``release.yml`` が起動して次を順に行います。

1. ``pyproject.toml`` の ``[project]`` セクションから ``version`` を読み取り、**パッチ番号を +1** して書き戻す
2. ``dist`` を削除して ``uv build``
3. PyPI へ公開する
4. バージョン更新をコミットして ``master`` へ push する

DLL のパスが変わったときだけ起動するため、他のコミットでは公開は走りません。

.. note::

   本番 PyPI へは **Trusted Publishing（OIDC）** で公開しており、API トークンは
   どこにも保存していません。PyPI 側に「``Mikimini9627/ipathelper`` の
   ``release.yml`` からの公開」を publisher として登録することで成立しています。

手動で公開する
==============

DLL を更新していないタイミングで公開したい場合は、GitHub の Actions タブから
``Release to PyPI`` を ``workflow_dispatch`` で実行します。入力は 2 つです。

.. list-table::
   :header-rows: 1

   * - 入力
     - 意味
   * - ``target``
     - ``pypi``（既定）または ``testpypi``
   * - ``dryrun``
     - ``true`` にするとバージョン更新も公開も行わず、ビルドのみ確認する

``testpypi`` を選ぶ場合のみ、リポジトリの secret に ``TESTPYPI_API_TOKEN`` が必要です
（TestPyPI 側には publisher を登録していないため、こちらはトークン方式です）。

.. warning::

   ``pyproject.toml`` の ``version`` を **手で上げないでください。**
   CI が +1 するため、手動でも上げると番号が飛びます。

   バージョンは ``pyproject.toml`` の値を基準に +1 されるため、この値が
   **PyPI の公開済み最新版と一致している**\ ことが前提です。ずれていると
   既に存在する番号を作ってしまい、ビルドは通っても最後のアップロードで拒否されます。

   ずれの確認は次のコマンドで行えます。

   .. code-block:: console

      > uv run --no-project --with requests python -c "import requests;print(requests.get('https://pypi.org/pypi/ipathelper/json').json()['info']['version'])"
