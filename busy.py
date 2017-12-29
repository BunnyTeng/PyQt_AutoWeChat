#coding:utf8
import itchat
from itchat.content import *

###################################busy#######################################

@itchat.msg_register(TEXT, isGroupChat = True)#group into this
def text_reply(msg):
    if msg['isAt']:
        return 'Sorry,I\'m busy at the moment'

@itchat.msg_register([TEXT, MAP, CARD, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])#single chat into this
def text_reply(msg):
    return 'Sorry,I\'m busy at the moment'

############################################################################

itchat.auto_login()
itchat.run()
