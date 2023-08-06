'''_3655.py

ExternalCADModelCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2166
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3524
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3628
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ExternalCADModelCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundStabilityAnalysis',)


class ExternalCADModelCompoundStabilityAnalysis(_3628.ComponentCompoundStabilityAnalysis):
    '''ExternalCADModelCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundStabilityAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_3524.ExternalCADModelStabilityAnalysis]':
        '''List[ExternalCADModelStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3524.ExternalCADModelStabilityAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3524.ExternalCADModelStabilityAnalysis]':
        '''List[ExternalCADModelStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3524.ExternalCADModelStabilityAnalysis))
        return value
