'''_5234.py

AssemblyCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2149, _2188
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.mbd_analyses import _5083
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
    _5235, _5237, _5240, _5246,
    _5247, _5248, _5253, _5258,
    _5268, _5270, _5272, _5276,
    _5282, _5283, _5284, _5291,
    _5298, _5301, _5302, _5303,
    _5305, _5307, _5312, _5313,
    _5314, _5323, _5316, _5318,
    _5322, _5328, _5329, _5334,
    _5337, _5340, _5344, _5348,
    _5352, _5355, _5227
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'AssemblyCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundMultibodyDynamicsAnalysis',)


class AssemblyCompoundMultibodyDynamicsAnalysis(_5227.AbstractAssemblyCompoundMultibodyDynamicsAnalysis):
    '''AssemblyCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundMultibodyDynamicsAnalysis.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_5083.AssemblyMultibodyDynamicsAnalysis]':
        '''List[AssemblyMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5083.AssemblyMultibodyDynamicsAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5235.BearingCompoundMultibodyDynamicsAnalysis]':
        '''List[BearingCompoundMultibodyDynamicsAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5235.BearingCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5237.BeltDriveCompoundMultibodyDynamicsAnalysis]':
        '''List[BeltDriveCompoundMultibodyDynamicsAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5237.BeltDriveCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5240.BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5240.BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5246.BoltCompoundMultibodyDynamicsAnalysis]':
        '''List[BoltCompoundMultibodyDynamicsAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5246.BoltCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5247.BoltedJointCompoundMultibodyDynamicsAnalysis]':
        '''List[BoltedJointCompoundMultibodyDynamicsAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5247.BoltedJointCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5248.ClutchCompoundMultibodyDynamicsAnalysis]':
        '''List[ClutchCompoundMultibodyDynamicsAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5248.ClutchCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5253.ConceptCouplingCompoundMultibodyDynamicsAnalysis]':
        '''List[ConceptCouplingCompoundMultibodyDynamicsAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5253.ConceptCouplingCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5258.ConceptGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[ConceptGearSetCompoundMultibodyDynamicsAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5258.ConceptGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5268.CVTCompoundMultibodyDynamicsAnalysis]':
        '''List[CVTCompoundMultibodyDynamicsAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5268.CVTCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5270.CycloidalAssemblyCompoundMultibodyDynamicsAnalysis]':
        '''List[CycloidalAssemblyCompoundMultibodyDynamicsAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5270.CycloidalAssemblyCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5272.CycloidalDiscCompoundMultibodyDynamicsAnalysis]':
        '''List[CycloidalDiscCompoundMultibodyDynamicsAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5272.CycloidalDiscCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5276.CylindricalGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[CylindricalGearSetCompoundMultibodyDynamicsAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5276.CylindricalGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5282.FaceGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[FaceGearSetCompoundMultibodyDynamicsAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5282.FaceGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_5283.FEPartCompoundMultibodyDynamicsAnalysis]':
        '''List[FEPartCompoundMultibodyDynamicsAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5283.FEPartCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5284.FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5284.FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5291.HypoidGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[HypoidGearSetCompoundMultibodyDynamicsAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5291.HypoidGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5298.KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5298.KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5301.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5301.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5302.MassDiscCompoundMultibodyDynamicsAnalysis]':
        '''List[MassDiscCompoundMultibodyDynamicsAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5302.MassDiscCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5303.MeasurementComponentCompoundMultibodyDynamicsAnalysis]':
        '''List[MeasurementComponentCompoundMultibodyDynamicsAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5303.MeasurementComponentCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5305.OilSealCompoundMultibodyDynamicsAnalysis]':
        '''List[OilSealCompoundMultibodyDynamicsAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5305.OilSealCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5307.PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis]':
        '''List[PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5307.PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5312.PlanetCarrierCompoundMultibodyDynamicsAnalysis]':
        '''List[PlanetCarrierCompoundMultibodyDynamicsAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5312.PlanetCarrierCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5313.PointLoadCompoundMultibodyDynamicsAnalysis]':
        '''List[PointLoadCompoundMultibodyDynamicsAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5313.PointLoadCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5314.PowerLoadCompoundMultibodyDynamicsAnalysis]':
        '''List[PowerLoadCompoundMultibodyDynamicsAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5314.PowerLoadCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5323.ShaftHubConnectionCompoundMultibodyDynamicsAnalysis]':
        '''List[ShaftHubConnectionCompoundMultibodyDynamicsAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5323.ShaftHubConnectionCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5316.RingPinsCompoundMultibodyDynamicsAnalysis]':
        '''List[RingPinsCompoundMultibodyDynamicsAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5316.RingPinsCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5318.RollingRingAssemblyCompoundMultibodyDynamicsAnalysis]':
        '''List[RollingRingAssemblyCompoundMultibodyDynamicsAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5318.RollingRingAssemblyCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5322.ShaftCompoundMultibodyDynamicsAnalysis]':
        '''List[ShaftCompoundMultibodyDynamicsAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5322.ShaftCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5328.SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5328.SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5329.SpringDamperCompoundMultibodyDynamicsAnalysis]':
        '''List[SpringDamperCompoundMultibodyDynamicsAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5329.SpringDamperCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5334.StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5334.StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5337.StraightBevelGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetCompoundMultibodyDynamicsAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5337.StraightBevelGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5340.SynchroniserCompoundMultibodyDynamicsAnalysis]':
        '''List[SynchroniserCompoundMultibodyDynamicsAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5340.SynchroniserCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5344.TorqueConverterCompoundMultibodyDynamicsAnalysis]':
        '''List[TorqueConverterCompoundMultibodyDynamicsAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5344.TorqueConverterCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5348.UnbalancedMassCompoundMultibodyDynamicsAnalysis]':
        '''List[UnbalancedMassCompoundMultibodyDynamicsAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5348.UnbalancedMassCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5352.WormGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[WormGearSetCompoundMultibodyDynamicsAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5352.WormGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5355.ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5355.ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5083.AssemblyMultibodyDynamicsAnalysis]':
        '''List[AssemblyMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5083.AssemblyMultibodyDynamicsAnalysis))
        return value
