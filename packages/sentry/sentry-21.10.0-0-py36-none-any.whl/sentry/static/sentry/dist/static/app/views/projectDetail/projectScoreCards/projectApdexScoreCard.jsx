Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const round_1 = (0, tslib_1.__importDefault)(require("lodash/round"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const utils_1 = require("app/components/organizations/timeRangeSelector/utils");
const scoreCard_1 = (0, tslib_1.__importDefault)(require("app/components/scoreCard"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_2 = require("app/utils");
const fields_1 = require("app/utils/discover/fields");
const getPeriod_1 = require("app/utils/getPeriod");
const data_1 = require("app/views/performance/data");
const missingPerformanceButtons_1 = (0, tslib_1.__importDefault)(require("../missingFeatureButtons/missingPerformanceButtons"));
const utils_3 = require("../utils");
class ProjectApdexScoreCard extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldRenderBadRequests = true;
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { currentApdex: null, previousApdex: null });
    }
    getEndpoints() {
        const { organization, selection, isProjectStabilized, hasTransactions, query } = this.props;
        if (!this.hasFeature() || !isProjectStabilized || !hasTransactions) {
            return [];
        }
        const { projects, environments, datetime } = selection;
        const { period } = datetime;
        const commonQuery = {
            environment: environments,
            project: projects.map(proj => String(proj)),
            field: ['apdex()'],
            query: ['event.type:transaction count():>0', query].join(' ').trim(),
        };
        const endpoints = [
            [
                'currentApdex',
                `/organizations/${organization.slug}/eventsv2/`,
                { query: Object.assign(Object.assign({}, commonQuery), (0, getParams_1.getParams)(datetime)) },
            ],
        ];
        if ((0, utils_3.shouldFetchPreviousPeriod)(datetime)) {
            const { start: previousStart } = (0, utils_1.parseStatsPeriod)((0, getPeriod_1.getPeriod)({ period, start: undefined, end: undefined }, { shouldDoublePeriod: true })
                .statsPeriod);
            const { start: previousEnd } = (0, utils_1.parseStatsPeriod)((0, getPeriod_1.getPeriod)({ period, start: undefined, end: undefined }, { shouldDoublePeriod: false })
                .statsPeriod);
            endpoints.push([
                'previousApdex',
                `/organizations/${organization.slug}/eventsv2/`,
                { query: Object.assign(Object.assign({}, commonQuery), { start: previousStart, end: previousEnd }) },
            ]);
        }
        return endpoints;
    }
    componentDidUpdate(prevProps) {
        const { selection, isProjectStabilized, hasTransactions, query } = this.props;
        if (prevProps.selection !== selection ||
            prevProps.hasTransactions !== hasTransactions ||
            prevProps.isProjectStabilized !== isProjectStabilized ||
            prevProps.query !== query) {
            this.remountComponent();
        }
    }
    hasFeature() {
        return this.props.organization.features.includes('performance-view');
    }
    get cardTitle() {
        return (0, locale_1.t)('Apdex');
    }
    get cardHelp() {
        const { organization } = this.props;
        const baseHelp = (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.APDEX_NEW);
        if (this.trend) {
            return baseHelp + (0, locale_1.t)(' This shows how it has changed since the last period.');
        }
        return baseHelp;
    }
    get currentApdex() {
        var _a;
        const { currentApdex } = this.state;
        const apdex = (_a = currentApdex === null || currentApdex === void 0 ? void 0 : currentApdex.data[0]) === null || _a === void 0 ? void 0 : _a[(0, fields_1.getAggregateAlias)('apdex()')];
        return typeof apdex === 'undefined' ? undefined : Number(apdex);
    }
    get previousApdex() {
        var _a;
        const { previousApdex } = this.state;
        const apdex = (_a = previousApdex === null || previousApdex === void 0 ? void 0 : previousApdex.data[0]) === null || _a === void 0 ? void 0 : _a[(0, fields_1.getAggregateAlias)('apdex()')];
        return typeof apdex === 'undefined' ? undefined : Number(apdex);
    }
    get trend() {
        if (this.currentApdex && this.previousApdex) {
            return (0, round_1.default)(this.currentApdex - this.previousApdex, 3);
        }
        return null;
    }
    get trendStatus() {
        if (!this.trend) {
            return undefined;
        }
        return this.trend > 0 ? 'good' : 'bad';
    }
    renderLoading() {
        return this.renderBody();
    }
    renderMissingFeatureCard() {
        const { organization } = this.props;
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={<missingPerformanceButtons_1.default organization={organization}/>}/>);
    }
    renderScore() {
        return (0, utils_2.defined)(this.currentApdex) ? <count_1.default value={this.currentApdex}/> : '\u2014';
    }
    renderTrend() {
        // we want to show trend only after currentApdex has loaded to prevent jumping
        return (0, utils_2.defined)(this.currentApdex) && (0, utils_2.defined)(this.trend) ? (<React.Fragment>
        {this.trend >= 0 ? (<icons_1.IconArrow direction="up" size="xs"/>) : (<icons_1.IconArrow direction="down" size="xs"/>)}
        <count_1.default value={Math.abs(this.trend)}/>
      </React.Fragment>) : null;
    }
    renderBody() {
        const { hasTransactions } = this.props;
        if (!this.hasFeature() || hasTransactions === false) {
            return this.renderMissingFeatureCard();
        }
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={this.renderScore()} trend={this.renderTrend()} trendStatus={this.trendStatus}/>);
    }
}
exports.default = ProjectApdexScoreCard;
//# sourceMappingURL=projectApdexScoreCard.jsx.map