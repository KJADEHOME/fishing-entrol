import json, os
from PIL import Image, ImageDraw

m = json.load(open('scripts/product_images_manifest.json', encoding='utf-8'))
SRC, OUT, COLS, CELL, PAD, LABEL = 'assets/images', '_raw', 3, 420, 24, 22

for slug, items in m.items():
    imgs = []
    for it in items:
        p = os.path.join(SRC, it['file'].split('/')[-1])
        if os.path.exists(p):
            imgs.append((it['file'].split('/')[-1], Image.open(p).convert('RGB')))
    rows = (len(imgs) + COLS - 1) // COLS
    W = COLS * CELL + (COLS + 1) * PAD
    H = rows * (CELL + LABEL) + (rows + 1) * PAD
    cv = Image.new('RGB', (W, H), (242, 242, 242))
    d = ImageDraw.Draw(cv)
    for i, (name, im) in enumerate(imgs):
        r, c = divmod(i, COLS)
        im2 = im.copy(); im2.thumbnail((CELL, CELL))
        x = PAD + c * (CELL + PAD) + (CELL - im2.width) // 2
        y = PAD + r * (CELL + LABEL + PAD)
        cv.paste(im2, (x, y))
        d.text((PAD + c * (CELL + PAD), y + CELL + 4), name.replace('.webp', ''), fill=(10, 10, 10))
    cv.save(os.path.join(OUT, 'final_sheet_%s.jpg' % slug), quality=90)
    print(slug, len(imgs), cv.size)
