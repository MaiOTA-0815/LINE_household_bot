from flask import Flask, request, abort
from dotenv import load_dotenv
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from notion_client import Client
from datetime import datetime

# .envから環境変数を読み込み（ここを最初に）
load_dotenv()

# Flaskサーバー起動
app = Flask(__name__)

# トークンとシークレットを環境変数から取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Notionの初期化
notion = Client(auth=os.environ["NOTION_TOKEN"])
DATABASE_ID = os.environ["DATABASE_ID"]

def create_notion_page(date_str, category, amount_str, memo):
    try:
        formatted_date = datetime.strptime(date_str, "%Y/%m/%d").date().isoformat()
    except ValueError:
        formatted_date = datetime.today().date().isoformat()

    try:
        amount = int(amount_str)
    except ValueError:
        amount = 0

    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "date": {"date": {"start": formatted_date}},
            "category": {"select": {"name": category}},
            "amount": {"number": amount},
            "memo": {"title": [{"text": {"content": memo}}]},
        }
    )

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    parts = text.split()

    if len(parts) < 4:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="フォーマットが正しくないよ！\n\n例: 2025/06/07 食費 1200 コンビニでおにぎり")
        )
        return

    date_str, category, amount_str = parts[:3]
    memo = " ".join(parts[3:])

    try:
        create_notion_page(date_str, category, amount_str, memo)
        reply_text = f" 登録したよ！\n{date_str} / {category} / ¥{amount_str}\n{memo}"
    except Exception as e:
        reply_text = f"エラーが発生しちゃった…\n{str(e)}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )


if __name__ == "__main__":
    app.run(port=5000)

print("LINE_CHANNEL_ACCESS_TOKEN:", os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
print("DATABASE_ID:", os.getenv("DATABASE_ID"))

