# dobby-speedtest

download is kbps(kilobit/second), divide by 1000 to get mbps<magabit/second)  
downloadbytes is size of download used  
latency(ping) in ms  
don't use pm2 watch or it will keep running as soon as it finishes  

run every 10 minutes  
pm2 start index.py --name dobby-speedtest --cron "*/10 * * * *"
