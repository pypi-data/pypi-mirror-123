'''_2323.py

BearingDetailSelection
'''


from typing import List

from mastapy.bearings.bearing_results import _1685
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model.part_model import _2150, _2149
from mastapy.system_model.part_model.configurations import _2325
from mastapy.bearings.bearing_designs import _1848
from mastapy._internal.python_net import python_net_import

_BEARING_DETAIL_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'BearingDetailSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingDetailSelection',)


class BearingDetailSelection(_2325.PartDetailSelection['_2149.Bearing', '_1848.BearingDesign']):
    '''BearingDetailSelection

    This is a mastapy class.
    '''

    TYPE = _BEARING_DETAIL_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingDetailSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def orientation(self) -> '_1685.Orientations':
        '''Orientations: 'Orientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Orientation)
        return constructor.new(_1685.Orientations)(value) if value else None

    @orientation.setter
    def orientation(self, value: '_1685.Orientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def mounting(self) -> 'List[_2150.BearingRaceMountingOptions]':
        '''List[BearingRaceMountingOptions]: 'Mounting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Mounting, constructor.new(_2150.BearingRaceMountingOptions))
        return value
