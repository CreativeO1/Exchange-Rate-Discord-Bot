import discord
import os
import requests
import json
import time
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Hello, I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target = run)
  t.start()

client = discord.Client()

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))
  channel = client.get_channel(935979688730435648)

  async def send_exrate():
    response = requests.get(os.environ['EXRATETOKEN'])
    json_data = json.loads(response.text)

    embedMsg = discord.Embed()
    embedMsg.add_field(name = "Turkish Lira", value = str(1/json_data['data']['TRY'])[0:6])
    embedMsg.add_field(name = "US Dollar", value = str(1/json_data['data']['USD'])[0:6])
    embedMsg.add_field(name = "Euro", value = str(1/json_data['data']['EUR'])[0:6])
    embedMsg.add_field(name = "Pound Sterling", value = str(1/json_data['data']['GBP'])[0:6])
    embedMsg.add_field(name = "Canadian Dollar", value = str(1/json_data['data']['CAD'])[0:6])
    embedMsg.add_field(name = "Australian Dollar", value = str(1/json_data['data']['AUD'])[0:6])
    embedMsg.add_field(name = "Japanese Yen", value = str(1/json_data['data']['JPY'])[0:6])
    embedMsg.add_field(name = "Russian Ruble", value = str(1/json_data['data']['RUB'])[0:6])
    embedMsg.add_field(name = "United Arab Emirates Dirham", value = str(1/json_data['data']['AED'])[0:6])
    embedMsg.add_field(name = "Mexican Peso", value = str(1/json_data['data']['MXN'])[0:6])
    embedMsg.add_field(name = "Chinese Yuan", value = str(1/json_data['data']['CNY'])[0:6])
    embedMsg.add_field(name = "Bitcoin", value = str(1/json_data['data']['BTC'])[0:6])
    embedMsg.add_field(name = "Etherum", value = str(1/json_data['data']['ETH'])[0:6])
    embedMsg.title = "**Exchange Rate**"
    embedMsg.colour = 0x00FF00

    await channel.send(embed=embedMsg)
  
  await send_exrate()

  while True:
    time.sleep(300)
    await send_exrate()

@client.event
async def on_message(message):
  if message.author == client.user:
    return

keep_alive()
client.run(os.environ['TOKEN'])
