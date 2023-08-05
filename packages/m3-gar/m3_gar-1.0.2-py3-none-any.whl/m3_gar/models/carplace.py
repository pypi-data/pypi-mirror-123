from m3_gar.base_models import (
    Carplaces as BaseCarplaces,
    OperationTypes,
)
from m3_gar.models.reestr import (
    ReestrObjects,
)
from m3_gar.models.util import (
    ParamsMixin,
    RegionCodeModelMixin,
    make_fk,
)


__all__ = ['Carplaces']


class Carplaces(BaseCarplaces, ParamsMixin, RegionCodeModelMixin):
    """
    Сведения по машино-местам
    """

    level = 17

    class Meta:
        verbose_name = 'Машино-место'
        verbose_name_plural = 'Машино-места'


make_fk(Carplaces, 'opertypeid', to=OperationTypes)
make_fk(Carplaces, 'objectid', to=ReestrObjects)
