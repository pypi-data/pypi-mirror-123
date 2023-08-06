Object.defineProperty(exports, "__esModule", { value: true });
exports.DataDisplay = exports.GenericPerformanceWidget = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const iconWarning_1 = require("app/icons/iconWarning");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const performanceWidgetContainer_1 = (0, tslib_1.__importDefault)(require("app/views/performance/landing/widgets/components/performanceWidgetContainer"));
const dataStateSwitch_1 = require("./dataStateSwitch");
const queryHandler_1 = require("./queryHandler");
const widgetHeader_1 = require("./widgetHeader");
// Generic performance widget for type T, where T defines all the data contained in the widget.
function GenericPerformanceWidget(props) {
    const [widgetData, setWidgetData] = (0, react_1.useState)({});
    const setWidgetDataForKey = (0, react_1.useCallback)((dataKey, result) => {
        if (result) {
            setWidgetData(Object.assign(Object.assign({}, widgetData), { [dataKey]: result }));
        }
    }, [setWidgetData]);
    const widgetProps = { widgetData, setWidgetDataForKey };
    const queries = Object.entries(props.Queries).map(([key, definition]) => (Object.assign(Object.assign({}, definition), { queryKey: key })));
    const api = (0, useApi_1.default)();
    return (<react_1.Fragment>
      <queryHandler_1.QueryHandler widgetData={widgetData} setWidgetDataForKey={setWidgetDataForKey} queryProps={props} queries={queries} api={api}/>
      <_DataDisplay {...props} {...widgetProps}/>
    </react_1.Fragment>);
}
exports.GenericPerformanceWidget = GenericPerformanceWidget;
function _DataDisplay(props) {
    const { Visualizations, chartHeight, containerType } = props;
    const Container = (0, performanceWidgetContainer_1.default)({
        containerType,
    });
    const missingDataKeys = !Object.values(props.widgetData).length;
    const hasData = !missingDataKeys && Object.values(props.widgetData).every(d => !d || d.hasData);
    const isLoading = !missingDataKeys && Object.values(props.widgetData).some(d => !d || d.isLoading);
    const isErrored = !missingDataKeys && Object.values(props.widgetData).some(d => d && d.isErrored);
    return (<Container data-test-id="performance-widget-container">
      <ContentContainer>
        <widgetHeader_1.WidgetHeader {...props}/>
      </ContentContainer>
      <dataStateSwitch_1.DataStateSwitch isLoading={isLoading} isErrored={isErrored} hasData={hasData} errorComponent={<DefaultErrorComponent height={chartHeight}/>} dataComponents={Visualizations.map((Visualization, index) => (<ContentContainer key={index} noPadding={Visualization.noPadding} bottomPadding={Visualization.bottomPadding}>
            <Visualization.component grid={defaultGrid} queryFields={Visualization.fields} widgetData={props.widgetData} height={chartHeight}/>
          </ContentContainer>))} emptyComponent={<placeholder_1.default height={`${chartHeight}px`}/>}/>
    </Container>);
}
exports.DataDisplay = (0, react_router_1.withRouter)(_DataDisplay);
const DefaultErrorComponent = (props) => {
    return (<errorPanel_1.default height={`${props.height}px`}>
      <iconWarning_1.IconWarning color="gray300" size="lg"/>
    </errorPanel_1.default>);
};
const defaultGrid = {
    left: (0, space_1.default)(0),
    right: (0, space_1.default)(0),
    top: (0, space_1.default)(2),
    bottom: (0, space_1.default)(0),
};
const ContentContainer = (0, styled_1.default)('div') `
  padding-left: ${p => (p.noPadding ? (0, space_1.default)(0) : (0, space_1.default)(2))};
  padding-right: ${p => (p.noPadding ? (0, space_1.default)(0) : (0, space_1.default)(2))};
  padding-bottom: ${p => (p.bottomPadding ? (0, space_1.default)(1) : (0, space_1.default)(0))};
`;
GenericPerformanceWidget.defaultProps = {
    containerType: 'panel',
    chartHeight: 200,
};
//# sourceMappingURL=performanceWidget.jsx.map