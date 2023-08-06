Object.defineProperty(exports, "__esModule", { value: true });
exports.SingleFieldAreaWidget = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const chart_1 = (0, tslib_1.__importDefault)(require("app/views/performance/charts/chart"));
const performanceWidget_1 = require("../components/performanceWidget");
const transformEventsToArea_1 = require("../transforms/transformEventsToArea");
function SingleFieldAreaWidget(props) {
    const { ContainerActions } = props;
    const globalSelection = props.eventView.getGlobalSelection();
    if (props.fields.length !== 1) {
        throw new Error(`Single field area can only accept a single field (${props.fields})`);
    }
    const Queries = (0, react_1.useMemo)(() => {
        return {
            chart: {
                fields: props.fields[0],
                component: provided => (<EventsRequest {...provided} limit={1} includePrevious includeTransformedData partial currentSeriesName={props.fields[0]} query={props.eventView.getQueryWithAdditionalConditions()}/>),
                transform: transformEventsToArea_1.transformEventsRequestToArea,
            },
        };
    }, [props.eventView, props.fields, props.organization.slug]);
    return (<performanceWidget_1.GenericPerformanceWidget {...props} subtitle={<Subtitle>{(0, locale_1.t)('Compared to last %s ', globalSelection.datetime.period)}</Subtitle>} HeaderActions={provided => {
            var _a, _b, _c;
            return (<react_1.Fragment>
          <HighlightNumber color={props.chartColor}>
            {((_a = provided.widgetData.chart) === null || _a === void 0 ? void 0 : _a.hasData)
                    ? (_c = (_b = provided.widgetData.chart) === null || _b === void 0 ? void 0 : _b.dataMean) === null || _c === void 0 ? void 0 : _c[0].label
                    : null}
          </HighlightNumber>
          <ContainerActions {...provided.widgetData.chart}/>
        </react_1.Fragment>);
        }} Queries={Queries} Visualizations={[
            {
                component: provided => (<DurationChart {...provided.widgetData.chart} {...provided} disableMultiAxis disableXAxis chartColors={props.chartColor ? [props.chartColor] : undefined}/>),
                height: 160,
            },
        ]}/>);
}
exports.SingleFieldAreaWidget = SingleFieldAreaWidget;
const EventsRequest = (0, withApi_1.default)(eventsRequest_1.default);
const DurationChart = (0, react_router_1.withRouter)(chart_1.default);
const Subtitle = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeMedium};
`;
const HighlightNumber = (0, styled_1.default)('div') `
  color: ${p => p.color};
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
//# sourceMappingURL=singleFieldAreaWidget.jsx.map