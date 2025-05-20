# FAQ Chatbot 
This is a FAQ chatbot implementation with TF-IDF and Cosine Similarity. TF-IDF is used to vectorize and cosine similarity is used to get the most similar question from a FAQ dictionary. If a question is provided to the ```get_faq_answer()``` function as
an argument then it will match from the stored frequently asked questions dictionary and fetch the answer from there.

## Code Description
### FAQ dataset
FAQ answering training will be done from the following dictionary of Frequently Asked Questions and Answers
```python
faq_data = {
    "What is your return policy?": "We accept returns within 30 days of delivery. Items must be unused and in their original packaging. Some items may be non-returnable or subject to a restocking fee.",

    "How long will it take to receive my order?": "Standard delivery usually takes 3–7 business days. Expedited and next-day delivery options are also available at checkout.",

    "Do you offer free shipping?": "Yes, we offer free standard shipping on orders over $50. Shipping charges apply for orders below that threshold or for expedited options.",

    "Can I change my shipping address after placing an order?": "If your order hasn’t been shipped yet, you can request a shipping address change by contacting our support team immediately.",

    "How do I cancel my order?": "You can cancel an order within one hour of placing it by going to your order history and clicking 'Cancel'. For shipped orders, you'll need to initiate a return.",

    "How do I track my order?": "Once your order is shipped, you'll receive a tracking link via email. You can also track it under 'My Orders' in your account.",

    "What payment methods do you accept?": "We accept Visa, MasterCard, American Express, PayPal, Apple Pay, Google Pay, and store gift cards.",

    "Is it safe to shop on your site?": "Yes, we use SSL encryption and PCI-compliant payment systems to ensure your data and transactions are secure.",

    "Can I place an order without creating an account?": "Yes, we offer guest checkout. However, creating an account lets you track orders, manage returns, and receive special offers.",

    "How do I apply a discount code?": "You can enter your discount or promo code during checkout in the 'Apply Promo Code' section before payment.",

    "Do you offer gift wrapping?": "Yes, gift wrapping is available for most items at checkout. You can also include a custom message.",

    "Do you ship internationally?": "Currently, we ship to select countries. International shipping fees and delivery times vary by location.",

    "What should I do if I received the wrong item?": "We're sorry for the mix-up! Please contact our support team with your order number, and we'll arrange a replacement or refund.",

    "How do I return an item?": "Go to 'My Orders' in your account, select the item, and click 'Return Item'. Follow the instructions to print a return label.",

    "When will I receive my refund?": "Refunds are typically processed within 5–7 business days after we receive your return.",

    "Are your products under warranty?": "Most of our products are covered by a 6- or 12-month warranty. Specific warranty information is available on each product page.",

    "Do you have a loyalty program?": "Yes! Sign up for our rewards program to earn points on every purchase and redeem them for discounts or free items.",

    "How do I update my account information?": "Log in and go to 'Account Settings' to update your email, password, shipping address, and payment methods.",

    "Do you offer bulk or wholesale pricing?": "Yes, we offer special pricing for bulk orders. Please contact our sales team at wholesale@example.com for a custom quote.",

    "Can I preorder items that are out of stock?": "Some popular items are available for preorder. The estimated shipping date will be listed on the product page.",

    "Do you offer delivery?": "Yes, we provide delivery service for all orders above 500 BDT.",

    "Where are you located?": "We are located at 123 Main Road, Dhaka.",

    "Can I return a product?": "You can return a product within 7 days of delivery."
}
```
Only the questions are seperated for further processing as we will try to find similarity with the questions
```python
questions = [i for i in faq_data.keys()]
```
#### Preprocessing Questions
Both the training and user asked questions will be preprocessed using the ```preprocess()``` function by doing the following tasks:
* Lowercasing
* Punctuation Removal
* Stopwords Removal
* Tokenization
* Lemmatization
```python
def preprocess(data):
  data = [question.lower() for question in data]
  # Remove punctuations
  removed_punct = [re.sub(r'[^\w\s]', '', text) for text in data]

  # Stopwords removal
  nltk.download('stopwords')
  from nltk.corpus import stopwords
  stop_words = set(stopwords.words('english'))
  removed_stopwords = [' '.join([word for word in text.split() if word not in stop_words]) for text in removed_punct]

  # Tokenization
  nltk.download('punkt_tab')
  tokenized_corpus = [word_tokenize(text) for text in removed_stopwords]

  # Lemmatization
  nltk.download('wordnet')
  lemmatizer = WordNetLemmatizer()
  lemmatized_corpus = [[lemmatizer.lemmatize(word) for word in doc] for doc in tokenized_corpus]

  return lemmatized_corpus

preprocessed_questions = preprocess(questions)
```
### Fitting the questions into the TF-IDF Vectorizer
```python
vectorizer = TfidfVectorizer()
tfidf_matrix_stored = vectorizer.fit_transform([' '.join(doc) for doc in preprocessed_questions])
```

### Retriving Answer
Through the ```get_faq_answer(question)``` function a question from the user is taken and preprocessed. After that the previous vectorizer is used to transform the question and then use cosine similarity to get the similarity matrix. The 2D matrix is flattened
to make simpler and the maximum similarity score is taken. That score is then used to get the answer. The threshold here to take a match is 0.5, which will allow to even match single word quesiton like: "policy?".
```python
def get_faq_answer(question):
  user_question = [question]

  preprocessed_user_question = preprocess(user_question)
  # Uses the previous vectorizer to transform user question
  tfidf_matrix_user_question = vectorizer.transform([' '.join(doc) for doc in preprocessed_user_question])
  # Calculate Cosine Similarity
  similarity_scores = cosine_similarity(tfidf_matrix_user_question, tfidf_matrix_stored)

  scores = similarity_scores.flatten()
  max_score = np.max(scores)
  best_match_index = np.argmax(scores)
  best_question = questions[best_match_index]
  best_answer = faq_data[best_question]

  if max_score >= 0.5: 
    return best_answer
  else:
    return "Sorry, I couldn’t find a suitable answer to your question."

answer = get_faq_answer("creating an account?")
print("Output: ",answer)
```
