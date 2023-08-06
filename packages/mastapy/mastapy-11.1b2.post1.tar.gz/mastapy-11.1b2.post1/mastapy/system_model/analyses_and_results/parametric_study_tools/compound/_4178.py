'''_4178.py

ConceptGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2235
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4176, _4177, _4207
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4031
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ConceptGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundParametricStudyTool',)


class ConceptGearSetCompoundParametricStudyTool(_4207.GearSetCompoundParametricStudyTool):
    '''ConceptGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2235.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2235.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2235.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2235.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def concept_gears_compound_parametric_study_tool(self) -> 'List[_4176.ConceptGearCompoundParametricStudyTool]':
        '''List[ConceptGearCompoundParametricStudyTool]: 'ConceptGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundParametricStudyTool, constructor.new(_4176.ConceptGearCompoundParametricStudyTool))
        return value

    @property
    def concept_meshes_compound_parametric_study_tool(self) -> 'List[_4177.ConceptGearMeshCompoundParametricStudyTool]':
        '''List[ConceptGearMeshCompoundParametricStudyTool]: 'ConceptMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundParametricStudyTool, constructor.new(_4177.ConceptGearMeshCompoundParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4031.ConceptGearSetParametricStudyTool]':
        '''List[ConceptGearSetParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4031.ConceptGearSetParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4031.ConceptGearSetParametricStudyTool]':
        '''List[ConceptGearSetParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4031.ConceptGearSetParametricStudyTool))
        return value
