"""sonra. gerçek uygulama ekran yakalayıcı. Kullanım: python3 capture.py OUT_DIR [light|dark] [tr|en]"""
import sys, json, time, asyncio, os, glob
from playwright.async_api import async_playwright
OUT=sys.argv[1]; SCHEME=sys.argv[2] if len(sys.argv)>2 else 'light'; LANG=sys.argv[3] if len(sys.argv)>3 else 'tr'
HERE=os.path.dirname(os.path.abspath(__file__)); os.makedirs(OUT,exist_ok=True)
now=int(time.time()*1000); items=[]
for i,(cat,url,title,src,th) in enumerate(json.load(open(os.environ.get('SEED') or (f'{HERE}/seed.json' if LANG=='tr' else f'{HERE}/seed_en.json')))):
    items.append({"id":f"demo-{i}","url":url,"resolvedUrl":url,"title":title,"category":cat,"source":src,"createdAt":now-i*5*3600*1000,"syncUpdatedAt":now-i*5*3600*1000,"analysisStatus":"ready","analysisMethod":"ai","confidence":0.92,"imageUrl":f"https://demo-img.sonra.local/t{th}.jpg","description":"","tags":[]})
seed={"@sonra/items-v5":json.dumps(items),"@sonra/language-v1":LANG,"@sonra/theme-v1":SCHEME,"@sonra/ios-action-guide-v2":"1","@sonra/backup-nudge-dismissed-v1":str(now)}
init="const s="+json.dumps(seed)+";for(const k in s){if(localStorage.getItem(k)===null)localStorage.setItem(k,s[k]);}"
T={'İzle':'İzle','Git':'Git','Satın Al':'Satın Al','Yap':'Yap','Keşfet':'Keşfet','Sonra':'Sonra','Profil':'Profil'} if LANG=='tr' else {'İzle':'Watch','Git':'Go','Satın Al':'Buy','Yap':'Do','Keşfet':'Explore','Sonra':'Later','Profil':'Profile'}
async def shot(pg,name): await pg.wait_for_timeout(900); await pg.screenshot(path=f'{OUT}/{name}.png'); print('ok',name)
async def tap(pg,text,exact=True):
    loc=pg.get_by_text(text,exact=exact).last
    await loc.click(timeout=4000); await pg.wait_for_timeout(700)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':393,'height':852},device_scale_factor=3,locale='tr-TR' if LANG=='tr' else 'en-US',timezone_id='Europe/Istanbul',color_scheme=SCHEME)
        async def route(r):
            u=r.request.url
            if 'demo-img.sonra.local' in u: return await r.fulfill(path=f"{HERE}/thumbs/{u.rsplit('/',1)[1]}",content_type='image/jpeg')
            if u.startswith('http://localhost'): return await r.continue_()
            return await r.abort()
        await ctx.route('**/*',route); await ctx.add_init_script(init)
        pg=await ctx.new_page(); await pg.goto('http://localhost:8090/'); await pg.wait_for_timeout(3500)
        steps=[('01-ana-sayfa',None)]
        await shot(pg,'01-ana-sayfa')
        for name,acts in [('02-izle',['İzle']),('03-git',['Git']),('04-satin-al',['Satın Al']),('05-yap',['Yap'])]:
            try:
                await pg.goto('http://localhost:8090/'); await pg.wait_for_timeout(2500)
                for a in acts: await tap(pg,T.get(a,a))
                await shot(pg,name)
            except Exception as e: print('skip',name,e)
        for name,acts in [('06-kesfet',['Keşfet']),('07-sonra-liste',['Sonra']),('08-profil',['Profil'])]:
            try:
                await pg.goto('http://localhost:8090/'); await pg.wait_for_timeout(2500)
                for a in acts: await tap(pg,T.get(a,a))
                await shot(pg,name)
                await pg.mouse.wheel(0,900); await shot(pg,name+'-alt')
            except Exception as e: print('skip',name,e)
        try:
            await pg.goto('http://localhost:8090/'); await pg.wait_for_timeout(2500)
            await tap(pg,os.environ.get('DETAIL') or ('Gece 2\'de kaydedilen kremalı mantarlı makarna' if LANG=='tr' else 'Creamy mushroom pasta saved at 2 a.m.')); await shot(pg,'09-kayit-detay')
        except Exception as e: print('skip detay',e)
        try:
            await pg.goto('http://localhost:8090/'); await pg.wait_for_timeout(2500)
            await tap(pg,T['Sonra']); inp=pg.locator('input').first; await inp.click(); await inp.type(os.environ.get('QUERY') or ('kafe' if LANG=='tr' else 'café'),delay=60)
            await shot(pg,'10-arama-kafe')
        except Exception as e: print('skip arama',e)
        try:
            await pg.goto('http://localhost:8090/'); await pg.wait_for_timeout(2500)
            await tap(pg,T['Keşfet']); await tap(pg,'15 dakikam var' if LANG=='tr' else '15 min',exact=False); await shot(pg,'11-kesfet-15dk')
        except Exception as e: print('skip 15dk',e)
        await b.close()
asyncio.run(main())
