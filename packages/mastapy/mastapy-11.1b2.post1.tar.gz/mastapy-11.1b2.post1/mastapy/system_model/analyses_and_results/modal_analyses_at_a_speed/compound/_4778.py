'''_4778.py

SynchroniserHalfCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2317
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4648
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4779
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'SynchroniserHalfCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundModalAnalysisAtASpeed',)


class SynchroniserHalfCompoundModalAnalysisAtASpeed(_4779.SynchroniserPartCompoundModalAnalysisAtASpeed):
    '''SynchroniserHalfCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2317.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2317.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4648.SynchroniserHalfModalAnalysisAtASpeed]':
        '''List[SynchroniserHalfModalAnalysisAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4648.SynchroniserHalfModalAnalysisAtASpeed))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4648.SynchroniserHalfModalAnalysisAtASpeed]':
        '''List[SynchroniserHalfModalAnalysisAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4648.SynchroniserHalfModalAnalysisAtASpeed))
        return value
