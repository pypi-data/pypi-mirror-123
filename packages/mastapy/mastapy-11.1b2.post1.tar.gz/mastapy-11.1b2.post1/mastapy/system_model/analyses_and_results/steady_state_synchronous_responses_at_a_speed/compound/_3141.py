'''_3141.py

GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2169
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3011
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3105
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed',)


class GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed(_3105.ComponentCompoundSteadyStateSynchronousResponseAtASpeed):
    '''GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2169.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2169.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3011.GuideDxfModelSteadyStateSynchronousResponseAtASpeed]':
        '''List[GuideDxfModelSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3011.GuideDxfModelSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3011.GuideDxfModelSteadyStateSynchronousResponseAtASpeed]':
        '''List[GuideDxfModelSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3011.GuideDxfModelSteadyStateSynchronousResponseAtASpeed))
        return value
