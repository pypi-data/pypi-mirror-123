'''_5739.py

PartHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import (
    _2182, _2149, _2150, _2151,
    _2152, _2155, _2157, _2158,
    _2159, _2162, _2163, _2166,
    _2167, _2168, _2169, _2176,
    _2177, _2178, _2180, _2183,
    _2185, _2186, _2188, _2190,
    _2191, _2193
)
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2196
from mastapy.system_model.part_model.gears import (
    _2226, _2227, _2228, _2229,
    _2230, _2231, _2232, _2233,
    _2234, _2235, _2236, _2237,
    _2238, _2239, _2240, _2241,
    _2242, _2243, _2245, _2247,
    _2248, _2249, _2250, _2251,
    _2252, _2253, _2254, _2255,
    _2256, _2257, _2258, _2259,
    _2260, _2261, _2262, _2263,
    _2264, _2265, _2266, _2267
)
from mastapy.system_model.part_model.cycloidal import _2281, _2282, _2283
from mastapy.system_model.part_model.couplings import (
    _2289, _2291, _2292, _2294,
    _2295, _2296, _2297, _2299,
    _2300, _2301, _2302, _2303,
    _2309, _2310, _2311, _2313,
    _2314, _2315, _2317, _2318,
    _2319, _2320, _2321, _2323
)
from mastapy.system_model.analyses_and_results.harmonic_analyses import _2345, _2346, _5719
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6763
from mastapy.system_model.analyses_and_results.modal_analyses import (
    _4878, _4793, _4794, _4795,
    _4798, _4799, _4800, _4801,
    _4803, _4805, _4806, _4807,
    _4808, _4810, _4811, _4812,
    _4813, _4815, _4816, _4818,
    _4820, _4821, _4823, _4824,
    _4826, _4827, _4829, _4832,
    _4833, _4835, _4836, _4837,
    _4839, _4842, _4843, _4844,
    _4845, _4846, _4848, _4849,
    _4850, _4851, _4854, _4855,
    _4856, _4858, _4859, _4862,
    _4863, _4865, _4866, _4868,
    _4869, _4870, _4871, _4875,
    _4876, _4880, _4881, _4883,
    _4884, _4885, _4886, _4887,
    _4888, _4890, _4892, _4893,
    _4894, _4895, _4898, _4900,
    _4901, _4903, _4904, _4906,
    _4907, _4909, _4910, _4911,
    _4912, _4913, _4914, _4915,
    _4916, _4918, _4919, _4920,
    _4921, _4922, _4929, _4930,
    _4932, _4933
)
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5438
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2493, _2398, _2399, _2400,
    _2403, _2404, _2405, _2406,
    _2408, _2410, _2411, _2412,
    _2413, _2415, _2416, _2417,
    _2418, _2420, _2421, _2423,
    _2426, _2427, _2429, _2430,
    _2433, _2434, _2436, _2438,
    _2439, _2441, _2442, _2443,
    _2446, _2450, _2451, _2452,
    _2453, _2454, _2455, _2458,
    _2459, _2460, _2463, _2464,
    _2465, _2466, _2468, _2469,
    _2470, _2472, _2473, _2477,
    _2478, _2480, _2481, _2483,
    _2484, _2487, _2488, _2490,
    _2492, _2495, _2496, _2498,
    _2499, _2500, _2501, _2502,
    _2505, _2507, _2508, _2509,
    _2512, _2514, _2516, _2517,
    _2519, _2520, _2522, _2523,
    _2525, _2526, _2527, _2528,
    _2529, _2530, _2531, _2532,
    _2537, _2538, _2539, _2542,
    _2543, _2545, _2546, _2548,
    _2549
)
from mastapy.system_model.drawing import _1963
from mastapy.system_model.analyses_and_results.analysis_cases import _7238
from mastapy._internal.python_net import python_net_import

_PART_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'PartHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartHarmonicAnalysis',)


class PartHarmonicAnalysis(_7238.PartStaticLoadAnalysisCase):
    '''PartHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2182.Part':
        '''Part: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2182.Part.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Part. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_assembly(self) -> '_2149.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_abstract_assembly(self) -> '_2150.AbstractAssembly':
        '''AbstractAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2150.AbstractAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_abstract_shaft(self) -> '_2151.AbstractShaft':
        '''AbstractShaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.AbstractShaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_abstract_shaft_or_housing(self) -> '_2152.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2152.AbstractShaftOrHousing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_bearing(self) -> '_2155.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2155.Bearing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Bearing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_bolt(self) -> '_2157.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2157.Bolt.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Bolt. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_bolted_joint(self) -> '_2158.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2158.BoltedJoint.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BoltedJoint. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_component(self) -> '_2159.Component':
        '''Component: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.Component.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Component. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_connector(self) -> '_2162.Connector':
        '''Connector: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2162.Connector.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Connector. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_datum(self) -> '_2163.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.Datum.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Datum. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_external_cad_model(self) -> '_2166.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2166.ExternalCADModel.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ExternalCADModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_fe_part(self) -> '_2167.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2167.FEPart.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FEPart. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_flexible_pin_assembly(self) -> '_2168.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2168.FlexiblePinAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_guide_dxf_model(self) -> '_2169.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2169.GuideDxfModel.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to GuideDxfModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_mass_disc(self) -> '_2176.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2176.MassDisc.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MassDisc. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_measurement_component(self) -> '_2177.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.MeasurementComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MeasurementComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_mountable_component(self) -> '_2178.MountableComponent':
        '''MountableComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2178.MountableComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MountableComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_oil_seal(self) -> '_2180.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2180.OilSeal.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to OilSeal. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_planet_carrier(self) -> '_2183.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2183.PlanetCarrier.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PlanetCarrier. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_point_load(self) -> '_2185.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.PointLoad.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PointLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_power_load(self) -> '_2186.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2186.PowerLoad.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PowerLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_root_assembly(self) -> '_2188.RootAssembly':
        '''RootAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2188.RootAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RootAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_specialised_assembly(self) -> '_2190.SpecialisedAssembly':
        '''SpecialisedAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2190.SpecialisedAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpecialisedAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_unbalanced_mass(self) -> '_2191.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2191.UnbalancedMass.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to UnbalancedMass. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_virtual_component(self) -> '_2193.VirtualComponent':
        '''VirtualComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2193.VirtualComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to VirtualComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_shaft(self) -> '_2196.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.Shaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_agma_gleason_conical_gear(self) -> '_2226.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.AGMAGleasonConicalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_agma_gleason_conical_gear_set(self) -> '_2227.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2227.AGMAGleasonConicalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_bevel_differential_gear(self) -> '_2228.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.BevelDifferentialGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_bevel_differential_gear_set(self) -> '_2229.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2229.BevelDifferentialGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_bevel_differential_planet_gear(self) -> '_2230.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2230.BevelDifferentialPlanetGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_bevel_differential_sun_gear(self) -> '_2231.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2231.BevelDifferentialSunGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_bevel_gear(self) -> '_2232.BevelGear':
        '''BevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2232.BevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_bevel_gear_set(self) -> '_2233.BevelGearSet':
        '''BevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2233.BevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_concept_gear(self) -> '_2234.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2234.ConceptGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_concept_gear_set(self) -> '_2235.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2235.ConceptGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_conical_gear(self) -> '_2236.ConicalGear':
        '''ConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2236.ConicalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConicalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_conical_gear_set(self) -> '_2237.ConicalGearSet':
        '''ConicalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2237.ConicalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConicalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_cylindrical_gear(self) -> '_2238.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2238.CylindricalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_cylindrical_gear_set(self) -> '_2239.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2239.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_cylindrical_planet_gear(self) -> '_2240.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2240.CylindricalPlanetGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_face_gear(self) -> '_2241.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2241.FaceGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FaceGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_face_gear_set(self) -> '_2242.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2242.FaceGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FaceGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_gear(self) -> '_2243.Gear':
        '''Gear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2243.Gear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Gear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_gear_set(self) -> '_2245.GearSet':
        '''GearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2245.GearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to GearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_hypoid_gear(self) -> '_2247.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.HypoidGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to HypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_hypoid_gear_set(self) -> '_2248.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2248.HypoidGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to HypoidGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2249.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2249.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2250.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2251.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2251.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2252.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2253.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2253.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2254.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_planetary_gear_set(self) -> '_2255.PlanetaryGearSet':
        '''PlanetaryGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2255.PlanetaryGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_spiral_bevel_gear(self) -> '_2256.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.SpiralBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_spiral_bevel_gear_set(self) -> '_2257.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2257.SpiralBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_straight_bevel_diff_gear(self) -> '_2258.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.StraightBevelDiffGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_straight_bevel_diff_gear_set(self) -> '_2259.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2259.StraightBevelDiffGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_straight_bevel_gear(self) -> '_2260.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.StraightBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_straight_bevel_gear_set(self) -> '_2261.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.StraightBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_straight_bevel_planet_gear(self) -> '_2262.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.StraightBevelPlanetGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_straight_bevel_sun_gear(self) -> '_2263.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2263.StraightBevelSunGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_worm_gear(self) -> '_2264.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.WormGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to WormGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_worm_gear_set(self) -> '_2265.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.WormGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to WormGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_zerol_bevel_gear(self) -> '_2266.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2266.ZerolBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_zerol_bevel_gear_set(self) -> '_2267.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2267.ZerolBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_cycloidal_assembly(self) -> '_2281.CycloidalAssembly':
        '''CycloidalAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2281.CycloidalAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_cycloidal_disc(self) -> '_2282.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2282.CycloidalDisc.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDisc. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_ring_pins(self) -> '_2283.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.RingPins.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RingPins. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_belt_drive(self) -> '_2289.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2289.BeltDrive.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BeltDrive. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_clutch(self) -> '_2291.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2291.Clutch.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Clutch. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_clutch_half(self) -> '_2292.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2292.ClutchHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ClutchHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_concept_coupling(self) -> '_2294.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2294.ConceptCoupling.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCoupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_concept_coupling_half(self) -> '_2295.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2295.ConceptCouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_coupling(self) -> '_2296.Coupling':
        '''Coupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2296.Coupling.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Coupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_coupling_half(self) -> '_2297.CouplingHalf':
        '''CouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2297.CouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_cvt(self) -> '_2299.CVT':
        '''CVT: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2299.CVT.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVT. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_cvt_pulley(self) -> '_2300.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2300.CVTPulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVTPulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_part_to_part_shear_coupling(self) -> '_2301.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2301.PartToPartShearCoupling.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCoupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_part_to_part_shear_coupling_half(self) -> '_2302.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2302.PartToPartShearCouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_pulley(self) -> '_2303.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2303.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_rolling_ring(self) -> '_2309.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2309.RollingRing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_rolling_ring_assembly(self) -> '_2310.RollingRingAssembly':
        '''RollingRingAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2310.RollingRingAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRingAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_shaft_hub_connection(self) -> '_2311.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2311.ShaftHubConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_spring_damper(self) -> '_2313.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2313.SpringDamper.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamper. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_spring_damper_half(self) -> '_2314.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2314.SpringDamperHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_synchroniser(self) -> '_2315.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2315.Synchroniser.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Synchroniser. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_synchroniser_half(self) -> '_2317.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.SynchroniserHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_synchroniser_part(self) -> '_2318.SynchroniserPart':
        '''SynchroniserPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2318.SynchroniserPart.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserPart. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_synchroniser_sleeve(self) -> '_2319.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2319.SynchroniserSleeve.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_torque_converter(self) -> '_2320.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2320.TorqueConverter.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverter. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_torque_converter_pump(self) -> '_2321.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2321.TorqueConverterPump.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_design_of_type_torque_converter_turbine(self) -> '_2323.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2323.TorqueConverterTurbine.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def harmonic_analysis(self) -> '_2345.HarmonicAnalysis':
        '''HarmonicAnalysis: 'HarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2345.HarmonicAnalysis.TYPE not in self.wrapped.HarmonicAnalysis.__class__.__mro__:
            raise CastException('Failed to cast harmonic_analysis to HarmonicAnalysis. Expected: {}.'.format(self.wrapped.HarmonicAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicAnalysis.__class__)(self.wrapped.HarmonicAnalysis) if self.wrapped.HarmonicAnalysis is not None else None

    @property
    def harmonic_analysis_options(self) -> '_5719.HarmonicAnalysisOptions':
        '''HarmonicAnalysisOptions: 'HarmonicAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5719.HarmonicAnalysisOptions.TYPE not in self.wrapped.HarmonicAnalysisOptions.__class__.__mro__:
            raise CastException('Failed to cast harmonic_analysis_options to HarmonicAnalysisOptions. Expected: {}.'.format(self.wrapped.HarmonicAnalysisOptions.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicAnalysisOptions.__class__)(self.wrapped.HarmonicAnalysisOptions) if self.wrapped.HarmonicAnalysisOptions is not None else None

    @property
    def coupled_modal_analysis(self) -> '_4878.PartModalAnalysis':
        '''PartModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4878.PartModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to PartModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_abstract_assembly_modal_analysis(self) -> '_4793.AbstractAssemblyModalAnalysis':
        '''AbstractAssemblyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4793.AbstractAssemblyModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to AbstractAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_abstract_shaft_modal_analysis(self) -> '_4794.AbstractShaftModalAnalysis':
        '''AbstractShaftModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4794.AbstractShaftModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to AbstractShaftModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_abstract_shaft_or_housing_modal_analysis(self) -> '_4795.AbstractShaftOrHousingModalAnalysis':
        '''AbstractShaftOrHousingModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4795.AbstractShaftOrHousingModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to AbstractShaftOrHousingModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_agma_gleason_conical_gear_modal_analysis(self) -> '_4798.AGMAGleasonConicalGearModalAnalysis':
        '''AGMAGleasonConicalGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4798.AGMAGleasonConicalGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to AGMAGleasonConicalGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_agma_gleason_conical_gear_set_modal_analysis(self) -> '_4799.AGMAGleasonConicalGearSetModalAnalysis':
        '''AGMAGleasonConicalGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4799.AGMAGleasonConicalGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to AGMAGleasonConicalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_assembly_modal_analysis(self) -> '_4800.AssemblyModalAnalysis':
        '''AssemblyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4800.AssemblyModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to AssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_bearing_modal_analysis(self) -> '_4801.BearingModalAnalysis':
        '''BearingModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4801.BearingModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BearingModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_belt_drive_modal_analysis(self) -> '_4803.BeltDriveModalAnalysis':
        '''BeltDriveModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4803.BeltDriveModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BeltDriveModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_bevel_differential_gear_modal_analysis(self) -> '_4805.BevelDifferentialGearModalAnalysis':
        '''BevelDifferentialGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4805.BevelDifferentialGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BevelDifferentialGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_bevel_differential_gear_set_modal_analysis(self) -> '_4806.BevelDifferentialGearSetModalAnalysis':
        '''BevelDifferentialGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4806.BevelDifferentialGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BevelDifferentialGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_bevel_differential_planet_gear_modal_analysis(self) -> '_4807.BevelDifferentialPlanetGearModalAnalysis':
        '''BevelDifferentialPlanetGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4807.BevelDifferentialPlanetGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BevelDifferentialPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_bevel_differential_sun_gear_modal_analysis(self) -> '_4808.BevelDifferentialSunGearModalAnalysis':
        '''BevelDifferentialSunGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4808.BevelDifferentialSunGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BevelDifferentialSunGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_bevel_gear_modal_analysis(self) -> '_4810.BevelGearModalAnalysis':
        '''BevelGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4810.BevelGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_bevel_gear_set_modal_analysis(self) -> '_4811.BevelGearSetModalAnalysis':
        '''BevelGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4811.BevelGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_bolted_joint_modal_analysis(self) -> '_4812.BoltedJointModalAnalysis':
        '''BoltedJointModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4812.BoltedJointModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BoltedJointModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_bolt_modal_analysis(self) -> '_4813.BoltModalAnalysis':
        '''BoltModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4813.BoltModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to BoltModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_clutch_half_modal_analysis(self) -> '_4815.ClutchHalfModalAnalysis':
        '''ClutchHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4815.ClutchHalfModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ClutchHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_clutch_modal_analysis(self) -> '_4816.ClutchModalAnalysis':
        '''ClutchModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4816.ClutchModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ClutchModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_component_modal_analysis(self) -> '_4818.ComponentModalAnalysis':
        '''ComponentModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4818.ComponentModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ComponentModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_concept_coupling_half_modal_analysis(self) -> '_4820.ConceptCouplingHalfModalAnalysis':
        '''ConceptCouplingHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4820.ConceptCouplingHalfModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ConceptCouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_concept_coupling_modal_analysis(self) -> '_4821.ConceptCouplingModalAnalysis':
        '''ConceptCouplingModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4821.ConceptCouplingModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ConceptCouplingModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_concept_gear_modal_analysis(self) -> '_4823.ConceptGearModalAnalysis':
        '''ConceptGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4823.ConceptGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ConceptGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_concept_gear_set_modal_analysis(self) -> '_4824.ConceptGearSetModalAnalysis':
        '''ConceptGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4824.ConceptGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ConceptGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_conical_gear_modal_analysis(self) -> '_4826.ConicalGearModalAnalysis':
        '''ConicalGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4826.ConicalGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ConicalGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_conical_gear_set_modal_analysis(self) -> '_4827.ConicalGearSetModalAnalysis':
        '''ConicalGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4827.ConicalGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ConicalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_connector_modal_analysis(self) -> '_4829.ConnectorModalAnalysis':
        '''ConnectorModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4829.ConnectorModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ConnectorModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_coupling_half_modal_analysis(self) -> '_4832.CouplingHalfModalAnalysis':
        '''CouplingHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4832.CouplingHalfModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to CouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_coupling_modal_analysis(self) -> '_4833.CouplingModalAnalysis':
        '''CouplingModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4833.CouplingModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to CouplingModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_cvt_modal_analysis(self) -> '_4835.CVTModalAnalysis':
        '''CVTModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4835.CVTModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to CVTModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_cvt_pulley_modal_analysis(self) -> '_4836.CVTPulleyModalAnalysis':
        '''CVTPulleyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4836.CVTPulleyModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to CVTPulleyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_cycloidal_assembly_modal_analysis(self) -> '_4837.CycloidalAssemblyModalAnalysis':
        '''CycloidalAssemblyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4837.CycloidalAssemblyModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to CycloidalAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_cycloidal_disc_modal_analysis(self) -> '_4839.CycloidalDiscModalAnalysis':
        '''CycloidalDiscModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4839.CycloidalDiscModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to CycloidalDiscModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_cylindrical_gear_modal_analysis(self) -> '_4842.CylindricalGearModalAnalysis':
        '''CylindricalGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4842.CylindricalGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to CylindricalGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_cylindrical_gear_set_modal_analysis(self) -> '_4843.CylindricalGearSetModalAnalysis':
        '''CylindricalGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4843.CylindricalGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to CylindricalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_cylindrical_planet_gear_modal_analysis(self) -> '_4844.CylindricalPlanetGearModalAnalysis':
        '''CylindricalPlanetGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4844.CylindricalPlanetGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to CylindricalPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_datum_modal_analysis(self) -> '_4845.DatumModalAnalysis':
        '''DatumModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4845.DatumModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to DatumModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_external_cad_model_modal_analysis(self) -> '_4846.ExternalCADModelModalAnalysis':
        '''ExternalCADModelModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4846.ExternalCADModelModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ExternalCADModelModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_face_gear_modal_analysis(self) -> '_4848.FaceGearModalAnalysis':
        '''FaceGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4848.FaceGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to FaceGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_face_gear_set_modal_analysis(self) -> '_4849.FaceGearSetModalAnalysis':
        '''FaceGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4849.FaceGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to FaceGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_fe_part_modal_analysis(self) -> '_4850.FEPartModalAnalysis':
        '''FEPartModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4850.FEPartModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to FEPartModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_flexible_pin_assembly_modal_analysis(self) -> '_4851.FlexiblePinAssemblyModalAnalysis':
        '''FlexiblePinAssemblyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4851.FlexiblePinAssemblyModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to FlexiblePinAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_gear_modal_analysis(self) -> '_4854.GearModalAnalysis':
        '''GearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4854.GearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to GearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_gear_set_modal_analysis(self) -> '_4855.GearSetModalAnalysis':
        '''GearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4855.GearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to GearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_guide_dxf_model_modal_analysis(self) -> '_4856.GuideDxfModelModalAnalysis':
        '''GuideDxfModelModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4856.GuideDxfModelModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to GuideDxfModelModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_hypoid_gear_modal_analysis(self) -> '_4858.HypoidGearModalAnalysis':
        '''HypoidGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4858.HypoidGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to HypoidGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_hypoid_gear_set_modal_analysis(self) -> '_4859.HypoidGearSetModalAnalysis':
        '''HypoidGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4859.HypoidGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to HypoidGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_conical_gear_modal_analysis(self) -> '_4862.KlingelnbergCycloPalloidConicalGearModalAnalysis':
        '''KlingelnbergCycloPalloidConicalGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4862.KlingelnbergCycloPalloidConicalGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to KlingelnbergCycloPalloidConicalGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis(self) -> '_4863.KlingelnbergCycloPalloidConicalGearSetModalAnalysis':
        '''KlingelnbergCycloPalloidConicalGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4863.KlingelnbergCycloPalloidConicalGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to KlingelnbergCycloPalloidConicalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis(self) -> '_4865.KlingelnbergCycloPalloidHypoidGearModalAnalysis':
        '''KlingelnbergCycloPalloidHypoidGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4865.KlingelnbergCycloPalloidHypoidGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to KlingelnbergCycloPalloidHypoidGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis(self) -> '_4866.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis':
        '''KlingelnbergCycloPalloidHypoidGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4866.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to KlingelnbergCycloPalloidHypoidGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis(self) -> '_4868.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis':
        '''KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4868.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis(self) -> '_4869.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4869.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_mass_disc_modal_analysis(self) -> '_4870.MassDiscModalAnalysis':
        '''MassDiscModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4870.MassDiscModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to MassDiscModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_measurement_component_modal_analysis(self) -> '_4871.MeasurementComponentModalAnalysis':
        '''MeasurementComponentModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4871.MeasurementComponentModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to MeasurementComponentModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_mountable_component_modal_analysis(self) -> '_4875.MountableComponentModalAnalysis':
        '''MountableComponentModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4875.MountableComponentModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to MountableComponentModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_oil_seal_modal_analysis(self) -> '_4876.OilSealModalAnalysis':
        '''OilSealModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4876.OilSealModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to OilSealModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_part_to_part_shear_coupling_half_modal_analysis(self) -> '_4880.PartToPartShearCouplingHalfModalAnalysis':
        '''PartToPartShearCouplingHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4880.PartToPartShearCouplingHalfModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to PartToPartShearCouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_part_to_part_shear_coupling_modal_analysis(self) -> '_4881.PartToPartShearCouplingModalAnalysis':
        '''PartToPartShearCouplingModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4881.PartToPartShearCouplingModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to PartToPartShearCouplingModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_planetary_gear_set_modal_analysis(self) -> '_4883.PlanetaryGearSetModalAnalysis':
        '''PlanetaryGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4883.PlanetaryGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to PlanetaryGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_planet_carrier_modal_analysis(self) -> '_4884.PlanetCarrierModalAnalysis':
        '''PlanetCarrierModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4884.PlanetCarrierModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to PlanetCarrierModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_point_load_modal_analysis(self) -> '_4885.PointLoadModalAnalysis':
        '''PointLoadModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4885.PointLoadModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to PointLoadModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_power_load_modal_analysis(self) -> '_4886.PowerLoadModalAnalysis':
        '''PowerLoadModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4886.PowerLoadModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to PowerLoadModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_pulley_modal_analysis(self) -> '_4887.PulleyModalAnalysis':
        '''PulleyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4887.PulleyModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to PulleyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_ring_pins_modal_analysis(self) -> '_4888.RingPinsModalAnalysis':
        '''RingPinsModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4888.RingPinsModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to RingPinsModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_rolling_ring_assembly_modal_analysis(self) -> '_4890.RollingRingAssemblyModalAnalysis':
        '''RollingRingAssemblyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4890.RollingRingAssemblyModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to RollingRingAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_rolling_ring_modal_analysis(self) -> '_4892.RollingRingModalAnalysis':
        '''RollingRingModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4892.RollingRingModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to RollingRingModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_root_assembly_modal_analysis(self) -> '_4893.RootAssemblyModalAnalysis':
        '''RootAssemblyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4893.RootAssemblyModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to RootAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_shaft_hub_connection_modal_analysis(self) -> '_4894.ShaftHubConnectionModalAnalysis':
        '''ShaftHubConnectionModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4894.ShaftHubConnectionModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ShaftHubConnectionModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_shaft_modal_analysis(self) -> '_4895.ShaftModalAnalysis':
        '''ShaftModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4895.ShaftModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ShaftModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_specialised_assembly_modal_analysis(self) -> '_4898.SpecialisedAssemblyModalAnalysis':
        '''SpecialisedAssemblyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4898.SpecialisedAssemblyModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to SpecialisedAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_spiral_bevel_gear_modal_analysis(self) -> '_4900.SpiralBevelGearModalAnalysis':
        '''SpiralBevelGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4900.SpiralBevelGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to SpiralBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_spiral_bevel_gear_set_modal_analysis(self) -> '_4901.SpiralBevelGearSetModalAnalysis':
        '''SpiralBevelGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4901.SpiralBevelGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to SpiralBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_spring_damper_half_modal_analysis(self) -> '_4903.SpringDamperHalfModalAnalysis':
        '''SpringDamperHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4903.SpringDamperHalfModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to SpringDamperHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_spring_damper_modal_analysis(self) -> '_4904.SpringDamperModalAnalysis':
        '''SpringDamperModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4904.SpringDamperModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to SpringDamperModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_diff_gear_modal_analysis(self) -> '_4906.StraightBevelDiffGearModalAnalysis':
        '''StraightBevelDiffGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4906.StraightBevelDiffGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelDiffGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_diff_gear_set_modal_analysis(self) -> '_4907.StraightBevelDiffGearSetModalAnalysis':
        '''StraightBevelDiffGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4907.StraightBevelDiffGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelDiffGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_gear_modal_analysis(self) -> '_4909.StraightBevelGearModalAnalysis':
        '''StraightBevelGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4909.StraightBevelGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_gear_set_modal_analysis(self) -> '_4910.StraightBevelGearSetModalAnalysis':
        '''StraightBevelGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4910.StraightBevelGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_planet_gear_modal_analysis(self) -> '_4911.StraightBevelPlanetGearModalAnalysis':
        '''StraightBevelPlanetGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4911.StraightBevelPlanetGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_sun_gear_modal_analysis(self) -> '_4912.StraightBevelSunGearModalAnalysis':
        '''StraightBevelSunGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4912.StraightBevelSunGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelSunGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_synchroniser_half_modal_analysis(self) -> '_4913.SynchroniserHalfModalAnalysis':
        '''SynchroniserHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4913.SynchroniserHalfModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to SynchroniserHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_synchroniser_modal_analysis(self) -> '_4914.SynchroniserModalAnalysis':
        '''SynchroniserModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4914.SynchroniserModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to SynchroniserModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_synchroniser_part_modal_analysis(self) -> '_4915.SynchroniserPartModalAnalysis':
        '''SynchroniserPartModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4915.SynchroniserPartModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to SynchroniserPartModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_synchroniser_sleeve_modal_analysis(self) -> '_4916.SynchroniserSleeveModalAnalysis':
        '''SynchroniserSleeveModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4916.SynchroniserSleeveModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to SynchroniserSleeveModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_torque_converter_modal_analysis(self) -> '_4918.TorqueConverterModalAnalysis':
        '''TorqueConverterModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4918.TorqueConverterModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to TorqueConverterModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_torque_converter_pump_modal_analysis(self) -> '_4919.TorqueConverterPumpModalAnalysis':
        '''TorqueConverterPumpModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4919.TorqueConverterPumpModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to TorqueConverterPumpModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_torque_converter_turbine_modal_analysis(self) -> '_4920.TorqueConverterTurbineModalAnalysis':
        '''TorqueConverterTurbineModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4920.TorqueConverterTurbineModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to TorqueConverterTurbineModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_unbalanced_mass_modal_analysis(self) -> '_4921.UnbalancedMassModalAnalysis':
        '''UnbalancedMassModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4921.UnbalancedMassModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to UnbalancedMassModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_virtual_component_modal_analysis(self) -> '_4922.VirtualComponentModalAnalysis':
        '''VirtualComponentModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4922.VirtualComponentModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to VirtualComponentModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_worm_gear_modal_analysis(self) -> '_4929.WormGearModalAnalysis':
        '''WormGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4929.WormGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to WormGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_worm_gear_set_modal_analysis(self) -> '_4930.WormGearSetModalAnalysis':
        '''WormGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4930.WormGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to WormGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_zerol_bevel_gear_modal_analysis(self) -> '_4932.ZerolBevelGearModalAnalysis':
        '''ZerolBevelGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4932.ZerolBevelGearModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ZerolBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def coupled_modal_analysis_of_type_zerol_bevel_gear_set_modal_analysis(self) -> '_4933.ZerolBevelGearSetModalAnalysis':
        '''ZerolBevelGearSetModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4933.ZerolBevelGearSetModalAnalysis.TYPE not in self.wrapped.CoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast coupled_modal_analysis to ZerolBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CoupledModalAnalysis.__class__)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def harmonic_analyses_of_single_excitations(self) -> 'List[_5438.HarmonicAnalysisOfSingleExcitation]':
        '''List[HarmonicAnalysisOfSingleExcitation]: 'HarmonicAnalysesOfSingleExcitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HarmonicAnalysesOfSingleExcitations, constructor.new(_5438.HarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def system_deflection_results(self) -> '_2493.PartSystemDeflection':
        '''PartSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2493.PartSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to PartSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_abstract_assembly_system_deflection(self) -> '_2398.AbstractAssemblySystemDeflection':
        '''AbstractAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2398.AbstractAssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AbstractAssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_abstract_shaft_or_housing_system_deflection(self) -> '_2399.AbstractShaftOrHousingSystemDeflection':
        '''AbstractShaftOrHousingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2399.AbstractShaftOrHousingSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AbstractShaftOrHousingSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_abstract_shaft_system_deflection(self) -> '_2400.AbstractShaftSystemDeflection':
        '''AbstractShaftSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2400.AbstractShaftSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AbstractShaftSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_agma_gleason_conical_gear_set_system_deflection(self) -> '_2403.AGMAGleasonConicalGearSetSystemDeflection':
        '''AGMAGleasonConicalGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2403.AGMAGleasonConicalGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AGMAGleasonConicalGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_agma_gleason_conical_gear_system_deflection(self) -> '_2404.AGMAGleasonConicalGearSystemDeflection':
        '''AGMAGleasonConicalGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2404.AGMAGleasonConicalGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AGMAGleasonConicalGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_assembly_system_deflection(self) -> '_2405.AssemblySystemDeflection':
        '''AssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2405.AssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_bearing_system_deflection(self) -> '_2406.BearingSystemDeflection':
        '''BearingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2406.BearingSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BearingSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_belt_drive_system_deflection(self) -> '_2408.BeltDriveSystemDeflection':
        '''BeltDriveSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2408.BeltDriveSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BeltDriveSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_bevel_differential_gear_set_system_deflection(self) -> '_2410.BevelDifferentialGearSetSystemDeflection':
        '''BevelDifferentialGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2410.BevelDifferentialGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BevelDifferentialGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_bevel_differential_gear_system_deflection(self) -> '_2411.BevelDifferentialGearSystemDeflection':
        '''BevelDifferentialGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2411.BevelDifferentialGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BevelDifferentialGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_bevel_differential_planet_gear_system_deflection(self) -> '_2412.BevelDifferentialPlanetGearSystemDeflection':
        '''BevelDifferentialPlanetGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2412.BevelDifferentialPlanetGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BevelDifferentialPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_bevel_differential_sun_gear_system_deflection(self) -> '_2413.BevelDifferentialSunGearSystemDeflection':
        '''BevelDifferentialSunGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2413.BevelDifferentialSunGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BevelDifferentialSunGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_bevel_gear_set_system_deflection(self) -> '_2415.BevelGearSetSystemDeflection':
        '''BevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2415.BevelGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BevelGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_bevel_gear_system_deflection(self) -> '_2416.BevelGearSystemDeflection':
        '''BevelGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2416.BevelGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_bolted_joint_system_deflection(self) -> '_2417.BoltedJointSystemDeflection':
        '''BoltedJointSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2417.BoltedJointSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BoltedJointSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_bolt_system_deflection(self) -> '_2418.BoltSystemDeflection':
        '''BoltSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2418.BoltSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BoltSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_clutch_half_system_deflection(self) -> '_2420.ClutchHalfSystemDeflection':
        '''ClutchHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2420.ClutchHalfSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ClutchHalfSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_clutch_system_deflection(self) -> '_2421.ClutchSystemDeflection':
        '''ClutchSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2421.ClutchSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ClutchSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_component_system_deflection(self) -> '_2423.ComponentSystemDeflection':
        '''ComponentSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2423.ComponentSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ComponentSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_concept_coupling_half_system_deflection(self) -> '_2426.ConceptCouplingHalfSystemDeflection':
        '''ConceptCouplingHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2426.ConceptCouplingHalfSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ConceptCouplingHalfSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_concept_coupling_system_deflection(self) -> '_2427.ConceptCouplingSystemDeflection':
        '''ConceptCouplingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2427.ConceptCouplingSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ConceptCouplingSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_concept_gear_set_system_deflection(self) -> '_2429.ConceptGearSetSystemDeflection':
        '''ConceptGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2429.ConceptGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ConceptGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_concept_gear_system_deflection(self) -> '_2430.ConceptGearSystemDeflection':
        '''ConceptGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2430.ConceptGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ConceptGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_conical_gear_set_system_deflection(self) -> '_2433.ConicalGearSetSystemDeflection':
        '''ConicalGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2433.ConicalGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ConicalGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_conical_gear_system_deflection(self) -> '_2434.ConicalGearSystemDeflection':
        '''ConicalGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2434.ConicalGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ConicalGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_connector_system_deflection(self) -> '_2436.ConnectorSystemDeflection':
        '''ConnectorSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2436.ConnectorSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ConnectorSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_coupling_half_system_deflection(self) -> '_2438.CouplingHalfSystemDeflection':
        '''CouplingHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2438.CouplingHalfSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CouplingHalfSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_coupling_system_deflection(self) -> '_2439.CouplingSystemDeflection':
        '''CouplingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2439.CouplingSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CouplingSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cvt_pulley_system_deflection(self) -> '_2441.CVTPulleySystemDeflection':
        '''CVTPulleySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2441.CVTPulleySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CVTPulleySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cvt_system_deflection(self) -> '_2442.CVTSystemDeflection':
        '''CVTSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2442.CVTSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CVTSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cycloidal_assembly_system_deflection(self) -> '_2443.CycloidalAssemblySystemDeflection':
        '''CycloidalAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2443.CycloidalAssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CycloidalAssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cycloidal_disc_system_deflection(self) -> '_2446.CycloidalDiscSystemDeflection':
        '''CycloidalDiscSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2446.CycloidalDiscSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CycloidalDiscSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_set_system_deflection(self) -> '_2450.CylindricalGearSetSystemDeflection':
        '''CylindricalGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2450.CylindricalGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CylindricalGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_set_system_deflection_timestep(self) -> '_2451.CylindricalGearSetSystemDeflectionTimestep':
        '''CylindricalGearSetSystemDeflectionTimestep: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2451.CylindricalGearSetSystemDeflectionTimestep.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CylindricalGearSetSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_set_system_deflection_with_ltca_results(self) -> '_2452.CylindricalGearSetSystemDeflectionWithLTCAResults':
        '''CylindricalGearSetSystemDeflectionWithLTCAResults: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2452.CylindricalGearSetSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CylindricalGearSetSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_system_deflection(self) -> '_2453.CylindricalGearSystemDeflection':
        '''CylindricalGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2453.CylindricalGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CylindricalGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_system_deflection_timestep(self) -> '_2454.CylindricalGearSystemDeflectionTimestep':
        '''CylindricalGearSystemDeflectionTimestep: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2454.CylindricalGearSystemDeflectionTimestep.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CylindricalGearSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_system_deflection_with_ltca_results(self) -> '_2455.CylindricalGearSystemDeflectionWithLTCAResults':
        '''CylindricalGearSystemDeflectionWithLTCAResults: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2455.CylindricalGearSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CylindricalGearSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_cylindrical_planet_gear_system_deflection(self) -> '_2458.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2458.CylindricalPlanetGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CylindricalPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_datum_system_deflection(self) -> '_2459.DatumSystemDeflection':
        '''DatumSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2459.DatumSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to DatumSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_external_cad_model_system_deflection(self) -> '_2460.ExternalCADModelSystemDeflection':
        '''ExternalCADModelSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2460.ExternalCADModelSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ExternalCADModelSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_face_gear_set_system_deflection(self) -> '_2463.FaceGearSetSystemDeflection':
        '''FaceGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2463.FaceGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to FaceGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_face_gear_system_deflection(self) -> '_2464.FaceGearSystemDeflection':
        '''FaceGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2464.FaceGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to FaceGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_fe_part_system_deflection(self) -> '_2465.FEPartSystemDeflection':
        '''FEPartSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2465.FEPartSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to FEPartSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_flexible_pin_assembly_system_deflection(self) -> '_2466.FlexiblePinAssemblySystemDeflection':
        '''FlexiblePinAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2466.FlexiblePinAssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to FlexiblePinAssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_gear_set_system_deflection(self) -> '_2468.GearSetSystemDeflection':
        '''GearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2468.GearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to GearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_gear_system_deflection(self) -> '_2469.GearSystemDeflection':
        '''GearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2469.GearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to GearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_guide_dxf_model_system_deflection(self) -> '_2470.GuideDxfModelSystemDeflection':
        '''GuideDxfModelSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2470.GuideDxfModelSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to GuideDxfModelSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_hypoid_gear_set_system_deflection(self) -> '_2472.HypoidGearSetSystemDeflection':
        '''HypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2472.HypoidGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to HypoidGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_hypoid_gear_system_deflection(self) -> '_2473.HypoidGearSystemDeflection':
        '''HypoidGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2473.HypoidGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to HypoidGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_klingelnberg_cyclo_palloid_conical_gear_set_system_deflection(self) -> '_2477.KlingelnbergCycloPalloidConicalGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2477.KlingelnbergCycloPalloidConicalGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to KlingelnbergCycloPalloidConicalGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_klingelnberg_cyclo_palloid_conical_gear_system_deflection(self) -> '_2478.KlingelnbergCycloPalloidConicalGearSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2478.KlingelnbergCycloPalloidConicalGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to KlingelnbergCycloPalloidConicalGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_system_deflection(self) -> '_2480.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2480.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to KlingelnbergCycloPalloidHypoidGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(self) -> '_2481.KlingelnbergCycloPalloidHypoidGearSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2481.KlingelnbergCycloPalloidHypoidGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to KlingelnbergCycloPalloidHypoidGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_system_deflection(self) -> '_2483.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2483.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(self) -> '_2484.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2484.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_mass_disc_system_deflection(self) -> '_2487.MassDiscSystemDeflection':
        '''MassDiscSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2487.MassDiscSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to MassDiscSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_measurement_component_system_deflection(self) -> '_2488.MeasurementComponentSystemDeflection':
        '''MeasurementComponentSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2488.MeasurementComponentSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to MeasurementComponentSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_mountable_component_system_deflection(self) -> '_2490.MountableComponentSystemDeflection':
        '''MountableComponentSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2490.MountableComponentSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to MountableComponentSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_oil_seal_system_deflection(self) -> '_2492.OilSealSystemDeflection':
        '''OilSealSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2492.OilSealSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to OilSealSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_part_to_part_shear_coupling_half_system_deflection(self) -> '_2495.PartToPartShearCouplingHalfSystemDeflection':
        '''PartToPartShearCouplingHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2495.PartToPartShearCouplingHalfSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to PartToPartShearCouplingHalfSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_part_to_part_shear_coupling_system_deflection(self) -> '_2496.PartToPartShearCouplingSystemDeflection':
        '''PartToPartShearCouplingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2496.PartToPartShearCouplingSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to PartToPartShearCouplingSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_planet_carrier_system_deflection(self) -> '_2498.PlanetCarrierSystemDeflection':
        '''PlanetCarrierSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2498.PlanetCarrierSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to PlanetCarrierSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_point_load_system_deflection(self) -> '_2499.PointLoadSystemDeflection':
        '''PointLoadSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2499.PointLoadSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to PointLoadSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_power_load_system_deflection(self) -> '_2500.PowerLoadSystemDeflection':
        '''PowerLoadSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2500.PowerLoadSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to PowerLoadSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_pulley_system_deflection(self) -> '_2501.PulleySystemDeflection':
        '''PulleySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2501.PulleySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to PulleySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_ring_pins_system_deflection(self) -> '_2502.RingPinsSystemDeflection':
        '''RingPinsSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2502.RingPinsSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to RingPinsSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_rolling_ring_assembly_system_deflection(self) -> '_2505.RollingRingAssemblySystemDeflection':
        '''RollingRingAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2505.RollingRingAssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to RollingRingAssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_rolling_ring_system_deflection(self) -> '_2507.RollingRingSystemDeflection':
        '''RollingRingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2507.RollingRingSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to RollingRingSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_root_assembly_system_deflection(self) -> '_2508.RootAssemblySystemDeflection':
        '''RootAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2508.RootAssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to RootAssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_shaft_hub_connection_system_deflection(self) -> '_2509.ShaftHubConnectionSystemDeflection':
        '''ShaftHubConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2509.ShaftHubConnectionSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ShaftHubConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_shaft_system_deflection(self) -> '_2512.ShaftSystemDeflection':
        '''ShaftSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2512.ShaftSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ShaftSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_specialised_assembly_system_deflection(self) -> '_2514.SpecialisedAssemblySystemDeflection':
        '''SpecialisedAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2514.SpecialisedAssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to SpecialisedAssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_spiral_bevel_gear_set_system_deflection(self) -> '_2516.SpiralBevelGearSetSystemDeflection':
        '''SpiralBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2516.SpiralBevelGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to SpiralBevelGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_spiral_bevel_gear_system_deflection(self) -> '_2517.SpiralBevelGearSystemDeflection':
        '''SpiralBevelGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2517.SpiralBevelGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to SpiralBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_spring_damper_half_system_deflection(self) -> '_2519.SpringDamperHalfSystemDeflection':
        '''SpringDamperHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2519.SpringDamperHalfSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to SpringDamperHalfSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_spring_damper_system_deflection(self) -> '_2520.SpringDamperSystemDeflection':
        '''SpringDamperSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2520.SpringDamperSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to SpringDamperSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_straight_bevel_diff_gear_set_system_deflection(self) -> '_2522.StraightBevelDiffGearSetSystemDeflection':
        '''StraightBevelDiffGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2522.StraightBevelDiffGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to StraightBevelDiffGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_straight_bevel_diff_gear_system_deflection(self) -> '_2523.StraightBevelDiffGearSystemDeflection':
        '''StraightBevelDiffGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2523.StraightBevelDiffGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to StraightBevelDiffGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_straight_bevel_gear_set_system_deflection(self) -> '_2525.StraightBevelGearSetSystemDeflection':
        '''StraightBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2525.StraightBevelGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to StraightBevelGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_straight_bevel_gear_system_deflection(self) -> '_2526.StraightBevelGearSystemDeflection':
        '''StraightBevelGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2526.StraightBevelGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to StraightBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_straight_bevel_planet_gear_system_deflection(self) -> '_2527.StraightBevelPlanetGearSystemDeflection':
        '''StraightBevelPlanetGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2527.StraightBevelPlanetGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to StraightBevelPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_straight_bevel_sun_gear_system_deflection(self) -> '_2528.StraightBevelSunGearSystemDeflection':
        '''StraightBevelSunGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2528.StraightBevelSunGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to StraightBevelSunGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_synchroniser_half_system_deflection(self) -> '_2529.SynchroniserHalfSystemDeflection':
        '''SynchroniserHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2529.SynchroniserHalfSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to SynchroniserHalfSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_synchroniser_part_system_deflection(self) -> '_2530.SynchroniserPartSystemDeflection':
        '''SynchroniserPartSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2530.SynchroniserPartSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to SynchroniserPartSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_synchroniser_sleeve_system_deflection(self) -> '_2531.SynchroniserSleeveSystemDeflection':
        '''SynchroniserSleeveSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2531.SynchroniserSleeveSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to SynchroniserSleeveSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_synchroniser_system_deflection(self) -> '_2532.SynchroniserSystemDeflection':
        '''SynchroniserSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2532.SynchroniserSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to SynchroniserSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_torque_converter_pump_system_deflection(self) -> '_2537.TorqueConverterPumpSystemDeflection':
        '''TorqueConverterPumpSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2537.TorqueConverterPumpSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to TorqueConverterPumpSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_torque_converter_system_deflection(self) -> '_2538.TorqueConverterSystemDeflection':
        '''TorqueConverterSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2538.TorqueConverterSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to TorqueConverterSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_torque_converter_turbine_system_deflection(self) -> '_2539.TorqueConverterTurbineSystemDeflection':
        '''TorqueConverterTurbineSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2539.TorqueConverterTurbineSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to TorqueConverterTurbineSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_unbalanced_mass_system_deflection(self) -> '_2542.UnbalancedMassSystemDeflection':
        '''UnbalancedMassSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2542.UnbalancedMassSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to UnbalancedMassSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_virtual_component_system_deflection(self) -> '_2543.VirtualComponentSystemDeflection':
        '''VirtualComponentSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2543.VirtualComponentSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to VirtualComponentSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_worm_gear_set_system_deflection(self) -> '_2545.WormGearSetSystemDeflection':
        '''WormGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2545.WormGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to WormGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_worm_gear_system_deflection(self) -> '_2546.WormGearSystemDeflection':
        '''WormGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2546.WormGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to WormGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_zerol_bevel_gear_set_system_deflection(self) -> '_2548.ZerolBevelGearSetSystemDeflection':
        '''ZerolBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2548.ZerolBevelGearSetSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ZerolBevelGearSetSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def system_deflection_results_of_type_zerol_bevel_gear_system_deflection(self) -> '_2549.ZerolBevelGearSystemDeflection':
        '''ZerolBevelGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2549.ZerolBevelGearSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ZerolBevelGearSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    def create_viewable(self) -> '_1963.HarmonicAnalysisViewable':
        ''' 'CreateViewable' is the original name of this method.

        Returns:
            mastapy.system_model.drawing.HarmonicAnalysisViewable
        '''

        method_result = self.wrapped.CreateViewable()
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None
