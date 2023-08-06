# CampusSquare

## 使い方

```sh
# 科目名から内部シラバスを検索
python3 main.py syllabus search -s 'コンピュータサイエンス'

# 履修登録している時間割コードの一覧を取得
python3 main.py courses
# 年度:所属コード:時間割コード
# 2021:31:21124229

# 時間割コードから内部シラバスをMarkdownで表示
python3 main.py --markdown syllabus get 2021:31:21124229
```
