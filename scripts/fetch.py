import json, urllib.request, re, html, sys, time
exec(open("fetch.py").read().split("out={}")[0])
def oa_abs(doi):
    d=get("https://api.openalex.org/works/doi:"+doi+"?select=abstract_inverted_index")
    if not d or not d.get("abstract_inverted_index"): return ""
    pos=[]
    for w,ps in d["abstract_inverted_index"].items():
        for p in ps: pos.append((p,w))
    return clean(" ".join(w for p,w in sorted(pos)))
out={}
for name,issn in J:
    res=[]
    for since,cap in [("2026-10-21",15),("2026-07-20",8)]:
        u=f"https://api.crossref.org/journals/{issn}/works?filter=from-pub-date:{since},type:journal-article&sort=published&order=desc&rows=80&select=DOI,title,published,abstract,volume,issue,author"
        d=get(u); items=d["message"]["items"] if d else []
        res=[]
        for it in items:
            t=clean((it.get("title") or [""])[0])
            if not t or SKIP.match(t) or re.match(r"^(book review|review of)",t,re.I): continue
            au=it.get("author") or []
            res.append(dict(doi=it["DOI"],title=t,abstract=clean(it.get("abstract")),date="-".join(str(x) for x in it.get("published",{}).get("date-parts",[[0]])[0]),
              vol=it.get("volume"),iss=it.get("issue"),authors=", ".join(((a.get("given","")+" "+a.get("family","")).strip()) for a in au[:3])+(" et al." if len(au)>3 else "")))
        if len(res)>=5: break
    res=res[:cap]
    for r in res:
        if len(r["abstract"])<100:
            a=oa_abs(r["doi"])
            if a: r["abstract"]=a
    out[name]=res
    print(name,len(res),sum(1 for r in res if r["abstract"]),file=sys.stderr)
json.dump(out,open("sel.json","w"),ensure_ascii=False,indent=1)
