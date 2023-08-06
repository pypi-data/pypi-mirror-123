'''_524.py

FlankMicroGeometry
'''


from mastapy.gears import _301
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility.scripting import _1499
from mastapy.gears.gear_designs import _887
from mastapy.gears.gear_designs.zerol_bevel import _892
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _896, _897, _900
from mastapy.gears.gear_designs.straight_bevel_diff import _901
from mastapy.gears.gear_designs.straight_bevel import _905
from mastapy.gears.gear_designs.spiral_bevel import _909
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _913
from mastapy.gears.gear_designs.klingelnberg_hypoid import _917
from mastapy.gears.gear_designs.klingelnberg_conical import _921
from mastapy.gears.gear_designs.hypoid import _925
from mastapy.gears.gear_designs.face import _929, _934, _937
from mastapy.gears.gear_designs.cylindrical import _952, _979
from mastapy.gears.gear_designs.conical import _1085
from mastapy.gears.gear_designs.concept import _1107
from mastapy.gears.gear_designs.bevel import _1111
from mastapy.gears.gear_designs.agma_gleason_conical import _1124
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FLANK_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'FlankMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('FlankMicroGeometry',)


class FlankMicroGeometry(_0.APIBase):
    '''FlankMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _FLANK_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlankMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def micro_geometry_input_type(self) -> '_301.MicroGeometryInputTypes':
        '''MicroGeometryInputTypes: 'MicroGeometryInputType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MicroGeometryInputType)
        return constructor.new(_301.MicroGeometryInputTypes)(value) if value is not None else None

    @micro_geometry_input_type.setter
    def micro_geometry_input_type(self, value: '_301.MicroGeometryInputTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MicroGeometryInputType = value

    @property
    def user_specified_data(self) -> '_1499.UserSpecifiedData':
        '''UserSpecifiedData: 'UserSpecifiedData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1499.UserSpecifiedData)(self.wrapped.UserSpecifiedData) if self.wrapped.UserSpecifiedData is not None else None

    @property
    def gear_design(self) -> '_887.GearDesign':
        '''GearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _887.GearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to GearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_zerol_bevel_gear_design(self) -> '_892.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _892.ZerolBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_worm_design(self) -> '_896.WormDesign':
        '''WormDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _896.WormDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to WormDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_worm_gear_design(self) -> '_897.WormGearDesign':
        '''WormGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _897.WormGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to WormGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_worm_wheel_design(self) -> '_900.WormWheelDesign':
        '''WormWheelDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _900.WormWheelDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to WormWheelDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_901.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _901.StraightBevelDiffGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_straight_bevel_gear_design(self) -> '_905.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _905.StraightBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_spiral_bevel_gear_design(self) -> '_909.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _909.SpiralBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_913.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _913.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_917.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_klingelnberg_conical_gear_design(self) -> '_921.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _921.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_hypoid_gear_design(self) -> '_925.HypoidGearDesign':
        '''HypoidGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.HypoidGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to HypoidGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_face_gear_design(self) -> '_929.FaceGearDesign':
        '''FaceGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _929.FaceGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to FaceGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_face_gear_pinion_design(self) -> '_934.FaceGearPinionDesign':
        '''FaceGearPinionDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _934.FaceGearPinionDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to FaceGearPinionDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_face_gear_wheel_design(self) -> '_937.FaceGearWheelDesign':
        '''FaceGearWheelDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _937.FaceGearWheelDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to FaceGearWheelDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_cylindrical_gear_design(self) -> '_952.CylindricalGearDesign':
        '''CylindricalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _952.CylindricalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_cylindrical_planet_gear_design(self) -> '_979.CylindricalPlanetGearDesign':
        '''CylindricalPlanetGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _979.CylindricalPlanetGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to CylindricalPlanetGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_conical_gear_design(self) -> '_1085.ConicalGearDesign':
        '''ConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1085.ConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_concept_gear_design(self) -> '_1107.ConceptGearDesign':
        '''ConceptGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1107.ConceptGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ConceptGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_bevel_gear_design(self) -> '_1111.BevelGearDesign':
        '''BevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1111.BevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to BevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None

    @property
    def gear_design_of_type_agma_gleason_conical_gear_design(self) -> '_1124.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1124.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign is not None else None
