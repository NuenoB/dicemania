# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 17:46:12 2016

@author: enzoc
"""

import sys
import time
import telepot
import random
import re
from pprint import pprint
#import numpy as nps

cmd={}
def parse_str_dice(str_dice):# "6d5" o "d6" o "1d2k1"
    rs_str="(?P<c>\d*)d(?P<t>\d*)k?(?P<k>\d*)(?P<s>[\+|-])?(?P<o>\d*)"
    m=re.match(rs_str,str_dice)
    dice_type=m.group("t")
    max_dados= 1 if m.group("c")=="" else int(m.group("c"))
    Nkeep= max_dados if m.group("k")=="" else int(m.group("k"))
    print(m.group("o"))
    offsett= 0 if m.group("o")=="" else int(m.group("s")+m.group("o"))

    return int(max_dados),int(dice_type),int(Nkeep),int(offsett)

def rand_dados(Ncaras,cuantity=1,Nkeep=0,offset=0):
    rand=0
    msg=""
    tiradas=[]
    for i in range(0,(cuantity)):
        temp_rand=random.randrange(1,(Ncaras)+1)
        tiradas.append(temp_rand)
#        msg=msg+str(i+1) +"  ("+ str(temp_rand)+")\n"      
#        rand=rand+temp_rand
    order_tiradas=sorted(tiradas)
    if Nkeep>0:
        order_tiradas.reverse()
    for i in range(0,int(cuantity)):
        t=order_tiradas[i]
#        msg=msg+str(i+1)+"  ("+ str(t)+")\n"
        if i<(Nkeep):
            rand=rand+t
            msg=msg+str(i+1)+"  ("+ str(t)+") keept\n"
        else:
            msg=msg+str(i+1)+"  ("+ str(t)+") not keept\n"
    if not offset==0:
        msg = msg + "plus " +str(offset) +"\n"
    rand=rand+offset
    msg=msg+"Total " +str(rand)
    return  msg
    
def handle(msg):
    global run
    content_type, chat_type, chat_id = telepot.glance(msg)
    pprint(msg)
    print(content_type, chat_type, chat_id)
    
    if content_type == 'text':
        print(msg['text'])
        if "/save_dice" in msg['text']:
            print("true")
            temp= msg['text'].strip()
            args=temp.split(" ")
            if len(args)>=3:
                name_cmd = args[1]
                n_dice, type_dice, nkeep = parse_str_dice(args[2])
                key=name_cmd+str(msg["from"]["id"])
                cmd[key] ={"name_cmd":name_cmd, "n_dice":n_dice, "type_dice":type_dice, "desc": args[3] if len(args)>3 else ""}
            #            print("asd  " + cmd[chat_id])
                #TODO: ack
        elif "/use" in msg['text']:
            temp= msg['text'].strip()
            args=temp.split(" ")
            if len(args)>1:
                name_cmd = args[1]
                key=name_cmd+str(msg["from"]["id"])
                cmd_dic=cmd.get(key,"no tenias un cmd guardado")
                msg=rand_dados(cmd_dic["type_dice"],cmd_dic["n_dice"])
                bot.sendMessage(chat_id, msg)
    #            print
#            np.save("cmd",cmd)
        elif "/autokill" in msg['text']:
            run=False
            bot.sendMessage(chat_id, "apagando en proximo ciclo")
            
            
        elif msg['text'][0]=='/' and "d" in msg['text']: # clean "d" change to /dice 2d10 
            temp= msg['text'].strip()
            args=temp.split(" ")
            
            n_dice, type_dice , nkeep , offsett = parse_str_dice(args[0][1:])
            
            msg=rand_dados(type_dice,n_dice,nkeep,offsett)
            
            if(len(msg)>=4096):
                bot.sendMessage(chat_id,"sorry")    
                
#                for i in range(0,len(msg)%4096):
#                    bot.sendMessage(chat_id, msg[i*4096:(i+1)*4096])
            else:
                bot.sendMessage(chat_id, msg)
            
#        else:
#                
#            bot.sendMessage(chat_id, msg['text'])            
    
    elif content_type=='document':
        bot.sendMessage(chat_id, "you send a archive")
        

TOKEN ='290842773:AAE2YbSjls7xzgk3sRSoJ9v0DkS8aO-IF-k'  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')
run=True
# Keep the program running.
while run:
    time.sleep(5)