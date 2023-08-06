'''_3288.py

OilSealSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _2180
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6617
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3245
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'OilSealSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealSteadyStateSynchronousResponse',)


class OilSealSteadyStateSynchronousResponse(_3245.ConnectorSteadyStateSynchronousResponse):
    '''OilSealSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2180.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6617.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6617.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
