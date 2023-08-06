'''_6273.py

CVTBeltConnectionCriticalSpeedAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1988
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6240
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'CVTBeltConnectionCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionCriticalSpeedAnalysis',)


class CVTBeltConnectionCriticalSpeedAnalysis(_6240.BeltConnectionCriticalSpeedAnalysis):
    '''CVTBeltConnectionCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1988.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None
