# importing dependencies

#from sensor.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os



class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        """
        Returns:
            dict: {'neg': 0, 'pos': 1}
        """
        return self.__dict__ 

    def reverse_mapping(self):
        """
        Returns:
            dict: {0: 'neg', 1: 'pos'}
        """
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class SensorModel:
    
    def __init__(self,preprocessor,model):
        self.preprocessor = preprocessor
        self.model = model

    def predict(self,x):
        try:
            x_transform =  self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise e


  

