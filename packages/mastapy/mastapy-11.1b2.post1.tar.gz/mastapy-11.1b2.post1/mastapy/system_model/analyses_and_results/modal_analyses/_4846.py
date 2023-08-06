'''_4846.py

ExternalCADModelModalAnalysis
'''


from mastapy.system_model.part_model import _2166
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6571
from mastapy.system_model.analyses_and_results.system_deflections import _2460
from mastapy.system_model.analyses_and_results.modal_analyses import _4818
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ExternalCADModelModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelModalAnalysis',)


class ExternalCADModelModalAnalysis(_4818.ComponentModalAnalysis):
    '''ExternalCADModelModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2166.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2166.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6571.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6571.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2460.ExternalCADModelSystemDeflection':
        '''ExternalCADModelSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.ExternalCADModelSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
