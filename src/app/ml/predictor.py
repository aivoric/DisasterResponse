import pickle

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'tokenize':
            from ..helpers.tokenize import tokenize
            return tokenize
        return super().find_class(module, name)

class Predictor():
    def __init__(self, raw_string, df):
        self.raw_string = [raw_string]
        self.pipeline = CustomUnpickler(open('pipeline.pkl', 'rb')).load()
        self.labels = pickle.load(open('xgb_model_labels.pkl', 'rb'))
        self.df = df
    
    def predict(self):
        prediction = self.pipeline.predict(self.raw_string)[0]
        classification_result = dict(zip(self.df.columns[4:], prediction))
        return classification_result