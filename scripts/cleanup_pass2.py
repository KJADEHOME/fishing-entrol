import subprocess, sys, os, json, shutil, re

SKILL = "C:/Users/wangy/AppData/Local/Programs/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/buddy-image-processing/scripts/buddy-image-processing.py"
PY = "C:/Users/wangy/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
TOKEN = sys.argv[1]
ONLY = sys.argv[2].split(",") if len(sys.argv) > 2 else None
IMG, OUT = "assets/images", "_raw/erased"
os.makedirs(OUT, exist_ok=True)

JOBS = [
 ("spinning-rod-04.webp", "Remove the white 'Cross BASS RODS' brand text printed on both dark rod blanks. Keep the rods, cork handles, background and layout unchanged."),
 ("spinning-rod-06.webp", "Remove the small yellow label sticker on the blue rod blank near the top. Keep the rod, reel seat, background and caption unchanged."),
 ("carp-rod-02.webp", "Remove the golden 'PROGRESS' script lettering on the black rod blank. Keep the rod, reels, guides, blue background and layout unchanged."),
 ("carp-rod-03.webp", "Remove the small white brand sticker/label on the rod just above the reel seat. Keep everything else unchanged."),
 ("carp-rod-06.webp", "Remove the golden 'PROGRESS' script lettering on the black rod blank. Keep the rod, guides, blue frame and layout unchanged."),
 ("saltwater-rod-01.webp", "Remove the golden 'MEASPLUS BOAT' script lettering on the black rod. Keep the rod, guides, dark background and layout unchanged."),
 ("saltwater-rod-05.webp", "Remove the white 'MORE CATCH' lettering on the orange rod blank. Keep the rod, guides, black frame and caption unchanged."),
 ("rock-surf-rod-03.webp", "Remove the 'REMANSO' brand text on the green rod, and remove the person wearing sunglasses visible in the top-right area. Keep the rods and layout unchanged."),
]

for name, prompt in JOBS:
    if ONLY and name not in ONLY:
        continue
    src = os.path.abspath(os.path.join(IMG, name))
    print("==>", name, flush=True)
    r = subprocess.run([PY, SKILL, "image-edit", "--operation", "erase",
        "--image-file", src, "--prompt", prompt, "--token", TOKEN],
        capture_output=True, text=True, timeout=580)
    m = re.search(r'\{.*\}', r.stdout, re.S)
    if not m:
        print("FAIL-parse", name, r.stdout[-200:], flush=True); continue
    try:
        data = json.loads(m.group(0))
        path = data["result_files"][0]["path"]
        shutil.copyfile(path, os.path.join(OUT, name.replace(".webp", ".png")))
        print("OK", name, flush=True)
    except Exception as e:
        print("FAIL", name, repr(e), r.stdout[-200:], flush=True)
print("PASS2 DONE", flush=True)
