import pickle
import base64

from slai.loaders import base_loader


class SklearnLoader(base_loader.BaseLoader):
    @classmethod
    def load_model(cls, model_metadata, model_data):
        model_artifact_model_binary = base64.b64decode(model_data)

        loaded_model_class = pickle.loads(model_artifact_model_binary)
        loaded_model = loaded_model_class()

        inference_method_name = "predict"
        return loaded_model, inference_method_name
