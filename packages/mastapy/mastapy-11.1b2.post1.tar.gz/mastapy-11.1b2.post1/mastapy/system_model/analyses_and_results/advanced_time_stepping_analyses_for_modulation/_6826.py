'''_6826.py

WormGearMeshAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.connections_and_sockets.gears import _2044
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6675
from mastapy.system_model.analyses_and_results.system_deflections import _2544
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6760
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'WormGearMeshAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshAdvancedTimeSteppingAnalysisForModulation',)


class WormGearMeshAdvancedTimeSteppingAnalysisForModulation(_6760.GearMeshAdvancedTimeSteppingAnalysisForModulation):
    '''WormGearMeshAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2044.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2044.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6675.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6675.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2544.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2544.WormGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
