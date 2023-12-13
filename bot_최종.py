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
import logging # 로깅 모듈 불러오기
from logging.handlers import HTTPHandler # 상속받을 HTTPHandler
import copy
import os

class SlackHandler(HTTPHandler): # 클래스 상속
    def mapLogRecord(self, record): # 메소드 오버라이딩
        # slack 수신 웹훅에서 요청하는 페이로드 형식과
        # HTTPHandler의 mapLogRecord에서 설정한 리턴 형 - dict에 맞춰서 내용 리턴
        return {"payload": json.dumps({"text": self.format(record)})} 
now = datetime.datetime.now(pytz.timezone('Asia/Seoul')) # 현재 시간, 중복트 방지 용
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
# 출력 포맷 (변경 가능)
# 월-일 시:분:초 : 현재 파일(모듈)이름 : 레벨 : 로그 메세지  
f = logging.Formatter(fmt='%(asctime)s : %(module)s : %(levelname)s : %(message)s',)
host = "hooks.slack.com"
url = "https://hooks.slack.com/services/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"
method = "POST"

logger = logging.getLogger("slacktest.py") # slacktest.py를 키로 로거 생성
logger.setLevel(logging.INFO) # 레벨 세팅.
# INFO DEBUG WARN ERROR FATAL 순으로 레벨이 높아진다. 높은 레벨로 세팅하면 낮은 레벨 메세지는 인식하지 않는다.
logger_handler = SlackHandler(host, url, method, secure=True) # 핸들러 생성. HTTPHandler에서 요구하는 형식을 따른다.
logger_handler.setFormatter(f) # 핸들러에 출력 포맷 세팅
logger.addHandler(logger_handler) # 로거에 핸들러 추가

Errer_url = "https://hooks.slack.com/services/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"
Errer_logger_handler = SlackHandler(host, Errer_url, method, secure=True) # 핸들러 생성. HTTPHandler에서 요구하는 형식을 따른다.
Errer_logger = logging.getLogger("jin")
Errer_logger_handler.setFormatter(f) # 핸들러에 출력 포맷 세팅
Errer_logger.setLevel(logging.INFO) # 레벨 세팅.
Errer_logger.addHandler(Errer_logger_handler) # 로거에 핸들러 추가

TOKEN = 'MTE1NDgxMTY1ODY5MTE1ODA3NQ.GR1vr-.E7kDzYJu08j5z2JFIOnBGYXN4zJ5ZhzUX9Hji0'

gc = gspread.service_account(filename='golden-agency-385110-9a8c83a04372.json')

#상점시트-러너 물건
wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1kLT0MtNC0MtpbYcku0VU6SbL6Qp12G2_q9k-gxIK1K0/edit#gid=0") 

#시스템 시트
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1Ds_D15XI_ujU1ovd43-S2FfruzIYiEGsLRPTZDC1Pz4/edit#gid=208945099") 


intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents) # client 생성. 디스코드와 연결

rjtemf = ['구형 심장제세동기', '심장제세동기', '진통제', '수제 붕대', '붕대', '구급키트', 
           '망치', '나이프', '새총', '드로잉나이프', '야구방망이', '야경봉', '골프채', '소방도끼',
            '마체테', '전기톱', '활', '석궁', '토마호크', '테이저건', '작살총', '데저트이글']

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
    keywords = ['기록', '각성제', '재화', '장착', '탈착', '치료', '양도', '재화양도', 
                '파기', '갈취', '보관', '출고', '전투', 
                '조사', '섭취', '요리', '제작', '사용', '불침번'] # 키워드
    print("! 멘션을 확인하는 함수를 호출합니다")
    
                    ###################### 키워드 별 함수 호출. 키워드가 늘어나면 여기가 길어진다. ######################
    if first_keyword in keywords: # 준비된 키워드 내용(25)중에 첫번째 키워드가 있으면 (예시 : '다이스')
        if first_keyword == '기록': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = sozi(mention_keyword, message) 

            await message.channel.send(keyword_action_return, reference=message) # 답장 o
            
        if first_keyword == '각성제': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = Experience_value(mention_keyword, message) 
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o
            
        if first_keyword == '재화': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = mony(mention_keyword, message)
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        if first_keyword == '장착': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = weapon(mention_keyword, message)
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        if first_keyword == '탈착': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = off(mention_keyword, message)
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        if first_keyword == '치료': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = treat(mention_keyword, message)
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        if first_keyword == '양도': # 첫번째 키워드가 '다이스' 라면
            print('! 역극전투 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = shere(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o
        
        if first_keyword == '재화양도': # 첫번째 키워드가 '다이스' 라면
            print('! 재화양도 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = shere_G(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        if first_keyword == '파기': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = destruction(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        if first_keyword == '갈취': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = chantage(mention_keyword, message)  
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        if first_keyword == '보관': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = storage(mention_keyword, message)  
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        elif first_keyword == '출고': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = storage_out(mention_keyword, message)  
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        elif first_keyword == '조사': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = Dice(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        elif first_keyword == '섭취': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = eat(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        elif first_keyword == '요리': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = cook(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        elif first_keyword == '사용': # 첫번째 키워드가 '다이스' 라면
            print('! 다이스 굴리는 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = use(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        elif first_keyword == '불침번': # 첫번째 키워드가 '다이스' 라면
            print('! 불침번 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = cool(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        elif first_keyword == '요리': # 첫번째 키워드가 '다이스' 라면
            print('! 요리 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = cook(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o

        elif first_keyword == '제작': # 첫번째 키워드가 '다이스' 라면
            print('! 제작 함수를 호출합니다.')
            # 다이스 굴리는 함수 호출. 매개변수로는 멘션으로 받은 키워드 (예시 : ['다이스', '1d2']) 를 넘기고, 리턴값을 keyword_action_return에 저장한다.
            keyword_action_return = make(mention_keyword, message)
            
            await message.channel.send(keyword_action_return, reference=message) # 답장 o





    else:
        await message.channel.send("양식 오류. 양식 확인 후 재시도 해주시길 바랍니다.", reference=message) # 답장 o
    #################################################################################################

                

def select_sheet(sheet_name): #상점시트
    worksheet = wks.worksheet(sheet_name)
    return worksheet

def select_sheet_2(sheet_name): #시스템시트
    worksheet = sh.worksheet(sheet_name)
    return worksheet

#소지품 넣는 함수
def my_bag(keyword,things_2,things_3):
    print('! 소지품 넣는 함수를 호출합니다.')
    print(keyword) 
    worksheet = select_sheet('생존자 목록')
    #logger.info('{}'.format('아이디 찾기 완료!'))

    cell = worksheet.find(keyword)
    print("Found something at R%sC%s" % (cell.row, cell.col))
    val = worksheet.cell(cell.row, 9).value
    print(val)
    if val != None:
        all_shop_info =  spliT(val) #물건들
    else: all_shop_info = [[],[]]

    print(all_shop_info)            
    #logger.info(f'기존 물건: {all_shop_info}')
    all_shop_info_1 = all_shop_info[0]
    all_shop_info_2 = all_shop_info[1]

    print(all_shop_info_1)
        
    logger.info(f"{keyword}의 기존 물건: {all_shop_info}\n{nowDatetime}")

    for t in range(len(things_2)) :
        if things_2[t] in rjtemf: #겹쳐서 넣을 수 없는 거
            all_shop_info_1.append(things_2[t])
            all_shop_info_2.append(1)
            if len(all_shop_info_1) > 5:
                    return -1
        else:  
            if things_2[t] in all_shop_info_1:
                print("있다")
                a = int(all_shop_info_1.index(things_2[t]))
                if all_shop_info_2[a] + int(things_3[t]) >5:
                    return -1
                all_shop_info_2[a] += int(things_3[t])

            else:
                all_shop_info_1.append(things_2[t])
                all_shop_info_2.append(things_3[t])
                if len(all_shop_info_1) > 5:
                    return -1
                
    logger.info(f"{keyword}의 넣은 후: {all_shop_info}\n{nowDatetime}")
    print(f"{keyword}의 넣은 후: {all_shop_info}\n{nowDatetime}")

    thing_list = ""

    for i in range(len(all_shop_info_1)):
        thing_list += f'{all_shop_info_1[i]}({all_shop_info_2[i]}),'
        print(thing_list)

    print(thing_list)

    try:
        print( thing_list)
        print('업데이트')
        worksheet.update_cell(cell.row, 9, thing_list[:-1])

    except:
        logger.error("물건을 넣는 도중 오류가 발생했습니다.")
        Errer_logger.error("물건을 넣는 도중 오류가 발생했습니다.")
        print('API 에러 발생. 총괄계 문의 부탁드립니다.')
        return 'API 에러 발생. 총괄계 문의 부탁드립니다.'

#공용창고 넣는 함수
def storagE(things_2,things_3):
    print('! 창고에 넣는 함수를 호출합니다.')
    worksheet = select_sheet('공용창고')
    #logger.info('{}'.format('아이디 찾기 완료!'))
    all_shop_info = worksheet.get('C4:D23')              
    #logger.info(f'기존 물건: {all_shop_info}')
    all_shop_info_1 = []
    all_shop_info = [v for v in all_shop_info if v!=['-', '-']]   
    for i in all_shop_info:
        all_shop_info_1.append(i[0])
        
    print( all_shop_info_1)
    logger.info(f"기존 물건: {all_shop_info}\n{nowDatetime}")

    for t in range(len(things_2)) :
        if things_2[t] in rjtemf: #겹쳐서 넣을 수 없는 거
            all_shop_info.append([things_2[t],1])
            print(all_shop_info)
        else:  
            if things_2[t] in all_shop_info_1:
                print("있다")
                a = int(all_shop_info[all_shop_info_1.index(things_2[t])][1])
                all_shop_info[all_shop_info_1.index(things_2[t])][1] = a + int(things_3[t])
            else:
                print(len(all_shop_info))
                if len(all_shop_info) > 19:
                    return -1
                all_shop_info.append([things_2[t],things_3[t]])

    logger.info(f"넣은 후: {all_shop_info}\n{nowDatetime}")
    for i in range(20-len(all_shop_info)):
        all_shop_info.append(['-', '-'])               
    try:
        print( all_shop_info)
        print('업데이트')
        worksheet.update('C4:D23', all_shop_info)
    except:
        logger.error("물건을 넣는 도중 오류가 발생했습니다.")
        Errer_logger.error("물건을 넣는 도중 오류가 발생했습니다.")
        return 'API 에러 발생. 총괄계 문의 부탁드립니다.'

#물품 분리함수
def spliT(second_keyword):
    food =second_keyword.strip().split(',')
    things = [i.strip() for i in food ]
    things_2 = []
    things_3 = []
    for i in things:
        if '(' in i:
            a = i.strip().split('(')
            things_2.append(a[0])
            things_3.append(int(a[1][:-1])) 
        else:
            return -1
    for t in range(len(things_2)):
        if things_2[t] in rjtemf: #겹쳐서 넣을 수 없는 거
            if things_3[t] >1:
                for o in range(int(things_3[t])-1):
                    things_2.append(things_2[t])
                    things_3.append(1)
                things_3[t] = 1
    return [things_2, things_3]

def correcT(keyword,things_2,things_3):
    print('! 소지품 확인 함수를 호출합니다.')
    worksheet = select_sheet('생존자 목록')
    #logger.info('{}'.format('아이디 찾기 완료!'))
    cell = worksheet.find(keyword)
    print("Found something at R%sC%s" % (cell.row, cell.col))
    val = worksheet.cell(cell.row, 9).value
    print(val)
    if val != None:
        all_shop_info =  spliT(val) #물건들
    else: all_shop_info = []

    print(all_shop_info)            
    #logger.info(f'기존 물건: {all_shop_info}')
    all_shop_info_1 = all_shop_info[0]
    all_shop_info_2 = all_shop_info[1]

    print(all_shop_info_1)
    

    for t in range(len(things_2)) :
        if things_2[t] in all_shop_info_1:
            p = all_shop_info_1.index(things_2[t])
            a = int(all_shop_info_1.index(things_2[t]))
            
            all_shop_info_2[a] -= int(things_3[t])
            if all_shop_info_2[a] < 0:
                print(-1)
                return -1
            if all_shop_info_2[a] == 0:
                del all_shop_info_2[a]
                del all_shop_info_1[a]
            
            
        else:
            return -1
    a=0
    logger.info(f"{keyword}의 결과: {all_shop_info}\n{nowDatetime}")

    thing_list = ""

    for i in range(len(all_shop_info_1)):
        thing_list += f'{all_shop_info_1[i]}({all_shop_info_2[i]}),'
        print(thing_list)

    print(thing_list)

    try:
        print( thing_list)
        print('업데이트')
        worksheet.update_cell(cell.row, 9, thing_list[:-1])

    except:
        logger.error("물건을 넣는 도중 오류가 발생했습니다.")
        Errer_logger.error("물건을 넣는 도중 오류가 발생했습니다.")
        print('API 에러 발생. 총괄계 문의 부탁드립니다.')
        return 'API 에러 발생. 총괄계 문의 부탁드립니다.'

#공용창고 여부 확인함수-삭제시키고 넣기까지 함
def storagE_correcT(things_2,things_3):
    print('! 공용창고 삭제 함수를 호출합니다.')
    worksheet = select_sheet('공용창고')
    #logger.info('{}'.format('아이디 찾기 완료!'))
    all_shop_info = worksheet.get('C4:D23')               
    #logger.info(f'기존 물건: {all_shop_info}')
    all_shop_info = [v for v in all_shop_info if v!=['-', '-']]   
    all_shop_info_1 = []
    for i in all_shop_info:
        all_shop_info_1.append(i[0])
    logger.info(f"기존 물건: {all_shop_info}\n{nowDatetime}")

    for t in range(len(things_2)) :
        if things_2[t] in all_shop_info_1:
            print(things_2[t])
            p = all_shop_info_1.index(things_2[t] )
            a = int(all_shop_info[all_shop_info_1.index(things_2[t])][1])
            all_shop_info[all_shop_info_1.index(things_2[t])][1] = a - int(things_3[t])
            if a - int(things_3[t]) < 0:
                print(-1)
                return -1
            if a - int(things_3[t]) == 0:
                print(p)
                all_shop_info[all_shop_info_1.index(things_2[t])] = [' ', ' ']
                all_shop_info_1[p] = " "
                print(all_shop_info_1[p])
            
        else:
            return -1
    a=0
    print('종료')
    for i in range(len(all_shop_info_1)):
        try: m = all_shop_info[a][0]
        except: m = ' '
        if m == ' ':
            all_shop_info.pop(a)
            #all_shop_info.append(['-','-'])
            print(all_shop_info)
        else: a += 1
    print(a)
    logger.info(f"넣은 후: {all_shop_info}\n{nowDatetime}")
    for i in range(20-len(all_shop_info)):
        all_shop_info.append(['-', '-'])
        print(all_shop_info)

    worksheet.update('C4:D23', all_shop_info)

#재화기록함수
def mony_sozi(worksheet, keyword, second_keyword):
    user =  worksheet.find(keyword)
    print("Found something at R%sC%s" % (user.row, user.col))

    mOny = int(worksheet.cell(user.row, 4).value)
    print(mOny)
    logger.info(f"{keyword}의 기존 재화: {mOny}\n{nowDatetime}")
    mOny += second_keyword
    logger.info(f"{keyword}의 이후 재화: {mOny}\n{nowDatetime}")
    if mOny <0:
        return '재화가 부족합니다. 재화를 확인해주세요.'
    worksheet.update_cell(user.row, 4, mOny )
    return mOny

#--------------------------------------------------------------------------------------------------

# 기록함수
def sozi(mention_keyword, message):
    print('! 물품 소지 함수를 호출합니다.')      
    second_keyword = mention_keyword[2].strip() #물품명
    if spliT(second_keyword) == -1:
        return "양식 오류. 양식 확인 후 재시도 해주시길 바랍니다."
    things_2 = spliT(second_keyword)[0]
    things_3 = spliT(second_keyword)[1]
    print(things_2)
    print(things_3)
    keyword = mention_keyword[0].strip()

    try:
        if my_bag(keyword,things_2,things_3) == -1:
            return "현재 소지할 수 있는 소지품의 갯수를 초과하였습니다."
        return f"{keyword}, {mention_keyword[2]} 기록 확인되었습니다."
        
    except:
        logger.error("기록 도중 오류가 발생했습니다.")
        Errer_logger.error("기록 도중 오류가 발생했습니다.")

#각성제
def Experience_value(mention_keyword, message):
    print('! 경험치 함수를 호출합니다.')      
    things_2 = '각성제'
    things_3 = 1
    keyword = mention_keyword[0].strip()
    second_keyword = mention_keyword[2].strip() #스탯
    worksheet = select_sheet_2("생존자목록")
    user =  worksheet.find(keyword)
    print("Found something at R%sC%s" % (user.row, user.col))

    if correcT(keyword,['각성제'],['1']) == -1:
            return "물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."
    
    stats = {'근력':22, '민첩':25, '관찰':38, '행운':31 }

    try:
        a = int(worksheet.cell(user.row, stats[second_keyword]).value)
        print(a)
    except:
        a = 0
    a += int(1)
    worksheet.update_cell(user.row, stats[second_keyword],a)
    worksheet.update_cell(user.row, 51,bool(True))


    return f"사용 확인되었습니다."

#재화
def mony(mention_keyword, message):
    print('! 재화 함수를 호출합니다.')      
    second_keyword = int(mention_keyword[2].strip().strip('G').strip('g').strip('원')) #재화
    keyword = mention_keyword[0].strip()
    worksheet = select_sheet("러너관리")
    return f"{second_keyword}G 기록 확인되었습니다. 총 재화: {mony_sozi(worksheet, keyword, second_keyword)}G"

#무기 장착
def weapon(mention_keyword, message):
    second_keyword = mention_keyword[2].strip() #무기 종류
    therd_keyword = mention_keyword[3].strip() #무기
    keyword = mention_keyword[0].strip()
    worksheet = select_sheet_2("생존자목록")
    user =  worksheet.find(keyword)
    print("Found something at R%sC%s" % (user.row, user.col))

    if second_keyword == '주무기' :
        worksheet.update_cell(user.row, 34,therd_keyword)
        return f'{therd_keyword} 장착 확인되었습니다.'

    elif second_keyword == '보조무기' :
        worksheet.update_cell(user.row, 33,therd_keyword)
        return f'{therd_keyword} 장착 확인되었습니다.'
        pass

    else:
        worksheet.update_cell(user.row, 32,therd_keyword)
        return f'{therd_keyword} 장착 확인되었습니다.'
    pass

#무기 탈착
def off(mention_keyword, message):
    second_keyword = mention_keyword[2].strip() #무기 종류
    keyword = mention_keyword[0].strip()
    worksheet = select_sheet_2("생존자목록")
    user =  worksheet.find(keyword)
    print("Found something at R%sC%s" % (user.row, user.col))

    if second_keyword == '주무기' :
        worksheet.update_cell(user.row, 34,' ')
        return '탈착 확인되었습니다.'

    elif second_keyword == '보조무기' :
        worksheet.update_cell(user.row, 33,' ')
        return '탈착 확인되었습니다.'
        pass

    else:
        worksheet.update_cell(user.row, 32,' ')
        return '탈착 확인되었습니다.'
    pass

#치료
def treat(mention_keyword, message):
    print('! 치료함수를 호출합니다.')
    second_keyword = mention_keyword[3].strip() #물품명
    people = mention_keyword[2].strip() #대상자
    keyword = mention_keyword[0].strip()

    if spliT(second_keyword) == -1:
        return "양식 오류. 양식 확인 후 재시도 해주시길 바랍니다."
    things_2 = spliT(second_keyword)[0]
    things_3 = spliT(second_keyword)[1]
    kit = {'진통제': 20, '붕대': 40, '수제 붕대': 30, '구급키트': 80, '응급 주사기': 20, '심장제세동기': 1, '구형 심장제세동기': 1}
    print(kit[things_2[0]])
    
    if things_2 ==['응급 주사기']:
        if correcT(keyword,things_2,things_3) == -1:
            return "치료물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."
        worksheet = select_sheet_2('생존자목록')
        user =  worksheet.find(people)
        print("Found something at R%sC%s" % (user.row, user.col))
        worksheet.update_cell(user.row, 48,bool(True))
        return f'{things_2} 사용 확인되었습니다.'

    elif things_2 ==['심장제세동기']:
        if correcT(keyword,things_2,things_3) == -1:
            return "치료물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."
        worksheet = select_sheet_2('생존자목록')
        user =  worksheet.find(people)
        print("Found something at R%sC%s" % (user.row, user.col))
        worksheet.update_cell(user.row, 12,1)
        return f'{things_2} 사용 확인되었습니다.\n{people}, 체력 1로 부활합니다.'
    elif things_2 ==['구형 심장제세동기']:
        print('구형 심장제세동기')
        if correcT(keyword,things_2,things_3) == -1:
            return "치료물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."
        worksheet = select_sheet_2('생존자목록')
        a = random.randrange(1,101)
        print(a)
        user =  worksheet.find(people)
        print("Found something at R%sC%s" % (user.row, user.col))
        a = random.randrange(1,101)
        print(a)
        if a < 40:
            return '구형 심장제세동기 사용 실패합니다. 구형 심장제세동기 파기됩니다' 

        worksheet.update_cell(user.row, 12,1)
        return f'{things_2} 사용 확인되었습니다.\n{people}, 체력 1로 부활합니다.'

    elif things_2 ==['구급키트']:
        if correcT(keyword,things_2,things_3) == -1:
            return "치료물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."
        worksheet = select_sheet_2('생존자목록')
        porsen =people.strip().split(',')
        people = [y.strip() for y in porsen ]
        heal = 80/len(people)
        for t in people:
            user =  worksheet.find(t)
            print("Found something at R%sC%s" % (user.row, user.col))
            a = int(worksheet.cell(user.row, 12).value)
            logger.info(f"{keyword}의 이전 체력: {a}\n{nowDatetime}")
            a += heal
            if a > 150:
                a = 150
            logger.info(f"{keyword}의 이후 체력: {a}\n{nowDatetime}")
            worksheet.update_cell(user.row, 12,a)

        return f'{things_2} 사용 확인되었습니다.'

    else:
        if correcT(keyword,things_2,things_3) == -1:
            return "치료물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."
        worksheet = select_sheet_2('생존자목록')
        user =  worksheet.find(people)
        user2 =  worksheet.find(keyword)
        print("Found something at R%sC%s" % (user.row, user.col))
        a = int(worksheet.cell(user.row, 12).value)
        logger.info(f"{keyword}의 이전 체력: {a}\n{nowDatetime}")
        b = worksheet.row_values(user2.row)
        print(b)
        print(a)

        o = 0

        for i in things_2:
            print(a)
            a += int(kit[i])*int(things_3[o])
            if a > 150:
                a = 150
            o += 1
        
        logger.info(f"{keyword}의 이후 체력: {a}\n{nowDatetime}")

        worksheet.update_cell(user.row, 12,a)
        return f'{things_2} 사용 확인되었습니다.'

#양도
def shere(mention_keyword, message):
    print('! 양도함수를 호출합니다.')
    things = mention_keyword[3].strip() #물품명
    if spliT(things) == -1:
        return "양식 오류. 양식 확인 후 재시도 해주시길 바랍니다."
    things_2 = spliT(things)[0]
    things_3 = spliT(things)[1]
    print(things_2)
    print(things_3)
    keyword = mention_keyword[0].strip()
    person = mention_keyword[2].strip() 

    if correcT(keyword,things_2,things_3) == -1:
        return "양도물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."

    else:
        if my_bag(person,things_2,things_3) == -1:
            my_bag(keyword,things_2,things_3) 
            return f'소지품이 가득 차 양도가 불가능합니다.'
        return f'{keyword}, [ {things} ]양도 확인했습니다.'

#재화양도
def shere_G(mention_keyword, message):
    goled = int(mention_keyword[3].strip().strip('G').strip('g').strip('원')) #재화
    keyword = mention_keyword[0].strip()
    porsen = mention_keyword[2].strip()
    worksheet = select_sheet("러너관리")

    a = mony_sozi(worksheet, keyword, -goled)
    if a == '재화가 부족합니다. 재화를 확인해주세요.':
        return '재화가 부족합니다. 재화를 확인해주세요.'
    b = mony_sozi(worksheet, porsen, goled)
    return f"{goled}G 양도 확인되었습니다.\n{keyword}의 잔여 재화: {a}G\n{porsen}의 잔여 재화: {b}G"

#파기
def destruction(mention_keyword, message):
    second_keyword = mention_keyword[2].strip() #물품명
    if spliT(second_keyword) == -1:
        return "양식 오류. 양식 확인 후 재시도 해주시길 바랍니다."
    things_2 = spliT(second_keyword)[0]
    things_3 = spliT(second_keyword)[1]
    print(things_2)
    print(things_3)
    keyword = mention_keyword[0].strip()

    try:
        if correcT(keyword,things_2,things_3) == -1:
            return "물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."

        return f"{keyword}, {mention_keyword[2]} 파기 확인되었습니다."
        
    except:
        logger.error("기록 도중 오류가 발생했습니다.")
        Errer_logger.error("기록 도중 오류가 발생했습니다.")
    pass

#갈취
def chantage(mention_keyword, message):
    print('! 갈취 함수를 호출합니다.')
    things = mention_keyword[3].strip() #물품명
    if spliT(things) == -1:
        return "양식 오류. 양식 확인 후 재시도 해주시길 바랍니다."
    things_2 = spliT(things)[0]
    things_3 = spliT(things)[1]
    print(things_2)
    print(things_3)
    keyword = mention_keyword[0].strip()
    person = mention_keyword[2].strip() 

    a =correcT(person,things_2,things_3)

    if a == -1:
        return "물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."

    else:
        my_bag(keyword,things_2,things_3)
        return f'{keyword}, [ {things} ]을 {person}(으)로부터 갈취합니다.'

#보관
def storage(mention_keyword, message)  :
    print('! 보관함수를 호출합니다.')
    things = mention_keyword[2].strip() #물품명
    if spliT(things) == -1:
        return "양식 오류. 양식 확인 후 재시도 해주시길 바랍니다."
    things_2 = spliT(things)[0]
    things_3 = spliT(things)[1]
    print(things_2)
    print(things_3)
    keyword = mention_keyword[0].strip()

    if correcT(keyword,things_2,things_3) == -1:
        return "물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."

    else:
        l = storagE(things_2,things_3)
        if l == -1:
            my_bag(keyword,things_2,things_3)
            return '창고가 가득 차 넣을 수 없습니다.'

        return f'{keyword}, [ {things} ]보관 확인했습니다.'

#출고
def storage_out(mention_keyword, message)  :
    print('! 출고 함수를 호출합니다.')
    things = mention_keyword[2].strip() #물품명
    if spliT(things) == -1:
        return "양식 오류. 양식 확인 후 재시도 해주시길 바랍니다."
    things_2 = spliT(things)[0]
    things_3 = spliT(things)[1]
    print(things_2)
    print(things_3)
    keyword = mention_keyword[0].strip()

    a =storagE_correcT(things_2,things_3)

    if a == -1:
        return "창고의 재고가 부족합니다. 창고를 확인해주세요."

    else:
        my_bag(keyword,things_2,things_3)
        return f'{keyword}, [ {things} ]을 소지합니다.'


#다이스
def Dice(mention_keyword, message):
    usear = mention_keyword[0].strip()
    which = mention_keyword[2].strip()
    worksheet = select_sheet("조사")

    list = [ [ usear, which ] ]
    print(list)

    worksheet.update("B3:C3",list)

    val = worksheet.get("E3:G3")
    print(val)

    return f"{usear}, {which} 판정: {val[0][0]}\n{which}판정 {val[0][2]} 입니다."

#섭취
def eat(mention_keyword, message):
    print('! 섭취함수를 호출합니다.')
    second_keyword = mention_keyword[3].strip() #물품명
    people = mention_keyword[2].strip() #대상자
    keyword = mention_keyword[0].strip()

    if spliT(second_keyword) == -1:
        return "양식 오류. 양식 확인 후 재시도 해주시길 바랍니다."
    things_2 = spliT(second_keyword)[0]
    things_3 = spliT(second_keyword)[1]
    worksheet = select_sheet_2('생존자목록')
    user =  worksheet.find(people)
    print("Found something at R%sC%s" % (user.row, user.col))
    a = int(worksheet.cell(user.row, 14).value)
    
    worksheet2 = select_sheet_2('레시피')

    thing =  worksheet2.get('P4:Q54')
    print(thing)

    if correcT(keyword,things_2,things_3) == -1:
        return "물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."

    for i in range(len(things_2)):
        for n in thing:
            print(n)
            if n[0] == things_2[i]:
                a += int(n[1])*int(things_3[i])

    worksheet.update_cell(user.row, 14,a)
    return f'{things_2} 섭취 확인되었습니다.'

#요리
def cook(mention_keyword, message):
    keyword = mention_keyword[0].strip()
    which = mention_keyword[2].strip() #요리 이름
    worksheet = select_sheet_2("레시피")
    worksheet2 = select_sheet("생존자 목록")
    cell = worksheet.find(which)
    print("Found something at R%sC%s" % (cell.row, cell.col))
    a = worksheet.cell(cell.row, 5).value
    things_2 = spliT(a)[0]
    things_3 = spliT(a)[1]

    if correcT(keyword,things_2,things_3) == -1:
        return "재료를 소지하고 있지 않습니다. 소지품을 확인해주세요."
    
    b = int(worksheet.cell(cell.row, 11).value)

    cell2 = worksheet2.find(keyword)
    print("Found something at R%sC%s" % (cell2.row, cell2.col))

    number = random.randrange(1,101)
    if number < b :
        if my_bag(keyword,[f'성공한 {which}'],[1]) == -1:
            return "현재 소지할 수 있는 소지품의 갯수를 초과하였습니다."
        return f'성공한 {which}이/가 완성되었습니다.'
    else:
        if my_bag(keyword,[f'실패한 {which}'],[1]) == -1:
            return "현재 소지할 수 있는 소지품의 갯수를 초과하였습니다."
        return f'실패한 {which}이/가 완성되었습니다.'

    pass

#사용
def use(mention_keyword, message):
    print('! 사용함수를 호출합니다.')
    second_keyword = mention_keyword[3].strip() #물품명
    people = mention_keyword[2].strip() #대상자
    keyword = mention_keyword[0].strip()

    food =people.strip().split(',')
    things = [i.strip() for i in food ]
    worksheet = select_sheet_2('생존자목록')
    
    if second_keyword == '큰 천막':
        if correcT(keyword,['큰 천막'],[1]) == -1:
            return "물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."
        if len(things) == 5:
            for i in things:
                print(i)
                cell = worksheet.find(i)
                print("Found something at R%sC%s" % (cell.row, cell.col))
                a = int(worksheet.cell(cell.row, 17).value)
                a -= 10
                worksheet.update_cell(cell.row, 17,a)
        else: 
            return '사용인원 오류. 사용인원을 확인해주세요.'

    if second_keyword == '작은 천막':
        if len(things) == 3:
            if correcT(keyword,['작은 천막'],[1]) == -1:
                return "물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."
            for i in things:
                cell = worksheet.find(i)
                print("Found something at R%sC%s" % (cell.row, cell.col))
                a = int(worksheet.cell(cell.row, 17).value)
                a -= 5
                worksheet.update_cell(cell.row, 17,a)
        else: 
            return '사용인원 오류. 사용인원을 확인해주세요.'

    return f'{second_keyword} 사용 확인되었습니다.'

#동상
def cool(mention_keyword, message):
    usear = mention_keyword[0].strip()
    which = '행운'
    worksheet = select_sheet("동상")

    list = [ [ usear, which ] ]
    print(list)

    worksheet.update("B3:C3",list)

    val = worksheet.get("D3:G3")
    print(val[0][0])
    print(val[0][1])

    if int(val[0][1]) <= 10:
        return f"{usear}, 동상 판정: {val[0][1]}\n동상판정 대성공 입니다. 신체 말단 부분의 동상 진행도가 [ 0 ] 상승합니다."

    elif 10 < int(val[0][1]) <= int(val[0][0]) :
        worksheet2 = select_sheet_2('생존자목록')
        cell = worksheet2.find(usear)
        print("Found something at R%sC%s" % (cell.row, cell.col))
        a = int(worksheet2.cell(cell.row, 17).value)
        a += 10
        print(a)
        worksheet2.update_cell(cell.row, 17,a)
        return f"{usear}, 동상 판정: {val[0][1]}\n동상판정 성공 입니다. 신체 말단 부분의 동상 진행도가 [ 10 ] 상승합니다."

    elif int(val[0][0]) < int(val[0][1]) < 110 :
        worksheet2 = select_sheet_2('생존자목록')
        cell = worksheet2.find(usear)
        print("Found something at R%sC%s" % (cell.row, cell.col))
        a = int(worksheet2.cell(cell.row, 17).value)
        a += 20
        worksheet2.update_cell(cell.row, 17,a)
        print(a)
        return f"{usear}, 동상 판정: {val[0][1]}\n동상판정 실패 입니다. 신체 말단 부분의 동상 진행도가 [ 20 ] 상승합니다."

    elif 110 < int(val[0][1]):
        worksheet2 = select_sheet_2('생존자목록')
        cell = worksheet2.find(usear)
        print("Found something at R%sC%s" % (cell.row, cell.col))
        a = int(worksheet2.cell(cell.row, 17).value)
        a += 25
        worksheet2.update_cell(cell.row, 17,a)
        print(a)
        return f"{usear}, 동상 판정: {val[0][1]}\n동상판정 대실패 입니다. 신체 말단 부분의 동상 진행도가 [ 25 ] 상승합니다."

    pass

#제작
def make(mention_keyword, message):
    keyword = mention_keyword[0].strip()
    which = mention_keyword[2].strip() #물건 이름
    worksheet = select_sheet_2("레시피")
    worksheet2 = select_sheet("생존자 목록")

    thing =  worksheet.get('D24:K35')
    print(thing)

    b = 0
    a = ''
    for n in thing:
        print(n)
        if n[0] == which:
            b = int(n[7])
            a = n[1]
    
    things_2 = spliT(a)[0]
    things_3 = spliT(a)[1]

    if correcT(keyword,things_2,things_3) == -1:
        return "물품을 소지하고 있지 않습니다. 소지품을 확인해주세요."

    cell2 = worksheet2.find(keyword)
    print("Found something at R%sC%s" % (cell2.row, cell2.col))

    number = random.randrange(1,101)
    if number < b :
        if my_bag(keyword,[which],[1]) == -1:
            return "현재 소지할 수 있는 소지품의 갯수를 초과하였습니다."
        return f'{which}을/를 만드는데 성공하였습니다.'
    else:
        return f'{which}을/를 만드는데 실패하였습니다. {a}이/가 파기됩니다.'

client.run(TOKEN)