import subprocess, sys, os, json, shutil, re

SKILL = "C:/Users/wangy/AppData/Local/Programs/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/buddy-image-processing/scripts/buddy-image-processing.py"
PY = "C:/Users/wangy/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
TOKEN = sys.argv[1]
BATCH = int(sys.argv[2])
IMG = "assets/images"
OUT = "_raw/erased"
os.makedirs(OUT, exist_ok=True)

JOBS = [
 ("spinning-rod-04.webp", "Remove the 'Cross' brand script text printed on the dark rod blanks. Keep the rods, handles, background and layout unchanged."),
 ("spinning-rod-05.webp", "Remove the 'Cross' brand script text printed on the rod blank. Keep the rod, cork handle, reel seat, background and layout unchanged."),
 ("spinning-rod-07.webp", "Remove the small brand emblem logo near the lower left of the rod. Keep the rod, background and the descriptive caption text unchanged."),
 ("carp-rod-01.webp", "Remove the 'PROGRESS CARP' headline text and subtitle at the top. Keep the fishing rod photos and layout unchanged."),
 ("carp-rod-02.webp", "Remove the CRONY logo at the top and the 'PROGRESS carp' brand text printed on the rod blank. Keep the rod, background and layout unchanged."),
 ("carp-rod-03.webp", "Remove the small white CRONY brand sticker/label on the rod above the reel seat. Keep everything else unchanged."),
 ("carp-rod-06.webp", "Remove the CRONY logo and the 'PROGRESS' brand text printed on the rod blank. Keep the rod, background and layout unchanged."),
 ("carp-rod-07.webp", "Remove the small circular CRONY logo on the black rod butt cap. Keep the rod and background unchanged."),
 ("saltwater-rod-01.webp", "Remove the CRONY logo at top, the 'MEASPLUS BOAT' text, and the yellow tagline at the bottom. Keep the rods, background gradient and layout unchanged."),
 ("rock-surf-rod-01.webp", "Remove any small brand text printed on the rod blank. Keep the rods, guide ring insets and layout unchanged."),
 ("rock-surf-rod-02.webp", "Remove the CRONY logo at top, the 'AGGRESS SURF' text, and the yellow tagline at the bottom. Keep the rods, background and layout unchanged."),
 ("rock-surf-rod-03.webp", "Remove the brand text 'REMANSO' printed on the rod blanks. Keep the rods, blue caption boxes and layout unchanged."),
 ("rock-surf-rod-05.webp", "Remove only the word 'CRONY' from the chart title, keeping the rest of the title and the test-curve chart unchanged."),
 ("rock-surf-rod-06.webp", "Remove the brand text 'REMANSO' printed on the rod blank in the middle-left photo. Keep everything else unchanged."),
 ("about-factory-01.webp", "Remove the large Chinese characters printed on the building facade. Keep the building, flags, sky and everything else unchanged."),
]

if BATCH == 1:
    jobs = JOBS[:8]
elif BATCH == 3:
    jobs = [j for j in JOBS if j[0].startswith("rock-surf")]
else:
    jobs = JOBS[8:]
for name, prompt in jobs:
    src = os.path.join(IMG, name)
    print("==>", name, flush=True)
    r = subprocess.run([PY, SKILL, "image-edit", "--operation", "erase",
        "--image-file", os.path.abspath(src), "--prompt", prompt, "--token", TOKEN],
        capture_output=True, text=True, timeout=580)
    m = re.search(r'\{.*\}', r.stdout, re.S)
    if not m:
        print("FAIL-parse", name, r.stdout[-300:], r.stderr[-200:], flush=True); continue
    try:
        data = json.loads(m.group(0))
        path = data["result_files"][0]["path"]
        dst = os.path.join(OUT, name.replace(".webp", ".png"))
        shutil.copyfile(path, dst)
        print("OK", name, "->", dst, flush=True)
    except Exception as e:
        print("FAIL", name, repr(e), r.stdout[-300:], flush=True)
print("BATCH DONE", BATCH, flush=True)
