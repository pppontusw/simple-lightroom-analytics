from config import LR_CATALOG_FILE
from lightroom import LightroomDB

lightroom_db = LightroomDB(LR_CATALOG_FILE)
result = lightroom_db.get_all_picks()
print(result[0].keys())