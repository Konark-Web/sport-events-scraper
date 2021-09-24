import csv

from match_events.match import match

if __name__ == '__main__':
    tf_file = "../trailforks_09032021.csv"
    ws_file = "../webscorer_02032021.csv"
    print(match(existing_file=ws_file, file_to_clean=tf_file))
    # with open(tf_file, 'r') as f:
    #     reader = (csv.DictReader(f))
    #     for i in list(reader):
    #         print(i)

