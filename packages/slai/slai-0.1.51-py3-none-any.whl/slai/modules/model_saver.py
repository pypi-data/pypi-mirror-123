import io
import base64
import inspect
import json
import pickle
import uuid
import tarfile
import shutil
import os

from importlib import import_module

TMP_MODEL_ARTIFACT_PATH_ROOT = "/tmp/artifacts"


class ModelSaver:
    @staticmethod
    def save_pytorch(model):
        _torch = import_module("torch")
        model_state_dict_binary = io.BytesIO()
        model_class_file_location = inspect.getfile(model.__class__).split("/")[-1]

        _torch.save(model.state_dict(), model_state_dict_binary)

        # model parameters
        model_state_dict_binary_base64 = base64.b64encode(
            model_state_dict_binary.getvalue()
        ).decode()

        model_artifact = {
            "state_dict": model_state_dict_binary_base64,
        }

        model_metadata = {
            "model_class_file_location": model_class_file_location,
            "model_class_name": model.__class__.__name__,
        }

        model_artifact_base_64 = base64.b64encode(
            json.dumps(model_artifact).encode("utf-8")
        ).decode()

        return model_artifact_base_64, model_metadata

    @staticmethod
    def save_sklearn(model):
        model_binary = pickle.dumps(model)
        model_artifact_base64 = base64.b64encode(model_binary).decode()
        return model_artifact_base64

    @staticmethod
    def save_fastai(model):
        return None

    @staticmethod
    def save_keras(model):
        model_artifact_base64 = None
        model_tmp_location = f"{TMP_MODEL_ARTIFACT_PATH_ROOT}/{uuid.uuid4()}"

        try:
            model.save(model_tmp_location)

            with tarfile.open(f"{model_tmp_location}.tar.gz", "w:gz") as tar:
                tar.add(model_tmp_location, arcname="/")

            archive_file = f"{model_tmp_location}.tar.gz"
            with open(archive_file, "rb") as f:
                model_artifact_base64 = base64.b64encode(f.read()).decode()

            shutil.rmtree(model_tmp_location)
            os.remove(archive_file)
        except AttributeError:
            pass

        return model_artifact_base64, {}

    @staticmethod
    def save_tf(model):
        return None
