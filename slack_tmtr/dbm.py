'''

Connect to db -> get raw data -> calculate data -> update .json

'''

import cnf
import pyodbc
import datetime 
import codecs
import time
import csv
import uplog
import difflib

__regionList__ = []

#mine data for region_treemap
def regiontmap_mineData(regionName):
    #implement more code here to extend this procedure
    mineData(regionName)
    
def getSuggestionList(word, list):
    list = difflib.get_close_matches(word,list,cutoff=0.3)
    list = set(list)
    return list

def refresh_region_list():
    print('refreshing region list')
     #query string
    QUERY = 'SELECT [region] FROM [dbo].[clients] GROUP BY [region]'

    cnxn = pyodbc.connect("DRIVER={SQL Server Native Client 11.0};"
                          "Server=localhost;"
                          "Database=" + cnf.BASE_NAME + ";"
                          "Trusted_Connection=yes;")
    #register_launch(cnxn) #comment that if no need
    cursor = cnxn.cursor()
    # mapping of target month
    result = cursor.execute(QUERY).fetchall()
    log_file = open('region_list.csv','w',encoding='utf-8')
    log_file.write('region\n')
    for region in result:
        log_file.write(str(region[0]) + '\n')
        __regionList__.append(str(region[0]))
    log_file.close()


#mine data for pricing tec diagram
def ptec_mineData(month,year):
    print('execute sql script for pricing tecs diagram')
    
    #query string
    QUERY1 = "SET NOCOUNT ON EXEC [dbo].[price_algorythm_comparison] @month_str = '" + month + '.' + year + "'"
    
    cnxn = pyodbc.connect("DRIVER={SQL Server Native Client 11.0};"
                          "Server=localhost;"
                          "Database=" + cnf.BASE_NAME + ";"
                          "Trusted_Connection=yes;")
    #register_launch(cnxn) #comment that if no need
    cursor = cnxn.cursor()
    try:
        result = cursor.execute(QUERY1).fetchall()[0]
    except:
        print("result was null -> no data found...")

    jsonFile = codecs.open(cnf.PTEC_OUTPUT_PATH,'w','utf-8')
    jsonFile.write('[\n\t')

    if str(round(result[0])).__len__() >= 7:
        jsonFile.write('\t {"data": "' + str(round(result[0]/1000000)) + 'mln€"}\n\t\t')

    if result[0] > 1 and str(round(result[0])).__len__() < 7:
        jsonFile.write('\t {"data": "' + str(round(result[0])) + '€"}\n\t\t')
    else:
        if result[0] < 1:
            jsonFile.write('\t {"data": "' + str(round(result[0] * 100,1)) + '%"}\n\t\t')

    for val in result:
        if val != result[0]:
            parameter = val
            if str(round(parameter)).__len__() >= 7:
                jsonFile.write('\t ,{"data": "' + str(round(parameter)) + 'mln€"}\n\t\t')

            if parameter > 1 and str(round(parameter)).__len__() < 7:
                jsonFile.write('\t ,{"data": "' + str(round(parameter)) + '€"}\n\t\t')
            else:
                if parameter < 1:
                    jsonFile.write('\t ,{"data": "' + str(round(parameter * 100,1)) + '%"}\n\t\t')

    jsonFile.write(',{"month": "' + str(month) + '", "year": "' + str(year) + '"}\n\t\t')
    jsonFile.write('\n')
    jsonFile.write(']\n\t')

    jsonFile.close()
    cursor.close()
    cnxn.close()
    print('ptec sql connection mission complete')

#mine data for treemap 
def mineData(*args):
    if not args:
        print('execute sql query for treemap')
    else:
        print('execute sql query for region treemap')

    refresh_region_list()
    #set date interval for db query
    #today date
    toDate = datetime.datetime.now()
    montht = ''.join(['0',str(toDate.month)]) if str(toDate.month).__len__() == 1 else str(toDate.month) 
    t = ''.join([str(toDate.day),'-',montht,'-',str(toDate.year)])
    print('today:',t)

    #starting date 
    fromDate = toDate + datetime.timedelta(cnf.DATA_MINE_DEPH)
    monthf = ''.join(['0',str(fromDate.month)]) if str(fromDate.month).__len__() == 1 else str(fromDate.month) 
    f = ''.join([str(fromDate.day),'-',monthf,'-',str(fromDate.year)])
    print('30 days ago:',f)

    #30 days befor starting date
    fromDate2 = toDate + datetime.timedelta(cnf.DATA_MINE_DEPH2)
    monthf2 = ''.join(['0',str(fromDate2.month)]) if str(fromDate2.month).__len__() == 1 else str(fromDate2.month) 
    f2 = ''.join([str(fromDate2.day),'-',monthf2,'-',str(fromDate2.year)])
    print('60 days ago:',f2)

    #query string
    if not args:
        QUERY1 = open('treemap_query.sql','r').read()
    else:
        QUERY1 = "declare @region varchar(255) = '" + args[0] + "' " + open('client-treemap-query.sql','r').read()
    #print(QUERY1)

    cnxn = pyodbc.connect("DRIVER={SQL Server Native Client 11.0};"
                          "Server=localhost;"
                          "Database=" + cnf.BASE_NAME + ";"
                          "Trusted_Connection=yes;")
    #register_launch(cnxn) #comment that if no need
    cursor = cnxn.cursor()
    # mapping of target month
    region_mapping = cursor.execute(QUERY1).fetchall()

    #convert region_mapping to json data
    #target month mapping to dict
    
    rm = []
    for row in region_mapping:
        r = {}
        r['name'] = row[0]
        r['value'] = round(row[1]) if row[1] != None else 0
        r['pvalue'] = round(row[2]) if row[2] != None else 0
        r['change'] = round(row[3]) if row[3] != None else 0
        r['std_value'] = round(row[4]) if row[4] != None else 0
        r['std_pvalue'] = round(row[5]) if row[5] != None else 0
        #print('Extracted data:')
        #print(r)
        rm.append(r)

    total_stock = 0
    for r in rm:
        total_stock += r['value']

    #write data to json file dataset
    if not args:
        jsonFile = codecs.open(cnf.SQL_OUTPUT_PATH,'w','utf-8')
    else:
        jsonFile = codecs.open(cnf.SQL_OUTPUT_PATH2,'w','utf-8')

    jsonFile.write('{\n\t')
    if not args:
        jsonFile.write('\"name\":\"Продажи\",\n\t')
    else:
        jsonFile.write('\"name\":\"Продажи\",\n\t')
        jsonFile.write('\"region\":\"'+ cnf.translate(args[0]) +'\",\n\t')

    jsonFile.write("\"total\":"+ str(total_stock) +",\n\t")
    jsonFile.write("\"dfrom\":\""+ f2 +"\",\n\t")
    jsonFile.write("\"dto\":\""+ t +"\",\n\t")
    jsonFile.write('\"children\":[\n\t\t')
    jsonFile.write("{\"name\":\""+str(rm[0]['name'])+"\",\"value\":"+str(rm[0]['value'])+",\"pvalue\":"+str(rm[0]['pvalue'])+ ",\"change\":"+str(rm[0]['change'])+ ",\"std_value\":"+str(rm[0]['std_value'])+ ",\"std_pvalue\":"+str(rm[0]['std_pvalue'])+"}")
    for row in rm:
        if row['name'] != rm[0]['name']:
            name = str(row['name']).replace('"',"\"")
            jsonFile.write("\n\t\t,{\"name\":\""+name+"\",\"value\":"+str(row['value'])+",\"pvalue\":"+str(row['pvalue'])+ ",\"change\":"+str(row['change'])+ ",\"std_value\":"+str(row['std_value'])+ ",\"std_pvalue\":"+str(row['std_pvalue'])+"}")
    jsonFile.write('\n\t\t]\n}')
       
    jsonFile.close()
    cursor.close()
    cnxn.close()
    print('sql connection mission complete')

#register db connection if needed
def register_launch(cnxn):
    application_id = cnf.APP_ID
    cursor = cnxn.cursor()
    res = cursor.execute(
        "insert into admin.application_launch(application_id) output inserted.launch_id values (?)", application_id)
    row = res.fetchone()
    cnxn.commit()

#mineData()