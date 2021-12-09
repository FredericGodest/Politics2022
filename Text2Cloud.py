import os
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np


def TextToCloud(df, image_path, name, df_item):
    font_path = "./files/GillSans.ttc"
    exclure_mots = ['d', 'du', 'de', 'la', 'des', 'le', 'et', 'est', 'une', 'en', 'que', 'aux', 'qui', 'ces', 'les',
                    'dans', 'sur', 'l', 'un', 'pour', 'par', 'il', 'ou', 'à', 'ce', 'a', 'sont', 'cas', 'plus', 'leur',
                    'se', 's', 'vous', 'au', 'c', 'aussi', 'toutes', 'autre', 'comme', "C'est"]

    data = df

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
                          font_path=font_path,
                          color_func=image_colors,
                          max_font_size=200,
                          stopwords=exclure_mots,
                          relative_scaling=0.7,
                          background_color='white')

    wordcloud.generate_from_frequencies(data[df_item])

    # create coloring from image
    image_colors = ImageColorGenerator(mask)

    # fig creation
    plt.figure(figsize=(2, 1), facecolor='k')
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")

    # store to file
    temp_path = os.path.join("./files/", name, df_item +"_logo_cloud.png")
    plt.savefig(temp_path, bbox_inches='tight', dpi=500, pad_inches=0)