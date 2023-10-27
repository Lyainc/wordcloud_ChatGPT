import pandas as pd
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime

# Define a function to read a CSV file and generate a word cloud
def generate_korean_wordcloud(csv_file, output_png):
    # Read the CSV file (make sure it contains a column with Korean text)
    data = pd.read_csv(csv_file)

    # Initialize the Korean morpheme analyzer (in this case, Okt)
    analyzer = Okt()
    
    stop_words = ["은", "는", "이", "가", "을", "를", "으로", "에서", "에게", "에서", "부터"]

    # Tokenize the text data, filter out stop words, and join the tokens into a single string
    tokens = []
    for sentence in data['KoreanText']:
        for token, pos in analyzer.pos(sentence):
            if token not in stop_words:
                tokens.append(token)

    text = ' '.join(tokens)
    
    # Specify the local font path for Nanum Gothic
    font_path = 'data/NanumSquareR.ttf'  # Replace with the actual path to the TTF font file

    # Generate the word cloud with the local Nanum Gothic font
    wordcloud = WordCloud(
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
generate_korean_wordcloud(csv_file, output_directory)