import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()

def tokenize(text):
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower()).strip()
    
    # Todo: tokenize text
    words = word_tokenize(text)
    
    # Todo: lemmatize and remove stop words
    tokens = [w for w in words if w not in stop_words]
    lemmed = [lemmatizer.lemmatize(w) for w in tokens]
    return lemmed