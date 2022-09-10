from dataclasses import dataclass

@dataclass(frozen=True)
class  FillTemplateConfig(object):

    label: str
    """Readable experiment label"""

    templates_path: str
    """Templates path"""

    models_path: str
    """Models path"""

    n_predictions: int = 29
    """Number of predictions"""

    dimensions = [
        'male',
        'female'
    ]

    @property
    def n_dimensions(self): 
        return len(self.dimensions)