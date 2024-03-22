# Simple lightroom catalog analysis

A couple of small scripts to read data from a lightroom classic catalog

`config.py` defines the relative location of the catalog, it's highly recommended that you use a copy of the catalog just in case something goes wrong

`python3 list_most_used.py` will by default list the most used lenses in the last 365 days

```
usage: list_most_used.py [-h] [--lookback LOOKBACK] [--property {lensName,cameraName,focalLength}]

List most used lenses

options:
  -h, --help            show this help message and exit
  --lookback LOOKBACK   Number of days to look back (default: 365)
  --property {lensName,cameraName,focalLength}
                        The property to group by (default: lensName)
```