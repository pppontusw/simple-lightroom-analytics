from config import LR_CATALOG_FILE
from lightroom import LightroomDB
import pprint

lightroom_db = LightroomDB(LR_CATALOG_FILE)
result = lightroom_db.get_all_images()
cameras = []
lenses = []
for image in result:
    if image["cameraName"] not in cameras:
        cameras.append(image["cameraName"])
    if image["lensName"] not in lenses:
        lenses.append(image["lensName"])
print("Keys")
pprint.pprint(result[0].keys(), indent=4)
print("Cameras")
pprint.pprint(cameras, indent=4)
print("Lenses")
pprint.pprint(lenses, indent=4)
