import json

#show all regions in tanzania
def region():
    regions=[(region['Region'],region['Region']) for region in
    			json.load(open('regions.json'))]
    return regions
