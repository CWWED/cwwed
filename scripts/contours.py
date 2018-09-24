import math
from datetime import datetime
import xarray
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import geojsoncontour


# make these values less arbitrary by analyzing the input data density and spatial coverage
GRID_SIZE = 1000
MAX_CIRCUM_RADIUS = .015  # ~ 1 mile


def datetime64_to_datetime(dt64):
    unix_epoch = np.datetime64(0, 's')
    one_second = np.timedelta64(1, 's')
    seconds_since_epoch = (dt64 - unix_epoch) / one_second
    return datetime.utcfromtimestamp(seconds_since_epoch)


def circum_radius(pa, pb, pc):
    """
    returns circum-circle radius of triangle
    https://sgillies.net/2012/10/13/the-fading-shape-of-alpha.html
    https://en.wikipedia.org/wiki/Circumscribed_circle#/media/File:Circumcenter_Construction.svg
    """
    # lengths of sides of triangle
    a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
    b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
    c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)

    # semiperimeter of triangle
    s = (a + b + c)/2.0

    # area of triangle by Heron's formula
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))

    return a*b*c/(4.0*area)


def build_geojson_contours(water_depths, file_name):

    z = water_depths
    x = z.mesh2d_face_x
    y = z.mesh2d_face_y

    # convert to numpy arrays
    z = z.values
    x = x.values
    y = y.values

    # build grid constraints
    xi = np.linspace(np.floor(x.min()), np.ceil(x.max()), GRID_SIZE)
    yi = np.linspace(np.floor(y.min()), np.ceil(y.max()), GRID_SIZE)

    # build delaunay triangles
    triang = tri.Triangulation(x, y)

    # build a list of the triangle coordinates
    tri_coords = []
    for i in range(len(triang.triangles)):
        tri_coords.append(tuple(zip(x[triang.triangles[i]], y[triang.triangles[i]])))

    # filter out large triangles
    large_triangles = [i for i, t in enumerate(tri_coords) if circum_radius(*t) > MAX_CIRCUM_RADIUS]
    mask = [i in large_triangles for i, _ in enumerate(triang.triangles)]
    triang.set_mask(mask)

    # interpolate values from triangle data and build a mesh of data
    interpolator = tri.LinearTriInterpolator(triang, z)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)

    """
    # debug - save the triangulation as geojson
    import geojson
    from geojson import MultiPolygon, Polygon
    # TODO - factor in masked triangles
    polygons = [Polygon(coords + (coords[0],)) for coords in tri_coords]  # append the first coord to complete the polygon
    geojson.dump(MultiPolygon([polygons]), open('/tmp/geo.json', 'w'))
    """

    contourf = plt.contourf(xi, yi, zi, cmap=plt.cm.jet)

    # convert matplotlib contourf to geojson
    geojsoncontour.contourf_to_geojson(
        contourf=contourf,
        min_angle_deg=3.0,
        ndigits=5,
        stroke_width=2,
        fill_opacity=0.5,
        geojson_filepath='/tmp/{}.json'.format(file_name),
    )


# open the dataset for reading
dataset = xarray.open_dataset('/media/bucket/cwwed/THREDDS/PSA_demo/Sandy_DBay/DBay-run_map.nc')

for depths in dataset['mesh2d_waterdepth'][::50]:

    # convert to datetime
    dt = datetime64_to_datetime(depths.time)

    # build geojson contours
    build_geojson_contours(depths, file_name=dt.isoformat())