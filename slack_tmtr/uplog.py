#incapsulation of log writer
def append(log,file):
    log_file = open(file,'a',encoding='utf-8')
    log_file.seek(19)
    log_file.write("\n" + log)
    log_file.close()

def getLogAsFile(slack_client,channel):
    with open('C:\\Users\\kkoshaev\\slack_tmtr\\log.csv', 'rb') as file_content:
        api_call_msg = slack_client.api_call(
        "files.upload",
        channels=channel,
        file=file_content,
        title='bot log'
        )
    
    with open('C:\\Users\\kkoshaev\\slack_tmtr\\cmd_stat.csv', 'rb') as file_content:
        api_call_msg = slack_client.api_call(
        "files.upload",
        channels=channel,
        file=file_content,
        title='bot log'
        )
       
    with open('C:\\Users\\kkoshaev\\slack_tmtr\\region_list.csv', 'rb') as file_content:
        api_call_msg = slack_client.api_call(
        "files.upload",
        channels=channel,
        file=file_content,
        title='bot log'
        )
        channel_info = slack_client.api_call("channel.info",channel=channel)
        #print(channel_info)