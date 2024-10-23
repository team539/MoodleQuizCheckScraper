# MoodleQuizCheckScraper

* 教師が受験結果のページ `$(MOODLE)/mod/quiz/report.php?id=$(qid)&mode=overview` を開く．
  * 希望のソートをする．次で，その順にreview.htmlに番号がつく
* [DownThemAll](https://chromewebstore.google.com/detail/downthemall/nljkibfhlpcnanjgbnlnbjecgicbjkge?hl=ja&pli=1)などで， 全ユーザのreview.htmlをローカルにダウンロードする
  * Mac Chromeでは，ファイルの個数だけクリックしなきゃいけない？
     * No. Chromeのダウンロード設定で回避できる
* questionidを得るには，その問題を編集できるロール(Question Sharer on moodle.hig3.net)のユーザがダウンロードする必要がある

### 実行

* [scrape-decompose.py](scrape-decompose.py)と同じディレクトリのansconfig.pyに，意図した順に 'ans*','prt*' をリストする．
 ```sh
 vi ansconfig.py
 ```
  * それには問題の中を見る必要があるが，ダウンロードしたファイルに1回でも出てきたans, prtを知るだけなら，
```sh
  (grep -oh 'ans\d\d*' *.html; grep -oh 'prt\d\d*' *.html) | sort |uniq
# cannnot egrep with regexp
```
[decompose.py](decompose.py)はこれを自動でやるようなもの．


* 実行
```zsh
cat review.html | python3 scraper-decompose.py > review.csv
```

* 複数やるなら
```zsh
for file in review\ \(0\).html; do cat $file | python3 scrape-decompose.py ; done  | head -n 1 > all.csv
for file in review\ \(*\).html; do cat $file | python3 scrape-decompose.py -nh ; done  >> all.csv
```

* ansconfig.pyの編集を省き，複数のreview.htmlから抽出するには，
```zsh
for file in review\ \(0\).html; do cat $file | python3 scrape.py ; done  | head -n 1 > all.csv
for file in review\ \(*\).html; do cat $file | python3 scrape.py -nh ; done  >> all.csv
cat all.csv | python3 decompose.py > all1.csv
```

### コマンドラインオプション
`--noheading`,`-nh` 先頭のヘッディングを省く


### Update
* Moodle 4.4で，パンくずリストのコース略名に空白や改行が入るようになったのですべて除く修正
  * 途中の空白も除いていいのか？真剣にやるなら正規表現で
* allowemptyされている空白の数式解答は，EMPTYANSWER．allowemptyされている空白のノート記入は &quot;&quot; となる．BeatifulSoup4により&quot;&quot; "\"\""となる．従来はCSVでは""""に見えており，分解すると""""""となる．何かに強制的に置き換える？EMPTYSTRING（？）


## Note
* "q55259:1_ans1" のようなidやnameがある．55259はattempごとに異なる．1_ans1はfirst questionのans1 fieldの意味か？