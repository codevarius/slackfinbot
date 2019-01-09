import os
import time
import re
from slackclient import SlackClient
import cdat
import uplog
import sys
import traceback
import cnf
import dbm
import cmdbook

#slack client instance
slack_client = SlackClient(cnf.BOT_TOKEN)
# bot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# internal constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)" #bot name regexp
MMYYYY = "(?<![/\d])\d{1,2}/\d{2,4}(?![/\d])" #mm.yyyy regexp
REGIONREGEXP = "(?:\w{3,}|[\$\@()+.])+" #region attr regexp

#middle level code
def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])             
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    print('handling incoming command')
    # Finds and executes the given command, filling in response
    response = None
    # Implement more commands here
    if command.startswith(cmdbook.COMMAND) and command.__len__() <= cmdbook.COMMAND.__len__():
        uplog.append('treemap,' + cdat.getFormatedDate(),'cmd_stat.csv')
        construct_report(cnf.OUTPUT_IMG_PATH,cnf.OUTPUT_FILE_NAME,cnf.OPEN_CHROME,cnf.TMAP_TITLE,'','',flag='treemap')
    else:
        if command.startswith(cmdbook.COMMAND0):
            uplog.append('help,' + cdat.getFormatedDate(),'cmd_stat.csv')
            dbm.refresh_region_list()
            slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=cmdbook.HELP_DESCRIPTION
            )
        else:
            if command.startswith(cmdbook.COMMAND1) and not re.search(MMYYYY,command) and command.__len__() <= cmdbook.COMMAND1.__len__():
                uplog.append('сравнить,' + cdat.getFormatedDate(),'cmd_stat.csv')
                curDate = cdat.getFormatedDate()
                print(curDate)
                month = curDate[3:5]
                year = curDate[6:]
                construct_report(cnf.OUTPUT_IMG_PATH,cnf.OUTPUT_FILE_NAME1,cnf.OPEN_CHROME1,cnf.PTEC_TITLE,month,year,flag='ptec')
            else:
                if command.startswith(cmdbook.COMMAND1) and re.search(MMYYYY,command):
                    uplog.append('сравнить+атрибут,' + cdat.getFormatedDate(),'cmd_stat.csv')
                    rep_date = re.search(MMYYYY,command).group()
                    month = rep_date[0:2]
                    year = rep_date[3:]
                    construct_report(cnf.OUTPUT_IMG_PATH,cnf.OUTPUT_FILE_NAME1,cnf.OPEN_CHROME1,cnf.PTEC_TITLE,month,year,flag='ptec')
                else:
                    if command.startswith(cmdbook.COMMAND2):
                        uplog.getLogAsFile(slack_client,channel)
                        uplog.append('logf,' + cdat.getFormatedDate(),'cmd_stat.csv')
                    else:
                        if command.startswith(cmdbook.COMMAND) and re.search(REGIONREGEXP,command):
                            uplog.append('treemap_by_region,' + cdat.getFormatedDate(),'cmd_stat.csv')
                            region_attr = ' '.join(command.split(' ')[1:]) #re.search(REGIONREGEXP,command).group()
                            dbm.refresh_region_list()

                            if region_attr in dbm.__regionList__:
                                construct_report(cnf.OUTPUT_IMG_PATH,cnf.OUTPUT_FILE_NAME2,cnf.OPEN_CHROME2,cnf.TMAP_TITLE,region_attr,'',flag='region_treemap')
                            else:
                                #send_message('suggestion list return')
                                if dbm.getSuggestionList(region_attr,dbm.__regionList__).__len__() > 0:
                                    send_message(cmdbook.SUGGESTION_MES)
                                    send_message('\n'.join(dbm.getSuggestionList(region_attr,dbm.__regionList__)))
                                else:
                                    send_message(cmdbook.SUGGESTION_MES + '\n<совпадений не найдено>')
                            
                        else:
                            send_message(cmdbook.DEFAULT_RESPONSE)
                            uplog.append('wrong_cmd,' + cdat.getFormatedDate(),'cmd_stat.csv')
     
    print('handling command complete')
    print('waiting for new commands')
#bottom level code
#treemap report construction
def construct_report(out_img_path,out_img_fname,chrome_query,title, *args, **kwargs):
    # Sends the response back to the channel
    send_message(cnf.WAITING_TEXT)
    if kwargs.get('flag') == 'treemap':
        dbm.mineData()
    else:
        if kwargs.get('flag') == 'ptec':
            dbm.ptec_mineData(args[0],args[1])
        else:
            if kwargs.get('flag') == 'region_treemap':
                dbm.regiontmap_mineData(args[0])

    response = True
   
    print(out_img_path + cdat.getFormatedDate() + cnf.translate(args[0]).replace(' ','') + args[1] + out_img_fname)
        
    if not os.path.exists(out_img_path + cdat.getFormatedDate() + cnf.translate(args[0]).replace(' ','') + args[1] + out_img_fname):
        os.system(chrome_query)

    while not os.path.exists(out_img_path + cdat.getFormatedDate() + cnf.translate(args[0]).replace(' ','') + args[1] + out_img_fname):
        time.sleep(1)
          
    try:
        #pass
        os.system(cnf.KILL_CHROME)
    except:
        print('png output already exists on current date')
        print('no need to kill chrome because it was not opened to render image')
    print('continue running')

    send_message(cnf.WAITING_TEXT2)

    if response:
        print('sending file to user')
        with open(out_img_path + cdat.getFormatedDate() 
        + cnf.translate(args[0]).replace(' ','') + args[1] + out_img_fname, 'rb') as file_content:
            print(file_content)
            api_call_msg = slack_client.api_call(
            "files.upload",
            channels=channel,
            file=file_content,
            title= title
            )
            print('file delivered')

def send_message(mes):
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=mes
            )

#top level code
if __name__ == "__main__":
    try:
        if slack_client.rtm_connect(with_team_state=False):
            dbm.refresh_region_list()
            print('bot started listening commands')
            uplog.append(cdat.getFormatedDate() + "," 
            + str(cdat.dtime.time(cdat.dtime.now())) + ",bot waked up",'log.csv')       
            # Read bot's user ID by calling Web API method `auth.test`
            starterbot_id = slack_client.api_call("auth.test")["user_id"]
            
            while True:
                command, channel = parse_bot_commands(slack_client.rtm_read())
                if command:
                    handle_command(command, channel)
                    uplog.append(cdat.getFormatedDate() + "," 
                    + str(cdat.dtime.time(cdat.dtime.now())) + ",bot returned response",'log.csv')
                time.sleep(RTM_READ_DELAY)

        else:
            print("Connection failed. Exception traceback printed above.")
            uplog.append(cdat.getFormatedDate() + "," 
            + str(cdat.dtime.time(cdat.dtime.now())) + ",bot failed to connect",'log.csv')

    except Exception as err:
        send_message('Ошибка выполнения запроса.\nВведите команду *help*\nПерезапуск...')
        traceback.print_exc(file=sys.stdout)
        uplog.append(cdat.getFormatedDate() + "," 
        + str(cdat.dtime.time(cdat.dtime.now())) 
        + ",bot was interrupted by error:" 
        + str(err) + " in main",'log.csv')
        uplog.append(cdat.getFormatedDate() + "," 
        + str(cdat.dtime.time(cdat.dtime.now())) + ",bot restart attempt",'log.csv')