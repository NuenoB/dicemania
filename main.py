# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 17:27:58 2016

@author: enzoc
"""

import telepot
bot = telepot.Bot('290842773:AAE2YbSjls7xzgk3sRSoJ9v0DkS8aO-IF-k')
test=bot.getMe()
#%%
response2 = bot.getUpdates()
#%%
id=283392250
bot.sendMessage(id, 'Hey! hey listen')
#%%
content_type, chat_type, chat_id = telepot.glance(response2[10]["message"])
