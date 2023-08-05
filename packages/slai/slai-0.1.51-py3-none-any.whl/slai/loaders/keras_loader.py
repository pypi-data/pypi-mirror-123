import base64
import uuid
import tarfile
import importlib
import shutil
import os

from slai.loaders import base_loader

TMP_MODEL_ARTIFACT_PATH_ROOT = "/tmp/artifacts"


class KerasLoader(base_loader.BaseLoader):
    @classmethod
    def load_model(cls, model_metadata, model_data):
        loaded_model = None
        inference_method_name = None

        tensorflow = importlib.import_module("tensorflow")
        model_tmp_location = f"{TMP_MODEL_ARTIFACT_PATH_ROOT}/{uuid.uuid4()}"

        model_artifact_archive_binary = base64.b64decode(model_data)
        archive_file = f"{model_tmp_location}.tar.gz"

        with open(f"{archive_file}", "wb") as f:
            f.write(model_artifact_archive_binary)

        with tarfile.open(f"{archive_file}") as archive:
            archive.extractall(model_tmp_location)

        loaded_model = tensorflow.keras.models.load_model(model_tmp_location)

        shutil.rmtree(model_tmp_location)
        os.remove(archive_file)

        return loaded_model, inference_method_name
