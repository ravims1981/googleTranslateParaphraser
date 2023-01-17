from google.cloud import translate
from os import environ, path
from fastapi import FastAPI, Request
from time import perf_counter as pC
from fastapi.responses import JSONResponse as jR
from sys import exit as fOff
from uvicorn import run as r
from configparser import ConfigParser as cP
from bcrypt import checkpw as cpw, hashpw as hpw, gensalt as gs
cfg = cP()
if path.exists('config.cfg'):
    cfg.read('config.cfg')
    passthrough  = cfg.get('api','secret')
else:
    fOff('Make the fucking config file first')
project_id = environ.get("PROJECT_ID", "")
assert project_id
parent = f"projects/{project_id}"
client = translate.TranslationServiceClient()
target_list = ["ko","fr","ja","id","it","pt","ru","af","sq","am","ar","ca","nl","de","es","tr", "ta"]
hops = ["ko","ru", "ta"]
app = FastAPI()
@app.post('/api')
async def endPoint(txt:dict, hdr:Request):
    def reQ(txt, tgt):
        for translation in client.translate_text(contents=[txt], target_language_code=tgt, parent=parent).translations:
            return translation.translated_text
    if cpw(hdr.headers.get('X-RapidAPI-Proxy-Secret').encode(), passthrough.encode()):
        if 'text' in txt:
            text = txt['text']
            txtLen = len(text)
            if txtLen > 9999 or len(text.split()) > 2000:
                return jR(headers={'X-RapidAPI-Billing':'Characters=0'}, content={'error':'Exceeded Character limit of 10000 or Word limit of 2000 per request'})        
        else:
            return jR(headers={'X-RapidAPI-Billing':'Characters=0'}, content={'error':'Cannot proceed without text'})
        sTart = pC()
        if not 'output_language' in txt:
            tgt = 'en'
        else:
            if txt['output_language'] in target_list:
                tgt = txt['output_language']
            else:
                return jR(headers={'X-RapidAPI-Billing':'Characters=0'}, content={'error':f'Current supported languages are {target_list}'})       
        for hop in hops:
            text = reQ(text, hop)
        text = reQ(text, tgt)
        return jR(headers={'X-RapidAPI-Billing':f"Characters={txtLen}"}, content={'text':text, 'time':round(pC()-sTart), 'billed_characters':txtLen})
    else:
        return 'Unauthorized Access'
if __name__ == '__main__':
    wachawannado = input('''Howdy!
    1. Make a new API Key Hash
    2. Start the uvicorn server
        (1/2) : ''')
    if wachawannado =='1':
        with open('config.cfg','w') as cfgWrite:
            cfgWrite.write(f'''[api]
secret = {hpw(input('RapidAPI secret : ').encode(), gs()).decode()}''')
        fOff("Keyfile is created")
    elif wachawannado =='2':
        fOff(r(app, host='localhost', port=8000))
    else:
        fOff('You are what you are as a result of your bad choices')
