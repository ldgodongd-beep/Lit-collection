import json,glob,collections,sys
P=json.load(open("papers.json"))
T={}
for f in glob.glob("trans*.json"):
    for t in json.load(open(f)): T[t["id"]]=t
missing=[p["id"] for p in P if p["id"] not in T]
assert not missing, missing
TOP=dict(R1="区域发展、创新与产业政策 Regional development, innovation & industrial policy",R2="劳动、企业与全球生产网络 Labour, firms & global production networks",R3="金融化、资本与房地产 Finance, capital & real estate",U1="住房、城市更新与士绅化 Housing, regeneration & gentrification",U2="城市治理、规划与政策 Urban governance, planning & policy",U3="基础设施、交通与移动性 Infrastructure, transport & mobility",D1="数字技术、平台与人工智能 Digital technologies, platforms & AI",E1="环境、气候与能源转型 Environment, climate & energy transitions",E2="农业、粮食、资源与乡村 Agrarian, food, resources & rural",S1="移民、种族、性别与身份 Migration, race, gender & identity",S2="不平等、贫困与社会正义 Inequality, poverty & social justice",S3="健康、福祉与日常生活 Health, wellbeing & everyday life",P1="国家、地缘政治与边界 State, geopolitics & borders",M1="空间分析、GIS 与城市计算 Spatial analysis, GIS & urban analytics",T1="理论、认识论与学科反思 Theory, epistemology & the discipline")
ORDER=["Regional Studies","Economic Geography","Journal of Economic Geography","Urban Geography","Urban Studies","Applied Geography","Environment and Planning A","Environment and Planning B","Environment and Planning C","Annals of the AAG","Progress in Human Geography","Dialogues in Human Geography","Antipode","Eurasian Geography and Economics","IJURR","Geoforum"]
FULL={"Environment and Planning A":"Environment and Planning A: Economy and Space","Environment and Planning B":"Environment and Planning B: Urban Analytics and City Science","Environment and Planning C":"Environment and Planning C: Politics and Space","Annals of the AAG":"Annals of the American Association of Geographers","IJURR":"International Journal of Urban and Regional Research"}
for p in P:
    t=T[p["id"]];p.update(title_zh=t["title_zh"],abstract_zh=t["abstract_zh"],topic=t["topic"] if t["topic"] in TOP else "T1")
def vi(p): return f"Vol. {p['vol']}({p['issue']})" if p['vol'] and p['issue'] else (f"Vol. {p['vol']}" if p['vol'] else "Online first 在线优先")
def entry(p,show_j=False):
    au=", ".join(p["authors"][:4])+(" et al." if len(p["authors"])>4 else "")
    s=f"**{p['title']}**  \n**{p['title_zh']}**  \n"
    s+=f"*{au or '作者信息缺失'}*｜{('*'+FULL.get(p['journal'],p['journal'])+'*｜') if show_j else ''}{p['date']}｜{vi(p)}｜[doi:{p['doi']}](https://doi.org/{p['doi']})\n\n"
    if p["abstract"]:
        s+=f"> **Abstract:** {p['abstract']}\n>\n> **摘要：** {p['abstract_zh']}\n\n"
    else:
        s+="> *摘要：Crossref 未收录该文摘要（出版社未开放摘要元数据），请点击 DOI 查看。*\n\n"
    return s
date=sys.argv[1]
L=[f"# 人文/经济/城市地理期刊最新论文速递（{date}）\n",
"**收录范围：** 2026-10-18 至 2026-11-17 期间在 Crossref 新登记的研究论文（含在线优先 online first 与最新正式卷期），共 16 种期刊、%d 篇。已剔除社论、勘误、书评等非研究类条目。\n"%len(P),
"**数据来源：** Crossref API。Taylor & Francis（Regional Studies、Urban Geography、Annals of the AAG、Eurasian Geography and Economics）、Elsevier（Applied Geography、Geoforum）及 Economic Geography 不向 Crossref 提供摘要，这些文章只列中英文题目，摘要请点 DOI 查看。中文译文为机器辅助翻译，引用请以英文原文为准。\n",
"## 概览\n","| 期刊 | 篇数 | 有摘要 |","|---|---|---|"]
by_j=collections.defaultdict(list)
for p in P: by_j[p["journal"]].append(p)
for j in ORDER: L.append(f"| [{FULL.get(j,j)}](#{j.lower().replace(' ','-')}) | {len(by_j[j])} | {sum(1 for p in by_j[j] if p['abstract'])} |")
by_t=collections.defaultdict(list)
for p in P: by_t[p["topic"]].append(p)
L+=["","| 研究主题 | 篇数 |","|---|---|"]+[f"| {TOP[k]} | {len(by_t[k])} |" for k in TOP if by_t[k]]
L+=["","---","# 第一部分：按期刊分类\n"]
for j in ORDER:
    L.append(f"## {j}\n")
    if j in FULL: L.append(f"*{FULL[j]}*\n")
    if not by_j[j]: L.append("本期无新登记论文。\n")
    for p in sorted(by_j[j],key=lambda x:x["date"],reverse=True):
        L.append(f"`{p['topic']}` "+entry(p))
L+=["---","# 第二部分：按研究主题分类\n"]
for k in TOP:
    if not by_t[k]: continue
    L.append(f"## {k}｜{TOP[k]}（{len(by_t[k])} 篇）\n")
    for p in sorted(by_t[k],key=lambda x:(ORDER.index(x["journal"]),x["date"])):
        au=", ".join(p["authors"][:3])+(" et al." if len(p["authors"])>3 else "")
        L.append(f"- **{p['title']}**  \n  {p['title_zh']}  \n  *{FULL.get(p['journal'],p['journal'])}*｜{au}｜[doi:{p['doi']}](https://doi.org/{p['doi']})")
    L.append("")
open(sys.argv[2],"w").write("\n".join(L))
json.dump(P,open(sys.argv[2].replace(".md",".json"),"w"),ensure_ascii=False,indent=1)
print("ok",len(P))
