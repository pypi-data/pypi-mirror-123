Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const footer_1 = (0, tslib_1.__importDefault)(require("../../charts/footer"));
const utils_1 = require("../../utils");
const singleAxisChart_1 = require("./singleAxisChart");
const utils_2 = require("./utils");
function DoubleAxisDisplay(props) {
    const { eventView, location, organization, axisOptions, leftAxis, rightAxis } = props;
    const [usingBackupAxis, setUsingBackupAxis] = (0, react_1.useState)(false);
    const onFilterChange = (field) => (minValue, maxValue) => {
        const filterString = (0, utils_1.getTransactionSearchQuery)(location);
        const conditions = new tokenizeSearch_1.MutableSearch(filterString);
        conditions.setFilterValues(field, [
            `>=${Math.round(minValue)}`,
            `<${Math.round(maxValue)}`,
        ]);
        const query = conditions.formatString();
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance_views.landingv2.display.filter_change',
            eventName: 'Performance Views: Landing v2 Display Filter Change',
            organization_id: parseInt(organization.id, 10),
            field,
            min_value: parseInt(minValue, 10),
            max_value: parseInt(maxValue, 10),
        });
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: Object.assign(Object.assign({}, location.query), { query: String(query).trim() }),
        });
    };
    const didReceiveMultiAxis = (useBackup) => {
        setUsingBackupAxis(useBackup);
    };
    const leftAxisOrBackup = (0, utils_2.getAxisOrBackupAxis)(leftAxis, usingBackupAxis);
    const rightAxisOrBackup = (0, utils_2.getAxisOrBackupAxis)(rightAxis, usingBackupAxis);
    const optionsOrBackup = (0, utils_2.getBackupAxes)(axisOptions, usingBackupAxis);
    return (<panels_1.Panel>
      <DoubleChartContainer>
        <singleAxisChart_1.SingleAxisChart axis={leftAxis} onFilterChange={onFilterChange(leftAxis.field)} didReceiveMultiAxis={didReceiveMultiAxis} usingBackupAxis={usingBackupAxis} {...props}/>
        <singleAxisChart_1.SingleAxisChart axis={rightAxis} onFilterChange={onFilterChange(rightAxis.field)} didReceiveMultiAxis={didReceiveMultiAxis} usingBackupAxis={usingBackupAxis} {...props}/>
      </DoubleChartContainer>

      <Footer options={optionsOrBackup} leftAxis={leftAxisOrBackup.value} rightAxis={rightAxisOrBackup.value} organization={organization} eventView={eventView} location={location}/>
    </panels_1.Panel>);
}
const DoubleChartContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: ${(0, space_1.default)(3)};
  min-height: 282px;
`;
const Footer = (0, withApi_1.default)(footer_1.default);
exports.default = DoubleAxisDisplay;
//# sourceMappingURL=doubleAxisDisplay.jsx.map