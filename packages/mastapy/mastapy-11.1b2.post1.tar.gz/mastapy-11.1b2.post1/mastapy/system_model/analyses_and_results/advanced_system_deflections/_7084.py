'''_7084.py

TorqueConverterConnectionAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2067
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6664
from mastapy.system_model.analyses_and_results.system_deflections import _2536
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7002
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'TorqueConverterConnectionAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionAdvancedSystemDeflection',)


class TorqueConverterConnectionAdvancedSystemDeflection(_7002.CouplingConnectionAdvancedSystemDeflection):
    '''TorqueConverterConnectionAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2067.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2067.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6664.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6664.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2536.TorqueConverterConnectionSystemDeflection]':
        '''List[TorqueConverterConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2536.TorqueConverterConnectionSystemDeflection))
        return value
