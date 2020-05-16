import configparser
import subprocess
import json
import sqlite3 as lite
from datetime import datetime
from os.path import abspath


def initDB(databaseName):
    con = lite.connect(databaseName)
    c = con.cursor()
            
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND (name='speedtest') ''')
    #print('foo')
    #print(c.fetchone()[0])
    #if the count is 1, then table exists
    if c.fetchone()[0] == 1 :
        print('dobby-pi-base:tables exist')
        None
    
    else :
        print('dobby-pi-base: missing 1 or more tables, creating...')
        
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
    print('dobby-pi-base:starting speedtest...')
    response = subprocess.Popen('/usr/local/bin/speedtest-cli --json --server 29204', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    print(response)
    data=json.loads(response.rstrip().replace("'","\""))
    print('{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
        #Date
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #ConnType
        'Wi-Fi',
        #ConnDetails
        'SSID: Trupe_House',
        #Lat
        data["client"]["lat"],
        #Lon
        data["client"]["lon"],
        #Download
        data['download'],
        #DownloadBytes
        '',
        #Upload
        data['upload'],
        #UploadBytes
        '',
        #Latency
        data['server']['latency'],
        #ServerName
        data['server']['name'],
        #InternalIp
        '',
        #ExternalIp
        data['client']['ip'],
        #Is SpeedTest VPN
        'No'))

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    databaseName=config.get('default','databasePathAndName')
    initDB(databaseName)
    speedTest(databaseName)