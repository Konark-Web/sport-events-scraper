import ast
import csv
import math
import re


def read_csv(filename: str) -> list:
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = []
        for row in csvreader:
            rows.append(row)
        return rows


def coord_dist(point_a: dict, point_b: dict, range_limit=500) -> bool:
    """
    Functions calculate distance between two coords
    :param point_a:  dictionary with lat, long  for start point
    :param point_b:  dictionary with lat, long  for destination point
    :param range_limit: limit range between points
    :return:  true if point_a from point_b in limit range

    points examples
    point1 = {
            'lat': 3.148729,
            'lon': 101.721831
            }

    point2 = {
            'lat': 3.149086,
            'lon': 101.713093
            }
    """
    R = 6378.137
    d_lat = point_b['lat'] * math.pi / 180 - point_a['lat'] * math.pi / 180
    d_lon = point_b['lon'] * math.pi / 180 - point_a['lon'] * math.pi / 180
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(
        point_a['lat'] * math.pi / 180) * math.cos(
        point_b['lat'] * math.pi / 180) * math.sin(d_lon / 2) * math.sin(
        d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    distance = d * 1000

    return distance < range_limit


def create_point(location: str) -> dict:
    """
    converts input string to dict, finds coords using re,
    :param: location example:
         location = {
             'link': 'https://www.google.com/maps/search/?api=1&query=23.5460566708204,57.9777873651197',
             'description': 'Kiev, Ukraine'
         }
    :return: point = {'lat': float, 'lon': float } or empty dict {} if no coordinates provided
    """

    str_to_dict = ast.literal_eval(location)
    coords = re.findall(r'[-]?[\d]+[.][\d]*', str_to_dict['link'])
    if len(coords) == 2:
        return {"lat": float(coords[0]), "lon": float(coords[1])}
    return {}


def unique(indexes):
    unique_list = []
    for x in indexes:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def find_unique_events(rows_1: list, rows_2: list) -> list:
    """
    :param rows_1: existing file data
    :param rows_2: file to clean data
    :return: list of unique row indexes to remove
    """
    results = []
    for i in rows_1[1:]:
        for j in rows_2[1:]:
            if i[10] == j[10]:  # if dates are equal, start comparing distance between events
                point_1 = create_point(i[3])
                point_2 = create_point(j[3])
                if point_1 and point_2:  # check if points are not empty
                    if coord_dist(point_1, point_2) is True:  # check if distance is less than 500
                        results.append(rows_2.index(j))
    return unique(results)


def remove_existing_events(rows: csv.DictReader, indexes: list) -> list:
    indexes.sort()
    return [i for j, i in enumerate(rows) if j not in indexes]


def write_cleaned_csv(filename: str, cleaned_rows: list) -> None:
    with open(f'{filename}', 'w+') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(cleaned_rows)


def create_cleaned_filename(filename: str) -> str:
    splited = filename.split('.')
    splited[-2] += '_cleaned_DR'
    return '.'.join(splited)


def match(existing_file: str, file_to_clean: str) -> list:
    file_1_rows = read_csv(existing_file)
    file_2_rows = read_csv(file_to_clean)
    indexes = find_unique_events(file_1_rows, file_2_rows)
    with open(file_to_clean, 'r') as f:
        reader = csv.DictReader(f)
        cleaned_rows = remove_existing_events(reader, indexes)
    cleaned_filename = create_cleaned_filename(file_to_clean)
    write_cleaned_csv(cleaned_filename, cleaned_rows)
    return cleaned_rows
