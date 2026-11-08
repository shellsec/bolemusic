"""Check public metadata and bounded audio samples; never download full episodes."""
import argparse,concurrent.futures,datetime,hashlib,json,re,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STAMP=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
UA="BoleMusic/1.1.0"
def get(url,limit,headers=None):
    if urllib.parse.urlparse(url).scheme not in ("https","http"): raise ValueError("unsupported URL scheme")
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":UA,**(headers or {})}),timeout=12) as r:
        return r.status,r.url,dict(r.headers),r.read(limit)
def audio(url,seek=False):
    status,final,headers,data=get(url,4096,{"Range":"bytes=1048576-1052671"} if seek else {})
    mime=next((v for k,v in headers.items() if k.lower()=="content-type"),"").split(";")[0]
    if status not in (200,206) or not data or not mime.startswith(("audio/","application/octet-stream")): raise ValueError("response is not audio")
    if data.lstrip().startswith((b"#EXTM3U",b"<")): raise ValueError("playlist/HTML response")
    return {"http_status":status,"content_type":mime,"sample_bytes":len(data),"range":next((v for k,v in headers.items() if k.lower()=="content-range"),None),"transport_only":True,"device_tested":False}
def podcast(row):
    try:
        code,final,headers,body=get(row["feed_url"],12*1024*1024+1)
        if code!=200 or len(body)>12*1024*1024: raise ValueError("feed too large or HTTP failure")
        doc=ET.fromstring(body);channel=doc.find("channel")
        if channel is None: raise ValueError("RSS channel missing")
        entries=channel.findall("item");item=next(x for x in entries if x.find("enclosure") is not None)
        enclosure=item.find("enclosure");sample=audio(enclosure.get("url"),True)
        cover=channel.find("{http://www.itunes.com/dtds/podcast-1.0.dtd}image")
        image=channel.findtext("image/url")
        row["artwork_url"]=cover.get("href") if cover is not None else image
        row["latest_publication"]=item.findtext("pubDate")
        row["feed_audio_type"]=enclosure.get("type")
        row["feed_episode_count"]=len(entries)
        row["verification"]={"checked_at":STAMP,"rss_http_status":code,"guid_present":bool(item.findtext("guid")),"audio":sample}
        row["availability"]="reachable";row["last_verified_at"]=STAMP
    except Exception as e:
        row["availability"]="unreachable";row["verification"]={"checked_at":STAMP,"error":str(e)[:200],"device_tested":False}
    return row
def station(row):
    urls=[x["url"] for x in row.get("streams",[])]
    try:
        if row.get("playlist_url"):
            _,_,_,body=get(row["playlist_url"],65536)
            urls=[line.partition("=")[2].strip() for line in body.decode("utf-8","replace").splitlines() if line.lower().startswith("file") and "=" in line]
            if not urls: urls=[x for x in body.decode("utf-8","replace").splitlines() if x.startswith(("https://","http://"))]
        checks=[];streams=[]
        for url in urls[:3]:
            try:
                sample=audio(url)
                if sample["content_type"] not in ("audio/mpeg","audio/mp3"): raise ValueError("not an MP3 direct stream")
                streams.append({"url":url,"codec":"MP3"})
                checks.append({"url":url,**sample})
                if len(streams)==2:break
            except Exception as e:checks.append({"url":url,"error":str(e)[:160]})
        if not streams:raise ValueError("no reachable MP3 stream")
        row["streams"]=streams;row["availability"]="reachable";row["last_verified_at"]=STAMP
        row["verification"]={"checked_at":STAMP,"streams":checks,"transport_only":True,"device_tested":False}
    except Exception as e:
        row["availability"]="unreachable";row["verification"]={"checked_at":STAMP,"error":str(e)[:200],"device_tested":False}
    return row
def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+chr(10),encoding="utf-8")
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--write",action="store_true");args=parser.parse_args()
    report={"checked_at":STAMP,"scope":"RSS XML and bounded HTTP audio samples; no full decoding or Switch device certification","podcasts":[],"radio":[]}
    for filename,key,checker in (("podcasts","channels",podcast),("radio","stations",station)):
        path=ROOT/"catalogs"/(filename+".json");doc=json.loads(path.read_text(encoding="utf-8"))
        ids=[x["id"] for x in doc[key]]
        if len(ids)!=len(set(ids)):raise ValueError("duplicate IDs")
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(checker,doc[key]))
        report["podcasts" if filename=="podcasts" else "radio"]=[{"id":r["id"],"availability":r["availability"],"verification":r["verification"]} for r in rows]
        if args.write:
            doc[key]=rows;doc["updated_at"]=STAMP;write(path,doc)
        print(filename,len(rows),"reachable",sum(r["availability"]=="reachable" for r in rows))
    if args.write:
        write(ROOT/"health.json",report)
        manifest={"schema_version":1,"kind":"bolemusic-content","revision":1,"updated_at":STAMP,"catalogs":{},"delivery":{"primary":"https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/bolemusic/master/catalog.json","fallback":"https://raw.githubusercontent.com/shellsec/bolemusic/master/catalog.json","max_catalog_bytes":2097152,"keep_last_good":True,"refresh_hours":24},"merge_policy":{"stable_ids":True,"preserve_user_subscriptions":True,"preserve_favorites":True,"preserve_progress":True,"preserve_downloads":True}}
        for name in ("podcasts","radio"):
            path=ROOT/"catalogs"/(name+".json");raw="https://raw.githubusercontent.com/shellsec/bolemusic/master/catalogs/"+name+".json"
            manifest["catalogs"][name]={"url":raw,"accelerated_url":"https://gh-proxy.com/"+raw,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size}
        write(ROOT/"catalog.json",manifest)
if __name__=="__main__":main()
