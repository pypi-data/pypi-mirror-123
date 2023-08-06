Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const sentryAppComponents_1 = require("app/actionCreators/sentryAppComponents");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const groupEventDetailsLoadingError_1 = (0, tslib_1.__importDefault)(require("app/components/errors/groupEventDetailsLoadingError"));
const eventEntries_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventEntries"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const sidebar_1 = (0, tslib_1.__importDefault)(require("app/components/group/sidebar"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const mutedBox_1 = (0, tslib_1.__importDefault)(require("app/components/mutedBox"));
const reprocessedBox_1 = (0, tslib_1.__importDefault)(require("app/components/reprocessedBox"));
const resolutionBox_1 = (0, tslib_1.__importDefault)(require("app/components/resolutionBox"));
const suggestProjectCTA_1 = (0, tslib_1.__importDefault)(require("app/components/suggestProjectCTA"));
const fetchSentryAppInstallations_1 = (0, tslib_1.__importDefault)(require("app/utils/fetchSentryAppInstallations"));
const eventToolbar_1 = (0, tslib_1.__importDefault)(require("../eventToolbar"));
const reprocessingProgress_1 = (0, tslib_1.__importDefault)(require("../reprocessingProgress"));
const utils_1 = require("../utils");
class GroupEventDetails extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            eventNavLinks: '',
            releasesCompletion: null,
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, project, organization } = this.props;
            const orgSlug = organization.slug;
            const projSlug = project.slug;
            const projectId = project.id;
            /**
             * Perform below requests in parallel
             */
            const releasesCompletionPromise = api.requestPromise(`/projects/${orgSlug}/${projSlug}/releases/completion/`);
            (0, fetchSentryAppInstallations_1.default)(api, orgSlug);
            // TODO(marcos): Sometimes GlobalSelectionStore cannot pick a project.
            if (projectId) {
                (0, sentryAppComponents_1.fetchSentryAppComponents)(api, orgSlug, projectId);
            }
            else {
                Sentry.withScope(scope => {
                    scope.setExtra('props', this.props);
                    scope.setExtra('state', this.state);
                    Sentry.captureMessage('Project ID was not set');
                });
            }
            const releasesCompletion = yield releasesCompletionPromise;
            this.setState({ releasesCompletion });
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        const { environments, params, location, organization, project } = this.props;
        const environmentsHaveChanged = !(0, isEqual_1.default)(prevProps.environments, environments);
        // If environments are being actively changed and will no longer contain the
        // current event's environment, redirect to latest
        if (environmentsHaveChanged &&
            prevProps.event &&
            params.eventId &&
            !['latest', 'oldest'].includes(params.eventId)) {
            const shouldRedirect = environments.length > 0 &&
                !environments.find(env => env.name === (0, utils_1.getEventEnvironment)(prevProps.event));
            if (shouldRedirect) {
                react_router_1.browserHistory.replace({
                    pathname: `/organizations/${params.orgId}/issues/${params.groupId}/`,
                    query: location.query,
                });
                return;
            }
        }
        if (prevProps.organization.slug !== organization.slug ||
            prevProps.project.slug !== project.slug) {
            this.fetchData();
        }
    }
    componentWillUnmount() {
        const { api } = this.props;
        api.clear();
    }
    get showExampleCommit() {
        const { project } = this.props;
        const { releasesCompletion } = this.state;
        return ((project === null || project === void 0 ? void 0 : project.isMember) &&
            (project === null || project === void 0 ? void 0 : project.firstEvent) &&
            (releasesCompletion === null || releasesCompletion === void 0 ? void 0 : releasesCompletion.some(({ step, complete }) => step === 'commit' && !complete)));
    }
    renderContent(eventWithMeta) {
        const { group, project, organization, environments, location, loadingEvent, onRetry, eventError, router, route, } = this.props;
        if (loadingEvent) {
            return <loadingIndicator_1.default />;
        }
        if (eventError) {
            return (<groupEventDetailsLoadingError_1.default environments={environments} onRetry={onRetry}/>);
        }
        return (<eventEntries_1.default group={group} event={eventWithMeta} organization={organization} project={project} location={location} showExampleCommit={this.showExampleCommit} router={router} route={route}/>);
    }
    renderReprocessedBox(reprocessStatus, mostRecentActivity) {
        if (reprocessStatus !== utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
            reprocessStatus !== utils_1.ReprocessingStatus.REPROCESSED_AND_HAS_EVENT) {
            return null;
        }
        const { group, organization } = this.props;
        const { count, id: groupId } = group;
        const groupCount = Number(count);
        return (<reprocessedBox_1.default reprocessActivity={mostRecentActivity} groupCount={groupCount} groupId={groupId} orgSlug={organization.slug}/>);
    }
    render() {
        var _a;
        const { className, group, project, organization, environments, location, event, groupReprocessingStatus, } = this.props;
        const eventWithMeta = (0, metaProxy_1.withMeta)(event);
        // Reprocessing
        const hasReprocessingV2Feature = (_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('reprocessing-v2');
        const { activity: activities } = group;
        const mostRecentActivity = (0, utils_1.getGroupMostRecentActivity)(activities);
        return (<div className={className}>
        {event && (<errorBoundary_1.default customComponent={null}>
            <suggestProjectCTA_1.default event={event} organization={organization}/>
          </errorBoundary_1.default>)}
        <div className="event-details-container">
          {hasReprocessingV2Feature &&
                groupReprocessingStatus === utils_1.ReprocessingStatus.REPROCESSING ? (<reprocessingProgress_1.default totalEvents={mostRecentActivity.data.eventCount} pendingEvents={group.statusDetails
                    .pendingEvents}/>) : (<react_1.Fragment>
              <div className="primary">
                {eventWithMeta && (<eventToolbar_1.default group={group} event={eventWithMeta} organization={organization} location={location} project={project}/>)}
                {group.status === 'ignored' && (<mutedBox_1.default statusDetails={group.statusDetails}/>)}
                {group.status === 'resolved' && (<resolutionBox_1.default statusDetails={group.statusDetails} activities={activities} projectId={project.id}/>)}
                {this.renderReprocessedBox(groupReprocessingStatus, mostRecentActivity)}
                {this.renderContent(eventWithMeta)}
              </div>
              <div className="secondary">
                <sidebar_1.default organization={organization} project={project} group={group} event={eventWithMeta} environments={environments}/>
              </div>
            </react_1.Fragment>)}
        </div>
      </div>);
    }
}
exports.default = (0, styled_1.default)(GroupEventDetails) `
  display: flex;
  flex: 1;
  flex-direction: column;
`;
//# sourceMappingURL=groupEventDetails.jsx.map