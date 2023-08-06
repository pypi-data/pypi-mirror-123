'''_4254.py

StraightBevelDiffGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2259
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4252, _4253, _4165
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4125
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'StraightBevelDiffGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundParametricStudyTool',)


class StraightBevelDiffGearSetCompoundParametricStudyTool(_4165.BevelGearSetCompoundParametricStudyTool):
    '''StraightBevelDiffGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2259.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2259.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def straight_bevel_diff_gears_compound_parametric_study_tool(self) -> 'List[_4252.StraightBevelDiffGearCompoundParametricStudyTool]':
        '''List[StraightBevelDiffGearCompoundParametricStudyTool]: 'StraightBevelDiffGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundParametricStudyTool, constructor.new(_4252.StraightBevelDiffGearCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_diff_meshes_compound_parametric_study_tool(self) -> 'List[_4253.StraightBevelDiffGearMeshCompoundParametricStudyTool]':
        '''List[StraightBevelDiffGearMeshCompoundParametricStudyTool]: 'StraightBevelDiffMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundParametricStudyTool, constructor.new(_4253.StraightBevelDiffGearMeshCompoundParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4125.StraightBevelDiffGearSetParametricStudyTool]':
        '''List[StraightBevelDiffGearSetParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4125.StraightBevelDiffGearSetParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4125.StraightBevelDiffGearSetParametricStudyTool]':
        '''List[StraightBevelDiffGearSetParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4125.StraightBevelDiffGearSetParametricStudyTool))
        return value
