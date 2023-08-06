'''_6095.py

AGMAGleasonConicalGearMeshCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.dynamic_analyses import _5965
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6123
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'AGMAGleasonConicalGearMeshCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearMeshCompoundDynamicAnalysis',)


class AGMAGleasonConicalGearMeshCompoundDynamicAnalysis(_6123.ConicalGearMeshCompoundDynamicAnalysis):
    '''AGMAGleasonConicalGearMeshCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearMeshCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_5965.AGMAGleasonConicalGearMeshDynamicAnalysis]':
        '''List[AGMAGleasonConicalGearMeshDynamicAnalysis]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_5965.AGMAGleasonConicalGearMeshDynamicAnalysis))
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_5965.AGMAGleasonConicalGearMeshDynamicAnalysis]':
        '''List[AGMAGleasonConicalGearMeshDynamicAnalysis]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_5965.AGMAGleasonConicalGearMeshDynamicAnalysis))
        return value
