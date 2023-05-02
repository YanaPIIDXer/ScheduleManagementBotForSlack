# MEMO: {} は {{}} の形にエスケープする必要がある
# 参考資料: https://github.com/hwchase17/langchain/issues/2212
promptTemplate = """
以下の入力内容を以下の要素に従って要約し、指定したJSONフォーマットだけを出力してください。
出力するテキストはJSONフォーマットだけとし、注釈や説明等の余計な文字列は一切出力しないでください。
このルールには厳格に従ってください。

## 要素
- 要約成功フラグ
  - is_valid
  - 必須項目
  - 要約できたらtrue、日時不明等でできなかったらfalseとする
  - 要約できなかった場合、他の要素はすべて空文字とする
- 開始日時(yyyy-MM-dd hh:mm)
  - start_date_time
  - 必須項目
  - 指定がない場合は終日と見做す
  - 終日の場合、時間を00:00として出力する
- 終了日時(yyyy-MM-dd hh:mm)
  - end_date_time
  - 必須項目
  - 開始日時の判断で「終日」と判断されている場合は、日付を開始日の翌日、時間を00:00として出力する
 -  開始時刻は明示されているが終了時刻の明示が無い場合、ひとまず開始日時の1時間後とする
- 表題
  - title
  - 必須項目
- サマリ
  - summary

## フォーマット
{{
  \"is_valid\": 要約成功フラグ,
  \"start_date_time\": 開始日時,
  \"end_date_time\": 終了日時,
  \"title\": 表題,
  \"summary:\" サマリ
}}

## 入力
{input}

## 出力
"""
