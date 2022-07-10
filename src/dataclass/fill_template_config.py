from dataclasses import dataclass

@dataclass(frozen=True)
class  FillTemplateConfig(object):

    name: str
    """Unique experiment name"""
    label: str
    """Readable experiment label"""

    dimensions = [
        'male',
        'female'
    ]

    templates_path: str
    """Templates path"""

    n_predictions: int = 29
    """Number of predictions"""

    @property
    def n_dimensions(self): 
        return len(self.dimensions)
    
    # categories_path: str
    # check_is_adjective: bool = True
    # prefix: str

    # def categories_ready(self) -> bool:
    #     return self.categories_path != ''

    # def result_path(self) -> str:
    #     return self.prefix