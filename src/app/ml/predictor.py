import pickle
import os

pipeline_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pipeline.pkl")

class CustomUnpickler(pickle.Unpickler):
    """
    This custom unpickler is required because it unpickles the entire trained pipeline object.

    The saved Pipeline object had a helper function called "tokenize". When unpickling objects
    which reference other functions it is necessary to ensure the path to the function works.

    The find_class() method finds the tokenize reference and overrides its path so that the function
    can be references from within the web app.
    """
    def find_class(self, module, name):
        if name == 'tokenize':
            from .tokenize import tokenize
            return tokenize
        return super().find_class(module, name)

class Predictor():
    def __init__(self, raw_string, df):
        """Unpickle the trained Pipeline and instatiate the class with the pipeline 
        , pandas Dataframe data and the query string which needs to be classified."""
        self.raw_string = [raw_string]
        self.pipeline = CustomUnpickler(open(pipeline_location, 'rb')).load()
        self.df = df
    
    def predict(self):
        """
        Return a prediction based on the query string by running it through the trained
        classfication Pipeline.
        """
        prediction = self.pipeline.predict(self.raw_string)[0]
        classification_result = dict(zip(self.df.columns[4:], prediction))
        return classification_result