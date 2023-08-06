'''_4616.py

PartToPartShearCouplingHalfModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2302
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6621
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4573
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'PartToPartShearCouplingHalfModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfModalAnalysisAtASpeed',)


class PartToPartShearCouplingHalfModalAnalysisAtASpeed(_4573.CouplingHalfModalAnalysisAtASpeed):
    '''PartToPartShearCouplingHalfModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2302.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2302.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6621.PartToPartShearCouplingHalfLoadCase':
        '''PartToPartShearCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6621.PartToPartShearCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
