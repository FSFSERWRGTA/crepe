from asyncio import set_event_loop
import time
import random
import discord
import gspread
import pprint
import json # 딕셔너리를 json으로 변형시켜주는 모듈
import datetime
import pytz
import json # 딕셔너리를 json으로 변형시켜주는 모듈
import os

TOKEN = 'MTE2ODc0ODgzODA1NjYzNjUyOQ.GIhwvT.tsVW-YQqu4DylQS15N5nbYJvLkPnU22Pz_ySCg'

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents) # client 생성. 디스코드와 연결

# 콜백 스타일: 콜백은 기본적으로는 무엇인가 일어났을때 호출되는 기능
@client.event # 데코레이터 - 이벤트 등록
async def on_ready(): # 봇이 로깅을 끝내고 여러가지를 준비한 뒤 호출
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message): # 봇이 메시지를 받았을 때 호출됩니다
    

    if message.author == client.user: # 봇이 보낸 메세지면 무시
        return
    if '[' not in message.content:
        return
    try:
        start = message.content.find('[')
        end = message.content.find(']')
    except:
        return
    if (start != -1 and end != -1) and start<end: # [] 조건 찾기. [, ]가 존재해야 하고, 닫는 괄호가 여는 괄호보다 앞에 있으면 안된다.
        mention_keyword = message.content[start+1:end].strip().split('/') # /를 기준으로 나눠 리스트로 저장. 현재 받은 메세지에는 /가 없으므로 그냥 ['다이스'] 로 저장된다. 
        first_keyword = mention_keyword[1].replace(" " , "")
        print(first_keyword)
    
                    ###################### 키워드 별 함수 호출. 키워드가 늘어나면 여기가 길어진다. ######################
        print('! 다이스 굴리는 함수를 호출합니다.')
        # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
        keyword_action_return = Dice(mention_keyword, message) 

        await message.channel.send(keyword_action_return, reference=message) # 답장 o
        
    else:
        await message.channel.send("양식 오류. 양식 확인 후 재시도 해주시길 바랍니다.", reference=message) # 답장 o
    #################################################################################################

                
#다이스
def Dice(mention_keyword, message):
    usear = mention_keyword[0].strip()
    which = int(mention_keyword[1].strip('%').strip())

    a = random.randrange(1,101)
    print(a)

    if a > which:
        return f"실패!"
    
    else:
        return f"성공!"

client.run(TOKEN)
