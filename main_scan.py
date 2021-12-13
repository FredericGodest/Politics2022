"""
This is the main module that drives all the others modules.
"""

from Text2Cloud import TextToCloud
from scraping_folders import FolderScanning, ExtractSTR
import json
from twitter_data import *

def main(cloud: bool, twitter: bool):
    """

    :param cloud: True = Wordcloud creation (This operation take some time)
    :param twitter: True = Scrapping and updating all the tweet of the candidat.
    This is not always necessary since the result is saved in txt file each time.
    :return:
    """
    d, candidats = FolderScanning()
    dict_all = {}

    for name in candidats:
        if twitter:
            print(f"mise à jour des tweets de {name}")
            twitter_main(name)

        image_path, dict_list = ExtractSTR(d, name)
        dict_all[name] = dict_list

        if cloud:
            print(f"Création des wordcloud de {name}")
            for df_item in dict_list:
                TextToCloud(dict_list[df_item], image_path, name, df_item)

    with open('./files/data.json', 'w') as fp:
        json.dump(dict_all, fp, sort_keys=True, indent=4)

main(cloud=True, twitter=True)
