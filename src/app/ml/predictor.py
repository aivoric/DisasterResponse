import pickle
import os

pipeline_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pipeline.pkl")

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'tokenize':
            from .tokenize import tokenize
            return tokenize
        return super().find_class(module, name)

class Predictor():
    def __init__(self, raw_string, df):
        self.raw_string = [raw_string]
        self.pipeline = CustomUnpickler(open(pipeline_location, 'rb')).load()
        self.df = df
    
    def predict(self):
        prediction = self.pipeline.predict(self.raw_string)[0]
        classification_result = dict(zip(self.df.columns[4:], prediction))
        return classification_result