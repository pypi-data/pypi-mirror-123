'''_6436.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2254
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6434, _6435, _6430
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6307
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis(_6430.KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2254.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2254.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2254.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2254.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_critical_speed_analysis(self) -> 'List[_6434.KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundCriticalSpeedAnalysis, constructor.new(_6434.KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_critical_speed_analysis(self) -> 'List[_6435.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6435.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6307.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6307.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6307.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6307.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis))
        return value
