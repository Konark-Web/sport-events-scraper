from math import ceil


def get_first_last_name(athlete_full_name, reverse=False):
    athlete_first_name = ''
    athlete_last_name = ''
    athlete_name_len = len(athlete_full_name.split())
    if athlete_name_len:
        count = 0
        athlete_name_len_surname = ceil(athlete_name_len / 2)
        athlete_name_len = athlete_name_len - 1

        while count < athlete_name_len_surname:
            athlete_first_name += ' ' + athlete_full_name.split()[count]
            if (athlete_name_len_surname + count) <= athlete_name_len:
                athlete_last_name += ' ' + athlete_full_name.split()[
                    athlete_name_len_surname + count]

            count += 1

    if reverse:
        athlete_first_name, athlete_last_name = athlete_last_name, athlete_first_name

    return athlete_first_name.strip(), athlete_last_name.strip()
