\# 📊 LINE Household Bot（LINE家計簿Bot）



Notionに家計簿を自動登録できるLINE Botです。  

LINEで送ったメッセージを、AWS Lambda 経由で Notion に記録します。



---



\## 🛠 使用技術



\- Python 3.10

\- Flask

\- LINE Messaging API（line-bot-sdk）

\- Notion API（notion-client）

\- AWS Lambda + API Gateway（Zappa）

\- Git / GitHub



---



\## 🚀 セットアップ方法（ローカル動作）



\### 1. 仮想環境の作成と有効化



```bash

python -m venv venv

source venv/Scripts/activate  # Windows（Git Bash）







\### 2. 必要なライブラリのインストール

pip install -r requirements.txt



\### 3. .envファイルの作成

LINE\_CHANNEL\_ACCESS\_TOKEN=あなたのトークン

LINE\_CHANNEL\_SECRET=あなたのシークレット

NOTION\_TOKEN=あなたのNotionトークン

DATABASE\_ID=あなたのNotionデータベースID



.envは.gitignoreによってGitに含めません



\#### 4. ローカルサーバを起動

python line-bot-server.py



\#### 5. テスト用の公開(Ngrok使用)

ngrok http 5000

出力されるURLを LINE Developers の Webhook URL に登録。



\#### 6. 本番デプロイ(Zappa)

zappa deploy dev

\# 更新する場合は

zappa update dev

LINEのWebhook URLもZappaが発行したAPI GatewayのURLに変更してください。



\#### 7. メッセージのフォーマット

以下のようにメッセージを送ると、自動でNotionに登録されます。

2025/08/01 食費 1200 スーパーで買い物



\#### 8. 登録されるNotionの項目

・日付(例: 2025/08/01)

・カテゴリ(例: 食費)

・金額(例: 1200)

・メモ(例: スーパーで買い物)



\#### 9. セキュリティ対策

・envやzappa\_setting.jsonは.gitignore済み

・トークンなどの機密情報はAWS Lambdaの「環境変数」に安全に登録



\#### 10. 今後のTODO(アイデア)

・エラーログをClaudWatchに集約

・Notionで週次・月次レポートをまとめたり、予算を設定して使い過ぎ防止アラートをLINE Botに送信

・メッセージの定型化・自然言語処理対応

・仮想貯金や仮想投資が出来る仕組みづくり



\#### 11. Special Thanks

・LINE Message API

・Notion API

・Zappa

・Chat GPT





