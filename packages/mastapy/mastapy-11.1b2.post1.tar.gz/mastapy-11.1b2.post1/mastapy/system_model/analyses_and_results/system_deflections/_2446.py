'''_2446.py

CycloidalDiscSystemDeflection
'''


from mastapy.system_model.part_model.cycloidal import _2282
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6546
from mastapy.system_model.analyses_and_results.power_flows import _3784
from mastapy.system_model.analyses_and_results.system_deflections import _2400
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CycloidalDiscSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscSystemDeflection',)


class CycloidalDiscSystemDeflection(_2400.AbstractShaftSystemDeflection):
    '''CycloidalDiscSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2282.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2282.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6546.CycloidalDiscLoadCase':
        '''CycloidalDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6546.CycloidalDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3784.CycloidalDiscPowerFlow':
        '''CycloidalDiscPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3784.CycloidalDiscPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None
