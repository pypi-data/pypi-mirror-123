'''_3492.py

ClutchConnectionStabilityAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _2057
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6520
from mastapy.system_model.analyses_and_results.stability_analyses import _3508
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ClutchConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionStabilityAnalysis',)


class ClutchConnectionStabilityAnalysis(_3508.CouplingConnectionStabilityAnalysis):
    '''ClutchConnectionStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2057.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2057.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6520.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6520.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None
