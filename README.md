# MoodleQuizCheckScraper

* 教師が受験結果のページ `$(MOODLE)/mod/quiz/report.php?id=$(qid)&mode=overview` を開く．
  * 希望のソートをする．その順に review.html に番号がつく
* [DownThemAll](https://chromewebstore.google.com/detail/downthemall/nljkibfhlpcnanjgbnlnbjecgicbjkge?hl=ja&pli=1)などで， 全ユーザの review.html をローカルにダウンロードする
  * Mac Chrome では，ファイルの個数だけクリックしなきゃいけない？
     * Chrome のダウンロード設定で回避できる
* questionid を得るには，その問題を編集できるロールのユーザがダウンロードする必要がある

### 実行

* ansconfig.py に，意図した順に 'ans*','prt*' をリストする．
  * それには問題の中を見る必要があるが，ダウンロードしたファイルに1回でも出てきた ans, prt を知るだけなら，
```sh
 (grep -oh 'ans\d\d*' *.html; grep -oh 'prt\d\d*' *.html) | sort |uniq
# cannnot egrep with regexp
``


* 実行
```zsh
cat review.html | python3 checkscraper.py > review.csv
```



### コマンドラインオプション
`--noheading`,`-nh` 先頭のヘッディングを省く


```zsh
for file in review\ \(0\).html; do cat $file | python3 ~/G/00todo/MoodleQuizCheckScraper/checkscraper.py ; done  | head -n 1 > a.csv
for file in  a/*review\ \(*\).html; do cat $file | python3 ~/G/00todo/MoodleQuizCheckScraper/checkscraper.py -nh ; done  >> a.csv
```


### Update
* Moodle 4.4で，パンくずリストのコース略名に空白や改行が入るようになったのですべて除く修正
  * 途中の空白も除いていいのか？真剣にやるなら正規表現で
* allowempty されている空白の数式解答は，EMPTYANSWER．allowempty されている空白のノート記入は &quot;&quot; となる. BeatifulSoup4 により&quot;&quot; "\"\"" となる．従来はCSVでは """" に見えており，分解すると""""""となる．何かに強制的に置き換える？EMPTYSTRING（？）


## Note
* "q55259:1_ans1" のようなidやnameがある．55259はattempごとに異なる．1_ans1はfirst questionのans1 fieldの意味か？