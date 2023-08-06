'''_2237.py

ConicalGearSet
'''


from typing import List

from mastapy.gears.gear_designs.conical import _1087
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.zerol_bevel import _894
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _903
from mastapy.gears.gear_designs.straight_bevel import _907
from mastapy.gears.gear_designs.spiral_bevel import _911
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _915
from mastapy.gears.gear_designs.klingelnberg_hypoid import _919
from mastapy.gears.gear_designs.klingelnberg_conical import _923
from mastapy.gears.gear_designs.hypoid import _927
from mastapy.gears.gear_designs.bevel import _1113
from mastapy.gears.gear_designs.agma_gleason_conical import _1126
from mastapy.system_model.part_model.gears import _2236, _2245
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearSet',)


class ConicalGearSet(_2245.GearSet):
    '''ConicalGearSet

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_set_design(self) -> '_1087.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1087.ConicalGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to ConicalGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_894.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _894.ZerolBevelGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_903.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _903.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_907.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _907.StraightBevelGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_911.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _911.SpiralBevelGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_915.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _915.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_919.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_klingelnberg_conical_gear_set_design(self) -> '_923.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _923.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_hypoid_gear_set_design(self) -> '_927.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _927.HypoidGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_bevel_gear_set_design(self) -> '_1113.BevelGearSetDesign':
        '''BevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1113.BevelGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def active_gear_set_design_of_type_agma_gleason_conical_gear_set_design(self) -> '_1126.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1126.AGMAGleasonConicalGearSetDesign.TYPE not in self.wrapped.ActiveGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.wrapped.ActiveGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearSetDesign.__class__)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def conical_gear_set_design(self) -> '_1087.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1087.ConicalGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to ConicalGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_894.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _894.ZerolBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_903.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _903.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_907.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _907.StraightBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_911.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _911.SpiralBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_915.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _915.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_919.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_klingelnberg_conical_gear_set_design(self) -> '_923.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _923.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_hypoid_gear_set_design(self) -> '_927.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _927.HypoidGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_bevel_gear_set_design(self) -> '_1113.BevelGearSetDesign':
        '''BevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1113.BevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_agma_gleason_conical_gear_set_design(self) -> '_1126.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1126.AGMAGleasonConicalGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gears(self) -> 'List[_2236.ConicalGear]':
        '''List[ConicalGear]: 'ConicalGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalGears, constructor.new(_2236.ConicalGear))
        return value
