import os
import pandas as pd
import spacy
nlp = spacy.load("fr_core_news_sm")

def FolderScanning():
    root_main = "./files"
    d = {}
    root, files, dirs = os.walk(root_main, topdown=False)
    for directory in dirs[1]:
        path = os.path.join(root_main, directory)
        file_list = os.listdir(path)
        d[directory] = file_list

    candidats = dirs[1]

    return d, candidats

def ExtractSTR(d, name):
    files = d[name]
    root_main = "./files"
    stopwords = [".",
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
            path = os.path.join(root_main, name, file)
            f = open(path, "r", encoding="utf8")
            text = str(f.read())
            doc = nlp(text)
            text = " ".join([word.lemma_ for word in doc if not word.is_stop])

            for stop in stopwords:
                text = text.replace(stop, " ")

            text2list = []
            for word in text.split(" "):
                if not word.startswith("article_"):
                    if len(word) > 4:
                        word = word.replace(" ", "")
                        text2list.append(word.capitalize())

            text_dict[file] = text2list

        elif file == "logo.png":
            image_path = os.path.join(root_main, name, file)
        else:
            pass

    df_programme = pd.DataFrame(data={"mots": text_dict["programme.txt"]})
    df_programme["programme"] = 1
    df_programme = df_programme.groupby(by=["mots"]).sum()

    df_article = pd.DataFrame(data={"mots": text_dict["articles.txt"]})
    df_article["article"] = 1
    df_article = df_article.groupby(by=["mots"]).sum()

    df_merged = pd.concat([df_programme, df_article], axis=1, join='inner')
    df_merged["total"] = df_merged["programme"] + df_merged["article"]
    df_merged = df_merged.sort_values(by=["total"]).drop(columns=['programme', 'article'])

    dict_list = {
        "programme": df_programme.to_dict(),
        "article": df_article.to_dict(),
        "total": df_merged.to_dict()
    }

    return image_path, dict_list
