Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const locale_1 = require("app/locale");
const types_1 = require("./types");
const utils_1 = require("./utils");
/**
 * Making 1 extra API call to display this number isn't very efficient.
 * The other approach would be to fetch the data in UsageStatsOrg with 1min
 * interval and roll it up on the frontend, but that (1) adds unnecessary
 * complexity as it's gnarly to fetch + rollup 90 days of 1min intervals,
 * (3) API resultset has a limit of 1000, so 90 days of 1min would not work.
 *
 * We're going with this approach for simplicity sake. By keeping the range
 * as small as possible, this call is quite fast.
 */
class UsageStatsPerMin extends asyncComponent_1.default {
    getEndpoints() {
        return [['orgStats', this.endpointPath, { query: this.endpointQuery }]];
    }
    get endpointPath() {
        const { organization } = this.props;
        return `/organizations/${organization.slug}/stats_v2/`;
    }
    get endpointQuery() {
        return {
            statsPeriod: '5m',
            interval: '1m',
            groupBy: ['category', 'outcome'],
            field: ['sum(quantity)'],
        };
    }
    get minuteData() {
        const { dataCategory } = this.props;
        const { loading, error, orgStats } = this.state;
        if (loading || error || !orgStats || orgStats.intervals.length === 0) {
            return undefined;
        }
        // The last minute in the series is still "in progress"
        // Read data from 2nd last element for the latest complete minute
        const { intervals, groups } = orgStats;
        const lastMin = Math.max(intervals.length - 2, 0);
        const eventsLastMin = groups.reduce((count, group) => {
            const { outcome, category } = group.by;
            // HACK: The backend enum are singular, but the frontend enums are plural
            if (!dataCategory.includes(`${category}`) || outcome !== types_1.Outcome.ACCEPTED) {
                return count;
            }
            count += group.series['sum(quantity)'][lastMin];
            return count;
        }, 0);
        return (0, utils_1.formatUsageWithUnits)(eventsLastMin, dataCategory, (0, utils_1.getFormatUsageOptions)(dataCategory));
    }
    renderComponent() {
        if (!this.minuteData) {
            return null;
        }
        return (<Wrapper>
        {this.minuteData} {(0, locale_1.t)('in last min')}
      </Wrapper>);
    }
}
exports.default = UsageStatsPerMin;
const Wrapper = (0, styled_1.default)('div') `
  display: inline-block;
  color: ${p => p.theme.success};
  font-size: ${p => p.theme.fontSizeMedium};
`;
//# sourceMappingURL=usageStatsPerMin.jsx.map