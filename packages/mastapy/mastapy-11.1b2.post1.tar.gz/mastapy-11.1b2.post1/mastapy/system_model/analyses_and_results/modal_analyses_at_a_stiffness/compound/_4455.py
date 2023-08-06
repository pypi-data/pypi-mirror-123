'''_4455.py

CylindricalGearSetCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2239, _2255
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4453, _4454, _4466
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4325
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'CylindricalGearSetCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundModalAnalysisAtAStiffness',)


class CylindricalGearSetCompoundModalAnalysisAtAStiffness(_4466.GearSetCompoundModalAnalysisAtAStiffness):
    '''CylindricalGearSetCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2239.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2239.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2239.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2239.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def cylindrical_gears_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4453.CylindricalGearCompoundModalAnalysisAtAStiffness]':
        '''List[CylindricalGearCompoundModalAnalysisAtAStiffness]: 'CylindricalGearsCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundModalAnalysisAtAStiffness, constructor.new(_4453.CylindricalGearCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cylindrical_meshes_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4454.CylindricalGearMeshCompoundModalAnalysisAtAStiffness]':
        '''List[CylindricalGearMeshCompoundModalAnalysisAtAStiffness]: 'CylindricalMeshesCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundModalAnalysisAtAStiffness, constructor.new(_4454.CylindricalGearMeshCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4325.CylindricalGearSetModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetModalAnalysisAtAStiffness]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4325.CylindricalGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4325.CylindricalGearSetModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetModalAnalysisAtAStiffness]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4325.CylindricalGearSetModalAnalysisAtAStiffness))
        return value
