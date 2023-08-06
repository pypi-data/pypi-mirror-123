'''_4371.py

RootAssemblyModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model import _2188
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _2350, _4283
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'RootAssemblyModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyModalAnalysisAtAStiffness',)


class RootAssemblyModalAnalysisAtAStiffness(_4283.AssemblyModalAnalysisAtAStiffness):
    '''RootAssemblyModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2188.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2188.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def modal_analysis_at_a_stiffness_inputs(self) -> '_2350.ModalAnalysisAtAStiffness':
        '''ModalAnalysisAtAStiffness: 'ModalAnalysisAtAStiffnessInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2350.ModalAnalysisAtAStiffness)(self.wrapped.ModalAnalysisAtAStiffnessInputs) if self.wrapped.ModalAnalysisAtAStiffnessInputs is not None else None
