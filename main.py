import discord
import os
from discord import user
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests as rq

load_dotenv()
bot = discord.Client()
prefix = 'h!'

@bot.event
async def on_ready():
    print("機器人已就緒", bot.user)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    msg = message.content.split()
    if msg[0] == prefix:
        num = msg[1]
        my_url = "https://nhentai.net/g/" + num + "/"
        response = rq.get(my_url)
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        meta_tags = soup.find_all('meta')
        cnt = 0
        title_temp = 0
        cover_pic_temp = 0
        for tag in meta_tags:
            cnt += 1;
            if cnt == 3:
                title_temp = tag
            if cnt == 4:
                cover_pic_temp = tag
                break
        my_title = title_temp.get('content')
        my_cover_pic = cover_pic_temp.get('content')
        my_tags = soup.find(id="tags")
        my_tags_children = [d for d in my_tags.children]
        embed_value = [0 for j in range(9)]
        cnt = 0
        for i in my_tags_children:
            #print(i.prettify())
            temp = i.select(".tag-container .tags a .name")
            arr = [d.get_text() for d in temp]
            #print(arr)
            if len(arr) == 0 :
                embed_value[cnt] = "none"
            else:
                s = ""
                for j in range(len(arr)):
                    s += arr[j]
                    if(j != len(arr) - 1):
                        s += ", "
                embed_value[cnt] = s
            print(embed_value[cnt])
            cnt += 1



        embed = discord.Embed(
            title = my_title,
            colour = discord.Colour.from_rgb(236, 40, 84),
            url = my_url
        )
        embed.add_field(name="Parodies:", value=embed_value[0], inline=False)
        embed.add_field(name="Characters:" , value=embed_value[1], inline=False)
        embed.add_field(name="Tags:" , value=embed_value[2], inline=False)
        embed.add_field(name="Artists:" , value=embed_value[3], inline=False)
        embed.add_field(name="Groups:" , value=embed_value[4], inline=False)
        embed.add_field(name="Languages:" , value=embed_value[5], inline=False)
        embed.add_field(name="Categories:" , value=embed_value[6], inline=False)
        embed.add_field(name="Pages:" , value=embed_value[7], inline=False)
        embed.add_field(name="Uploaded:" , value=embed_value[8], inline=False)
        embed.set_image(url = my_cover_pic)
        await message.channel.send(embed = embed)

bot.run(os.getenv("TOKEN"))