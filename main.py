import os

import discord
import requests
import json
import openai
import random

from replit import db

from keep_alive import keep_alive

sad_words = ["sad", "depressed", "unhappy", "anrgy"]

happy_words = ["cheer up", "don't give up", "you can do it"]

intents = discord.Intents.default()
intents.message_content = True

AI_Key = os.environ['AI-KEY']

openai.api_key = os.environ['AI-KEY']

client = discord.Client(intents=intents)


def update_happy_words(new_happy_word):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(new_happy_word)
    db["encouragements"]=encouragements
  else:
    db["encouragements"] = [new_happy_word]


def delete_happy_words(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


def get_quote():
  response = requests.get("http://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = list(happy_words)  # Convert to a regular list
  if "encouragements" in db.keys():
    options = options + list(db["encouragements"])  # Convert to a regular list and concatenate


  msg = message.content
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encourage_msg = msg.split("$new ", 1)[1]
    update_happy_words(encourage_msg)
    await message.channel.send("New word has been added")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_happy_words(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)


keep_alive()

bot_token = os.environ['DISCORD-BOT']

client.run(bot_token)
