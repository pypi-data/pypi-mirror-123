'''_1538.py

DynamicCustomReportItem
'''


from mastapy._internal import constructor
from mastapy.utility.report import (
    _1519, _1502, _1507, _1508,
    _1509, _1510, _1511, _1512,
    _1514, _1515, _1516, _1517,
    _1518, _1520, _1522, _1523,
    _1526, _1527, _1528, _1530,
    _1531, _1532, _1533, _1535,
    _1536
)
from mastapy.shafts import _20
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _972
from mastapy.utility_gui.charts import _1599, _1600
from mastapy.bearings.bearing_results import (
    _1674, _1675, _1678, _1686
)
from mastapy.system_model.analyses_and_results.system_deflections.reporting import _2557
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4090
from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _4935, _4939
from mastapy._internal.python_net import python_net_import

_DYNAMIC_CUSTOM_REPORT_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'DynamicCustomReportItem')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicCustomReportItem',)


class DynamicCustomReportItem(_1527.CustomReportNameableItem):
    '''DynamicCustomReportItem

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_CUSTOM_REPORT_ITEM

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicCustomReportItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_main_report_item(self) -> 'bool':
        '''bool: 'IsMainReportItem' is the original name of this property.'''

        return self.wrapped.IsMainReportItem

    @is_main_report_item.setter
    def is_main_report_item(self, value: 'bool'):
        self.wrapped.IsMainReportItem = bool(value) if value else False

    @property
    def inner_item(self) -> '_1519.CustomReportItem':
        '''CustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1519.CustomReportItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_shaft_damage_results_table_and_chart(self) -> '_20.ShaftDamageResultsTableAndChart':
        '''ShaftDamageResultsTableAndChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _20.ShaftDamageResultsTableAndChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ShaftDamageResultsTableAndChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_cylindrical_gear_table_with_mg_charts(self) -> '_972.CylindricalGearTableWithMGCharts':
        '''CylindricalGearTableWithMGCharts: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _972.CylindricalGearTableWithMGCharts.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CylindricalGearTableWithMGCharts. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_ad_hoc_custom_table(self) -> '_1502.AdHocCustomTable':
        '''AdHocCustomTable: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1502.AdHocCustomTable.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to AdHocCustomTable. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_chart(self) -> '_1507.CustomChart':
        '''CustomChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1507.CustomChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_graphic(self) -> '_1508.CustomGraphic':
        '''CustomGraphic: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1508.CustomGraphic.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomGraphic. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_image(self) -> '_1509.CustomImage':
        '''CustomImage: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1509.CustomImage.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomImage. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report(self) -> '_1510.CustomReport':
        '''CustomReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1510.CustomReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_cad_drawing(self) -> '_1511.CustomReportCadDrawing':
        '''CustomReportCadDrawing: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1511.CustomReportCadDrawing.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportCadDrawing. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_chart(self) -> '_1512.CustomReportChart':
        '''CustomReportChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1512.CustomReportChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_column(self) -> '_1514.CustomReportColumn':
        '''CustomReportColumn: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1514.CustomReportColumn.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportColumn. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_columns(self) -> '_1515.CustomReportColumns':
        '''CustomReportColumns: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1515.CustomReportColumns.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportColumns. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_definition_item(self) -> '_1516.CustomReportDefinitionItem':
        '''CustomReportDefinitionItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1516.CustomReportDefinitionItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportDefinitionItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_horizontal_line(self) -> '_1517.CustomReportHorizontalLine':
        '''CustomReportHorizontalLine: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1517.CustomReportHorizontalLine.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportHorizontalLine. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_html_item(self) -> '_1518.CustomReportHtmlItem':
        '''CustomReportHtmlItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1518.CustomReportHtmlItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportHtmlItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_item_container(self) -> '_1520.CustomReportItemContainer':
        '''CustomReportItemContainer: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1520.CustomReportItemContainer.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainer. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_item_container_collection_base(self) -> '_1522.CustomReportItemContainerCollectionBase':
        '''CustomReportItemContainerCollectionBase: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1522.CustomReportItemContainerCollectionBase.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainerCollectionBase. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_item_container_collection_item(self) -> '_1523.CustomReportItemContainerCollectionItem':
        '''CustomReportItemContainerCollectionItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1523.CustomReportItemContainerCollectionItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainerCollectionItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_multi_property_item_base(self) -> '_1526.CustomReportMultiPropertyItemBase':
        '''CustomReportMultiPropertyItemBase: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1526.CustomReportMultiPropertyItemBase.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportMultiPropertyItemBase. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_nameable_item(self) -> '_1527.CustomReportNameableItem':
        '''CustomReportNameableItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1527.CustomReportNameableItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportNameableItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_named_item(self) -> '_1528.CustomReportNamedItem':
        '''CustomReportNamedItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1528.CustomReportNamedItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportNamedItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_status_item(self) -> '_1530.CustomReportStatusItem':
        '''CustomReportStatusItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1530.CustomReportStatusItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportStatusItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_tab(self) -> '_1531.CustomReportTab':
        '''CustomReportTab: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1531.CustomReportTab.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportTab. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_tabs(self) -> '_1532.CustomReportTabs':
        '''CustomReportTabs: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1532.CustomReportTabs.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportTabs. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_report_text(self) -> '_1533.CustomReportText':
        '''CustomReportText: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1533.CustomReportText.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportText. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_sub_report(self) -> '_1535.CustomSubReport':
        '''CustomSubReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1535.CustomSubReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomSubReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_table(self) -> '_1536.CustomTable':
        '''CustomTable: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1536.CustomTable.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomTable. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_dynamic_custom_report_item(self) -> 'DynamicCustomReportItem':
        '''DynamicCustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if DynamicCustomReportItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to DynamicCustomReportItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_line_chart(self) -> '_1599.CustomLineChart':
        '''CustomLineChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1599.CustomLineChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomLineChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_custom_table_and_chart(self) -> '_1600.CustomTableAndChart':
        '''CustomTableAndChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1600.CustomTableAndChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomTableAndChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_loaded_ball_element_chart_reporter(self) -> '_1674.LoadedBallElementChartReporter':
        '''LoadedBallElementChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1674.LoadedBallElementChartReporter.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBallElementChartReporter. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_loaded_bearing_chart_reporter(self) -> '_1675.LoadedBearingChartReporter':
        '''LoadedBearingChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1675.LoadedBearingChartReporter.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBearingChartReporter. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_loaded_bearing_temperature_chart(self) -> '_1678.LoadedBearingTemperatureChart':
        '''LoadedBearingTemperatureChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1678.LoadedBearingTemperatureChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBearingTemperatureChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_loaded_roller_element_chart_reporter(self) -> '_1686.LoadedRollerElementChartReporter':
        '''LoadedRollerElementChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1686.LoadedRollerElementChartReporter.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedRollerElementChartReporter. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_shaft_system_deflection_sections_report(self) -> '_2557.ShaftSystemDeflectionSectionsReport':
        '''ShaftSystemDeflectionSectionsReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2557.ShaftSystemDeflectionSectionsReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ShaftSystemDeflectionSectionsReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_parametric_study_histogram(self) -> '_4090.ParametricStudyHistogram':
        '''ParametricStudyHistogram: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4090.ParametricStudyHistogram.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ParametricStudyHistogram. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_campbell_diagram_report(self) -> '_4935.CampbellDiagramReport':
        '''CampbellDiagramReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4935.CampbellDiagramReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CampbellDiagramReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None

    @property
    def inner_item_of_type_per_mode_results_report(self) -> '_4939.PerModeResultsReport':
        '''PerModeResultsReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4939.PerModeResultsReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to PerModeResultsReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerItem.__class__)(self.wrapped.InnerItem) if self.wrapped.InnerItem is not None else None
