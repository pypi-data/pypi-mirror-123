from enum import Enum
from typing import List, Optional, Union

from cognite.well_model.models import PropertyFilter as PropertyFilterModel


class PropertyFilterConstant(Enum):
    DontCare = 1
    NotSet = 2


DontCare = PropertyFilterConstant.DontCare
NotSet = PropertyFilterConstant.NotSet

PropertyFilter = Union[PropertyFilterConstant, List[str]]


def filter_to_model(filter: PropertyFilter) -> Optional[PropertyFilterModel]:
    if filter == DontCare:
        return None
    elif filter == NotSet:
        return PropertyFilterModel(is_set=False)
    else:
        return PropertyFilterModel(is_set=True, one_of=filter)
