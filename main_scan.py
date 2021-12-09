from Text2Cloud import TextToCloud
from scraping_folders import FolderScanning, ExtractSTR
import json

def main(cloud: bool):
    d, candidats = FolderScanning()
    dict_all = {}

    for name in candidats:
        image_path, dict_list = ExtractSTR(d, name)
        dict_all[name] = dict_list

        if cloud:
            print(f"Création des wordcloud de {name}")
            for df_item in dict_list:
                TextToCloud(dict_list[df_item], image_path, name, df_item)

    with open('./files/data.json', 'w') as fp:
        json.dump(dict_all, fp, sort_keys=True, indent=4)

main(cloud=True)
