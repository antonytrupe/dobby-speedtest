import configparser
import subprocess
import json
import sqlite3 as lite
from datetime import datetime


def initDB(databaseName):
    con = lite.connect(databaseName)
    c = con.cursor()
            
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND (name='speedtest') ''')
    #print('foo')
    #print(c.fetchone()[0])
    #if the count is 1, then table exists
    if c.fetchone()[0] == 1 :
        print('dobby-speedtest:tables exist')
    else :
        print('dobby-speedtest: missing 1 or more tables, creating...')
        
        c.execute('''CREATE TABLE if not exists `speedtest` (
            `date`  TEXT,
            `conntype`  TEXT,
            `conndetails`   TEXT,
            `lat`   NUMERIC,
            `lon`   NUMERIC,
            `download`  NUMERIC,
            `downloadbytes` NUMERIC,
            `upload`    NUMERIC,
            `uploadbytes`   NUMERIC,
            `latency`   NUMERIC,
            `servername`    TEXT,
            `internalip`    TEXT,
            `externalip`    TEXT,
            `is speedtest vpn`  TEXT DEFAULT 'No');''')
            
def speedTest(databaseName):
    con = lite.connect(databaseName)
    
    print('dobby-speedtest:starting speedtest...')
    response = subprocess.Popen('/usr/local/bin/speedtest-cli --json --server 29204', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    print('dobby-speedtest:'+response)
    data=json.loads(response.rstrip().replace("'","\""))
    with con:

        cur = con.cursor()
        #print('about to insert')
        cur.execute(''' insert into speedtest (date,conntype,conndetails,lat,lon,download,downloadbytes,upload,uploadbytes,latency, servername,internalip,externalip,"is speedtest vpn") 
                    values (:date,:conntype,:conndetails,:lat,:lon,:download,:downloadbytes,:upload,:uploadbytes,:latency, :servername,:internalip,:externalip,:vpn) ''',
                    {"date":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     "conntype":'Wi-Fi',
                     "conndetails":'SSID: Trupe_House',
                     "lat":data["client"]["lat"],
                     "lon":data["client"]["lon"],
                     "download":data['download'],
                     "downloadbytes":None,
                     "upload":data['upload'],
                     "uploadbytes":None,
                     "latency":data['server']['latency'],
                     "servername":data['server']['name'],
                     "internalip":data['client']['ip'],
                     "externalip":None,
                     "vpn":'No'})

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    databaseName=config.get('default','databasePathAndName')
    initDB(databaseName)
    speedTest(databaseName)