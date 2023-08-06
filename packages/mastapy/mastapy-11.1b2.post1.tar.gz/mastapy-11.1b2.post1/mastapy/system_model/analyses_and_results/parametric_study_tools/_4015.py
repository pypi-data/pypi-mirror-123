'''_4015.py

BevelDifferentialSunGearParametricStudyTool
'''


from mastapy.system_model.part_model.gears import _2231
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4012
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BevelDifferentialSunGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearParametricStudyTool',)


class BevelDifferentialSunGearParametricStudyTool(_4012.BevelDifferentialGearParametricStudyTool):
    '''BevelDifferentialSunGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2231.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2231.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None
