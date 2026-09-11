import subprocess, sys, os, json, shutil, re
SKILL = "C:/Users/wangy/AppData/Local/Programs/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/buddy-image-processing/scripts/buddy-image-processing.py"
PY = "C:/Users/wangy/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
TOKEN = sys.argv[1]
IMG, OUT = "assets/images", "_raw/erased"

JOBS = [
 ("spinning-rod-04.webp", "The white cursive 'Cross' lettering on the two black rod blanks is a printed watermark overlay, not part of the rod paint. Erase the lettering completely and reconstruct the clean dark carbon blank surface underneath. Keep the rods, cork handles and background unchanged."),
 ("carp-rod-06.webp", "The golden cursive 'PROGRESS' lettering on the black rod is a printed watermark overlay, not part of the rod paint. Erase it completely and reconstruct the clean black carbon blank surface. Keep the rod, guides, blue frame and layout unchanged."),
 ("saltwater-rod-01.webp", "The golden cursive 'MEASPLUS BOAT' lettering on the black rod is a printed watermark overlay, not part of the rod paint. Erase it completely and reconstruct the clean black blank surface. Keep the rod, guides and dark background unchanged."),
 ("saltwater-rod-05.webp", "The white 'MORE CATCH' lettering on the orange rod is a printed watermark overlay, not part of the rod paint. Erase it and reconstruct the clean orange blank surface. Keep the rod, guides, black frame and caption unchanged."),
 ("rock-surf-rod-03.webp", "Remove the 'REMANSO' printed text on the green rod (it is a watermark overlay, not paint - reconstruct the clean green blank surface), and remove the person wearing sunglasses in the top-right photo. Keep the rods and layout otherwise unchanged."),
]

for name, prompt in JOBS:
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
        shutil.copyfile(data["result_files"][0]["path"], os.path.join(OUT, name.replace(".webp", ".png")))
        print("OK", name, flush=True)
    except Exception as e:
        print("FAIL", name, repr(e), flush=True)
print("PASS3 DONE", flush=True)
