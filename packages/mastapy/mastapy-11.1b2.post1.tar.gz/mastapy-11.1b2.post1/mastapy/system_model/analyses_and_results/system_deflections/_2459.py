'''_2459.py

DatumSystemDeflection
'''


from mastapy.system_model.part_model import _2163
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6556
from mastapy.system_model.analyses_and_results.power_flows import _3790
from mastapy.system_model.analyses_and_results.system_deflections import _2423
from mastapy._internal.python_net import python_net_import

_DATUM_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'DatumSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumSystemDeflection',)


class DatumSystemDeflection(_2423.ComponentSystemDeflection):
    '''DatumSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _DATUM_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2163.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6556.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6556.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3790.DatumPowerFlow':
        '''DatumPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3790.DatumPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None
