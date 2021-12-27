# -*- coding: utf-8 -*-
"""SpamClassifier_using_bert_embedding.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jRxrTHPdb_hG1wCvYv0AVfsKrT5nCIhW
"""

!pip install tensorflow_text
import tensorflow_text as text
import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd

df = pd.read_csv('SMSSpamCollection',sep= '\t',names=['label','message'])
df.head()

df.groupby('label').describe()

df['spam']= df['label'].apply(lambda x: 1 if x =='spam' else 0)
df.head()

"""## Split it into training and test data set"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df['message'],df['spam'], stratify=df['spam'])

X_train.head()

"""## Now lets import BERT model and get embeding vectors for few sample statements"""

bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4", trainable=True)
def get_sentence_embeding(sentences):
    preprocessed_text = bert_preprocess(sentences)
    return bert_encoder(preprocessed_text)['pooled_output']

get_sentence_embeding([
    "500$ discount. hurry up", 
    "Bhavin, are you up for a volleybal game tomorrow?"]
)

"""### Build Model"""

# Bert layers
text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
preprocessed_text = bert_preprocess(text_input)
outputs = bert_encoder(preprocessed_text)

# Neural network layers
l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])
l = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(l)

# Use inputs and outputs to construct a final model
model = tf.keras.Model(inputs=[text_input], outputs = [l])

model.summary()

len(X_train)

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

"""### Train the model

"""

history = model.fit(X_train, y_train, epochs=5,validation_split=0.1)

test_preds = model.evaluate(X_test, y_test)

import pickle
pickle.dump(model, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))

"""So, I created model using bert embedding """




