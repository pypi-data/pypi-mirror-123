Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
const utils_1 = require("./utils");
class TeamResolutionTime extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldRenderBadRequests = true;
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { resolutionTime: null });
    }
    getEndpoints() {
        const { organization, start, end, period, utc, teamSlug } = this.props;
        const datetime = { start, end, period, utc };
        return [
            [
                'resolutionTime',
                `/teams/${organization.slug}/${teamSlug}/time-to-resolution/`,
                {
                    query: Object.assign({}, (0, getParams_1.getParams)(datetime)),
                },
            ],
        ];
    }
    renderLoading() {
        return (<ChartWrapper>
        <loadingIndicator_1.default />
      </ChartWrapper>);
    }
    renderBody() {
        const { resolutionTime } = this.state;
        const data = Object.entries(resolutionTime !== null && resolutionTime !== void 0 ? resolutionTime : {}).map(([bucket, { avg }]) => ({
            value: avg,
            name: new Date(bucket).getTime(),
        }));
        const seriesData = (0, utils_1.convertDaySeriesToWeeks)(data);
        return (<ChartWrapper>
        <barChart_1.default style={{ height: 190 }} isGroupedByDate useShortDate period="7d" tooltip={{
                valueFormatter: (value) => (0, formatters_1.getDuration)(value, 1),
            }} yAxis={{
                // Each yAxis marker will increase by 1 day
                minInterval: 86400,
                axisLabel: {
                    formatter: (value) => {
                        if (value === 0) {
                            return '';
                        }
                        return (0, formatters_1.getDuration)(value, 0, true, true);
                    },
                },
            }} legend={{ right: 0, top: 0 }} xAxis={{
                type: 'time',
            }} series={[
                {
                    seriesName: (0, locale_1.t)('Time to Resolution'),
                    data: seriesData,
                },
            ].reverse()}/>
      </ChartWrapper>);
    }
}
exports.default = TeamResolutionTime;
const ChartWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(2)} 0 ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=teamResolutionTime.jsx.map