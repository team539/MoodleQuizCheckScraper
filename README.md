# MoodleQuizCheckScraper

* 教師が受験結果のページ $(MOODLE)/mod/quiz/report.php?id=$(qid)&mode=overview を開く．
  * 希望のソートをする．その順に review.html に番号がつく
* [DownThemAll](https://chromewebstore.google.com/detail/downthemall/nljkibfhlpcnanjgbnlnbjecgicbjkge?hl=ja&pli=1)などで， 全ユーザの review.html をローカルにダウンロードする
  * 個数だけクリックしなきゃいけない？

### 実行

```shell
cat review.html | python3 checkscraper.py > review.csv
```

### コマンドラインオプション
`--noheading`,`-nh` 先頭のヘッディングを省く
