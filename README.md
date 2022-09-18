# csv_viewer

## 使用方法

### 1. ファイルの用意
resultディレクトリの中に、2つのディレクトリを作成
- csv_files: GAで出力されたcsvファイルを全て格納
- html_files: html変換後のファイルが入るので最初は空

### 2. csvをhtmlに変換
parser.py を実行し、csvファイルをhtmlに書き換える

> source streamlt_csv/bin/activate
> make html

### 3. streamlitを起動

> make local
