'''_4251.py

SpringDamperHalfCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2314
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4121
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4186
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'SpringDamperHalfCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfCompoundParametricStudyTool',)


class SpringDamperHalfCompoundParametricStudyTool(_4186.CouplingHalfCompoundParametricStudyTool):
    '''SpringDamperHalfCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2314.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2314.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4121.SpringDamperHalfParametricStudyTool]':
        '''List[SpringDamperHalfParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4121.SpringDamperHalfParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4121.SpringDamperHalfParametricStudyTool]':
        '''List[SpringDamperHalfParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4121.SpringDamperHalfParametricStudyTool))
        return value
