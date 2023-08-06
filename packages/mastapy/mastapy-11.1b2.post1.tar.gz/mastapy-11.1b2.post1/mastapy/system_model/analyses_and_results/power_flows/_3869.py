'''_3869.py

ZerolBevelGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2266
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6677
from mastapy.gears.rating.zerol_bevel import _335
from mastapy.system_model.analyses_and_results.power_flows import _3755
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ZerolBevelGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearPowerFlow',)


class ZerolBevelGearPowerFlow(_3755.BevelGearPowerFlow):
    '''ZerolBevelGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2266.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2266.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6677.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6677.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def component_detailed_analysis(self) -> '_335.ZerolBevelGearRating':
        '''ZerolBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_335.ZerolBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None
