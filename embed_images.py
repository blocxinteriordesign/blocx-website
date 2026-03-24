"""
BlocX Portfolio — Image Embedder
ضع هذا الملف مع BlocX-Portfolio.html في نفس المجلد
شغّل: python embed_images.py
"""
import os, sys, re, base64, io

# ── إعدادات الضغط ────────────────────────────────────────────
MAX_DIM  = 1200   # أقصى أبعاد للصورة
QUALITY  = 72     # جودة JPEG
MAX_IMGS = 10     # أقصى عدد صور لكل مشروع
MIN_SIZE = 15000  # تجاهل الملفات أقل من 15KB

IMG_EXTS = ('.jpg','.jpeg','.png','.webp')

# ── تثبيت Pillow ──────────────────────────────────────────────
try:
    from PIL import Image
    HAS_PIL = True
except:
    print("Installing Pillow for compression...")
    os.system(f'"{sys.executable}" -m pip install Pillow -q')
    try: from PIL import Image; HAS_PIL = True
    except: HAS_PIL = False; print("  No Pillow — images won't compress")

# ── ربط المجلدات بأسماء المشاريع ─────────────────────────────
FOLDER_MAP = {
    "SOHO VINTAGE BARBERS_files":                   "SOHO VINTAGE BARBERS",
    "RE_MAX HUB_files":                             "RE/MAX HUB",
    "Aspen Pharmacare MENAT_files":                 "Aspen Pharmacare MENAT",
    "Assembly Global_files":                        "Assembly Global MEA",
    "Strada Real Estate_files":                     "Strada Real Estate",
    "IVI HOLDING_files":                            "IVI HOLDING",
    "FALCONS Auction warehouse 20&21 office_files": "FALCONS Auction Warehouse",
    "Create Nation Marketing_files":                "Create Nation Marketing",
    "A2B Global DMCC_files":                        "A2B Global DMCC",
    "Apartment - Al Arta 1_files":                  "Apartment \u2013 Al Arta 1",
    "Villa calida 23_files":                        "Villa Calida 23",
    "FEHD Barber shop Project_files":               "FEHD Barber Shop",
    "PESCOAG DMCC 2803_files":                      "PESCOAG DMCC 2803",
    "THE BOUTIQUE XII Project_files":               "THE BOUTIQUE XII",
    "Innospec_files":                               "Innospec",
    "VANTEC_files":                                 "__VANTEC__",
    "NSAS TOURISM_files":                           "__NSAS__",
    "VISTA CORPORATE BUSINESS CENTER L.L.C_files":  "VISTA Corporate Centre",
    "Epure Spa_files":                              "Epure Spa",
    "Mcontent_files":                               "Mcontent",
    "Enterprise systems_files":                     "Enterprise Systems",
    "Calculus Networks_files":                      "Calculus Networks",
    "SEACOR OFFSHORE DUBAI L.L.C_files":            "SEACOR Offshore Dubai",
    "XO MIDDLE EAST DMCC_files":                    "XO Middle East DMCC",
    "ONE BUSINESS CENTRE_files":                    "ONE BUSINESS CENTRE",
    "UNIT 1609 REGAL TOWER_files":                  "Unit 1609 \u2013 Regal Tower",
    "Bellevue apartment_files":                     "Bellevue Apartment",
    "The Palm Jumeirah Villa_files":                "The Palm Jumeirah Villa",
    "UNIT 1006_files":                              "Unit 1006",
    "Clients_LOGO":                                 "__LOGOS__",
}

def compress(path):
    if HAS_PIL:
        try:
            img = Image.open(path).convert("RGB")
            w,h = img.size
            if w>MAX_DIM or h>MAX_DIM:
                r=min(MAX_DIM/w,MAX_DIM/h)
                img=img.resize((int(w*r),int(h*r)),Image.LANCZOS)
            buf=io.BytesIO()
            img.save(buf,"JPEG",quality=QUALITY,optimize=True)
            return "data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()
        except: pass
    with open(path,"rb") as f: d=f.read()
    ext=os.path.splitext(path)[1].lower().strip('.')
    ct={"jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png"}.get(ext,"image/jpeg")
    return f"data:{ct};base64,"+base64.b64encode(d).decode()

def sort_key(f):
    m=re.search(r'(\d+)(?:\.\w+)?$',f); return int(m.group(1)) if m else 0

def is_img(fp):
    f=os.path.basename(fp).lower()
    if not any(f.endswith(e) for e in IMG_EXTS): return False
    try: return os.path.getsize(fp)>MIN_SIZE
    except: return False

HERE = os.getcwd()
print("="*60)
print("  BlocX Portfolio — Image Embedder")
print(f"  Folder: {HERE}")
print("="*60)

# تحديد ملف HTML
html_path = os.path.join(HERE,"BlocX-Portfolio.html")
if not os.path.exists(html_path):
    print(f"\n❌ BlocX-Portfolio.html not found in:\n   {HERE}")
    print("\n   Make sure BlocX-Portfolio.html is in this folder!")
    input("Press Enter..."); sys.exit()
print(f"\n  ✅ Found: BlocX-Portfolio.html")

# قراءة الصور
print("\n  Reading images...\n")
project_imgs = {}
logo_imgs    = {}
vantec_imgs  = []
nsas_imgs    = []

for folder_name, proj_name in FOLDER_MAP.items():
    fp = os.path.join(HERE, folder_name)
    if not os.path.isdir(fp): continue

    files = sorted([f for f in os.listdir(fp) if is_img(os.path.join(fp,f))], key=sort_key)
    if not files: print(f"  ⬜ {folder_name}"); continue

    imgs = []
    for i,fn in enumerate(files[:MAX_IMGS]):
        sys.stdout.write(f"\r  ⏳ {proj_name[:40]:<40} {i+1}/{min(MAX_IMGS,len(files))}  ")
        sys.stdout.flush()
        try: imgs.append(compress(os.path.join(fp,fn)))
        except: pass

    sys.stdout.write(f"\r  ✅ {proj_name[:40]:<40} {len(imgs)} images\n")
    sys.stdout.flush()

    if   proj_name == "__LOGOS__":  logo_imgs = {os.path.splitext(fn)[0].lower(): compress(os.path.join(fp,fn)) for fn in files[:30]}; print(f"  📌 Logos: {len(logo_imgs)}")
    elif proj_name == "__VANTEC__": vantec_imgs = imgs
    elif proj_name == "__NSAS__":   nsas_imgs   = imgs
    elif imgs:                      project_imgs[proj_name] = imgs

print(f"\n  Projects: {len(project_imgs)}  VANTEC: {len(vantec_imgs)}  NSAS: {len(nsas_imgs)}")

# تعديل HTML
print("\n  Patching HTML...")
with open(html_path,"r",encoding="utf-8") as f: html = f.read()

patched = 0
for name, imgs in project_imgs.items():
    pat = (
        r"(name:'" + re.escape(name) + r"'"
        r"(?:(?!name:').){0,600}?thumb:)(?:null|'[^']*')"
        r"(,\s*imgs:)\[[^\]]*\]"
    )
    new, n = re.subn(pat,
        rf"\g<1>'{imgs[0]}'\g<2>[{','.join(repr(i) for i in imgs)}]",
        html, flags=re.DOTALL)
    if n: html=new; patched+=1
    else: print(f"  ⚠ No match: '{name}'")

# تعديل openExh لـ VANTEC و NSAS
if vantec_imgs or nsas_imgs:
    nsas_js   = "[" + ",".join(repr(i) for i in nsas_imgs)   + "]"
    vantec_js = "[" + ",".join(repr(i) for i in vantec_imgs) + "]"
    old = re.search(r'function openExh\(i\)\{.*?\}(?=\s*function|\s*//|\s*var|\s*const|\s*document)',
                    html, re.DOTALL)
    if old:
        new_fn = (
            f"function openExh(i){{\n"
            f"  var nsas_imgs={nsas_js};\n"
            f"  var vantec_imgs={vantec_js};\n"
            f"  var e=[{{name:'NSAS Tourism',cat:'exhibition',loc:'UAE',status:'Completed',"
            f"concept:'Custom exhibition stand for the tourism sector.',imgs:nsas_imgs}},"
            f"{{name:'VANTEC',cat:'exhibition',loc:'UAE',status:'Completed',"
            f"concept:'High-impact booth for technology exhibition.',imgs:vantec_imgs}}][i];\n"
            f"  galOpen(e,0);\n}}"
        )
        html = html.replace(old.group(), new_fn)
        print(f"  ✅ Exhibition patched")

# Logos
if logo_imgs and "const LOGOS=" not in html:
    ljs = "const LOGOS={" + ",".join(f"'{k}':'{v}'" for k,v in list(logo_imgs.items())[:30]) + "};"
    html = html.replace("function buildGrid()", ljs+"\nfunction buildGrid()")

# حفظ
OUT = os.path.join(HERE,"BlocX-Portfolio-EMBEDDED.html")
with open(OUT,"w",encoding="utf-8") as f: f.write(html)
mb = os.path.getsize(OUT)/1024/1024

print(f"\n{'='*60}")
print(f"  ✅ Done!  {patched}/27 projects patched")
print(f"  ✅ File:  BlocX-Portfolio-EMBEDDED.html  ({mb:.1f} MB)")
print(f"  📂 Location: {OUT}")
print(f"{'='*60}")
print(f"\n  ⬆ Upload THIS file to Netlify:")
print(f"     BlocX-Portfolio-EMBEDDED.html  ({mb:.1f} MB)")
if mb > 200:
    print(f"\n  ⚠ File too large! Reduce MAX_DIM to 900 at top of script")
elif mb < 5:
    print(f"\n  ⚠ File too small — images may not have been found!")
    print(f"     Check that project folders are in: {HERE}")
input("\nPress Enter to exit...")
