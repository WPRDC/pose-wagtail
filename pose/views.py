import requests
from django.http import JsonResponse
from rest_framework.request import Request

from pose.settings.base import CATALOG_HOST


# Create your views here.
def site_geojson(request: Request):
    geojson = {"type": "FeatureCollection", "features": []}

    rows = 500
    start = 0

    while True:

        r = requests.get(
            f"{CATALOG_HOST}/api/3/action/package_search",
            params={
                "fq": "type:site",
                "rows": rows,
                "start": start,
            },
        )
        results = r.json()["result"]
        records = results["results"]

        if not records:
            break

        start += rows

        for row in records:
            try:
                geojson["features"].append(
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [row["longitude"], row["latitude"]],
                        },
                        "properties": {
                            "id": row["id"],
                            "name": row["name"],
                            "title": row["title"],
                            "url": row["url"],
                            "catalog_url": f"{CATALOG_HOST}/site/${row['name']}",
                            "state": row["state"],
                            "description": row["notes"],
                            "num_datasets": row["num_datasets"],
                            "num_organizations": row["num_organizations"],
                            "num_resources": row["num_resources"],
                        },
                    }
                )
            except KeyError:
                # todo: do something with these?
                print(row)

    return JsonResponse(geojson)
