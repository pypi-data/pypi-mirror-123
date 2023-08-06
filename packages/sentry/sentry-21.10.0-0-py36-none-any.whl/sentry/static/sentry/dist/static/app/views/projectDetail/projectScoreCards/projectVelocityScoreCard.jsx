Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const projects_1 = require("app/actionCreators/projects");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const utils_1 = require("app/components/organizations/timeRangeSelector/utils");
const scoreCard_1 = (0, tslib_1.__importDefault)(require("app/components/scoreCard"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_2 = require("app/utils");
const getPeriod_1 = require("app/utils/getPeriod");
const missingReleasesButtons_1 = (0, tslib_1.__importDefault)(require("../missingFeatureButtons/missingReleasesButtons"));
const utils_3 = require("../utils");
const API_LIMIT = 1000;
class ProjectVelocityScoreCard extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldRenderBadRequests = true;
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { currentReleases: null, previousReleases: null, noReleaseEver: false });
    }
    getEndpoints() {
        const { organization, selection, isProjectStabilized, query } = this.props;
        if (!isProjectStabilized) {
            return [];
        }
        const { projects, environments, datetime } = selection;
        const { period } = datetime;
        const commonQuery = {
            environment: environments,
            project: projects[0],
            query,
        };
        const endpoints = [
            [
                'currentReleases',
                `/organizations/${organization.slug}/releases/stats/`,
                {
                    includeAllArgs: true,
                    method: 'GET',
                    query: Object.assign(Object.assign({}, commonQuery), (0, getParams_1.getParams)(datetime)),
                },
            ],
        ];
        if ((0, utils_3.shouldFetchPreviousPeriod)(datetime)) {
            const { start: previousStart } = (0, utils_1.parseStatsPeriod)((0, getPeriod_1.getPeriod)({ period, start: undefined, end: undefined }, { shouldDoublePeriod: true })
                .statsPeriod);
            const { start: previousEnd } = (0, utils_1.parseStatsPeriod)((0, getPeriod_1.getPeriod)({ period, start: undefined, end: undefined }, { shouldDoublePeriod: false })
                .statsPeriod);
            endpoints.push([
                'previousReleases',
                `/organizations/${organization.slug}/releases/stats/`,
                {
                    query: Object.assign(Object.assign({}, commonQuery), { start: previousStart, end: previousEnd }),
                },
            ]);
        }
        return endpoints;
    }
    /**
     * If our releases are empty, determine if we had a release in the last 90 days (empty message differs then)
     */
    onLoadAllEndpointsSuccess() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { currentReleases, previousReleases } = this.state;
            const { organization, selection, isProjectStabilized } = this.props;
            if (!isProjectStabilized) {
                return;
            }
            if ([...(currentReleases !== null && currentReleases !== void 0 ? currentReleases : []), ...(previousReleases !== null && previousReleases !== void 0 ? previousReleases : [])].length !== 0) {
                this.setState({ noReleaseEver: false });
                return;
            }
            this.setState({ loading: true });
            const hasOlderReleases = yield (0, projects_1.fetchAnyReleaseExistence)(this.api, organization.slug, selection.projects[0]);
            this.setState({ noReleaseEver: !hasOlderReleases, loading: false });
        });
    }
    get cardTitle() {
        return (0, locale_1.t)('Number of Releases');
    }
    get cardHelp() {
        return this.trend
            ? (0, locale_1.t)('The number of releases for this project and how it has changed since the last period.')
            : (0, locale_1.t)('The number of releases for this project.');
    }
    get trend() {
        const { currentReleases, previousReleases } = this.state;
        if (!(0, utils_2.defined)(currentReleases) || !(0, utils_2.defined)(previousReleases)) {
            return null;
        }
        return currentReleases.length - previousReleases.length;
    }
    get trendStatus() {
        if (!this.trend) {
            return undefined;
        }
        return this.trend > 0 ? 'good' : 'bad';
    }
    componentDidUpdate(prevProps) {
        const { selection, isProjectStabilized } = this.props;
        if (prevProps.selection !== selection ||
            prevProps.isProjectStabilized !== isProjectStabilized) {
            this.remountComponent();
        }
    }
    renderLoading() {
        return this.renderBody();
    }
    renderMissingFeatureCard() {
        const { organization } = this.props;
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={<missingReleasesButtons_1.default organization={organization}/>}/>);
    }
    renderScore() {
        const { currentReleases, loading } = this.state;
        if (loading || !(0, utils_2.defined)(currentReleases)) {
            return '\u2014';
        }
        return currentReleases.length === API_LIMIT
            ? `${API_LIMIT - 1}+`
            : currentReleases.length;
    }
    renderTrend() {
        const { loading, currentReleases } = this.state;
        if (loading || !(0, utils_2.defined)(this.trend) || (currentReleases === null || currentReleases === void 0 ? void 0 : currentReleases.length) === API_LIMIT) {
            return null;
        }
        return (<React.Fragment>
        {this.trend >= 0 ? (<icons_1.IconArrow direction="up" size="xs"/>) : (<icons_1.IconArrow direction="down" size="xs"/>)}
        {Math.abs(this.trend)}
      </React.Fragment>);
    }
    renderBody() {
        const { noReleaseEver } = this.state;
        if (noReleaseEver) {
            return this.renderMissingFeatureCard();
        }
        return (<scoreCard_1.default title={this.cardTitle} help={this.cardHelp} score={this.renderScore()} trend={this.renderTrend()} trendStatus={this.trendStatus}/>);
    }
}
exports.default = ProjectVelocityScoreCard;
//# sourceMappingURL=projectVelocityScoreCard.jsx.map