"""Geniş ekran yakalayıcı. python3 capture2.py OUT light|dark tr|en SEEDFILE"""
import sys, json, time, asyncio, os
from playwright.async_api import async_playwright
OUT,SCHEME,LANG,SEED=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
HERE=os.path.dirname(os.path.abspath(__file__)); os.makedirs(OUT,exist_ok=True)
now=int(time.time()*1000); rows=json.load(open(SEED)); items=[]
for i,(cat,url,title,src,th) in enumerate(rows):
    items.append({"id":f"d{i}","url":url,"resolvedUrl":url,"title":title,"category":cat,"source":src,"createdAt":now-i*4*3600*1000,"syncUpdatedAt":now-i*4*3600*1000,"analysisStatus":"ready","analysisMethod":"ai","confidence":0.92,"imageUrl":f"https://demo-img.sonra.local/t{th}.jpg","description":"","tags":[]})
seed={"@sonra/items-v5":json.dumps(items),"@sonra/language-v1":LANG,"@sonra/theme-v1":SCHEME,"@sonra/ios-action-guide-v2":"1","@sonra/backup-nudge-dismissed-v1":str(now)}
init="const s="+json.dumps(seed)+";for(const k in s){if(localStorage.getItem(k)===null)localStorage.setItem(k,s[k]);}"
TR=LANG=='tr'
L=lambda tr,en: tr if TR else en
NAV={'home':L('Ana Sayfa','Home'),'disc':L('Keşfet','Explore'),'list':L('Sonra','Later'),'prof':L('Profil','Profile')}
CATS=[('izle',L('İzle','Watch')),('git',L('Git','Go')),('oku',L('Oku','Read')),('satin-al',L('Satın Al','Buy')),('dinle',L('Dinle','Listen')),('yap',L('Yap','Do'))]
async def scroll(pg,y):
    await pg.evaluate("""(y)=>{for(const e of document.querySelectorAll('div')){const s=getComputedStyle(e);if((s.overflowY=='auto'||s.overflowY=='scroll')&&e.scrollHeight>e.clientHeight+50){e.scrollTop=y;}}}""",y)
    await pg.wait_for_timeout(600)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':393,'height':852},device_scale_factor=3,locale=L('tr-TR','en-US'),timezone_id='Europe/Istanbul',color_scheme=SCHEME)
        async def route(r):
            u=r.request.url
            if 'demo-img.sonra.local' in u: return await r.fulfill(path=f"{HERE}/thumbs/{u.rsplit('/',1)[1]}",content_type='image/jpeg')
            if u.startswith('http://localhost'): return await r.continue_()
            return await r.abort()
        await ctx.route('**/*',route); await ctx.add_init_script(init)
        pg=await ctx.new_page()
        async def fresh(): await pg.goto('http://localhost:8090/'); await pg.wait_for_timeout(2300)
        async def tap(t,exact=True): await pg.get_by_text(t,exact=exact).last.click(timeout=4000); await pg.wait_for_timeout(800)
        async def shot(n): await pg.wait_for_timeout(500); await pg.screenshot(path=f'{OUT}/{n}.jpg',type='jpeg',quality=90)
        async def run(n,fn):
            try: await fresh(); await fn(); await shot(n)
            except Exception as e: print('skip',n,str(e)[:80])
        async def nop(): pass
        await run('ana-sayfa',nop)
        async def hs(): await scroll(pg,700)
        await run('ana-sayfa-asagi',hs)
        for slug,lab in CATS:
            async def f(lab=lab): await tap(lab)
            await run(f'kart-{slug}',f)
            async def f2(lab=lab):
                await tap(lab); await tap(L('Geç','Skip'),False)
            await run(f'kart-{slug}-2',f2)
        async def d(): await tap(NAV['disc'])
        await run('kesfet',d)
        async def d2(): await tap(NAV['disc']); await scroll(pg,800)
        await run('kesfet-asagi',d2)
        for slug,lab in [('15dk',L('15 dakikam var','15 min')),('1saat',L('1 saatim var','1 hour')),('disari',L('Dışarı çıkacağım','going out')),('sec',L('Bana bir şey seç','Pick'))]:
            async def f(lab=lab): await tap(NAV['disc']); await tap(lab,False)
            await run(f'kesfet-{slug}',f)
        async def l(): await tap(NAV['list'])
        await run('liste',l)
        async def l2(): await tap(NAV['list']); await scroll(pg,900)
        await run('liste-asagi',l2)
        for slug,lab in CATS[:4]:
            async def f(lab=lab): await tap(NAV['list']); await tap(lab,False)
            await run(f'liste-filtre-{slug}',f)
        for q in json.load(open(SEED.replace('.json','.queries.json'))) if os.path.exists(SEED.replace('.json','.queries.json')) else []:
            async def f(q=q):
                await tap(NAV['list']); i=pg.locator('input').first; await i.click(); await i.type(q,delay=50)
            await run('arama-'+q.replace(' ','-'),f)
        async def pr(): await tap(NAV['prof'])
        await run('profil',pr)
        async def pr2(): await tap(NAV['prof']); await scroll(pg,700)
        await run('profil-asagi',pr2)
        async def st(): await tap(NAV['prof']); await tap(L('Ayarlar','Settings'),False)
        await run('ayarlar',st)
        async def st2(): await tap(NAV['prof']); await tap(L('Ayarlar','Settings'),False); await scroll(pg,800)
        await run('ayarlar-asagi',st2)
        async def ad():
            await pg.mouse.click(196,790); await pg.wait_for_timeout(1000)
        await run('ekle',ad)
        for k,(cat,url,title,src,th) in enumerate(rows[:8:2]):
            async def f(title=title): await tap(NAV['list']); await tap(title)
            await run(f'detay-{k}',f)
        await b.close()
asyncio.run(main())
