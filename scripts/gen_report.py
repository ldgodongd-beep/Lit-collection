import json,sys,collections
ORDER=["Regional Studies","Economic Geography","Journal of Economic Geography","Urban Geography","Urban Studies","Applied Geography",
"Environment and Planning A: Economy and Space","Environment and Planning B: Urban Analytics and City Science","Environment and Planning C: Politics and Space",
"Annals of the American Association of Geographers","Progress in Human Geography","Dialogues in Human Geography","Antipode",
"Eurasian Geography and Economics","International Journal of Urban and Regional Research","Geoforum"]
TOP=["区域发展、创新与演化经济地理","全球化、地缘经济与产业网络","金融化、住房与房地产","城市治理、规划与政策","城市空间、社会分异与不平等","劳动、生计与日常生活","环境、气候与政治生态","能源转型与基础设施","城市分析、GIS与空间方法","政治地理、国家与地缘政治","批判理论、知识生产与学科反思","健康、移动性与可达性","移民、种族与身份"]
d={}
for i in range(4): d.update(json.load(open(f"chunk{i}_zh.json")))
for j in d: d[j]=[p for p in d[j] if not p.get("drop")]
def anchor(j): return "".join(c for c in j.lower().replace(" ","-") if c.isalnum() or c=="-").replace(":","")
def issue(p):
    if p.get("vol") and p.get("iss"): return f"Vol. {p['vol']}({p['iss']})"
    return "Online first / 在线优先"
def fmtdate(s):
    a=s.split("-"); return "-".join([a[0]]+[x.zfill(2) for x in a[1:]])
L=[]; W=L.append
total=sum(len(v) for v in d.values())
W(f"# 人文/经济地理学期刊最新论文速递（2026-11-20）\n")
W(f"> 数据来源：Crossref / OpenAlex 元数据（检索日期 2026-11-20）。收录范围：各刊近 30 天在线发表的研究论文（每刊最多 15 篇，按发表日期倒序）；近 30 天不足 5 篇的期刊回溯至近 4 个月或最新一期。共 **{total}** 篇。中文译文由 AI 翻译，引用请以原文为准。部分 Elsevier 期刊（Applied Geography、Geoforum）的最新在线论文尚未在开放元数据中提供摘要，仅列出题目。\n")
W("## 目录\n\n**一、按期刊分类**\n")
for j in ORDER:
    if j in d: W(f"- [{j}](#{anchor(j)})（{len(d[j])} 篇）")
W("\n**二、按研究主题分类**\n")
bytopic=collections.defaultdict(list)
for j in ORDER:
    for p in d.get(j,[]):
        bytopic[p["topic"]].append((j,p))
        if p.get("topic2") and p["topic2"]!=p["topic"]: bytopic[p["topic2"]].append((j,p))
for t in TOP:
    if bytopic[t]: W(f"- [{t}](#{anchor(t)})（{len(bytopic[t])} 篇）")
W("\n---\n\n# 一、按期刊分类\n")
n=0; idx={}
for j in ORDER:
    if j not in d: continue
    W(f"## {j}\n")
    iss=sorted({issue(p) for p in d[j]})
    W(f"*本期收录：{len(d[j])} 篇｜卷期：{'；'.join(iss)}*\n")
    for p in d[j]:
        n+=1; idx[p["doi"]]=n
        W(f"### [{n}] {p['title']}\n")
        W(f"**{p['title_zh']}**\n")
        meta=f"- 作者：{p['authors'] or '—'}\n- 发表：{fmtdate(p['date'])}｜{issue(p)}｜DOI: [{p['doi']}](https://doi.org/{p['doi']})\n- 主题：{p['topic']}" + (f"；{p['topic2']}" if p.get('topic2') else "") + (f"｜关键词：{'、'.join(p.get('keywords_zh',[]))}" if p.get('keywords_zh') else "")
        W(meta+"\n")
        if p.get("abstract_zh") and len(p.get("abstract",""))>=100:
            W(f"**Abstract:** {p['abstract']}\n")
            W(f"**摘要：** {p['abstract_zh']}\n")
        else:
            W("*（摘要暂未在开放元数据中提供 / Abstract not yet available）*\n")
W("---\n\n# 二、按研究主题分类\n")
for t in TOP:
    if not bytopic[t]: continue
    W(f"## {t}\n")
    W("| # | 题目 / Title | 期刊 |\n|---|---|---|")
    for j,p in bytopic[t]:
        W(f"| [{idx[p['doi']]}] | {p['title_zh']}<br>*{p['title'].replace('|','/')}* | {j} |")
    W("")
open(sys.argv[1],"w").write("\n".join(L))
print(total, {t:len(bytopic[t]) for t in TOP})
