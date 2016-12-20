# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 17:46:12 2016

@author: enzoc
"""

import sys
import time
import telepot
import random
from pprint import pprint
#import numpy as nps

cmd={}
def parse_str_dice(str_dice):# "6d5" o "d6"
    pre_num=str_dice.split("d")
    max_dados= 1 if pre_num[0]=="" else int(pre_num[0])
    dice_type=pre_num[1]
    return max_dados,dice_type

def rand_dados(Ncaras,cuantity=1):
    rand=0
    msg=""
    for i in range(0,int(cuantity)):
        temp_rand=random.randrange(1,int(Ncaras)+1)
        msg=msg+str(i+1) +"  ("+ str(temp_rand)+")\n"      
        rand=rand+temp_rand
    msg=msg+"Total " +str(rand)
    return  msg
    
def handle(msg):
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
                n_dice, type_dice = parse_str_dice(args[2])
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
            
        elif msg['text'][0]=='/' and "d" in msg['text']: # clean "d" change to /dice 2d10 
            pre_num=msg['text'].split("d")
            max_dados= 1 if pre_num[0][1:]=="" else int(pre_num[0][1:])
            dice_type=pre_num[1].split("@")[0]
            msg=rand_dados(int(dice_type),max_dados)
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

# Keep the program running.
while 1:
    time.sleep(10)