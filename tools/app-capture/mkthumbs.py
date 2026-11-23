from PIL import Image, ImageDraw, ImageFilter
import random
pal=[[(214,139,80),(120,70,40),(240,200,150)],[(70,110,150),(30,50,80),(170,200,220)],[(90,130,80),(40,70,40),(190,210,160)],[(200,90,90),(110,40,50),(240,180,170)],[(160,120,190),(70,50,100),(220,200,235)],[(220,180,90),(130,90,30),(245,230,180)],[(60,60,70),(20,20,30),(150,150,160)],[(110,170,170),(40,90,90),(200,230,225)]]
for i in range(16):
    random.seed(i); c=pal[i%len(pal)]
    im=Image.new('RGB',(600,600),c[1]); d=ImageDraw.Draw(im)
    for _ in range(14):
        x,y=random.randint(-100,600),random.randint(-100,600); r=random.randint(60,260)
        d.ellipse([x-r,y-r,x+r,y+r],fill=random.choice(c))
    im.filter(ImageFilter.GaussianBlur(38)).save(f'thumbs/t{i}.jpg',quality=85)
