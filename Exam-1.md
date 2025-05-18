# AI Chatbot Text Preprocessing Pipeline

This project demonstrates a text preprocessing pipeline for building an AI chatbot for customer service. It outlines key preprocessing steps to clean and normalize text input from users.

## 📆 Task Goal

The goal is to clean noisy input (e.g., different cases, punctuation, repetitive characters, abbreviations, etc.) before fitting the data into a model. While emotional markers like emojis or punctuation may be valuable in tasks like sentiment analysis, for a task-based chatbot system, they are often unnecessary. Therefore, this pipeline focuses on cleaning the data while preserving key semantic information.

## ✅ Preprocessing Steps Performed:

### 1. **Lowercasing**

Using list comprehension to lowercase all data using Python's built-in `.lower()` method.

```python
corpus = [text.lower() for text in corpus]
```

### 2. **Expanding Contractions**

Transforms contracted forms like `can't`, `don't`, etc. into their full forms (`cannot`, `do not`) using the `contractions` library.

```python
corpus = [contractions.fix(text) for text in corpus]
```

### 3. **Expanding Abbreviations & Removing Emojis**

A custom abbreviation map is created to expand common slang terms (e.g., `u` to `you`, `plz` to `please`). Emojis are also removed by extracting clean word tokens using regex (`\b\w+\b`).

```python
abbreviation_map = {
    'u': 'you',
    'plz': 'please',
    'whr': 'where',
    'af': 'as fuck'
}

def expand_abbreviations(text):
    words = re.findall(r'\b\w+\b', text)
    expanded_words = [abbreviation_map.get(word, word) for word in words]
    return " ".join(expanded_words)

corpus = [expand_abbreviations(text) for text in corpus]
```

### 4. **Removing Punctuation**

Removes punctuation using Python's `string.punctuation` and the `str.translate()` function.

```python
corpus = [text.translate(str.maketrans('', '', string.punctuation)) for text in corpus]
```

### 5. **Correcting Spelling**

Uses the `TextBlob` library to correct misspelled words in the corpus.

```python
from textblob import TextBlob
corpus = [str(TextBlob(text).correct()) for text in corpus]
```

### 6. **Tokenization**

Uses NLTK's `word_tokenize()` function to tokenize the cleaned text into individual words.

```python
from nltk.tokenize import word_tokenize
tokenized_corpus = [word_tokenize(text) for text in corpus]
```

### 7. **Removing Stopwords**

Downloads English stopwords from NLTK and filters them out of the tokenized text.

```python
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
filtered_corpus = [[word for word in doc if word not in stop_words] for doc in tokenized_corpus]
```

### 8. **Lemmatization**

Uses `WordNetLemmatizer` to transform words into their base dictionary form. Stemming is intentionally not used as lemmatization is generally more accurate.

```python
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmatized_corpus = [[lemmatizer.lemmatize(word) for word in doc] for doc in filtered_corpus]
```

### 9. **Preserving Emotional Intensity**
To preserve emotional intensity in the dataset we can keep the emojis and translate them into text so that the model can categorize different emotion.
We can do this before expanding the abbreviations so that they are translated properly.
```python
import emoji
corpus = [
    'Hey, can u plz tell me where’s my order?',

    'i didn’t receive my parcel yet!!!!',

    'Whr’s my ordr 😡😡',

    'delivery late af... i want refund now'
]
emoji_corpus = [emoji.demojize(doc, delimiters=(" <", "> ")) for doc in corpus]
print(emoji_corpus)
```
We can also add tags to repetative punctuations like !!! -> <exclaim> and so on and keep the delimeters <> intact in the dataset
```
def tag_emotional_punctuation(text):
    text = re.sub(r'!{2,}', ' <exclaim> ', text)       # 2+ exclamation marks
    text = re.sub(r'\?{2,}', ' <question> ', text)     # 2+ question marks
    text = re.sub(r'\.{2,}', ' <pause> ', text)        # 2+ periods
    return text
corpus = [tag_emotional_punctuation(text) for text in emoji_corpus]

# emoji and punctuation tag delimeters (<>) are kept while removing punctuations.
preserve_punct = "<>"
remove_punct = ''.join([p for p in string.punctuation if p not in preserve_punct])
corpus = [text.translate(str.maketrans('', '', remove_punct)) for text in corpus]

print(corpus)
```
## 📊 Libraries Used

* `nltk`
* `re`
* `contractions`
* `textblob`
* `string`

---

