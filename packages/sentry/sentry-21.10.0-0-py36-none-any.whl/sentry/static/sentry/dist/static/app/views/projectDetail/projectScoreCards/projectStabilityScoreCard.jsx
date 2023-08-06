Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const round_1 = (0, tslib_1.__importDefault)(require("lodash/round"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const utils_1 = require("app/components/charts/utils");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const scoreCard_1 = (0, tslib_1.__importDefault)(require("app/components/scoreCard"));
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_2 = require("app/utils");
const formatters_1 = require("app/utils/formatters");
const getPeriod_1 = require("app/utils/getPeriod");
const utils_3 = require("app/views/releases/utils");
const sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
const missingReleasesButtons_1 = (0, tslib_1.__importDefault)(require("../missingFeatureButtons/missingReleasesButtons"));
const utils_4 = require("../utils");
class ProjectStabilityScoreCard extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldRenderBadRequests = true;
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { currentSessions: null, previousSessions: null });
    }
    getEndpoints() {
        const { organization, selection, isProjectStabilized, hasSessions, query } = this.props;
        if (!isProjectStabilized || !hasSessions) {
            return [];
        }
        const { projects, environments: environment, datetime } = selection;
        const { period } = datetime;
        const commonQuery = {
            environment,
            project: projects[0],
            field: 'sum(session)',
            groupBy: 'session.status',
            interval: (0, utils_1.getDiffInMinutes)(datetime) > 24 * 60 ? '1d' : '1h',
            query,
        };
        // Unfortunately we can't do something like statsPeriod=28d&interval=14d to get scores for this and previous interval with the single request
        // https://github.com/getsentry/sentry/pull/22770#issuecomment-758595553
        const endpoints = [
            [
                'currentSessions',
                `/organizations/${organization.slug}/sessions/`,
                {
                    query: Object.assign(Object.assign({}, commonQuery), (0, getParams_1.getParams)(datetime)),
                },
            ],
        ];
        if ((0, utils_4.shouldFetchPreviousPeriod)(datetime)) {
            const doubledPeriod = (0, getPeriod_1.getPeriod)({ period, start: undefined, end: undefined }, { shouldDoublePeriod: true }).statsPeriod;
            endpoints.push([
                'previousSessions',
                `/organizations/${organization.slug}/sessions/`,
                {
                    query: Object.assign(Object.assign({}, commonQuery), { statsPeriodStart: doubledPeriod, statsPeriodEnd: period !== null && period !== void 0 ? period : constants_1.DEFAULT_STATS_PERIOD }),
                },
            ]);
        }
        return endpoints;
    }
    get cardTitle() {
        return (0, locale_1.t)('Crash Free Sessions');
    }
    get cardHelp() {
        return this.trend
            ? (0, locale_1.t)('The percentage of crash free sessions and how it has changed since the last period.')
            : (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.STABILITY, null);
    }
    get score() {
        const { currentSessions } = this.state;
        return this.calculateCrashFree(currentSessions);
    }
    get trend() {
        const { previousSessions } = this.state;
        const previousScore = this.calculateCrashFree(previousSessions);
        if (!(0, utils_2.defined)(this.score) || !(0, utils_2.defined)(previousScore)) {
            return undefined;
        }
        return (0, round_1.default)(this.score - previousScore, 3);
    }
    get trendStatus() {
        if (!this.trend) {
            return undefined;
        }
        return this.trend > 0 ? 'good' : 'bad';
    }
    componentDidUpdate(prevProps) {
        const { selection, isProjectStabilized, hasSessions, query } = this.props;
        if (prevProps.selection !== selection ||
            prevProps.hasSessions !== hasSessions ||
            prevProps.isProjectStabilized !== isProjectStabilized ||
            prevProps.query !== query) {
            this.remountComponent();
        }
    }
    calculateCrashFree(data) {
        var _a;
        if (!data) {
            return undefined;
        }
        const totalSessions = data.groups.reduce((acc, group) => acc + group.totals['sum(session)'], 0);
        const crashedSessions = (_a = data.groups.find(group => group.by['session.status'] === 'crashed')) === null || _a === void 0 ? void 0 : _a.totals['sum(session)'];
        if (totalSessions === 0 || !(0, utils_2.defined)(totalSessions) || !(0, utils_2.defined)(crashedSessions)) {
            return undefined;
        }
        const crashedSessionsPercent = (0, utils_2.percent)(crashedSessions, totalSessions);
        return (0, utils_3.getCrashFreePercent)(100 - crashedSessionsPercent);
    }
    renderLoading() {
        return this.renderBody();
    }
    renderMissingFeatureCard() {
        const { organization } = this.props;
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={<missingReleasesButtons_1.default organization={organization} health/>}/>);
    }
    renderScore() {
        const { loading } = this.state;
        if (loading || !(0, utils_2.defined)(this.score)) {
            return '\u2014';
        }
        return (0, utils_3.displayCrashFreePercent)(this.score);
    }
    renderTrend() {
        const { loading } = this.state;
        if (loading || !(0, utils_2.defined)(this.score) || !(0, utils_2.defined)(this.trend)) {
            return null;
        }
        return (<div>
        {this.trend >= 0 ? (<icons_1.IconArrow direction="up" size="xs"/>) : (<icons_1.IconArrow direction="down" size="xs"/>)}
        {`${(0, formatters_1.formatAbbreviatedNumber)(Math.abs(this.trend))}\u0025`}
      </div>);
    }
    renderBody() {
        const { hasSessions } = this.props;
        if (hasSessions === false) {
            return this.renderMissingFeatureCard();
        }
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={this.renderScore()} trend={this.renderTrend()} trendStatus={this.trendStatus}/>);
    }
}
exports.default = ProjectStabilityScoreCard;
//# sourceMappingURL=projectStabilityScoreCard.jsx.map