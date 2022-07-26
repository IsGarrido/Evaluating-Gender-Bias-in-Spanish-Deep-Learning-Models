from dataclasses import dataclass

@dataclass(frozen=True)
class  EvaluateCategoriesConfig(object):

    label: str
    """Readable experiment label"""

    categories_path: str
    """Number of predictions"""

    dimensions = [
        'male',
        'female'
    ]

    @property
    def n_dimensions(self): 
        return len(self.dimensions)