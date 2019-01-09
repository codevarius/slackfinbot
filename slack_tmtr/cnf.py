'''
Configrations of bot
'''

BOT_TOKEN = 'xoxb-388256914452-389360380593-gfhE61w9zJzjKXUrEjHsSBAA' #use your token
OUTPUT_IMG_PATH = 'C:\\Users\\kkoshaev\\Downloads\\' #use chrome download path because of saveSvgAsPng.js specifics
OUTPUT_FILE_NAME = 'treemap.png'
OUTPUT_FILE_NAME1 = 'pricing_tec.png'
OUTPUT_FILE_NAME2 = 'region_treemap.png'
TMAP_TITLE = "treemap готов!"
PTEC_TITLE = "pricing_tec готов!"
WAITING_TEXT = "секунду..."
WAITING_TEXT2 = "почти готово!"
KILL_CHROME = 'taskkill /f /im chrome.exe'
OPEN_CHROME = 'start \"\" \"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" --new-window \"http://localhost:8000/js_parts/treeMap.html\"'
OPEN_CHROME1 = 'start \"\" \"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" --new-window \"http://localhost:8000/js_parts/pricing_tech.html\"'
OPEN_CHROME2 = 'start \"\" \"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" --new-window \"http://localhost:8000/js_parts/RegionTreeMap.html\"'
APP_ID = 1
DATA_MINE_DEPH = -90 # change to -30 when there will be relevant data DEPRICATED
DATA_MINE_DEPH2 = DATA_MINE_DEPH - 30 #DEPRICATED
SQL_OUTPUT_PATH = 'C:\\Users\\kkoshaev\\slack_tmtr\\js_parts\\dt.json' #change path up to js_parts folder
SQL_OUTPUT_PATH2 = 'C:\\Users\\kkoshaev\\slack_tmtr\\js_parts\\dt_region_tmap.json' #change path up to js_parts folder
PTEC_OUTPUT_PATH = 'C:\\Users\\kkoshaev\\slack_tmtr\\js_parts\\ptec_dt.json' #change path up to js_parts folder
BASE_NAME = 'stock_management'

symbolsRus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA- "
symbolsEng = "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA1234567890abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA- "
symRu = []
symEn = []

for s in symbolsRus:
    symRu.append(s)

for s in symbolsEng:
    symEn.append(s)

dictionary = dict(zip(symRu, symEn))

def translate(word):
    result = ''
    for w in word:
        result += dictionary.get(w)
    return result

print('python part config file read complete')