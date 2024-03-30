# Simple lightroom catalog analysis

A couple of small scripts to read data from a lightroom classic catalog

`config.py` defines the relative location of the catalog, it's highly recommended that you use a copy of the catalog just in case something goes wrong

`python3 list_most_used.py` will by default list the most used lenses in the last 365 days

```bash
usage: list_most_used.py [-h] [--lookback LOOKBACK] [--property {lensName,cameraName,focalLength,aperture,shutterSpeed}]
                         [--catalog-path CATALOG_PATH] [--picks-only]

List most used lenses

options:
  -h, --help            show this help message and exit
  --lookback LOOKBACK   Number of days to look back (default: 365)
  --property {lensName,cameraName,focalLength,aperture,shutterSpeed}
                        The property to group by (default: lensName)
  --catalog-path CATALOG_PATH
                        The path to the Lightroom catalog file (default: catalog-v13.lrcat)
  --picks-only          Count only picks (flagged)
```
