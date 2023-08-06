from slai.types import ModelTypes
from slai.base_handler import BaseModelHandler
from slai.login import Login
from slai.model import Model
from slai.dataset import DataSet

__version__ = "0.1.54"


# most used slai actions go here
model = Model
types = ModelTypes
login = Login
dataset = DataSet
BaseModelHandler = BaseModelHandler

__all__ = [
    "__version__",
    "dataset",
    "model",
    "types",
    "base_handler",
    "login",
]
