from pydantic.class_validators import validator
from pydantic.fields import Field, Any
from pydantic import BaseModel
from pydantic.typing import Dict, List
import numpy as np


class DataConfig(BaseModel):
    noise_rate: float = Field(None, description="The noise rate added to the outcome from N(0,1) distribution ex (0.1)")
    shuffle_noise: float = Field(None, description="Adding noise by shuffling the outcomes randomly")
    use_name_proxy: bool = Field(None, description="Is the name proxy used for this experiment ? ex(True)")
    process_proxy: bool = Field(None, description="Do we need to process the proxy using the proxy model ? ex(True)")
    base_y_val: int = Field(None, description="The base value for the outcome without adding disparity ex(100)")
    correlation: float = Field(None, description="Correlation value with the protected attribute ex()")
    proportion: Dict = Field(None,
                             description="Proportion of individuals for each group ex({'a': 0.3, 'b': 0.3, 'c': 0.4})")
    add_disparity: List[float] = Field(None,
                                       description="Disparate treatment for each group in terms of adding ex([0.0, 100.0, 200.0])")
    factor_disparity: List[float] = Field(None,
                                          description="Disparate treatment for each group in terms of multiplying ex([0.0, 1.0, 2.0])")
    name: str = Field(None, description="The name of the experiment")
    model_name: str = Field(None, description="Name of the proxy model used to predict ethnicity from name")
    t_labels: List[str] = Field(None,
                                description="Protected attribute values by index ex(['white', 'black', 'hispanic'])")

    @validator('proportion')
    def proportion_val(cls, v):
        if sum(list(v.values())) != 1.0:
            raise ValueError('sum percent must equal to one')
        if len(list(filter(lambda x: x == 0, list(v.values())))) != 0:
            raise ValueError('Positivity among all the treatments must be upheld')
        return v

    @validator('correlation')
    def correlation_val(cls, v):
        if v > 1 or v < 0:
            raise ValueError('Correlation with the treatment must be between 0 and 1')
        return v

    def _same_correlation_length_val(cls, v):
        if len(v) == len(cls.proportion.keys()):
            raise ValueError("Factor and Adds need to have the same length of the configuration")
        return v

    @validator('factor_disparity')
    def factor_disparity_val(cls, v):
        return cls._same_correlation_length_val(v)

    @validator('add_disparity')
    def add_disparity_val(cls, v):
        return cls._same_correlation_length_val(v)

    # raise

    # TODO : Finish validations


class Dataset(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    t_test: np.ndarray = Field(description="")
    t_proxy_test: np.ndarray = Field(description="")
    x_test: np.ndarray = Field(description="")
    y_test: np.ndarray = Field(description="")

    t_train: np.ndarray = Field(description="")
    t_proxy_train: np.ndarray = Field(description="")
    x_train: np.ndarray = Field(description="")
    y_train: np.ndarray = Field(description="")

    labels: List[str] = Field(description="")
    proxy: Any = Field(None, description="")
