import csv
import sqlite3

from config import LR_CATALOG_FILE

class LightroomDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def execute_query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_column_names(self):
        return [description[0] for description in self.cur.description]

    def get_results_as_dicts(self):
        column_names = self.get_column_names()
        result = []
        rows = self.cur.fetchall()
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                row_dict[column_names[i]] = value
            result.append(row_dict)
        return result

    def write_results_to_csv(self, file_path, fieldnames, data):
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow({field: item[field] for field in fieldnames})

    def get_all_picks(self):
        """
        Get all images marked as picks in the Lightroom catalog
        and return them as a list of dictionaries.
        """
        
        query = """
            SELECT *,
            AgInternedExifLens.value as lensName,
            AgInternedExifCameraModel.value as cameraName
            FROM Adobe_images
            JOIN AgHarvestedExifMetadata ON Adobe_images.id_local = AgHarvestedExifMetadata.image
            JOIN AgInternedExifLens ON AgHarvestedExifMetadata.lensRef = AgInternedExifLens.id_local
            JOIN AgInternedExifCameraModel ON AgHarvestedExifMetadata.cameraModelRef = AgInternedExifCameraModel.id_local
            WHERE Adobe_images.pick = 1
        """
        self.cur.execute(query)
        result = self.get_results_as_dicts()

        return result

def main():
    lightroom_db = LightroomDB(LR_CATALOG_FILE)
    result = lightroom_db.get_all_picks()

    for item in result:
        print(
            item["captureTime"],
            item["lensName"],
            item["cameraName"],
            item["focalLength"],
            item["aperture"],
        )

if __name__ == "__main__":
    main()