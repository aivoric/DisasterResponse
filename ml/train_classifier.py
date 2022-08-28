import pickle
import re
import nltk
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score,make_scorer
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from xgboost import XGBClassifier
from tabulate import tabulate

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

stop_words = stopwords.words("english")

class MLPipeline:
    def __init__(self, debug: bool = False):
        self.engine = create_engine('sqlite:///data/DisasterResponse.db')
        self.pipeline = Pipeline([
                ('vect', CountVectorizer(tokenizer=MLPipeline.tokenize)),
                ('tfidf', TfidfTransformer()),
                ('clf', MultiOutputClassifier(XGBClassifier()))
            ])
        self.debug = debug

    def load_data(self):
        df = pd.read_sql_table(table_name="disaster_messages", con=self.engine)
        if self.debug:
            df = df.head(100)
        Y = df.drop(columns=['message', 'original', 'genre', 'id'])
        X = df['message']
        self.column_names = Y.columns
        self.xtrain, self.xtest, self.ytrain, self.ytest = train_test_split(X, Y, train_size=0.7, random_state=12)

    def train_no_cv(self):
        self.pipeline.fit(self.xtrain, self.ytrain)
    
    def train_cv(self):
        parameters = {
            'clf__estimator__learning_rate': [0.01, 0.1, 0.3],
            'clf__estimator__n_estimators': [100,150,200,250,300,350,400],
        }
        cv = RandomizedSearchCV(estimator=self.pipeline,
                                param_distributions=parameters,
                                n_iter=10,
                                n_jobs=-1,
                                cv=5,
                                verbose=100,
                                scoring="f1",
                                random_state=88
                            )
        cv.fit(self.xtrain, self.ytrain)

    @staticmethod
    def tokenize(text) -> list:
        text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower()).strip()
        words = word_tokenize(text)
        tokens = [w for w in words if w not in stop_words]
        lemmed = [WordNetLemmatizer().lemmatize(w) for w in tokens]
        return lemmed

    @staticmethod
    def get_score(ytest, ypred, column_names) -> pd.DataFrame():
        results = []
        for i, column_name in enumerate(column_names):
            accuracy = accuracy_score(ytest.iloc[:, i], ypred.iloc[:, i])
            f1 = f1_score(ytest.iloc[:, i], ypred.iloc[:, i], average='micro')
            precision = precision_score(ytest.iloc[:, i], ypred.iloc[:, i], average='micro')
            recall = recall_score(ytest.iloc[:, i], ypred.iloc[:, i], average='micro')        
            results.append([column_name, accuracy, f1, precision, recall])
        return pd.DataFrame(results, columns=['category', 'accuracy score', 'f1 score', 'precision score', 'recall score'])

    def evaluate_no_cv_model(self):
        ypred = self.pipeline.predict(self.xtest)
        scores_df = MLPipeline.get_score(self.ytest, ypred, self.column_names)
        scores_df.sort_values(by=["f1 score"], inplace=True)
        print(tabulate(scores_df, headers='keys', tablefmt='psql'))
    
    def evaluate_cv_model(self):
        pass

    def save_pipeline(self, filename: str = "./models/pipeline.pkl"):
        outfile = open(filename, "wb")
        pickle.dump(self.pipeline, outfile)
        outfile.close()

def main():
    ml_pipeline = MLPipeline(debug=True)
    ml_pipeline.load_data()
    ml_pipeline.train_no_cv()
    ml_pipeline.evaluate_no_cv_model()
    ml_pipeline.save_pipeline()

if __name__ == '__main__':
    main()