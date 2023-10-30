import pandas as pd
import numpy as np
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
from collections import Counter

# Define a list of custom Korean stopwords
custom_stopwords = ["것", "하는", "되는", "때", "있는", "대한", "할", "더", "일", "등", "대해", "없이", "수", "및", "하여", "점", "내", "조직", "개선", "모습", "위해", "많은", "진행", "환경", "많이", "부분", "가지"]

# Define a list of meaningless morphemes (POS tags to exclude)
meaningless_pos = ["Josa", "Punctuation", "Eomi", "Suffix", "Conjunction"]

# Define a function to read a CSV file and generate a word cloud
def generate_korean_wordcloud(csv_file, output_directory, mask_image_path):
    # Read the CSV file (make sure it contains a column with Korean text)
    data = pd.read_csv(csv_file)

    # Initialize the Korean morpheme analyzer (in this case, Okt)
    analyzer = Okt()

    # Tokenize the text data, filtering out custom stopwords and meaningless morphemes
    tokens = []
    for sentence in data['KoreanText']:
        for token, pos in analyzer.pos(sentence):
            if token not in custom_stopwords and pos not in meaningless_pos:
                tokens.append(token)

    text = ' '.join(tokens)
    
    # Specify the local font path for Nanum Gothic
    font_path = 'data/NanumSquareR.ttf'  # Replace with the actual path to the TTF font file

    # Load the mask image
    mask_image = np.array(Image.open(mask_image_path))

    # Generate the word cloud with the local Nanum Gothic font
    wordcloud = WordCloud(
        mask=mask_image,
        font_path=font_path,
        background_color='white',
        width=800,
        height=600,
        colormap='viridis',  # You can choose a different colormap
    ).generate(text)

    # Display the word cloud (optional)
    plt.figure(figsize=(8, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # Generate a timestamp for the output file name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Save the word cloud as a PNG file with a timestamp in the file name
    output_png = f"{output_directory}/wordcloud_{timestamp}.png"
    wordcloud.to_file(output_png)

# Usage
csv_file = 'data/조직문화_rawdata - 장점.csv'
output_directory = 'wordcloud/'  # Replace with the path to the directory where you want to save the file
mask_image_path = 'data/logo_mask.png'  # Replace with the path to your custom mask image
generate_korean_wordcloud(csv_file, output_directory, mask_image_path)