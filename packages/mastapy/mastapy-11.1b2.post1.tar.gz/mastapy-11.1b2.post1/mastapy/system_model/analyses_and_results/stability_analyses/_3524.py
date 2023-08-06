'''_3524.py

ExternalCADModelStabilityAnalysis
'''


from mastapy.system_model.part_model import _2166
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6571
from mastapy.system_model.analyses_and_results.stability_analyses import _3496
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ExternalCADModelStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelStabilityAnalysis',)


class ExternalCADModelStabilityAnalysis(_3496.ComponentStabilityAnalysis):
    '''ExternalCADModelStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelStabilityAnalysis.TYPE'):
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
