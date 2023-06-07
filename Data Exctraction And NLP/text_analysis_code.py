import os
import json
import nltk
from textblob import TextBlob

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

# Define file path and read text files
data_folder = os.path.join(os.getcwd(), 'articles')
files = os.listdir(data_folder)
data = []

for file in files:
    path = os.path.join(data_folder, file)
    with open(path, encoding='utf-8') as f:
        text = f.read()

    # Text cleaning and preprocessing
    text = text.lower()  # Convert text to lowercase
    text = ''.join(c for c in text if c.isalnum() or c.isspace())  # Remove all non-alphanumeric characters except whitespaces
    words = nltk.word_tokenize(text)  # Tokenize text into words
    stop_words = set(nltk.corpus.stopwords.words('english'))  # Get stop words
    words = [w for w in words if not w in stop_words]  # Remove stop words
    words = [nltk.stem.WordNetLemmatizer().lemmatize(w) for w in words]  # Lemmatize words
    sentences = nltk.sent_tokenize(text)  # Tokenize text into sentences
    sentence_lengths = [len(nltk.word_tokenize(s)) for s in sentences]  # Calculate sentence lengths

    # Calculate variables
    positive_score = 0
    negative_score = 0
    polarity_score = 0
    subjectivity_score = 0
    complex_word_count = 0
    syllable_count = 0
    word_count = len(words)
    personal_pronouns_count = 0
    if word_count > 0:
        avg_word_length = sum(len(word) for word in words) / word_count
    else:
        avg_word_length = 0
    for word in words:
        blob = TextBlob(word)
        if blob.sentiment.polarity > 0:
            positive_score += 1
        elif blob.sentiment.polarity < 0:
            negative_score += 1
        polarity_score += blob.sentiment.polarity
        subjectivity_score += blob.sentiment.subjectivity
        if blob.tags[0][1] in ['JJ', 'VBG', 'VBN', 'RB']:
            complex_word_count += 1

    personal_pronouns_count = sum(1 for word in words if word.lower() in ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours'])
    if len(sentence_lengths) > 0 :
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
    else :
        avg_sentence_length = 0
    if word_count > 0 :
        percentage_complex_words = complex_word_count / word_count * 100
    else :
        percentage_complex_words = 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Store results in dictionary
    if len(sentences) > 0:
        result = {
            'Filename': file,
            'Positive Score': positive_score,
            'Negative Score': negative_score,
            'Polarity Score': polarity_score,
            'Subjectivity Score': subjectivity_score,
            'Avg Sentence Length': avg_sentence_length,
            'Percentage of Complex Words': percentage_complex_words,
            'FOG Index': fog_index,
            'Avg Number of Words per Sentence': word_count/len(sentences),
            'Complex Word Count': complex_word_count,
            'Word Count': word_count,
            'Syllable per Word': syllable_count/word_count,
            'Personal Pronouns': personal_pronouns_count,
            'Avg Word Length': avg_word_length
        }

        # Append result to data list
        data.append(result)
    with open('Out_put.json', 'w') as json_file:
        json.dump(data, json_file)

