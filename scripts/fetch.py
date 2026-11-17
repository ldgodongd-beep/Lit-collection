import json,urllib.request,urllib.parse,sys,time
J={"Regional Studies":"0034-3404","Economic Geography":"0013-0095","Journal of Economic Geography":"1468-2702","Urban Geography":"0272-3638","Urban Studies":"0042-0980","Applied Geography":"0143-6228","Environment and Planning A":"0308-518X","Environment and Planning B":"2399-8083","Environment and Planning C":"2399-6544","Annals of the AAG":"2469-4452","Progress in Human Geography":"0309-1325","Dialogues in Human Geography":"2043-8206","Antipode":"0066-4812","Eurasian Geography and Economics":"1538-7216","IJURR":"0309-1317","Geoforum":"0016-7185"}
out=sys.argv[1]
for name,issn in J.items():
    items=[];cursor="*"
    while True:
        q=urllib.parse.urlencode({"filter":"from-created-date:2026-08-01,type:journal-article","rows":500,"cursor":cursor,"select":"DOI,title,abstract,volume,issue,published-print,published-online,created,author,container-title,type"})
        url=f"https://api.crossref.org/journals/{issn}/works?{q}"
        for t in range(4):
            try:
                d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"lit-collection/1.0"}),timeout=60));break
            except Exception as e:
                print(name,e);time.sleep(5)
        m=d["message"];items+=m["items"]
        if len(m["items"])<500:break
        cursor=m["next-cursor"]
    json.dump(items,open(f"{out}/{name}.json","w"))
    print(name,len(items))
