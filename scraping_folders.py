"""
This module is looking and scrapping all the files of all the folders.
This module is also applying NLP with spacy.
"""

import os
import pandas as pd
import spacy
nlp = spacy.load("fr_core_news_sm") # French dictionnary set

def FolderScanning() -> object:
    """
    This function is scanning all the folders to extract file name and candidat names.

    :return d: dictionnary with files and candidates.
    :return candidats: list of candidats names
    """
    ROOT_MAIN = "./files"
    d = {}
    root, files, dirs = os.walk(ROOT_MAIN, topdown=False)
    for directory in dirs[1]:
        path = os.path.join(ROOT_MAIN, directory)
        file_list = os.listdir(path)
        d[directory] = file_list

    candidats = dirs[1]

    return d, candidats

def ExtractSTR(d: dict, name: str) -> object:
    """
    This function is extracting and classifing all the file texts in dictionnary of pandas data frame.

    :param d: dictionary of all the candidates and all the files
    :param name: name of the candidats
    :return image_path: path of the logo base file
    :return dict_list: dictionnary of pandas dataframe
    """
    files = d[name]
    ROOT_MAIN = "./files"
    STOPWORDS = [".",
                 ",",
                 ":",
                 '"',
                 ";",
                 "\n",
                 "(",
                 ")",
                 "[",
                 "]",
                 "'",
                 name,
                 "C'est"]
    text_dict = {
    }

    for file in files:
        if ".txt" in file:
            path = os.path.join(ROOT_MAIN, name, file)
            f = open(path, "r", encoding="utf8") # UTF8 is mandatory for accent.
            text = str(f.read())
            doc = nlp(text) #NLP
            text = " ".join([word.lemma_ for word in doc if not word.is_stop]) #Lemmatization NLP

            for stop in STOPWORDS:
                text = text.replace(stop, " ")

            text2list = []
            for word in text.split(" "):
                if not word.startswith("article_"):
                    if len(word) > 4:
                        word = word.replace(" ", "")
                        text2list.append(word.capitalize())

            text_dict[file] = text2list

        elif file == "logo.png":
            image_path = os.path.join(ROOT_MAIN, name, file)
        else:
            pass

    # Creation and concatenation of all the dataframes
    df_programme = pd.DataFrame(data={"mots": text_dict["programme.txt"]})
    df_programme["programme"] = 1
    df_programme = df_programme.groupby(by=["mots"]).sum()

    df_article = pd.DataFrame(data={"mots": text_dict["articles.txt"]})
    df_article["article"] = 1
    df_article = df_article.groupby(by=["mots"]).sum()

    df_tweets = pd.DataFrame(data={"mots": text_dict["twitter.txt"]})
    df_tweets["twitter"] = 1
    df_tweets = df_tweets.groupby(by=["mots"]).sum()

    df_merged = pd.concat([df_programme, df_article, df_tweets], axis=1, join='inner')
    df_merged["total"] = df_merged["programme"] + df_merged["article"] + df_merged["twitter"]
    df_merged = df_merged.sort_values(by=["total"]).drop(columns=['programme', 'article', 'twitter'])

    dict_list = {
        "programme": df_programme.to_dict(),
        "article": df_article.to_dict(),
        "twitter": df_tweets.to_dict(),
        "total": df_merged.to_dict()
    }

    return image_path, dict_list
