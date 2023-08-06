Object.defineProperty(exports, "__esModule", { value: true });
exports.DisplayModes = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const react_2 = require("@emotion/react");
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const loadingPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/loadingPanel"));
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const styles_1 = require("app/components/charts/styles");
const utils_1 = require("app/components/charts/utils");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const chartPalette_1 = (0, tslib_1.__importDefault)(require("app/constants/chartPalette"));
const notAvailableMessages_1 = (0, tslib_1.__importDefault)(require("app/constants/notAvailableMessages"));
const locale_1 = require("app/locale");
const utils_2 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
const data_1 = require("../performance/data");
const projectBaseEventsChart_1 = (0, tslib_1.__importDefault)(require("./charts/projectBaseEventsChart"));
const projectBaseSessionsChart_1 = (0, tslib_1.__importDefault)(require("./charts/projectBaseSessionsChart"));
const projectErrorsBasicChart_1 = (0, tslib_1.__importDefault)(require("./charts/projectErrorsBasicChart"));
var DisplayModes;
(function (DisplayModes) {
    DisplayModes["APDEX"] = "apdex";
    DisplayModes["FAILURE_RATE"] = "failure_rate";
    DisplayModes["TPM"] = "tpm";
    DisplayModes["ERRORS"] = "errors";
    DisplayModes["TRANSACTIONS"] = "transactions";
    DisplayModes["STABILITY"] = "crash_free";
    DisplayModes["SESSIONS"] = "sessions";
})(DisplayModes = exports.DisplayModes || (exports.DisplayModes = {}));
class ProjectCharts extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            totalValues: null,
        };
        this.handleDisplayModeChange = (value) => {
            const { location, chartId, chartIndex, organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: `project_detail.change_chart${chartIndex + 1}`,
                eventName: `Project Detail: Change Chart #${chartIndex + 1}`,
                organization_id: parseInt(organization.id, 10),
                metric: value,
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { [chartId]: value }),
            });
        };
        this.handleTotalValuesChange = (value) => {
            if (value !== this.state.totalValues) {
                this.setState({ totalValues: value });
            }
        };
    }
    get defaultDisplayModes() {
        const { hasSessions, hasTransactions } = this.props;
        if (!hasSessions && !hasTransactions) {
            return [DisplayModes.ERRORS];
        }
        if (hasSessions && !hasTransactions) {
            return [DisplayModes.STABILITY, DisplayModes.ERRORS];
        }
        if (!hasSessions && hasTransactions) {
            return [DisplayModes.FAILURE_RATE, DisplayModes.APDEX];
        }
        return [DisplayModes.STABILITY, DisplayModes.APDEX];
    }
    get otherActiveDisplayModes() {
        const { location, visibleCharts, chartId } = this.props;
        return visibleCharts
            .filter(visibleChartId => visibleChartId !== chartId)
            .map(urlKey => {
            return (0, queryString_1.decodeScalar)(location.query[urlKey], this.defaultDisplayModes[visibleCharts.findIndex(value => value === urlKey)]);
        });
    }
    get displayMode() {
        const { location, chartId, chartIndex } = this.props;
        const displayMode = (0, queryString_1.decodeScalar)(location.query[chartId]) || this.defaultDisplayModes[chartIndex];
        if (!Object.values(DisplayModes).includes(displayMode)) {
            return this.defaultDisplayModes[chartIndex];
        }
        return displayMode;
    }
    get displayModes() {
        const { organization, hasSessions, hasTransactions } = this.props;
        const hasPerformance = organization.features.includes('performance-view');
        const noPerformanceTooltip = notAvailableMessages_1.default.performance;
        const noHealthTooltip = notAvailableMessages_1.default.releaseHealth;
        return [
            {
                value: DisplayModes.STABILITY,
                label: (0, locale_1.t)('Crash Free Sessions'),
                disabled: this.otherActiveDisplayModes.includes(DisplayModes.STABILITY) || !hasSessions,
                tooltip: !hasSessions ? noHealthTooltip : undefined,
            },
            {
                value: DisplayModes.APDEX,
                label: (0, locale_1.t)('Apdex'),
                disabled: this.otherActiveDisplayModes.includes(DisplayModes.APDEX) ||
                    !hasPerformance ||
                    !hasTransactions,
                tooltip: hasPerformance && hasTransactions
                    ? (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.APDEX)
                    : noPerformanceTooltip,
            },
            {
                value: DisplayModes.FAILURE_RATE,
                label: (0, locale_1.t)('Failure Rate'),
                disabled: this.otherActiveDisplayModes.includes(DisplayModes.FAILURE_RATE) ||
                    !hasPerformance ||
                    !hasTransactions,
                tooltip: hasPerformance && hasTransactions
                    ? (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE)
                    : noPerformanceTooltip,
            },
            {
                value: DisplayModes.TPM,
                label: (0, locale_1.t)('Transactions Per Minute'),
                disabled: this.otherActiveDisplayModes.includes(DisplayModes.TPM) ||
                    !hasPerformance ||
                    !hasTransactions,
                tooltip: hasPerformance && hasTransactions
                    ? (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.TPM)
                    : noPerformanceTooltip,
            },
            {
                value: DisplayModes.ERRORS,
                label: (0, locale_1.t)('Number of Errors'),
                disabled: this.otherActiveDisplayModes.includes(DisplayModes.ERRORS),
            },
            {
                value: DisplayModes.SESSIONS,
                label: (0, locale_1.t)('Number of Sessions'),
                disabled: this.otherActiveDisplayModes.includes(DisplayModes.SESSIONS) || !hasSessions,
                tooltip: !hasSessions ? noHealthTooltip : undefined,
            },
            {
                value: DisplayModes.TRANSACTIONS,
                label: (0, locale_1.t)('Number of Transactions'),
                disabled: this.otherActiveDisplayModes.includes(DisplayModes.TRANSACTIONS) ||
                    !hasPerformance ||
                    !hasTransactions,
                tooltip: hasPerformance && hasTransactions ? undefined : noPerformanceTooltip,
            },
        ];
    }
    get summaryHeading() {
        switch (this.displayMode) {
            case DisplayModes.ERRORS:
                return (0, locale_1.t)('Total Errors');
            case DisplayModes.STABILITY:
            case DisplayModes.SESSIONS:
                return (0, locale_1.t)('Total Sessions');
            case DisplayModes.APDEX:
            case DisplayModes.FAILURE_RATE:
            case DisplayModes.TPM:
            case DisplayModes.TRANSACTIONS:
            default:
                return (0, locale_1.t)('Total Transactions');
        }
    }
    get barChartInterval() {
        const { query } = this.props.location;
        const diffInMinutes = (0, utils_1.getDiffInMinutes)(Object.assign(Object.assign({}, query), { period: (0, queryString_1.decodeScalar)(query.statsPeriod) }));
        if (diffInMinutes >= utils_1.TWO_WEEKS) {
            return '1d';
        }
        if (diffInMinutes >= utils_1.ONE_WEEK) {
            return '12h';
        }
        if (diffInMinutes > utils_1.TWENTY_FOUR_HOURS) {
            return '6h';
        }
        if (diffInMinutes === utils_1.TWENTY_FOUR_HOURS) {
            return '1h';
        }
        if (diffInMinutes <= utils_1.ONE_HOUR) {
            return '1m';
        }
        return '15m';
    }
    render() {
        const { api, router, location, organization, theme, projectId, hasSessions, query } = this.props;
        const { totalValues } = this.state;
        const hasDiscover = organization.features.includes('discover-basic');
        const displayMode = this.displayMode;
        return (<panels_1.Panel>
        <styles_1.ChartContainer>
          {!(0, utils_2.defined)(hasSessions) ? (<loadingPanel_1.default />) : (<react_1.Fragment>
              {displayMode === DisplayModes.APDEX && (<projectBaseEventsChart_1.default title={(0, locale_1.t)('Apdex')} help={(0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.APDEX_NEW)} query={new tokenizeSearch_1.MutableSearch([
                        'event.type:transaction',
                        query !== null && query !== void 0 ? query : '',
                    ]).formatString()} yAxis="apdex()" field={['apdex()']} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[chartPalette_1.default[0][0], theme.purple200]}/>)}
              {displayMode === DisplayModes.FAILURE_RATE && (<projectBaseEventsChart_1.default title={(0, locale_1.t)('Failure Rate')} help={(0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE)} query={new tokenizeSearch_1.MutableSearch([
                        'event.type:transaction',
                        query !== null && query !== void 0 ? query : '',
                    ]).formatString()} yAxis="failure_rate()" field={[`failure_rate()`]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.red300, theme.purple200]}/>)}
              {displayMode === DisplayModes.TPM && (<projectBaseEventsChart_1.default title={(0, locale_1.t)('Transactions Per Minute')} help={(0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.TPM)} query={new tokenizeSearch_1.MutableSearch([
                        'event.type:transaction',
                        query !== null && query !== void 0 ? query : '',
                    ]).formatString()} yAxis="tpm()" field={[`tpm()`]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.yellow300, theme.purple200]} disablePrevious/>)}
              {displayMode === DisplayModes.ERRORS &&
                    (hasDiscover ? (<projectBaseEventsChart_1.default title={(0, locale_1.t)('Number of Errors')} query={new tokenizeSearch_1.MutableSearch([
                            '!event.type:transaction',
                            query !== null && query !== void 0 ? query : '',
                        ]).formatString()} yAxis="count()" field={[`count()`]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.purple300, theme.purple200]} interval={this.barChartInterval} chartComponent={barChart_1.default} disableReleases/>) : (<projectErrorsBasicChart_1.default organization={organization} projectId={projectId} location={location} onTotalValuesChange={this.handleTotalValuesChange}/>))}
              {displayMode === DisplayModes.TRANSACTIONS && (<projectBaseEventsChart_1.default title={(0, locale_1.t)('Number of Transactions')} query={new tokenizeSearch_1.MutableSearch([
                        'event.type:transaction',
                        query !== null && query !== void 0 ? query : '',
                    ]).formatString()} yAxis="count()" field={[`count()`]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.gray200, theme.purple200]} interval={this.barChartInterval} chartComponent={barChart_1.default} disableReleases/>)}
              {displayMode === DisplayModes.STABILITY && (<projectBaseSessionsChart_1.default title={(0, locale_1.t)('Crash Free Sessions')} help={(0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.STABILITY, null)} router={router} api={api} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} displayMode={displayMode} query={query}/>)}
              {displayMode === DisplayModes.SESSIONS && (<projectBaseSessionsChart_1.default title={(0, locale_1.t)('Number of Sessions')} router={router} api={api} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} displayMode={displayMode} disablePrevious query={query}/>)}
            </react_1.Fragment>)}
        </styles_1.ChartContainer>
        <styles_1.ChartControls>
          {/* if hasSessions is not yet defined, it means that request is still in progress and we can't decide what default chart to show */}
          {(0, utils_2.defined)(hasSessions) ? (<react_1.Fragment>
              <styles_1.InlineContainer>
                <styles_1.SectionHeading>{this.summaryHeading}</styles_1.SectionHeading>
                <styles_1.SectionValue>
                  {typeof totalValues === 'number'
                    ? totalValues.toLocaleString()
                    : '\u2014'}
                </styles_1.SectionValue>
              </styles_1.InlineContainer>
              <styles_1.InlineContainer>
                <optionSelector_1.default title={(0, locale_1.t)('Display')} selected={displayMode} options={this.displayModes} onChange={this.handleDisplayModeChange}/>
              </styles_1.InlineContainer>
            </react_1.Fragment>) : (<placeholder_1.default height="34px"/>)}
        </styles_1.ChartControls>
      </panels_1.Panel>);
    }
}
exports.default = (0, withApi_1.default)((0, react_2.withTheme)(ProjectCharts));
//# sourceMappingURL=projectCharts.jsx.map