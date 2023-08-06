'''_4754.py

RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2056
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4625
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4729
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed',)


class RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed(_4729.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed):
    '''RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2056.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2056.RingPinsToDiscConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def connection_design(self) -> '_2056.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2056.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_4625.RingPinsToDiscConnectionModalAnalysisAtASpeed]':
        '''List[RingPinsToDiscConnectionModalAnalysisAtASpeed]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_4625.RingPinsToDiscConnectionModalAnalysisAtASpeed))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_4625.RingPinsToDiscConnectionModalAnalysisAtASpeed]':
        '''List[RingPinsToDiscConnectionModalAnalysisAtASpeed]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_4625.RingPinsToDiscConnectionModalAnalysisAtASpeed))
        return value
