# Seating Chart Generator

生徒リストと座席の情報からランダムな座席表を作成するツール

* サンプル

![DEMO](https://github.com/nananaman/make_seating_chart/blob/master/seating_chart.png)

## Installation

```
git clone https://github.com/nananaman/make_seating_chart.git
```

## Requirement

* OpenCV
* NumPy

## 使い方

* list.txt に生徒の学生番号一覧を、seats.txt に座席の情報を記す
* `python make.py -t 'Title'`

### list.txt

* 生徒の学生番号を改行を挟んで記す

### seats.txt

* 座席の数を列ごとに記す
* 列内に間隔がある場合はスペースを開ける
* 通路がある場合は改行する

### オプション

#### コマンドライン引数で以下の要素を指定できる

##### -t, --title

* 講義名を指定する
* 必須

##### -p, --podium_name

* 教卓名を指定できる

##### --list_pass

* list.txtのパスを指定できる

##### --seats_pass

* seats.txtのパスを指定できる

##### --sort 

* 生徒の並べ方を指定できる
* デフォルトでは前から詰めるようになっている
* 'center'を渡すことで中央の列から座らせるようになる
