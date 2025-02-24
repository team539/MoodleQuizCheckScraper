# MoodleQuizCheckScraper

* 教師が受験結果のページ `$(MOODLE)/mod/quiz/report.php?id=$(qid)&mode=overview` を開く．
  * 希望のソートをする．ダウンロードされた際に，review.htmlのファイル名にに番号がその順でつく
* [DownThemAll!](https://addons.mozilla.org/ja/firefox/addon/downthemall/)などで， 全ユーザのreview.phpをローカルにダウンロードする
  * Mask（ファイル名変換）は `*name*_*idx*.html` などで．
  * Mac Chromeでは，ファイルの個数だけクリックしなきゃいけない？
     * No. Chromeのダウンロード設定で回避できる
* questionidを得るには，その問題を編集できるロール（システムコンテクストの共有問題ならそれに対応した）のユーザがダウンロードする必要．

### 実行



* [scrape.py](scrape.py)で，すべてのreview.htmlからCSV形式でデータを取り出して連結する
```zsh
for file in review_001.html; do cat $file | python3 scrape.py ; done  | head -n 1 > all.csv
for file in review_*.html; do cat $file | python3 scrape.py -nh ; done  >> all.csv
```
* [decompose.py](decompose.py)で，どのようなans,prtがあるのか，CSV内を探索し，それに対応するカラムを作って記録する．
```zsh
cat all.csv | python3 decompose.py > all1.csv
```

#### コマンドラインオプション
* `--noheading`,`-nh` 先頭のヘッディングを省く
* `-q 整数` 問題番号を指定する．問題番号は，review.html表が現れる順序で，1から始まる．指定しないとき，すべての問題を対象とする．

### 手でカラムを指定した1段階実行
* `decompose.py`に任せず，[scrape-decompose.py](scrape-decompose.py)と同じディレクトリの`ansconfig.py`に，[ansconfig-dist.py](ansconfig-dist.py)の形式で，意図した順に 'ans*','prt*' をリストする．
 ```sh
 vi ansconfig.py
 ```
  * それには問題の中を見る必要があるが，ダウンロードしたファイルに1回でも出てきたans, prtを知るだけなら，
```sh
  (grep -oh 'ans\d\d*' *.html; grep -oh 'prt\d\d*' *.html) | sort |uniq
# cannnot egrep with regexp
```

* 実行
```sh
cat review.html | python3 scrape-decompose.py > review.csv
```

* 複数やるなら
```zsh
for file in review_001.html; do cat $file | python3 scrape-decompose.py ; done  | head -n 1 > all.csv
for file in review_*.html; do cat $file | python3 scrape-decompose.py -nh ; done  >> all.csv
```

* review.html内の複数問題には対応していない

### Update
* Moodle 4.4で，パンくずリストのコース略名に空白や改行が入るようになったのですべて除く修正
  * 途中の空白も除いていいのか？真剣にやるなら正規表現で
* allowemptyされている空白の数式解答は，EMPTYANSWER．allowemptyされている空白のノート記入は &quot;&quot; となる．BeatifulSoup4により&quot;&quot; "\"\""となる．従来はCSVでは""""に見えており，分解すると""""""となる．何かに強制的に置き換える？EMPTYSTRING（？）


## Note
* "q55259:1_ans1" のようなidやnameがある．55259はattempごとに異なる．1_ans1はfirst questionのans1 fieldの意味か？