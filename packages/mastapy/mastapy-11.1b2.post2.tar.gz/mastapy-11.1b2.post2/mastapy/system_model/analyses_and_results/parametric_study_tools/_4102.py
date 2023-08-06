'''_4102.py

PlanetaryGearSetParametricStudyTool
'''


from mastapy.system_model.part_model.gears import _2255
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4049
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'PlanetaryGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetParametricStudyTool',)


class PlanetaryGearSetParametricStudyTool(_4049.CylindricalGearSetParametricStudyTool):
    '''PlanetaryGearSetParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2255.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2255.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None
