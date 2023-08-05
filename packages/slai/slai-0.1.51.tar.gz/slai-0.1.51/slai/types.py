from abc import ABC, abstractmethod
from importlib import import_module


class InvalidTypeException(Exception):
    def __init__(self, msg, errors=None):
        super().__init__(msg)
        self.msg = msg
        self.errors = errors


class InvalidPayloadException(Exception):
    def __init__(self, msg, errors=None):
        super().__init__(msg)
        self.msg = msg
        self.errors = errors


class ModelTypeSerializer(ABC):
    def __init__(self, *args, **kwargs):
        return self.define(*args, **kwargs)

    @abstractmethod
    def define(self, *args, **kwargs):
        pass

    @abstractmethod
    def serialize(self, input):
        pass


class FloatType(ModelTypeSerializer):
    def define(self):
        pass

    def serialize(self, input):
        try:
            output = float(input)
        except ValueError:
            raise InvalidTypeException("invalid_float_value")

        return output


class StringType(ModelTypeSerializer):
    def define(self, max_length=None):
        self.max_length = max_length

    def serialize(self, input):
        output = str(input)

        if self.max_length:
            if len(output) > self.max_length:
                raise InvalidTypeException("input_string_too_long")

        return output


class ImageType(ModelTypeSerializer):
    def define(self):
        pass

    def serialize(self, input):
        output = str(input)

        return output


class NumpyType(ModelTypeSerializer):
    def define(self, shape=None, dtype=float):
        self.shape = shape
        self.dtype = dtype

    def serialize(self, input):
        try:
            np = import_module("numpy")
        except ModuleNotFoundError:
            raise RuntimeError("numpy_required_for_numpy_inputs")

        output = np.array(input, dtype=self.dtype)

        errors = []
        if self.shape is not None and output.shape != self.shape:
            errors = ["invalid_shape"]

        if errors:
            raise InvalidTypeException("invalid_numpy_shape", errors=errors)

        return output


class DataframeType(ModelTypeSerializer):
    def define(self, max_rows=None, max_cols=None):
        self.max_rows = max_rows
        self.max_cols = max_cols

    def serialize(self, input):
        try:
            pd = import_module("pandas")
        except ModuleNotFoundError:
            raise RuntimeError("pandas_required_for_dataframe_inputs")

        try:
            output = pd.read_json(input)
        except ValueError:
            raise InvalidTypeException("invalid_dataframe")

        return output


class TensorType(ModelTypeSerializer):
    def define(self, shape=None, dtype=float):
        self.shape = shape
        self.dtype = dtype

    def serialize(self, input):
        try:
            torch = import_module("torch")
        except ModuleNotFoundError:
            raise RuntimeError("torch_required_for_tensor_inputs")

        output = torch.tensor(input, dtype=self.dtype)

        errors = []
        if self.shape is not None and output.shape != self.shape:
            errors = ["invalid_shape"]

        if errors:
            raise InvalidTypeException("invalid_tensor_shape", errors=errors)

        return output


class ModelTypes:
    Float = FloatType
    String = StringType
    NumpyArray = NumpyType
    Dataframe = DataframeType
    Tensor = TensorType
    Image = ImageType

    @staticmethod
    def serialize_payload(payload, expected_types):
        serialized_payload = {}
        errors = []

        if not isinstance(payload, dict):
            raise InvalidTypeException("invalid_payload_format")

        for key in expected_types.keys():
            if key not in payload.keys():
                errors.append(f"{key}:required")
            else:
                _type = expected_types[key]
                _input = payload[key]

                try:
                    serialized_payload[key] = _type.serialize(_input)
                except InvalidTypeException as exc:
                    errors.append(f"{key}:invalid_type")

        if errors:
            raise InvalidPayloadException("invalid_payload", errors=errors)

        return serialized_payload
