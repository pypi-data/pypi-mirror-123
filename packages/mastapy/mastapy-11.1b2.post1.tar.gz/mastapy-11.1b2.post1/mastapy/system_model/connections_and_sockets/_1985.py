'''_1985.py

ComponentConnection
'''


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2159, _2151, _2152, _2155,
    _2157, _2162, _2163, _2166,
    _2167, _2169, _2176, _2177,
    _2178, _2180, _2183, _2185,
    _2186, _2191, _2193
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2196
from mastapy.system_model.part_model.gears import (
    _2226, _2228, _2230, _2231,
    _2232, _2234, _2236, _2238,
    _2240, _2241, _2243, _2247,
    _2249, _2251, _2253, _2256,
    _2258, _2260, _2262, _2263,
    _2264, _2266
)
from mastapy.system_model.part_model.cycloidal import _2282, _2283
from mastapy.system_model.part_model.couplings import (
    _2292, _2295, _2297, _2300,
    _2302, _2303, _2309, _2311,
    _2314, _2317, _2318, _2319,
    _2321, _2323
)
from mastapy.system_model.connections_and_sockets import _1986
from mastapy._internal.python_net import python_net_import

_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentConnection',)


class ComponentConnection(_1986.ComponentMeasurer):
    '''ComponentConnection

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def socket(self) -> 'str':
        '''str: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Socket

    @property
    def connected_components_socket(self) -> 'str':
        '''str: 'ConnectedComponentsSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConnectedComponentsSocket

    @property
    def assembly_view(self) -> 'Image':
        '''Image: 'AssemblyView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.AssemblyView)
        return value

    @property
    def detail_view(self) -> 'Image':
        '''Image: 'DetailView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.DetailView)
        return value

    @property
    def connected_component(self) -> '_2159.Component':
        '''Component: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.Component.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Component. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_abstract_shaft(self) -> '_2151.AbstractShaft':
        '''AbstractShaft: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.AbstractShaft.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AbstractShaft. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_abstract_shaft_or_housing(self) -> '_2152.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2152.AbstractShaftOrHousing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_bearing(self) -> '_2155.Bearing':
        '''Bearing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2155.Bearing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bearing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_bolt(self) -> '_2157.Bolt':
        '''Bolt: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2157.Bolt.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bolt. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_connector(self) -> '_2162.Connector':
        '''Connector: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2162.Connector.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Connector. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_datum(self) -> '_2163.Datum':
        '''Datum: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.Datum.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Datum. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_external_cad_model(self) -> '_2166.ExternalCADModel':
        '''ExternalCADModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2166.ExternalCADModel.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ExternalCADModel. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_fe_part(self) -> '_2167.FEPart':
        '''FEPart: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2167.FEPart.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to FEPart. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_guide_dxf_model(self) -> '_2169.GuideDxfModel':
        '''GuideDxfModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2169.GuideDxfModel.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to GuideDxfModel. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_mass_disc(self) -> '_2176.MassDisc':
        '''MassDisc: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2176.MassDisc.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MassDisc. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_measurement_component(self) -> '_2177.MeasurementComponent':
        '''MeasurementComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.MeasurementComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MeasurementComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_mountable_component(self) -> '_2178.MountableComponent':
        '''MountableComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2178.MountableComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MountableComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_oil_seal(self) -> '_2180.OilSeal':
        '''OilSeal: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2180.OilSeal.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to OilSeal. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_planet_carrier(self) -> '_2183.PlanetCarrier':
        '''PlanetCarrier: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2183.PlanetCarrier.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PlanetCarrier. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_point_load(self) -> '_2185.PointLoad':
        '''PointLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.PointLoad.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PointLoad. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_power_load(self) -> '_2186.PowerLoad':
        '''PowerLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2186.PowerLoad.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PowerLoad. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_unbalanced_mass(self) -> '_2191.UnbalancedMass':
        '''UnbalancedMass: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2191.UnbalancedMass.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to UnbalancedMass. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_virtual_component(self) -> '_2193.VirtualComponent':
        '''VirtualComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2193.VirtualComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to VirtualComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_shaft(self) -> '_2196.Shaft':
        '''Shaft: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.Shaft.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Shaft. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_agma_gleason_conical_gear(self) -> '_2226.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.AGMAGleasonConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_bevel_differential_gear(self) -> '_2228.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.BevelDifferentialGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_bevel_differential_planet_gear(self) -> '_2230.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2230.BevelDifferentialPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_bevel_differential_sun_gear(self) -> '_2231.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2231.BevelDifferentialSunGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_bevel_gear(self) -> '_2232.BevelGear':
        '''BevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2232.BevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_concept_gear(self) -> '_2234.ConceptGear':
        '''ConceptGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2234.ConceptGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_conical_gear(self) -> '_2236.ConicalGear':
        '''ConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2236.ConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_cylindrical_gear(self) -> '_2238.CylindricalGear':
        '''CylindricalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2238.CylindricalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_cylindrical_planet_gear(self) -> '_2240.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2240.CylindricalPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_face_gear(self) -> '_2241.FaceGear':
        '''FaceGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2241.FaceGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to FaceGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_gear(self) -> '_2243.Gear':
        '''Gear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2243.Gear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Gear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_hypoid_gear(self) -> '_2247.HypoidGear':
        '''HypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.HypoidGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to HypoidGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2249.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2249.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2251.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2251.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2253.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2253.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_spiral_bevel_gear(self) -> '_2256.SpiralBevelGear':
        '''SpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.SpiralBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_straight_bevel_diff_gear(self) -> '_2258.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.StraightBevelDiffGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_straight_bevel_gear(self) -> '_2260.StraightBevelGear':
        '''StraightBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.StraightBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_straight_bevel_planet_gear(self) -> '_2262.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.StraightBevelPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_straight_bevel_sun_gear(self) -> '_2263.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2263.StraightBevelSunGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_worm_gear(self) -> '_2264.WormGear':
        '''WormGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.WormGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to WormGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_zerol_bevel_gear(self) -> '_2266.ZerolBevelGear':
        '''ZerolBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2266.ZerolBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_cycloidal_disc(self) -> '_2282.CycloidalDisc':
        '''CycloidalDisc: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2282.CycloidalDisc.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CycloidalDisc. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_ring_pins(self) -> '_2283.RingPins':
        '''RingPins: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.RingPins.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to RingPins. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_clutch_half(self) -> '_2292.ClutchHalf':
        '''ClutchHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2292.ClutchHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ClutchHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_concept_coupling_half(self) -> '_2295.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2295.ConceptCouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_coupling_half(self) -> '_2297.CouplingHalf':
        '''CouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2297.CouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_cvt_pulley(self) -> '_2300.CVTPulley':
        '''CVTPulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2300.CVTPulley.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CVTPulley. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_part_to_part_shear_coupling_half(self) -> '_2302.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2302.PartToPartShearCouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_pulley(self) -> '_2303.Pulley':
        '''Pulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2303.Pulley.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Pulley. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_rolling_ring(self) -> '_2309.RollingRing':
        '''RollingRing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2309.RollingRing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to RollingRing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_shaft_hub_connection(self) -> '_2311.ShaftHubConnection':
        '''ShaftHubConnection: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2311.ShaftHubConnection.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_spring_damper_half(self) -> '_2314.SpringDamperHalf':
        '''SpringDamperHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2314.SpringDamperHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_synchroniser_half(self) -> '_2317.SynchroniserHalf':
        '''SynchroniserHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.SynchroniserHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_synchroniser_part(self) -> '_2318.SynchroniserPart':
        '''SynchroniserPart: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2318.SynchroniserPart.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserPart. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_synchroniser_sleeve(self) -> '_2319.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2319.SynchroniserSleeve.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_torque_converter_pump(self) -> '_2321.TorqueConverterPump':
        '''TorqueConverterPump: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2321.TorqueConverterPump.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    @property
    def connected_component_of_type_torque_converter_turbine(self) -> '_2323.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2323.TorqueConverterTurbine.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectedComponent.__class__)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent is not None else None

    def delete(self):
        ''' 'Delete' is the original name of this method.'''

        self.wrapped.Delete()

    def swap(self):
        ''' 'Swap' is the original name of this method.'''

        self.wrapped.Swap()
