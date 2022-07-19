from dataclasses import dataclass

@dataclass(frozen=True)
class  FillTemplateConfig(object):

    name: str
    """Unique experiment name"""
    label: str
    """Readable experiment label"""

    templates_path: str
    """Templates path"""

    n_predictions: int = 29
    """Number of predictions"""

    dimensions = [
        'male',
        'female'
    ]

    @property
    def n_dimensions(self): 
        return len(self.dimensions)