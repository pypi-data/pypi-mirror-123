from slai.loaders.torch_loader import TorchLoader
from slai.loaders.sklearn_loader import SklearnLoader
from slai.loaders.keras_loader import KerasLoader
from slai.exceptions import UnsupportedModelFormat


class ValidModelFrameworks:
    Torch = "TORCH"
    Sklearn = "SKLEARN"
    Keras = "KERAS"


class ModelLoader:
    @classmethod
    def load_model(cls, *, model_metadata, model_data, artifact_type):
        loaded_model = None

        if artifact_type == ValidModelFrameworks.Torch:
            loaded_model, inference_method_name = TorchLoader.load_model(
                model_metadata=model_metadata,
                model_data=model_data,
            )
        elif artifact_type == ValidModelFrameworks.Sklearn:
            loaded_model, inference_method_name = SklearnLoader.load_model(
                model_metadata=model_metadata,
                model_data=model_data,
            )
        elif artifact_type == ValidModelFrameworks.Keras:
            loaded_model, inference_method_name = KerasLoader.load_model(
                model_metadata=model_metadata,
                model_data=model_data,
            )
        else:
            raise UnsupportedModelFormat("invalid_artifact_type")

        return loaded_model, inference_method_name
