import os

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

# OUT_DIR = os.path.join(ROOT_DIR, "results")
OUT_DIR = "results"
if not os.path.exists(OUT_DIR):
    print(f"Creating data output directory: {OUT_DIR}")
    os.mkdir(OUT_DIR)

APK_DIR = os.path.join("resources", "apks")
if not os.path.exists(APK_DIR):
    print(f"Creating apk directory: {APK_DIR}")
    os.mkdir(APK_DIR)

CSV_PATH = os.path.join(OUT_DIR, "results.csv")

# get serial number by $>adb devices
PHONE_ID = "LMK420TSUKR8PVTG7P"
TABLET_ID = "R52RA0C2MFF"
