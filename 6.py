input = """132, 308
325, 300
310, 231
177, 248
111, 304
65, 135
227, 116
60, 80
182, 353
60, 42
314, 164
142, 50
90, 266
234, 219
68, 121
168, 153
258, 50
354, 92
126, 154
303, 324
90, 47
236, 316
316, 217
180, 110
70, 300
256, 221
56, 256
235, 190
56, 197
168, 145
250, 117
107, 77
259, 156
188, 301
183, 76
92, 224
41, 113
343, 90
162, 176
186, 77
312, 134
89, 98
191, 313
68, 225
85, 273
96, 161
260, 93
343, 153
247, 327
151, 197"""

test_input = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

MAX_DIMENSION = 0

# assign IDs
coordinates_by_id = {}
id_count = 0
for i in input.split("\n"):
    coords = i.split(", ")
    new_id = (chr((id_count / 26) + 97) + chr((id_count % 26) + 97)).upper()
    coordinates_by_id[new_id] = {"x": int(coords[0]), "y": int(coords[1])}
    id_count += 1
    if int(coords[0]) > MAX_DIMENSION:
        MAX_DIMENSION = int(coords[0])
    elif int(coords[1]) > MAX_DIMENSION:
        MAX_DIMENSION = int(coords[1])

import sys

MAX_DISTANCE_TO_ALL_POINTS = 10000

# assign every space and count
spaces_within_max_distance = 0
area_per_point_id = {}
points_that_touch_infinity = set()
for y in range(0, MAX_DIMENSION + 1):
    for x in range(0, MAX_DIMENSION + 1):

        # search for nearest upper point
        min_distance = sys.maxint

        # calculate all distances to all major points
        total_distance = 0
        distance_by_point_id = {}
        for point_id in coordinates_by_id:
            coords = coordinates_by_id[point_id]
            point_x = coords["x"]
            point_y = coords["y"]
            distance = abs(x - point_x) + abs(y - point_y)
            if distance < min_distance:
                distance_by_point_id[point_id] = distance
            total_distance += distance

        if total_distance < MAX_DISTANCE_TO_ALL_POINTS:
            spaces_within_max_distance += 1

        # get min distance
        min_distance = min(distance_by_point_id.itervalues())

        # find id to point that is closest
        min_distance_point_id = None
        found = 0
        for point, distance in distance_by_point_id.iteritems():
            if distance == min_distance:
                min_distance_point_id = point
                found += 1

        if found > 1:
            # spaces that are equally close to 2 or more points are not owned by anyone
            continue

        if min_distance_point_id not in area_per_point_id:
            area_per_point_id[min_distance_point_id] = 0
        area_per_point_id[min_distance_point_id] = area_per_point_id[min_distance_point_id] + 1

        if x == 0 or y == 0 or x == MAX_DIMENSION or y == MAX_DIMENSION:
            points_that_touch_infinity.add(min_distance_point_id)

for i in points_that_touch_infinity:
    del area_per_point_id[i]

max_area = 0
for i in area_per_point_id:
    if area_per_point_id[i] > max_area:
        max_area = area_per_point_id[i]

print ("part 1: " + str(max_area))
print ("part 2: " + str(spaces_within_max_distance))