'''_6745.py

CycloidalDiscAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model.cycloidal import _2282
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6546
from mastapy.system_model.analyses_and_results.system_deflections import _2446
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6698
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'CycloidalDiscAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscAdvancedTimeSteppingAnalysisForModulation',)


class CycloidalDiscAdvancedTimeSteppingAnalysisForModulation(_6698.AbstractShaftAdvancedTimeSteppingAnalysisForModulation):
    '''CycloidalDiscAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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
    def system_deflection_results(self) -> '_2446.CycloidalDiscSystemDeflection':
        '''CycloidalDiscSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2446.CycloidalDiscSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
