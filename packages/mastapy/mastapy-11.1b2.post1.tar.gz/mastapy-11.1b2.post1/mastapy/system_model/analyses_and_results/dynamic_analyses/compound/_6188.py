'''_6188.py

RollingRingCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2309
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6060
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6135
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'RollingRingCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundDynamicAnalysis',)


class RollingRingCompoundDynamicAnalysis(_6135.CouplingHalfCompoundDynamicAnalysis):
    '''RollingRingCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2309.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2309.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6060.RollingRingDynamicAnalysis]':
        '''List[RollingRingDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6060.RollingRingDynamicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundDynamicAnalysis]':
        '''List[RollingRingCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6060.RollingRingDynamicAnalysis]':
        '''List[RollingRingDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6060.RollingRingDynamicAnalysis))
        return value
