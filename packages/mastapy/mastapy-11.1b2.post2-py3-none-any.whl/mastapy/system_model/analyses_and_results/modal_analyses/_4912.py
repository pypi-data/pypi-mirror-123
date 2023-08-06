'''_4912.py

StraightBevelSunGearModalAnalysis
'''


from mastapy.system_model.part_model.gears import _2263
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2528
from mastapy.system_model.analyses_and_results.modal_analyses import _4906
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'StraightBevelSunGearModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearModalAnalysis',)


class StraightBevelSunGearModalAnalysis(_4906.StraightBevelDiffGearModalAnalysis):
    '''StraightBevelSunGearModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2263.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2263.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def system_deflection_results(self) -> '_2528.StraightBevelSunGearSystemDeflection':
        '''StraightBevelSunGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2528.StraightBevelSunGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
