from m3_gar.base_models import (
    Param as BaseParam,
    ParamTypes as BaseParamTypes,
)
from m3_gar.models.util import (
    RegionCodeModelMixin,
    make_fk,
)


__all__ = ['Param', 'ParamTypes']


class ParamTypes(BaseParamTypes):
    """
    Сведения по типу параметра
    """
    class Meta:
        verbose_name = 'Тип параметра'
        verbose_name_plural = 'Типы параметров'


class Param(BaseParam, RegionCodeModelMixin):
    """
    Сведения о классификаторе параметров адресообразующих элементов и объектов недвижимости
    """
    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'


make_fk(Param, 'typeid', to=ParamTypes)
