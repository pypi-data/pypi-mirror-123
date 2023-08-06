'''_1974.py

AbstractShaftToMountableComponentConnection
'''


from mastapy.system_model.part_model import (
    _2172, _2149, _2156, _2170,
    _2171, _2174, _2177, _2179,
    _2180, _2185, _2187, _2145
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.gears import (
    _2220, _2222, _2224, _2225,
    _2226, _2228, _2230, _2232,
    _2234, _2235, _2237, _2241,
    _2243, _2245, _2247, _2250,
    _2252, _2254, _2256, _2257,
    _2258, _2260
)
from mastapy.system_model.part_model.cycloidal import _2277, _2276
from mastapy.system_model.part_model.couplings import (
    _2286, _2289, _2291, _2294,
    _2296, _2297, _2303, _2305,
    _2308, _2311, _2312, _2313,
    _2315, _2317
)
from mastapy.system_model.part_model.shaft_model import _2190
from mastapy.system_model.connections_and_sockets import _1981
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnection',)


class AbstractShaftToMountableComponentConnection(_1981.Connection):
    '''AbstractShaftToMountableComponentConnection

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mountable_component(self) -> '_2172.MountableComponent':
        '''MountableComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2172.MountableComponent.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MountableComponent. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_bearing(self) -> '_2149.Bearing':
        '''Bearing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.Bearing.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Bearing. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_connector(self) -> '_2156.Connector':
        '''Connector: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2156.Connector.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Connector. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_mass_disc(self) -> '_2170.MassDisc':
        '''MassDisc: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2170.MassDisc.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MassDisc. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_measurement_component(self) -> '_2171.MeasurementComponent':
        '''MeasurementComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2171.MeasurementComponent.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MeasurementComponent. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_oil_seal(self) -> '_2174.OilSeal':
        '''OilSeal: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2174.OilSeal.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to OilSeal. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_planet_carrier(self) -> '_2177.PlanetCarrier':
        '''PlanetCarrier: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.PlanetCarrier.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PlanetCarrier. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_point_load(self) -> '_2179.PointLoad':
        '''PointLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2179.PointLoad.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PointLoad. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_power_load(self) -> '_2180.PowerLoad':
        '''PowerLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2180.PowerLoad.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PowerLoad. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_unbalanced_mass(self) -> '_2185.UnbalancedMass':
        '''UnbalancedMass: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.UnbalancedMass.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to UnbalancedMass. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_virtual_component(self) -> '_2187.VirtualComponent':
        '''VirtualComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2187.VirtualComponent.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to VirtualComponent. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_agma_gleason_conical_gear(self) -> '_2220.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2220.AGMAGleasonConicalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_bevel_differential_gear(self) -> '_2222.BevelDifferentialGear':
        '''BevelDifferentialGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2222.BevelDifferentialGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_bevel_differential_planet_gear(self) -> '_2224.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2224.BevelDifferentialPlanetGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_bevel_differential_sun_gear(self) -> '_2225.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2225.BevelDifferentialSunGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_bevel_gear(self) -> '_2226.BevelGear':
        '''BevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.BevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_concept_gear(self) -> '_2228.ConceptGear':
        '''ConceptGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.ConceptGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_conical_gear(self) -> '_2230.ConicalGear':
        '''ConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2230.ConicalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConicalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_cylindrical_gear(self) -> '_2232.CylindricalGear':
        '''CylindricalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2232.CylindricalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_cylindrical_planet_gear(self) -> '_2234.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2234.CylindricalPlanetGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_face_gear(self) -> '_2235.FaceGear':
        '''FaceGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2235.FaceGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to FaceGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_gear(self) -> '_2237.Gear':
        '''Gear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2237.Gear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Gear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_hypoid_gear(self) -> '_2241.HypoidGear':
        '''HypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2241.HypoidGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to HypoidGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2243.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2243.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2245.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2245.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2247.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_spiral_bevel_gear(self) -> '_2250.SpiralBevelGear':
        '''SpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.SpiralBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_straight_bevel_diff_gear(self) -> '_2252.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.StraightBevelDiffGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_straight_bevel_gear(self) -> '_2254.StraightBevelGear':
        '''StraightBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.StraightBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_straight_bevel_planet_gear(self) -> '_2256.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.StraightBevelPlanetGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_straight_bevel_sun_gear(self) -> '_2257.StraightBevelSunGear':
        '''StraightBevelSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2257.StraightBevelSunGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_worm_gear(self) -> '_2258.WormGear':
        '''WormGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.WormGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to WormGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_zerol_bevel_gear(self) -> '_2260.ZerolBevelGear':
        '''ZerolBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.ZerolBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_ring_pins(self) -> '_2277.RingPins':
        '''RingPins: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2277.RingPins.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RingPins. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_clutch_half(self) -> '_2286.ClutchHalf':
        '''ClutchHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.ClutchHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ClutchHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_concept_coupling_half(self) -> '_2289.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2289.ConceptCouplingHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_coupling_half(self) -> '_2291.CouplingHalf':
        '''CouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2291.CouplingHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CouplingHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_cvt_pulley(self) -> '_2294.CVTPulley':
        '''CVTPulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2294.CVTPulley.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CVTPulley. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_part_to_part_shear_coupling_half(self) -> '_2296.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2296.PartToPartShearCouplingHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_pulley(self) -> '_2297.Pulley':
        '''Pulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2297.Pulley.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Pulley. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_rolling_ring(self) -> '_2303.RollingRing':
        '''RollingRing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2303.RollingRing.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RollingRing. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_shaft_hub_connection(self) -> '_2305.ShaftHubConnection':
        '''ShaftHubConnection: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2305.ShaftHubConnection.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_spring_damper_half(self) -> '_2308.SpringDamperHalf':
        '''SpringDamperHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2308.SpringDamperHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_synchroniser_half(self) -> '_2311.SynchroniserHalf':
        '''SynchroniserHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2311.SynchroniserHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_synchroniser_part(self) -> '_2312.SynchroniserPart':
        '''SynchroniserPart: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2312.SynchroniserPart.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserPart. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_synchroniser_sleeve(self) -> '_2313.SynchroniserSleeve':
        '''SynchroniserSleeve: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2313.SynchroniserSleeve.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_torque_converter_pump(self) -> '_2315.TorqueConverterPump':
        '''TorqueConverterPump: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2315.TorqueConverterPump.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def mountable_component_of_type_torque_converter_turbine(self) -> '_2317.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.TorqueConverterTurbine.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent else None

    @property
    def shaft(self) -> '_2145.AbstractShaft':
        '''AbstractShaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.AbstractShaft.TYPE not in self.wrapped.Shaft.__class__.__mro__:
            raise CastException('Failed to cast shaft to AbstractShaft. Expected: {}.'.format(self.wrapped.Shaft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaft.__class__)(self.wrapped.Shaft) if self.wrapped.Shaft else None

    @property
    def shaft_of_type_shaft(self) -> '_2190.Shaft':
        '''Shaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2190.Shaft.TYPE not in self.wrapped.Shaft.__class__.__mro__:
            raise CastException('Failed to cast shaft to Shaft. Expected: {}.'.format(self.wrapped.Shaft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaft.__class__)(self.wrapped.Shaft) if self.wrapped.Shaft else None

    @property
    def shaft_of_type_cycloidal_disc(self) -> '_2276.CycloidalDisc':
        '''CycloidalDisc: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2276.CycloidalDisc.TYPE not in self.wrapped.Shaft.__class__.__mro__:
            raise CastException('Failed to cast shaft to CycloidalDisc. Expected: {}.'.format(self.wrapped.Shaft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaft.__class__)(self.wrapped.Shaft) if self.wrapped.Shaft else None
