import random

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent, GroupMessageEvent
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.permission import SUPERUSER

import os
import json
import numpy as np

with open(os.getcwd()+'/data/remake/remake.json','r',encoding='utf-8') as f:
    coundict=json.load(f)

CONTINENT_DICT = {
    'AF': '非洲',
    'EU': '欧洲',
    'AS': '亚洲',
    'OA': '大洋洲',
    'NA': '北美洲',
    'SA': '南美洲',
    'AN': '南极洲'
}

class Remake:
    remakelist=[]
    def __init__(self,times):
        self.remakelist=[]
        indices = self.__get_random_index(times)
        for index in indices:
            bp_instance = coundict[index]
            self.remakelist.append(bp_instance)

    def __get_random_index(self,times):
        alist=np.random.uniform(0,100,times)
        indices=[]
        for a in alist:
            for j in range(len(coundict)):
                if a>coundict[j]['left_prob'] and a<coundict[j]['right_prob']:
                    break
            indices.append(j)
        return indices

remake = on_command('重开', aliases={'remake', '重开'})
@remake.handle()
async def _(bot: Bot, event: GroupMessageEvent,args: Message = CommandArg()):
    user_id=event.get_user_id()
    if str(user_id) == "2289991923":
        messagestr1=f"恭喜你重开到位于 亚洲 的"
        messagestr2=f"日本！出生率：0.646\n"
        messagestr3=f"重开统计：\n亚洲：1"
        file=f"file:///{os.getcwd()+'/data/remake/'+'日本'+'.png'}"
        at = MessageSegment.at(user_id)
        await remake.finish(Message(at+messagestr1+MessageSegment(type='image', data={'file': file})+messagestr2+messagestr3))
    at = MessageSegment.at(user_id)
    times = 1
    rmk = Remake(times).remakelist
    with open(os.getcwd()+'/data/remake/count.json','r',encoding='utf-8') as f:
        count=json.load(f)
    if user_id not in count:
        count.update({user_id:{}})
    for coun in rmk:
        if coun['cn'] == '中国':
            if '种花家' not in count[user_id]:
                count[user_id].update({'种花家':1})
            else:
                count[user_id]['种花家']+=1
            if '亚洲' not in count[user_id]:
                count[user_id].update({'亚洲':1})
            else:
                count[user_id]['亚洲']+=1
        else:
            if CONTINENT_DICT[coun['continent']] not in count[user_id]:
                count[user_id].update({CONTINENT_DICT[coun['continent']]:1})
            else:
                count[user_id][CONTINENT_DICT[coun['continent']]]+=1
    with open(os.getcwd()+'/data/remake/count.json','w',encoding='utf-8') as f:
        json.dump(count,f,indent=4,ensure_ascii=False,sort_keys=True)
    messagestr1=f"恭喜你重开到位于 {CONTINENT_DICT[rmk[0]['continent']]} 的"
    messagestr2=f"{rmk[0]['cn']}！出生率：{str(rmk[0]['birth_rate'])}\n"
    messagestr3=f"重开统计：\n{' '.join([key+'：'+str(count[user_id][key]) for key in count[user_id]])}"
    file=f"file:///{os.getcwd()+'/data/remake/'+rmk[0]['cn']+'.png'}"
    await remake.finish(Message(at+messagestr1+MessageSegment(type='image', data={'file': file})+messagestr2+messagestr3))
    
reborn_clear = on_command('清空重开统计', aliases={'清空重开统计'}, block=True)
@reborn_clear.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_id=event.get_user_id()
    with open(os.getcwd()+'/data/remake/count.json','r',encoding='utf-8') as f:
        count=json.load(f)
    count[user_id]={}
    with open(os.getcwd()+'/data/remake/count.json','w',encoding='utf-8') as f:
        json.dump(count,f,indent=4,ensure_ascii=False,sort_keys=True)
    await reborn_clear.finish('清空成功！')
    
reborn_all = on_command('清空全部重开统计', aliases={'清空全部重开统计'}, block=True,permission=SUPERUSER)
@reborn_all.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    count={}
    with open(os.getcwd()+'/data/remake/count.json','w',encoding='utf-8') as f:
        json.dump(count,f,indent=4,ensure_ascii=False,sort_keys=True)
    await reborn_all.finish('清空成功！')
    