'''_6838.py

AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model import _2149, _2188
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6707
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _6839, _6841, _6844, _6850,
    _6851, _6852, _6857, _6862,
    _6872, _6874, _6876, _6880,
    _6886, _6887, _6888, _6895,
    _6902, _6905, _6906, _6907,
    _6909, _6911, _6916, _6917,
    _6918, _6927, _6920, _6922,
    _6926, _6932, _6933, _6938,
    _6941, _6944, _6948, _6952,
    _6956, _6959, _6831
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation',)


class AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation(_6831.AbstractAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2149.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

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
    def assembly_analysis_cases_ready(self) -> 'List[_6707.AssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[AssemblyAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6707.AssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bearings(self) -> 'List[_6839.BearingCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BearingCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6839.BearingCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def belt_drives(self) -> 'List[_6841.BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6841.BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6844.BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6844.BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bolts(self) -> 'List[_6850.BoltCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6850.BoltCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bolted_joints(self) -> 'List[_6851.BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6851.BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def clutches(self) -> 'List[_6852.ClutchCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ClutchCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6852.ClutchCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_couplings(self) -> 'List[_6857.ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6857.ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6862.ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6862.ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cv_ts(self) -> 'List[_6872.CVTCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CVTCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6872.CVTCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6874.CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6874.CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6876.CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6876.CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6880.CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6880.CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6886.FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6886.FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def fe_parts(self) -> 'List[_6887.FEPartCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FEPartCompoundAdvancedTimeSteppingAnalysisForModulation]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6887.FEPartCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6888.FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6888.FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6895.HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6895.HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6902.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6902.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6905.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6905.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def mass_discs(self) -> 'List[_6906.MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6906.MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def measurement_components(self) -> 'List[_6907.MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6907.MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def oil_seals(self) -> 'List[_6909.OilSealCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[OilSealCompoundAdvancedTimeSteppingAnalysisForModulation]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6909.OilSealCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6911.PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6911.PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def planet_carriers(self) -> 'List[_6916.PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6916.PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def point_loads(self) -> 'List[_6917.PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6917.PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def power_loads(self) -> 'List[_6918.PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6918.PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6927.ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6927.ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def ring_pins(self) -> 'List[_6920.RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6920.RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6922.RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6922.RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def shafts(self) -> 'List[_6926.ShaftCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ShaftCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6926.ShaftCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6932.SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6932.SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def spring_dampers(self) -> 'List[_6933.SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6933.SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6938.StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6938.StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6941.StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6941.StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def synchronisers(self) -> 'List[_6944.SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6944.SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def torque_converters(self) -> 'List[_6948.TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6948.TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6952.UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6952.UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6956.WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6956.WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6959.ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6959.ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6707.AssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[AssemblyAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6707.AssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value
