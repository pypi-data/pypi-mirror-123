'''_2517.py

SpiralBevelGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2256
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6645
from mastapy.system_model.analyses_and_results.power_flows import _3841
from mastapy.gears.rating.spiral_bevel import _368
from mastapy.system_model.analyses_and_results.system_deflections import _2416
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SpiralBevelGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSystemDeflection',)


class SpiralBevelGearSystemDeflection(_2416.BevelGearSystemDeflection):
    '''SpiralBevelGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2256.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2256.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6645.SpiralBevelGearLoadCase':
        '''SpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6645.SpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3841.SpiralBevelGearPowerFlow':
        '''SpiralBevelGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3841.SpiralBevelGearPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None

    @property
    def component_detailed_analysis(self) -> '_368.SpiralBevelGearRating':
        '''SpiralBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_368.SpiralBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None
