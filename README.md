# MoodleQuizCheckScraper

* 教師が受験結果のページ $(MOODLE)/mod/quiz/report.php?id=$(qid)&mode=overview を開く．
  * 希望のソートをする．その順に review.html に番号がつく
* [DownThemAll](https://chromewebstore.google.com/detail/downthemall/nljkibfhlpcnanjgbnlnbjecgicbjkge?hl=ja&pli=1)などで， 全ユーザの review.html をローカルにダウンロードする
  * Mac Chrome では，ファイルの個数だけクリックしなきゃいけない？
     * Chrome のダウンロード設定で回避できる

### 実行

* ansconfig.py に，意図した順に 'ans*','prt*' をリストする．

```zsh
cat review.html | python3 checkscraper.py > review.csv
```

### コマンドラインオプション
`--noheading`,`-nh` 先頭のヘッディングを省く


```zsh
for file in review\ \(0\).html; do cat $file | python3 ~/G/00todo/MoodleQuizCheckScraper/checkscraper.py ; done  | head -n 1 > a.csv
for file in  a/*review\ \(*\).html; do cat $file | python3 ~/G/00todo/MoodleQuizCheckScraper/checkscraper.py -nh ; done  >> a.csv
```
