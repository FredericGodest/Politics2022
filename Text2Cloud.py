"""
This module is creating .png files from text to wordcloud
"""


import os
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np


def TextToCloud(df: object, image_path: str, name: str, df_item: str):
    """
    This function is converting words to wordcloud png file.
    The png file is then saved.

    :param df: Pandas dataframe with all the data for the given item (see df_item).
    :param image_path: The path of the saved png file.
    :param name: The name of the candidate (basically the name of the directory).
    :param df_item: The name of the topic (it can either be "programme", "article" or "tweets".
    :return:
    """

    # Constants
    FONT_PATH = "./files/GillSans.ttc"
    EXCLURE_MOTS = ['d', 'du', 'de', 'la', 'des', 'le', 'et', 'est', 'une', 'en', 'que', 'aux', 'qui', 'ces', 'les',
                    'dans', 'sur', 'l', 'un', 'pour', 'par', 'il', 'ou', 'à', 'ce', 'a', 'sont', 'cas', 'plus', 'leur',
                    'se', 's', 'vous', 'au', 'c', 'aussi', 'toutes', 'autre', 'comme', "C'est"]

    # Generate a word cloud image
    img = Image.open(image_path)
    rgbimg = Image.new("RGBA", img.size)
    rgbimg.paste(img)
    mask = np.array(rgbimg)
    image_colors = ImageColorGenerator(mask)
    ratio = mask.shape[0] / mask.shape[1]

    # Generate Wordcloud
    width = 400
    wordcloud = WordCloud(mask=mask,
                          width=width, height=width*ratio,
                          random_state=42,
                          max_words=500,
                          font_path=FONT_PATH,
                          color_func=image_colors,
                          max_font_size=200,
                          stopwords=EXCLURE_MOTS,
                          relative_scaling=0.7,
                          background_color='white')

    # Wordcloud generation
    wordcloud.generate_from_frequencies(df[df_item])

    # Create coloring from image
    image_colors = ImageColorGenerator(mask)

    # fig creation
    plt.figure(figsize=(2, 1), facecolor='k')
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")

    # store to file
    temp_path = os.path.join("./files/", name, df_item +"_logo_cloud.png")
    plt.savefig(temp_path, bbox_inches='tight', dpi=500, pad_inches=0)