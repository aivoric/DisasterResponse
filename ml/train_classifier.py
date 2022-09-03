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
    """
    Class for loading the disaster response data and training a prediction
    pipeline. The pipeline consist of:
    1) a CountVectorizer() which turns each string into tokens with the help
    of a custom tokenize() method.
    2) a TfidfTransformer() which transforms a count matrix (the output from the CountVertorizer)
    to a normalized tf or tf-idf representation.Tf means term-frequency while tf-idf means 
    term-frequency times inverse document-frequency. This is a common term weighting scheme 
    in information retrieval, that has also found good use in document classification.
    https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html
    3) a MultiOutputClassifier with XGBoost Classifier which takes the transformed word tokens and trains
    a prediction model.

    The class also contains various helper methods which are used for scoring, saving and load the models
    - evaluate_model()
    - get_score()
    - evaluate_model()
    - save_estimator()
    - save_cv_estimator()
    - load_estimator()
    """
    def __init__(self, debug: bool = False, debug_sample_size: int = 100):
        self.engine = create_engine('sqlite:///data/DisasterResponse.db')
        self.pipeline = Pipeline([
                ('vect', CountVectorizer(tokenizer=MLPipeline.tokenize)),
                ('tfidf', TfidfTransformer()),
                ('clf', MultiOutputClassifier(XGBClassifier()))
            ])
        self.debug = debug
        self.debug_sample_size = debug_sample_size

    def load_data(self):
        """
        Load the data from the disaster response SQLLite database.
        """
        df = pd.read_sql_table(table_name="disaster_messages", con=self.engine)
        if self.debug:
            df = df.head(self.debug_sample_size)
        Y = df.drop(columns=['message', 'original', 'genre', 'id'])
        X = df['message']
        self.column_names = Y.columns
        self.xtrain, self.xtest, self.ytrain, self.ytest = train_test_split(X, Y, train_size=0.7, random_state=12)

    def train_no_cv(self):
        """
        Train a pipeline without optimising for hyperparameters.
        """
        self.pipeline.fit(self.xtrain, self.ytrain)
    
    def train_cv(self):
        """
        Do basic hyperparameter optimisation via RandomizedSearchCV().

        For future improvements:
        - Add a custom scoring function.
        """
        parameters = {
            'clf__estimator__learning_rate': [0.01, 0.1, 0.3],
            'clf__estimator__n_estimators': [100,150,200,250,300,350,400],
        }
        self.cv = RandomizedSearchCV(estimator=self.pipeline,
                                param_distributions=parameters,
                                n_iter=10,
                                n_jobs=-1,
                                cv=5,
                                verbose=100,
                                # scoring=MLPipeline.scorer, #TODO: Complete the custom sctoring method
                                random_state=88
                            )
        self.cv.fit(self.xtrain, self.ytrain)

    # @staticmethod
    # def scorer(estimator, xtest, ytest) -> dict[str, float]:
    #     """
    #     To finish: custom scoring function for the pipeline training using RandomizedSearchCV(). 
    #     """
    #     #TODO: Complete the custom sctoring method 
    #     ypred = pd.DataFrame(estimator.predict(xtest))
    #     print(ypred)
    #     score = {'f1': f1_score(ytest.iloc[:, 1], ypred.iloc[:, 1], average='weighted', zero_division=0)}
    #     return score

    @staticmethod
    def tokenize(text) -> list:
        """
        Helper function to cleaned up,tokenize, and lemmatize all the strings.
        """
        text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower()).strip()
        words = word_tokenize(text)
        tokens = [w for w in words if w not in stop_words]
        lemmed = [WordNetLemmatizer().lemmatize(w) for w in tokens]
        return lemmed

    @staticmethod
    def get_score(ytest, ypred, column_names) -> pd.DataFrame():
        """
        Get the results for each class prediction to evaluate the model.
        """
        results = []
        for i, column_name in enumerate(column_names):
            accuracy = accuracy_score(ytest.iloc[:, i], ypred.iloc[:, i])
            f1 = f1_score(ytest.iloc[:, i], ypred.iloc[:, i], average='weighted', zero_division=0)
            precision = precision_score(ytest.iloc[:, i], ypred.iloc[:, i], average='weighted', zero_division=0)
            recall = recall_score(ytest.iloc[:, i], ypred.iloc[:, i], average='weighted', zero_division=0)        
            results.append([column_name, accuracy, f1, precision, recall])
        return pd.DataFrame(results, columns=['category', 'accuracy score', 'f1 score', 'precision score', 'recall score'])

    def evaluate_model(self, pipeline: bool=True):
        """
        1. Get the prediction using the trained pipeline.
        2. Evaluate the prediction using the get_score() help function
        3. Display the results using the tabulate() module
        """
        ypred = pd.DataFrame(self.pipeline.predict(self.xtest)) if pipeline else pd.DataFrame(self.cv.predict(self.xtest))
        scores_df = MLPipeline.get_score(self.ytest, ypred, self.column_names)
        scores_df.sort_values(by=["f1 score"], inplace=True)
        print(tabulate(scores_df, headers='keys', tablefmt='psql'))
    
    def save_estimator(self, filename: str = "./models/pipeline.pkl"):
        """
        Save the pipeline which hasn't been hyperparameter tuned.
        """
        outfile = open(filename, "wb")
        pickle.dump(self.pipeline, outfile)
        outfile.close()
    
    def save_cv_estimator(self, filename: str = "./models/pipeline_cv.pkl"):
        """
        Save the pipeline which has been hyperparameter tuned.
        """
        outfile = open(filename, "wb")
        pickle.dump(self.cv.estimator, outfile)
        outfile.close()

    def load_estimator(self, filename: str = "./models/pipeline_cv.pkl"):
        """
        Load a pipeline. This can be either the tuned one or not depending on
        the filename which is provided. Defaults to the tuned one.
        """
        outfile = open(filename, "rb")
        self.pipeline = pickle.load(outfile)
        outfile.close()

def main():
    """
    Run the full ML Pipeline which trains and evalulates 2 pipelines
    1) Basic one without hyperparameter tuning
    2) With hyperparameter tuning

    When instantiating the MLPipeline object you can use a debug mode which reduced
    the training sample size. This is useful if you want to make sure the pipeline works
    without training it on all the available data. To do this, instantiate the object like so:
        
    ml_pipeline = MLPipeline(debug=True, debug_sample_size=50)
    """
    ml_pipeline = MLPipeline(debug=False, debug_sample_size=1000)
    ml_pipeline.load_data()
    ml_pipeline.train_no_cv()
    ml_pipeline.evaluate_model(pipeline=True)
    ml_pipeline.save_estimator()
    ml_pipeline.train_cv()
    ml_pipeline.evaluate_model(pipeline=False)
    ml_pipeline.save_cv_estimator()
    ml_pipeline.load_estimator()
    ml_pipeline.evaluate_model(pipeline=True)

if __name__ == '__main__':
    main()