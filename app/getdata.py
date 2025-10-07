import requests
from bs4 import BeautifulSoup
import datetime
import time
import json
import discord
from discord.ext import tasks, commands

# botの設定
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# メッセージを送るチャンネルID（送信したいチャンネルのIDに置き換える）
CHANNEL_ID = 1424631412937592904  # ← ここを実際のチャンネルIDに変更

@bot.event
async def on_ready():
    print(f"ログイン完了: {bot.user}")
    send_message_loop.start()  # Bot起動時にループ開始



# 15分ごとに自動でメッセージを送信
@tasks.loop(minutes=15)
async def send_message_loop():
    print("実行")
    i = 0
    
    # ブラウザを模倣するUser-Agentを指定
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/115.0.0.0 Safari/537.36")
    }
    while True:
        i += 1
        print(i)
        # HTTPリクエストの処理とそのエラー処理
        try:
            response = requests.get(f"https://transit.yahoo.co.jp/diainfo/{i}/0", headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            continue
        except requests.exceptions.ConnectTimeout:
            print("タイムアウト")
            continue
        

        # HTML解析の処理とそのエラー処理
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h1", class_="title")
        title = titles[0].get_text(strip=True)
        dts = soup.find_all("dt")
        status = dts[0].get_text(strip=True)
        dds = soup.find_all("dd")
        reason = dds[0].get_text(strip=True)

            
        if (i >= 1000):
            break;
        
        # 用語変更
        if (status == "運転計画"):
            status = "遅延"
        elif (status == "列車遅延") :
            status = "遅延"
        elif (status == "運転計画") :
            status = "その他"
        elif (status == "列車遅延") :
            status = "遅延"
        elif (status == "運転状況") :
            status = "遅延"
        
        headers = {
            'Content-Type': 'application/json'
            }
        
        if (status != "平常運転"):
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(f"```{title} : {status} \n	{reason}```")
    
    
    
#　ループ終了後の処理

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"データ更新完了時刻: {current_time}")
bot.run("MTQyNTAwMzkyMzczNTA1MjMwOA.GpZi6I.VYY860UFgK379yUiMucalGNOJf4EkhWRkjv9GY")  # ← あなたのBotのトークンに置き換える