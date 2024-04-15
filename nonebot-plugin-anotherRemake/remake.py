# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 13:48:22 2022

@author: Administrator
"""

from nonebot.plugin import on_keyword,on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent, GroupMessageEvent
from nonebot.rule import to_me
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from nonebot.utils import DataclassEncoder

import json
import os
import random

remake = on_command('remake',aliases={'remake','重开'},priority=12)

@remake.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    user_id=event.get_user_id()
    at = MessageSegment.at(user_id)
    with open(os.getcwd()+'/data/remake/remake.json','r',encoding='utf-8') as f:
        coundict=json.load(f)
    a=random.uniform(0,1)
    for j in coundict:
        if a>coundict[j]['leftprob'] and a<coundict[j]['rightprob']:
            coun=coundict[j]
            break
    with open(os.getcwd()+'/data/remake/count.json','r',encoding='utf-8') as f:
        count=json.load(f)
    if user_id not in count:
        count.update({user_id:{}})
    if j == '中华人民共和国':
        if '种花家' not in count[user_id]:
            count[user_id].update({'种花家':1})
        else:
            count[user_id]['种花家']+=1
        if '亚洲' not in count[user_id]:
            count[user_id].update({'亚洲':1})
        else:
            count[user_id]['亚洲']+=1
    else:
        if coun['con'] not in count[user_id]:
            count[user_id].update({coun['con']:1})
        else:
            count[user_id][coun['con']]+=1
    with open(os.getcwd()+'/data/remake/count.json','w',encoding='utf-8') as f:
        json.dump(count,f,indent=4,ensure_ascii=False,sort_keys=True)
    messagestr1=f"恭喜你重开到位于 {coun['con']} 的"
    messagestr2=f"{j}！人口数：{str(coun['popu'])}\n"
    messagestr3=f'''重开统计：\n{' '.join([key+'：'+str(count[user_id][key]) for key in count[user_id]])}'''
    file=f"file:///{os.getcwd()+'/data/remake/'+j+'.png'}"
    await remake.finish(Message(at+messagestr1+MessageSegment(type='image', data={'file': file})+messagestr2+messagestr3))