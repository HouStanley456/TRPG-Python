from flask import Flask

app = Flask(__name__)
#LineBot
from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, FlexSendMessage, URIAction
from urllib.parse import parse_qsl

#PythonGame
import time,os,random  
from enum import Enum

class State(Enum):
    NORMAL = 1
    INPUT_MONSTER_LEVEL = 2
    INPUT_HERO_NAME =3
    COMBAT = 4
    OPTION = 5
    GAMEOVER = 6
#LineBot設定
line_bot_api = LineBotApi('你的 CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('你的 CHANNEL_SECRET')


#--------------------------------------------------------------------------#
#PythonGame 角色基本code

class character:
    #新角色能力值
    def __init__(self,name,maxhp=100,ac=15,speed=1.0,money=0):
        self.name=name
        self.hp=maxhp
        self.maxhp=maxhp
        self.minac=int(ac*0.5)
        self.maxac=int(ac*1.5)
        self.speed=speed
        self.exp=0
        self.money=money
        self.maxexp=100
        self.rank=0
        self.challenge=0
    #升等    
    def rankup(self):
        self.maxhp+=10+self.rank
        self.minac+=random.randint(5,8)
        self.maxac+=random.randint(8,12)
        self.hp=self.maxhp
        self.speed+=0.1
        self.exp-=self.maxexp
        self.maxexp=int(self.maxexp*1.1)
        self.rank+=1
    #查看能力值
    def printa(self):
        pA = []
        pA=['{}' .format(self.name)]
        pA.append('等級：%d(%d/%d)' %(self.rank,self.exp,self.maxexp))
        pA.append('生命值：%d/%d' %(self.hp,self.maxhp))
        pA.append('攻擊力：%d-%d' %(self.minac,self.maxac))
        pA.append('速度：%.1f' %self.speed)
        pA.append('財富：%d' %self.money)
        pA.append('敵人等級：%d' %self.challenge)
        return pA
        
    #傷害
    def ac(self):
            return random.randint(self.minac,self.maxac)
    #存檔
    def save(self):
        s=self.name+'\n'+str(self.rank)+'\n'+str(self.exp)+'\n'+str(self.maxexp)+'\n'+str(self.hp)+'\n'
        s+=str(self.maxhp)+'\n'+str(self.minac)+'\n'+str(self.maxac)+'\n'+str(self.speed)+'\n'+str(self.money)+'\n'
        s+=str(self.challenge)
        with open( f'{user_id}.save','w') as f:
            f.write(s)

class Monster:
    #新角色能力值
    def __init__(self,name,maxhp=100,ac=10,speed=1.0,money=0):
        self.name=name
        self.hp=maxhp
        self.maxhp=maxhp
        self.minac=int(ac*0.5)
        self.maxac=int(ac*1.5)
        self.speed=speed
        self.exp=0
        self.money=money
        self.maxexp=100
        self.rank=0
        self.challenge=0
    #升等    
    def rankup(self):
        self.maxhp+=10+self.rank
        self.minac+=random.randint(2,8)
        self.maxac+=random.randint(4,12)
        self.hp=self.maxhp
        self.speed+=0.1
        self.exp-=self.maxexp
        self.maxexp=int(self.maxexp*1.1)
        self.rank+=1
    #傷害
    def ac(self):
            return random.randint(self.minac,self.maxac)

class BOSS:
    def __init__(self,name,maxhp=250,ac=15,speed=1.5,money=0):
        self.name=name
        self.hp=maxhp
        self.maxhp=maxhp
        self.minac=int(ac*0.5)
        self.maxac=int(ac*1.5)
        self.speed=speed
        self.exp=0
        self.money=money
        self.maxexp=100
        self.rank=0
        self.challenge=0
    #升等    
    def rankup(self):
        self.maxhp+=10+self.rank
        self.minac+=random.randint(2,8)
        self.maxac+=random.randint(4,12)
        self.hp=self.maxhp
        self.speed+=0.1
        self.exp-=self.maxexp
        self.maxexp=int(self.maxexp*1.1)
        self.rank+=1
    #傷害
    def ac(self):
            return random.randint(self.minac,self.maxac)
#----------------------------#定義 player
          
state = State.NORMAL

player = character('英雄')

#------------------------------------------------------

#LineBot認證
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
#------------------------------------------------------

#串聯LineBOT API
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    global user_id
    
    user_id = event.source.user_id
#    print(user_id)

    
    if text == '@開始TRPG': #開始選單
        option(event)
    
    if text == '@打怪去':
        choose(event)
    

        
    if text == '@開始遊戲':
        global player
        heroname(event)

        
    
    if text == '@查看屬性':
        pA=player.printa()
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='\n'.join(pA)),TemplateSendMessage(alt_text='行動選單',
                template=ButtonsTemplate(thumbnail_image_url='https://i.imgur.com/wJPxRAo.png',title='行動選單',text=' 英雄你現在要做什麼？',
                                         actions=[MessageTemplateAction(label='打怪去',text='@打怪去'),
                                                  MessageTemplateAction(label='查看屬性',text='@查看屬性'),
                                                  MessageTemplateAction(label='治癒',text='@治癒'),
                                                  MessageTemplateAction(label='存檔',text='@存檔'),]))])

    if text == '@存檔':       
        player.save()
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='存檔完成'),TemplateSendMessage(alt_text='行動選單',
                template=ButtonsTemplate(thumbnail_image_url='https://i.imgur.com/wJPxRAo.png',title='行動選單',text=' 英雄你現在要做什麼？',
                                         actions=[MessageTemplateAction(label='打怪去',text='@打怪去'),
                                                  MessageTemplateAction(label='查看屬性',text='@查看屬性'),
                                                  MessageTemplateAction(label='治癒',text='@治癒'),
                                                  MessageTemplateAction(label='存檔',text='@存檔'),]))])
    global state  
    if text == '@讀取檔案':
        load=loadhero(event)
        state = State.OPTION
        
        
    if text == '@治癒':
        flag1=heal(event, player)
          
      
      
    if text == '@遊戲說明':
        try:
            bubble = BubbleContainer(
                direction='ltr',  #項目由左向右排列
                header=BoxComponent(  #標題
                    layout='vertical',
                    contents=[
                        TextComponent(text='遊戲說明', weight='bold', size='xxl'),
                    ]
                ),
                hero=ImageComponent(  #主圖片
                    url='https://i.imgur.com/wve9pBL.gif',
                    size='full',
                    aspect_ratio='792:555',  #長寬比例
                    aspect_mode='cover',
                ),
                body=BoxComponent(  #主要內容
                    layout='vertical',
                    contents=[
                        TextComponent(text='簡介', size='md'),
                        BoxComponent(
                            layout='baseline',  #水平排列
                            margin='md',
                            contents=[
     
                                TextComponent(text='這是一款簡單的TRGB遊戲', size='sm', color='#999999', flex=0),
                            ]
                        ),
                        BoxComponent(
                            layout='vertical',
                            margin='lg',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    contents=[
                                        TextComponent(text='操作說明', color='#aaaaaa', size='sm', flex=2),
                                        TextComponent(text='根據圖示及文字進行輸入', color='#666666', size='sm', flex=5)
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    contents=[
                                        TextComponent(text='作者的話', color='#aaaaaa', size='sm', flex=2),
                                        TextComponent(text="享受著打怪練等的快感吧！", color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            ],
                     ),     
                 ],
             
             ),
                footer=BoxComponent(  #底部版權宣告
                       layout='vertical',
                       contents=[
                               TextComponent(text='遊戲作者：侯秉之', color='#888888', size='sm', align='center'),
                        ]
                 )
         )
     
            message = FlexSendMessage(alt_text="遊戲說明", contents=bubble)
            line_bot_api.reply_message(event.reply_token,message)
            
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
       
          
    #輸入怪物等級
    #global state
    if state == State.INPUT_MONSTER_LEVEL: 
        global ss
        ss = text
        flag=attackmonster(event, player)
        state = State.NORMAL

    #輸入英雄    
    elif state == State.INPUT_HERO_NAME:     
        global nn  
        nn = text
        flagname = newhero(event)
        state = State.NORMAL
    
    elif state == State.OPTION:
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text='行動選單',
                template=ButtonsTemplate(thumbnail_image_url='https://i.imgur.com/wJPxRAo.png',title='行動選單',text=' 英雄你現在要做什麼？',
                                         actions=[MessageTemplateAction(label='打怪去',text='@打怪去'),
                                                  
                                                  MessageTemplateAction(label='查看屬性',text='@查看屬性'),
                                                  MessageTemplateAction(label='治癒',text='@治癒'),
                                                  MessageTemplateAction(label='存檔',text='@存檔'),])))
#    elif state == State.GAMEOVER:
#        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='很遺憾英雄，你被怪物殺死了...遊戲結束...請重新開始遊戲'))
        
    
    elif state == State.COMBAT:
        state = State.INPUT_MONSTER_LEVEL
        try:
            bubble = BubbleContainer(
                direction='ltr',  #項目由左向右排列
                header=BoxComponent(  #標題
                    layout='vertical',
                    contents=[
                        TextComponent(text='戰鬥', weight='bold', size='xxl'),
                    ]
                ),
                hero=ImageComponent(  #主圖片
                    url='https://imgur.com/ZxNkVMR.jpg',
                    size='full',
                    aspect_ratio='792:555',  #長寬比例
                    aspect_mode='cover',
                ),
                body=BoxComponent(  #主要內容
                    layout='vertical',
                    contents=[
                        TextComponent(text='戰鬥準備', size='md'),
                        BoxComponent(
                            layout='baseline',  #水平排列
                            margin='md',
                            contents=[
     
                                TextComponent(text='怪物等級設定中', size='sm', color='#999999', flex=0),
                            ]
                        ),
                        BoxComponent(
                            layout='vertical',
                            margin='lg',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    contents=[
                                        TextComponent(text='怪物說明', color='#aaaaaa', size='sm', flex=2),
                                        TextComponent(text='這是一隻細菌怪', color='#666666', size='sm', flex=5)
                                    ],
                                ),
                                BoxComponent(
                                    layout='baseline',
                                    contents=[
                                        TextComponent(text='敵人能力', color='#aaaaaa', size='sm', flex=2),
                                        TextComponent(text="會把敵人往死裡打", color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            ],
                     ),     
                 ],
             
             ),
                footer=BoxComponent(  #底部版權宣告
                       layout='vertical',
                       contents=[
                               TextComponent(text='請直接輸入怪物等級', color='#888888', size='sm', align='center'),
                        ]
                 )
         )
     
            message = FlexSendMessage(alt_text="請輸入怪物等級", contents=bubble)
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

#Function

def heroname(event):
    global state
    state = State.INPUT_HERO_NAME
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入英雄名稱'))

def choose(event):
    global state
    state = State.COMBAT
    
   



def newhero(event):
    global player
    player = character(nn)
    line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=nn+'加入遊戲'),TemplateSendMessage(alt_text='行動選單',
            template=ButtonsTemplate(thumbnail_image_url='https://i.imgur.com/wJPxRAo.png',title='行動選單',text=' 英雄你現在要做什麼？',
                                     actions=[MessageTemplateAction(label='打怪去',text='@打怪去'),
                                              MessageTemplateAction(label='查看屬性',text='@查看屬性'),
                                              MessageTemplateAction(label='治癒',text='@治癒'),
                                              MessageTemplateAction(label='存檔',text='@存檔'),]))])


def loadhero(event):  
    if os.path.exists(f'{user_id}.save'):
        try:
            with open(f'{user_id}.save','r') as f:
                d=f.read().split('\n')
            player=character(d[0])
            player.rank=int(d[1])
            player.exp=int(d[2])
            player.maxexp=int(d[3])
            player.hp=int(d[4])
            player.maxhp=int(d[5])
            player.minac=int(d[6])
            player.maxac=int(d[7])
            player.speed=float(d[8])
            player.money=int(d[9])
            player.challenge=int(d[10])
            load=['歡迎回來，英雄！']
        except Exception as e:
            load=['存檔讀取出錯']        
    return load 


t = []            
def attackmonster(event,who):
    global times
    global attack
    attack = []
    
    s2= int(ss)

    if s2>0:
        # os.system('cls')
        #print('挑戰【%d】級怪物開始！\n' %s2)
        if who.challenge<s2:
            who.challenge=s2
            
        monster=Monster('怪物'+str(s2)+'號',s2*50,s2*8,s2/5+1,s2*random.randint(0,20))
        exp=int(s2*100*getexp(who.rank-s2))
        if s2%10==0:
            monster.hp+=40
            monster.minac+=6
            monster.maxac+=12
            monster.money+=s2//10*200
            exp*=2
            t=['這個怪物太強大了！']

        times=0
        while monster.hp>0 and who.hp>0:
            if monster.speed>who.speed:
                if attackevent(who,monster):
                    break
                #time.sleep(0.5)
                if attackevent(monster,who):
                    break
                #time.sleep(0.5)
            else:
                if attackevent(monster,who):
                    break
                #time.sleep(0.5)
                if attackevent(who,monster):
                    break
                #time.sleep(0.5)
                
        if who.hp>0:
            if monster.money>0:
                t=['你成功的消滅了怪物，經驗值和財富增加了！']
                
            else:
               t=['你成功的消滅了怪物，經驗值增加了！']
               
            who.exp+=exp
            
            ranktmp=0
            while who.exp>=who.maxexp:
                who.rankup()
                ranktmp+=1
            if ranktmp==1:
                t=[ '{}升等了，能力值獲得了提升！'.format(who.name) ]
            elif ranktmp>1 and ranktmp<100:
                t=[ '{}升等了，能力值獲得了大量的提升！'.format(who.name) ]
            elif ranktmp>=100:
                t=[ '{}一次升太多等囉，請把修改器開小一點！'.format(who.name) ]
                
            who.money+=monster.money
        else:
            t = ['很遺憾英雄，你被怪物殺死了...遊戲結束...請重新開始遊戲']
           
            #return True
    else:
        t=['沒有更弱的怪物了，英雄。']
    #return False
    try:
        
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='\n'.join(attack)),TextSendMessage('\n'.join(t)),TemplateSendMessage(alt_text='行動選單',
                template=ButtonsTemplate(thumbnail_image_url='https://i.imgur.com/wJPxRAo.png',title='行動選單',text=' 英雄你現在要做什麼？',
                                         actions=[MessageTemplateAction(label='打怪去',text='@打怪去'),
                                                  
                                                  MessageTemplateAction(label='查看屬性',text='@查看屬性'),
                                                  MessageTemplateAction(label='治癒',text='@治癒'),
                                                  MessageTemplateAction(label='存檔',text='@存檔')]))])
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

healing = []
def heal(event,who):
    os.system('cls')
    if who.hp<who.maxhp and who.money>0:
        if who.money>=who.maxhp-who.hp:
            healing =['在聖光的照射下，你恢復如初了！']
            who.money-=who.maxhp-who.hp
            who.hp=who.maxhp
        else:
            healing =['由于你的財富不足，牧師只治癒了你部分傷口...！']
            who.hp+=who.money
            who.money=0
    else:
        healing =['你的心靈得到救贖...但生命值沒有...']
    try:
        
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='\n'.join(healing)),TemplateSendMessage(alt_text='行動選單',
                template=ButtonsTemplate(thumbnail_image_url='https://i.imgur.com/wJPxRAo.png',title='行動選單',text=' 英雄你現在要做什麼？',
                                         actions=[MessageTemplateAction(label='打怪去',text='@打怪去'),
                                                  MessageTemplateAction(label='查看屬性',text='@查看屬性'),
                                                  MessageTemplateAction(label='治癒',text='@治癒'),
                                                  MessageTemplateAction(label='存檔',text='@存檔')]))])
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


attack = []  
def attackevent(A,B):
    global times
    times+=1
    ac=B.ac()
    A.hp-=ac
    attack.append(('<%d>\n【%s】攻擊【%s】！\n【%s】受到 %d 點傷害！\n【%s】剩餘生命值：%d\n' %(times,B.name,A.name,A.name,ac,A.name,A.hp)))
    if A.hp<=0:
        return 1
    else:
        return 0
    
    
def getexp(x):
    if x<5:
        return -0.198*x+1
    if x>=5:
        return 0.01


def option(event):    #開始選單
    try:
        message = TemplateSendMessage(
            alt_text='按鈕選單',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/ziK2sGp.png',
                title='開始遊戲選單',
                text=' 英雄歡迎來到夢中世界',
                actions=[
                    MessageTemplateAction(
                        label='開始遊戲',
                        text='@開始遊戲'
                        ),
                    MessageTemplateAction(
                        label='讀取檔案',
                        text='@讀取檔案'
                        ),
                    ＭessageTemplateAction(
                        label='遊戲說明',
                        text ='@遊戲說明'
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))
        


#-----------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(debug=True)



            
            
