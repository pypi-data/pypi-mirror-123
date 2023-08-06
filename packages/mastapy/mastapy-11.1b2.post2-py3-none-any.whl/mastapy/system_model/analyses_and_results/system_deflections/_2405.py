'''_2405.py

AssemblySystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2149, _2188
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6506, _6639
from mastapy.system_model.analyses_and_results.power_flows import _3745, _3835
from mastapy.nodal_analysis import _47
from mastapy.shafts import _37
from mastapy.gears.analysis import _1155
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2406, _2408, _2410, _2418,
    _2417, _2421, _2427, _2429,
    _2442, _2443, _2446, _2450,
    _2463, _2465, _2466, _2472,
    _2480, _2483, _2487, _2488,
    _2492, _2496, _2498, _2499,
    _2500, _2509, _2502, _2505,
    _2512, _2516, _2520, _2522,
    _2525, _2532, _2538, _2542,
    _2545, _2548, _2399, _2435,
    _2423, _2490, _2467, _2398
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'AssemblySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySystemDeflection',)


class AssemblySystemDeflection(_2398.AbstractAssemblySystemDeflection):
    '''AssemblySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def overall_bearing_reliability(self) -> 'float':
        '''float: 'OverallBearingReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallBearingReliability

    @property
    def overall_shaft_reliability(self) -> 'float':
        '''float: 'OverallShaftReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallShaftReliability

    @property
    def overall_gear_reliability(self) -> 'float':
        '''float: 'OverallGearReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallGearReliability

    @property
    def overall_oil_seal_reliability(self) -> 'float':
        '''float: 'OverallOilSealReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallOilSealReliability

    @property
    def overall_system_reliability(self) -> 'float':
        '''float: 'OverallSystemReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallSystemReliability

    @property
    def assembly_design(self) -> '_2149.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6506.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6506.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3745.AssemblyPowerFlow':
        '''AssemblyPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3745.AssemblyPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to AssemblyPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None

    @property
    def analysis_settings(self) -> '_47.AnalysisSettingsObjects':
        '''AnalysisSettingsObjects: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_47.AnalysisSettingsObjects)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings is not None else None

    @property
    def shaft_settings(self) -> '_37.ShaftSettings':
        '''ShaftSettings: 'ShaftSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_37.ShaftSettings)(self.wrapped.ShaftSettings) if self.wrapped.ShaftSettings is not None else None

    @property
    def rating_for_all_gear_sets(self) -> '_1155.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1155.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets is not None else None

    @property
    def bearings(self) -> 'List[_2406.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2406.BearingSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_2408.BeltDriveSystemDeflection]':
        '''List[BeltDriveSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2408.BeltDriveSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2410.BevelDifferentialGearSetSystemDeflection]':
        '''List[BevelDifferentialGearSetSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2410.BevelDifferentialGearSetSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_2418.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2418.BoltSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_2417.BoltedJointSystemDeflection]':
        '''List[BoltedJointSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2417.BoltedJointSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_2421.ClutchSystemDeflection]':
        '''List[ClutchSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2421.ClutchSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_2427.ConceptCouplingSystemDeflection]':
        '''List[ConceptCouplingSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2427.ConceptCouplingSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2429.ConceptGearSetSystemDeflection]':
        '''List[ConceptGearSetSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2429.ConceptGearSetSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_2442.CVTSystemDeflection]':
        '''List[CVTSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2442.CVTSystemDeflection))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_2443.CycloidalAssemblySystemDeflection]':
        '''List[CycloidalAssemblySystemDeflection]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_2443.CycloidalAssemblySystemDeflection))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_2446.CycloidalDiscSystemDeflection]':
        '''List[CycloidalDiscSystemDeflection]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_2446.CycloidalDiscSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2450.CylindricalGearSetSystemDeflection]':
        '''List[CylindricalGearSetSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2450.CylindricalGearSetSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2463.FaceGearSetSystemDeflection]':
        '''List[FaceGearSetSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2463.FaceGearSetSystemDeflection))
        return value

    @property
    def fe_parts(self) -> 'List[_2465.FEPartSystemDeflection]':
        '''List[FEPartSystemDeflection]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_2465.FEPartSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2466.FlexiblePinAssemblySystemDeflection]':
        '''List[FlexiblePinAssemblySystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2466.FlexiblePinAssemblySystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2472.HypoidGearSetSystemDeflection]':
        '''List[HypoidGearSetSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2472.HypoidGearSetSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2480.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2480.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2483.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2483.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_2487.MassDiscSystemDeflection]':
        '''List[MassDiscSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2487.MassDiscSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_2488.MeasurementComponentSystemDeflection]':
        '''List[MeasurementComponentSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2488.MeasurementComponentSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_2492.OilSealSystemDeflection]':
        '''List[OilSealSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2492.OilSealSystemDeflection))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2496.PartToPartShearCouplingSystemDeflection]':
        '''List[PartToPartShearCouplingSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_2496.PartToPartShearCouplingSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_2498.PlanetCarrierSystemDeflection]':
        '''List[PlanetCarrierSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2498.PlanetCarrierSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_2499.PointLoadSystemDeflection]':
        '''List[PointLoadSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2499.PointLoadSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_2500.PowerLoadSystemDeflection]':
        '''List[PowerLoadSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2500.PowerLoadSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2509.ShaftHubConnectionSystemDeflection]':
        '''List[ShaftHubConnectionSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2509.ShaftHubConnectionSystemDeflection))
        return value

    @property
    def ring_pins(self) -> 'List[_2502.RingPinsSystemDeflection]':
        '''List[RingPinsSystemDeflection]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_2502.RingPinsSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2505.RollingRingAssemblySystemDeflection]':
        '''List[RollingRingAssemblySystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2505.RollingRingAssemblySystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_2512.ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2512.ShaftSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2516.SpiralBevelGearSetSystemDeflection]':
        '''List[SpiralBevelGearSetSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2516.SpiralBevelGearSetSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_2520.SpringDamperSystemDeflection]':
        '''List[SpringDamperSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2520.SpringDamperSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2522.StraightBevelDiffGearSetSystemDeflection]':
        '''List[StraightBevelDiffGearSetSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2522.StraightBevelDiffGearSetSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2525.StraightBevelGearSetSystemDeflection]':
        '''List[StraightBevelGearSetSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2525.StraightBevelGearSetSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_2532.SynchroniserSystemDeflection]':
        '''List[SynchroniserSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2532.SynchroniserSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_2538.TorqueConverterSystemDeflection]':
        '''List[TorqueConverterSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2538.TorqueConverterSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2542.UnbalancedMassSystemDeflection]':
        '''List[UnbalancedMassSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2542.UnbalancedMassSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2545.WormGearSetSystemDeflection]':
        '''List[WormGearSetSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2545.WormGearSetSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2548.ZerolBevelGearSetSystemDeflection]':
        '''List[ZerolBevelGearSetSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2548.ZerolBevelGearSetSystemDeflection))
        return value

    @property
    def shafts_and_housings(self) -> 'List[_2399.AbstractShaftOrHousingSystemDeflection]':
        '''List[AbstractShaftOrHousingSystemDeflection]: 'ShaftsAndHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftsAndHousings, constructor.new(_2399.AbstractShaftOrHousingSystemDeflection))
        return value

    @property
    def supercharger_rotor_sets(self) -> 'List[_2450.CylindricalGearSetSystemDeflection]':
        '''List[CylindricalGearSetSystemDeflection]: 'SuperchargerRotorSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SuperchargerRotorSets, constructor.new(_2450.CylindricalGearSetSystemDeflection))
        return value

    @property
    def rolling_bearings(self) -> 'List[_2406.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'RollingBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingBearings, constructor.new(_2406.BearingSystemDeflection))
        return value

    @property
    def connection_details(self) -> 'List[_2435.ConnectionSystemDeflection]':
        '''List[ConnectionSystemDeflection]: 'ConnectionDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDetails, constructor.new(_2435.ConnectionSystemDeflection))
        return value

    @property
    def sorted_converged_connection_details(self) -> 'List[_2435.ConnectionSystemDeflection]':
        '''List[ConnectionSystemDeflection]: 'SortedConvergedConnectionDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedConvergedConnectionDetails, constructor.new(_2435.ConnectionSystemDeflection))
        return value

    @property
    def sorted_unconverged_connection_details(self) -> 'List[_2435.ConnectionSystemDeflection]':
        '''List[ConnectionSystemDeflection]: 'SortedUnconvergedConnectionDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedUnconvergedConnectionDetails, constructor.new(_2435.ConnectionSystemDeflection))
        return value

    @property
    def component_details(self) -> 'List[_2423.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'ComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDetails, constructor.new(_2423.ComponentSystemDeflection))
        return value

    @property
    def mountable_component_details(self) -> 'List[_2490.MountableComponentSystemDeflection]':
        '''List[MountableComponentSystemDeflection]: 'MountableComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MountableComponentDetails, constructor.new(_2490.MountableComponentSystemDeflection))
        return value

    @property
    def sorted_converged_component_details(self) -> 'List[_2423.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'SortedConvergedComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedConvergedComponentDetails, constructor.new(_2423.ComponentSystemDeflection))
        return value

    @property
    def sorted_unconverged_component_details(self) -> 'List[_2423.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'SortedUnconvergedComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedUnconvergedComponentDetails, constructor.new(_2423.ComponentSystemDeflection))
        return value

    @property
    def unconverged_bearings_sorted_by_load(self) -> 'List[_2406.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'UnconvergedBearingsSortedByLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnconvergedBearingsSortedByLoad, constructor.new(_2406.BearingSystemDeflection))
        return value

    @property
    def unconverged_gear_meshes_sorted_by_power(self) -> 'List[_2467.GearMeshSystemDeflection]':
        '''List[GearMeshSystemDeflection]: 'UnconvergedGearMeshesSortedByPower' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnconvergedGearMeshesSortedByPower, constructor.new(_2467.GearMeshSystemDeflection))
        return value
