import re
import pandas as pd


def path_join(path1, path2):
    """ Une duas partes de um path """
    return "/".join([path1, path2])


def get_date_from_names(names_list, sep="_", occ=-1):
    """ Given a list with filenames, returns the dates contained within each filename
    """
    result_list = []
    for item in names_list:
        if sep == "_":
            match = re.search(r"\d{4}_\d{2}_\d{2}", item.split("/")[occ])
        elif sep == "-":
            match = re.search(r"\d{4}-\d{2}-\d{2}", item.split("/")[occ])
        elif sep == "/":
            match = re.search(r"\d{4}/\d{2}/\d{2}", item)
        result_list.append(str(match.group()))

    if sep == "_":
        return pd.to_datetime(result_list, format="%Y_%m_%d")
    if sep == "-":
        return pd.to_datetime(result_list, format="%Y-%m-%d")
    if sep == "/":
        return pd.to_datetime(result_list, format="%Y/%m/%d")

    raise "Date format not supported"
