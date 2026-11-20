import json, urllib.request, urllib.parse, re, html, sys, time
J = [("Regional Studies","0034-3404"),("Economic Geography","0013-0095"),("Journal of Economic Geography","1468-2702"),
("Urban Geography","0272-3638"),("Urban Studies","0042-0980"),("Applied Geography","0143-6228"),
("Environment and Planning A: Economy and Space","0308-518X"),("Environment and Planning B: Urban Analytics and City Science","2399-8083"),
("Environment and Planning C: Politics and Space","2399-6544"),("Annals of the American Association of Geographers","2469-4452"),
("Progress in Human Geography","0309-1325"),("Dialogues in Human Geography","2043-8206"),("Antipode","0066-4812"),
("Eurasian Geography and Economics","1538-7216"),("International Journal of Urban and Regional Research","0309-1317"),("Geoforum","0016-7185")]
UA={"User-Agent":"lit-collection-script/1.0"}
def get(u):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))
        except Exception as e:
            time.sleep(3)
    return None
def clean(a):
    if not a: return ""
    a=re.sub(r"<[^>]+>"," ",a); a=html.unescape(a); a=re.sub(r"\s+"," ",a).strip()
    a=re.sub(r"^(Abstract|ABSTRACT)\s*","",a); return a
SKIP=re.compile(r"^(editorial|erratum|correction|corrigendum|book review|reviewer|acknowledg|retraction|expression of concern|editorial board|in memoriam|obituary|index|issue information|front matter|call for)",re.I)
def oa_abs(doi):
    d=get("https://api.openalex.org/works/doi:"+doi+"?select=abstract_inverted_index")
    if not d or not d.get("abstract_inverted_index"): return ""
    pos=[]
    for w,ps in d["abstract_inverted_index"].items():
        for p in ps: pos.append((p,w))
    return clean(" ".join(w for p,w in sorted(pos)))
