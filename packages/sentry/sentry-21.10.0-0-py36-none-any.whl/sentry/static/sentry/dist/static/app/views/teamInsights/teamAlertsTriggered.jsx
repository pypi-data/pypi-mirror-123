Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("./utils");
class TeamAlertsTriggered extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldRenderBadRequests = true;
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { alertsTriggered: null });
    }
    getEndpoints() {
        const { organization, start, end, period, utc, teamSlug } = this.props;
        const datetime = { start, end, period, utc };
        return [
            [
                'alertsTriggered',
                `/teams/${organization.slug}/${teamSlug}/alerts-triggered/`,
                {
                    query: Object.assign({}, (0, getParams_1.getParams)(datetime)),
                },
            ],
        ];
    }
    componentDidUpdate(prevProps) {
        const { start, end, period, utc, teamSlug } = this.props;
        if (prevProps.start !== start ||
            prevProps.end !== end ||
            prevProps.period !== period ||
            prevProps.utc !== utc ||
            prevProps.teamSlug !== teamSlug) {
            this.remountComponent();
        }
    }
    renderLoading() {
        return (<ChartWrapper>
        <loadingIndicator_1.default />
      </ChartWrapper>);
    }
    renderBody() {
        const { alertsTriggered } = this.state;
        const data = (0, utils_1.convertDayValueObjectToSeries)(alertsTriggered !== null && alertsTriggered !== void 0 ? alertsTriggered : {});
        const seriesData = (0, utils_1.convertDaySeriesToWeeks)(data);
        return (<ChartWrapper>
        {alertsTriggered && (<barChart_1.default style={{ height: 190 }} isGroupedByDate useShortDate period="7d" legend={{ right: 0, top: 0 }} yAxis={{ minInterval: 1 }} xAxis={{
                    type: 'time',
                }} series={[
                    {
                        seriesName: (0, locale_1.t)('Alerts Triggered'),
                        data: seriesData,
                    },
                ].reverse()}/>)}
      </ChartWrapper>);
    }
}
exports.default = TeamAlertsTriggered;
const ChartWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(2)} 0 ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=teamAlertsTriggered.jsx.map