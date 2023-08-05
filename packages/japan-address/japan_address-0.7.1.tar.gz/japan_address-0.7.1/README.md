# japan_address

[![Build Status](https://github.com/kzthrk/japan_address/actions/workflows/python-app.yml/badge.svg)](https://github.com/kzthrk/japan_address/actions/workflows/python-app.yml?query=workflow%3A%22Python+application%22++)


## At the beginning
This utility is designed to process Japanese addresses. For this reason, the README is provided in Japanese only, since it is not likely to be used by people who do not understand Japanese.


## はじめに
日本語の住所を処理するユーティリティです。住所を処理する動機にはいくつかあると思いますが、このユーティリティを使用すると都道府県と市区町村とそれ以外に分割したり、2つの住所を比較するなどが可能です。
実装方法の1つに、正規表現の採用が考えられますが、開発途中は頭の体操としてとても有意義なのですが、テストや将来の変更に対してあまり得策ではないため、現在のところ以下の資料を元にした単純比較による判定を採用しています。

[総務省｜地方行政のデジタル化｜全国地方公共団体コード](https://www.soumu.go.jp/denshijiti/code.html) 令和元年5月1日更新

※現時点では旧住所に関する機能は未実装です。
 - 旧住所を新住所変換
 - 旧住所のままで都道府県、郡、市区町村の抽出


## 主な機能
- 都道府県の抽出
- 郡の抽出
- 市区町村の抽出
- 住所比較

## インストール
```
pip install japan_address
```

## サンプルコード

```
import japan_address

ja = japan_address.JapanAddress()

address = "東京都渋谷区代々木２丁目２番２号"
result = ja.extract_details(address)
print(result)   # ('東京都', '渋谷区', '代々木２丁目２番２号')

result = ja.resolve_prefecture("渋谷区代々木２－２－２")
print(result)   # '東京都'

result = ja.normalize_address("東京都渋谷区代々木２丁目２番２号")
print(result)   # '東京都渋谷区代々木２－２－２'

addr1 = "東京都渋谷区代々木２丁目２番２号"
addr2 = "東京都渋谷区代々木２－２－２"
result = ja.compare_address(addr1, addr2)
print(result)   # 100
```

## 機能紹介
使用頻度の多いと考えられるものを中心に簡易の説明を行います。

### 注意事項
「市区町村」とは、最小行政単位であり議会を有するものと考えると最も簡潔に理解が可能です。従って、aa市bb町のbb町はこれに当たりませんが、xx郡yy町のyy町はこれにあたります。また、郡は単なるグループを示す用語にすぎず、住所表記に含んでも含まなくても良いため住所を扱う上で注意が必要です。

なお、区の中にはこの定義に沿っている区と沿っていない区が存在します。東京都の23区は特別区といい"東京市"に相当する機能を区自体が保持しています。一方で"千葉県千葉市"にも区は存在しますが、こちらは地理的区分に過ぎません。政令指定都市における区がこれにあたります。

ただし一部の行政資料やシステムでは「市区町村」として政令指定都市の区までを含んで取り扱っているものがあります。

### get_prefecture_list
都道府県の**リスト**を返却します

### get_country_list
郡の**リスト**を返却します。
7つの郡が複数都道府県に存在しますが、重複のないリストを返却します。
引数に都道府県(prefecture)を指定することで、その都道府県内の郡の**リスト**を返却します。

### get_city_list
市区町村の**リスト**を返却します。
2つの市が複数都道府県に存在しますが、重複のないリストを返却します。
引数に都道府県(prefecture)や郡(country)を指定することで、その都道府県内や郡内の市区町村の**リスト**を返却します。

引数に政令指定都市(designated)を指定する(True)と、**リスト**内に"千葉市"は登場せず、代わりに"千葉市中央区"がリストされるようになります。

### prefecture_code_to_prefecture
都道府県番号(二桁)と都道府県の**辞書**を返却します。地方自治体コードの上二桁を返却するため、北海道の場合"01"を返却します。

### local_government_code_to_city
地方自治体コードと市区町村の**辞書**を返却します。

政令指定都市(designated)を指定する(True)と、**辞書**内に"千葉市"は登場せず、代わりに"千葉市中央区"がリストされるようになります。

### extract_details
指定した住所を、都道府県、市区町村、その他に分割して返却します。
政令指定都市(designated)を指定する(True)と、政令指定都市の区は市区町村側に含まれるようになります。

### resolve_prefecture
住所が郡、あるいは市区町村から始まっている場合に、都道府県を解決します。
ただし、2つの市、7つの郡が、複数の都道府県に存在しています。その場合はNoneを返却します。
※ここでは読みが異なっていても漢字表示が同じものが影響を受けています。

### normalize_address
住所の比較を念頭に、"1丁目1番1号"形式の部分を"１−１−１"形式に変換します。
"丁目"や"番"、"号"の他、"番地"や"番の"、それに"の"など様々な区切りがありますが、これまで開発者が経験したものにのみ対応しています。

### compare_address
二つの住所を比較し、同一である確信度を返却します。完全一致で100を返します。*normalize_address*を用いた上で、*extract_details*を用いて都道府県、市区町村、その他に分割し、都道府県、市区町村までの一致で50とし、その他の部分で使用されている文字がどの程度似通っているかを*SequenceMatcher*を用いて簡易評価しています。

現時点で「字」や「大字」の情報を保持していないため、これらに関する表記の揺れ(字や大字という表記を省略するかどうかは地域差のほか個人によっても異なります)には対応出来ていませんので、*SequenceMatcher*の範囲で評価が為されていることになります。

戻り値が85以上でほとんどが同一住所とみなせ、80を下回るとほとんど同一ではないというのが、開発者の感覚です。ご使用になられる場合には、ご自身でいくつかのパターンの住所でお試しになってから閾値をお決めにると良いと思います。

## License
This utility is protected under the MIT license

