'''_4183.py

ConnectorCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.analyses_and_results.parametric_study_tools import _4036
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4224
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ConnectorCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundParametricStudyTool',)


class ConnectorCompoundParametricStudyTool(_4224.MountableComponentCompoundParametricStudyTool):
    '''ConnectorCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_4036.ConnectorParametricStudyTool]':
        '''List[ConnectorParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4036.ConnectorParametricStudyTool))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_4036.ConnectorParametricStudyTool]':
        '''List[ConnectorParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4036.ConnectorParametricStudyTool))
        return value
