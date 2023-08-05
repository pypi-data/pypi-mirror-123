import io
import base64

from importlib import import_module
from slai.loaders import base_loader


class TorchLoader(base_loader.BaseLoader):
    @classmethod
    def load_model(cls, model_metadata, model_data):
        model_framework_module = import_module("torch")

        model_artifact_model_state_dict = base64.b64decode(
            eval(model_data)["state_dict"]
        )
        model_file_module = model_metadata["model_class_file_location"].split(".")[0]
        model_class_name = model_metadata["model_class_name"]
        model_module = import_module(f"{model_file_module}")
        model_class = getattr(model_module, model_class_name)

        # instantiate model class
        loaded_model = model_class()

        # load trained model parameters
        model_state_dict_binary = io.BytesIO(model_artifact_model_state_dict)
        _state_dict = model_framework_module.load(model_state_dict_binary)
        loaded_model.load_state_dict(_state_dict)
        loaded_model.eval()

        return loaded_model, None
