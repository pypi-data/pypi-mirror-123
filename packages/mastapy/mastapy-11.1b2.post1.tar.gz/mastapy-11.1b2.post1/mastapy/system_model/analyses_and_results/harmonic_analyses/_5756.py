'''_5756.py

ShaftHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses import _4895
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5721, _5637
from mastapy.system_model.part_model.shaft_model import _2196
from mastapy.system_model.analyses_and_results.static_loads import _6641
from mastapy.system_model.analyses_and_results.system_deflections import _2512
from mastapy._internal.python_net import python_net_import

_SHAFT_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ShaftHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHarmonicAnalysis',)


class ShaftHarmonicAnalysis(_5637.AbstractShaftHarmonicAnalysis):
    '''ShaftHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def coupled_modal_analysis(self) -> '_4895.ShaftModalAnalysis':
        '''ShaftModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4895.ShaftModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis is not None else None

    @property
    def export(self) -> '_5721.HarmonicAnalysisShaftExportOptions':
        '''HarmonicAnalysisShaftExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5721.HarmonicAnalysisShaftExportOptions)(self.wrapped.Export) if self.wrapped.Export is not None else None

    @property
    def component_design(self) -> '_2196.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6641.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6641.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2512.ShaftSystemDeflection':
        '''ShaftSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2512.ShaftSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def planetaries(self) -> 'List[ShaftHarmonicAnalysis]':
        '''List[ShaftHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHarmonicAnalysis))
        return value
