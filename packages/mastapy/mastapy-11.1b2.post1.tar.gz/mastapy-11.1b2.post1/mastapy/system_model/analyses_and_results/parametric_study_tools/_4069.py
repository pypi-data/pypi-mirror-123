'''_4069.py

HypoidGearMeshParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2030
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6596
from mastapy.system_model.analyses_and_results.system_deflections import _2471
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4004
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'HypoidGearMeshParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshParametricStudyTool',)


class HypoidGearMeshParametricStudyTool(_4004.AGMAGleasonConicalGearMeshParametricStudyTool):
    '''HypoidGearMeshParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2030.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2030.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6596.HypoidGearMeshLoadCase':
        '''HypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6596.HypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2471.HypoidGearMeshSystemDeflection]':
        '''List[HypoidGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2471.HypoidGearMeshSystemDeflection))
        return value
