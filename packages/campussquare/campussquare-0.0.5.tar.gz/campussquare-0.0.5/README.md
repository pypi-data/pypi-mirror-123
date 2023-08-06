# CampusSquare

## 使い方

```sh
# 科目名から内部シラバスを検索
python3 main.py syllabus search -s 'コンピュータサイエンス'

# 時間割コードから内部シラバスをMarkdownで表示
python3 main.py --markdown syllabus get -t 31 -c 21124229
```