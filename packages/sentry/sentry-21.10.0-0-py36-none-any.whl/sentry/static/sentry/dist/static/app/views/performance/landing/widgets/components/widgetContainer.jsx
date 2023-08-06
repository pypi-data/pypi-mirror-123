Object.defineProperty(exports, "__esModule", { value: true });
exports.WidgetContainerActions = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const useOrganization_1 = require("app/utils/useOrganization");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const contextMenu_1 = (0, tslib_1.__importDefault)(require("app/views/dashboardsV2/contextMenu"));
const types_1 = require("../types");
const widgetDefinitions_1 = require("../widgetDefinitions");
const singleFieldAreaWidget_1 = require("../widgets/singleFieldAreaWidget");
// Use local storage for chart settings for now.
const getContainerLocalStorageKey = (index, height) => `landing-chart-container#${height}#${index}`;
const getChartSetting = (index, height, defaultType, forceDefaultChartSetting // Used for testing.
) => {
    if (forceDefaultChartSetting) {
        return defaultType;
    }
    const key = getContainerLocalStorageKey(index, height);
    const value = localStorage_1.default.getItem(key);
    if (value &&
        Object.values(widgetDefinitions_1.PerformanceWidgetSetting).includes(value)) {
        const _value = value;
        return _value;
    }
    return defaultType;
};
const _setChartSetting = (index, height, setting) => {
    const key = getContainerLocalStorageKey(index, height);
    localStorage_1.default.setItem(key, setting);
};
const _WidgetContainer = (props) => {
    const { organization, index, chartHeight } = props, rest = (0, tslib_1.__rest)(props, ["organization", "index", "chartHeight"]);
    const _chartSetting = getChartSetting(index, chartHeight, rest.defaultChartSetting, rest.forceDefaultChartSetting);
    const [chartSetting, setChartSettingState] = (0, react_1.useState)(_chartSetting);
    const setChartSetting = (setting) => {
        if (!props.forceDefaultChartSetting) {
            _setChartSetting(index, chartHeight, setting);
        }
        setChartSettingState(setting);
    };
    const widgetProps = Object.assign(Object.assign({}, (0, widgetDefinitions_1.WIDGET_DEFINITIONS)({ organization })[chartSetting]), { ContainerActions: containerProps => (<exports.WidgetContainerActions {...containerProps} allowedCharts={props.allowedCharts} setChartSetting={setChartSetting}/>) });
    switch (widgetProps.dataType) {
        case types_1.GenericPerformanceWidgetDataType.trends:
            throw new Error('Trends not currently supported.');
        case types_1.GenericPerformanceWidgetDataType.area:
            return <singleFieldAreaWidget_1.SingleFieldAreaWidget {...props} {...widgetProps}/>;
        default:
            throw new Error(`Widget type "${widgetProps.dataType}" has no implementation.`);
    }
};
const WidgetContainerActions = ({ setChartSetting, allowedCharts, }) => {
    const organization = (0, useOrganization_1.useOrganization)();
    const menuOptions = [];
    const settingsMap = (0, widgetDefinitions_1.WIDGET_DEFINITIONS)({ organization });
    for (const setting of allowedCharts) {
        const options = settingsMap[setting];
        menuOptions.push(<menuItem_1.default key={setting} onClick={() => setChartSetting(setting)} data-test-id="performance-widget-menu-item">
        {options.title}
      </menuItem_1.default>);
    }
    return (<ChartActionContainer>
      <contextMenu_1.default>{menuOptions}</contextMenu_1.default>
    </ChartActionContainer>);
};
exports.WidgetContainerActions = WidgetContainerActions;
const ChartActionContainer = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
`;
const WidgetContainer = (0, withOrganization_1.default)(_WidgetContainer);
exports.default = WidgetContainer;
//# sourceMappingURL=widgetContainer.jsx.map