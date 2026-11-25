# Generates the demo product images for ShopDemo.
# before.html uses the large JPEGs (original, unoptimized); after.html uses the resized WebP files.
import numpy as np, os, sys
out=sys.argv[1] if len(sys.argv)>1 else "."
os.makedirs(out,exist_ok=True)
from PIL import Image, ImageDraw, ImageFont
names=["Leather Handbag","Running Shoes","Smart Watch","Cotton Kurta","Wireless Earbuds","Steel Water Bottle","Sunglasses","Backpack"]
cols=[(170,90,50),(40,110,190),(30,30,40),(200,170,120),(230,230,235),(120,160,150),(60,50,40),(90,110,60)]
rng=np.random.default_rng(1)
def art(W,H,c,text,fs):
    y,x=np.mgrid[0:H,0:W]; base=np.zeros((H,W,3))
    for k in range(3): base[...,k]=c[k]*(0.6+0.4*np.sin(x/(W/13)+k)*np.cos(y/(H/10)))+60
    base+=rng.normal(0,28,(H,W,3)); im=Image.fromarray(np.clip(base,0,255).astype('uint8'))
    d=ImageDraw.Draw(im)
    try: f=ImageFont.truetype("DejaVuSans-Bold.ttf",fs)
    except OSError: f=ImageFont.load_default(size=fs)
    if W==H: d.ellipse([W*.2,H*.2,W*.8,H*.8],fill=tuple(int(v*.8) for v in c),outline=(255,255,255),width=W//120)
    d.text((W//2,H-H//9 if W==H else H//2),text,font=f,fill=(255,255,255),anchor="mm"); return im
for n,c in zip(names,cols):
    s=n.lower().replace(" ","-"); im=art(1600,1600,c,n,110)
    im.save(f"{out}/{s}.jpg",quality=92)
    im.resize((400,400),Image.LANCZOS).save(f"{out}/{s}-400.webp",quality=72,method=6)
h=art(2000,800,(11,107,58),"WINTER SALE - FLAT 30% OFF",120)
h.save(f"{out}/hero-banner.jpg",quality=92)
for w in (480,960): h.resize((w,int(w*.4)),Image.LANCZOS).save(f"{out}/hero-banner-{w}.webp",quality=70,method=6)
