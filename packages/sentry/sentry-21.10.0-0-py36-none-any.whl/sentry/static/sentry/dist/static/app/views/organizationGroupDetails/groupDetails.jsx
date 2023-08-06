Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const react_router_1 = require("react-router");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const prop_types_1 = (0, tslib_1.__importDefault)(require("prop-types"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const missingProjectMembership_1 = (0, tslib_1.__importDefault)(require("app/components/projects/missingProjectMembership"));
const locale_1 = require("app/locale");
const sentryTypes_1 = (0, tslib_1.__importDefault)(require("app/sentryTypes"));
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const organization_1 = require("app/styles/organization");
const callIfFunction_1 = require("app/utils/callIfFunction");
const events_1 = require("app/utils/events");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const constants_1 = require("./constants");
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const types_1 = require("./types");
const utils_1 = require("./utils");
class GroupDetails extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.initialState;
        this.remountComponent = () => {
            this.setState(this.initialState);
            this.fetchData();
        };
        this.refetchGroup = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { loadingGroup, loading, loadingEvent, group } = this.state;
            if ((group === null || group === void 0 ? void 0 : group.status) !== utils_1.ReprocessingStatus.REPROCESSING ||
                loadingGroup ||
                loading ||
                loadingEvent) {
                return;
            }
            const { api } = this.props;
            this.setState({ loadingGroup: true });
            try {
                const updatedGroup = yield api.requestPromise(this.groupDetailsEndpoint, {
                    query: this.getGroupQuery(),
                });
                const reprocessingNewRoute = this.getReprocessingNewRoute(updatedGroup);
                if (reprocessingNewRoute) {
                    react_router_1.browserHistory.push(reprocessingNewRoute);
                    return;
                }
                this.setState({ group: updatedGroup, loadingGroup: false });
            }
            catch (error) {
                this.handleRequestError(error);
            }
        });
        this.listener = groupStore_1.default.listen(itemIds => this.onGroupChange(itemIds), undefined);
        this.interval = undefined;
    }
    getChildContext() {
        return {
            group: this.state.group,
            location: this.props.location,
        };
    }
    componentDidMount() {
        this.fetchData();
        this.updateReprocessingProgress();
    }
    componentDidUpdate(prevProps, prevState) {
        var _a, _b;
        if (prevProps.isGlobalSelectionReady !== this.props.isGlobalSelectionReady ||
            prevProps.location.pathname !== this.props.location.pathname) {
            this.fetchData();
        }
        if ((!this.canLoadEventEarly(prevProps) && !(prevState === null || prevState === void 0 ? void 0 : prevState.group) && this.state.group) ||
            (((_a = prevProps.params) === null || _a === void 0 ? void 0 : _a.eventId) !== ((_b = this.props.params) === null || _b === void 0 ? void 0 : _b.eventId) && this.state.group)) {
            this.getEvent(this.state.group);
        }
    }
    componentWillUnmount() {
        groupStore_1.default.reset();
        (0, callIfFunction_1.callIfFunction)(this.listener);
        if (this.interval) {
            clearInterval(this.interval);
        }
    }
    get initialState() {
        return {
            group: null,
            loading: true,
            loadingEvent: true,
            loadingGroup: true,
            error: false,
            eventError: false,
            errorType: null,
            project: null,
        };
    }
    canLoadEventEarly(props) {
        return !props.params.eventId || ['oldest', 'latest'].includes(props.params.eventId);
    }
    get groupDetailsEndpoint() {
        return `/issues/${this.props.params.groupId}/`;
    }
    get groupReleaseEndpoint() {
        return `/issues/${this.props.params.groupId}/first-last-release/`;
    }
    getEvent(group) {
        var _a;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (group) {
                this.setState({ loadingEvent: true, eventError: false });
            }
            const { params, environments, api } = this.props;
            const orgSlug = params.orgId;
            const groupId = params.groupId;
            const eventId = (params === null || params === void 0 ? void 0 : params.eventId) || 'latest';
            const projectId = (_a = group === null || group === void 0 ? void 0 : group.project) === null || _a === void 0 ? void 0 : _a.slug;
            try {
                const event = yield (0, utils_1.fetchGroupEvent)(api, orgSlug, groupId, eventId, environments, projectId);
                this.setState({ event, loading: false, eventError: false, loadingEvent: false });
            }
            catch (err) {
                // This is an expected error, capture to Sentry so that it is not considered as an unhandled error
                Sentry.captureException(err);
                this.setState({ eventError: true, loading: false, loadingEvent: false });
            }
        });
    }
    getCurrentRouteInfo(group) {
        const { routes, organization } = this.props;
        const { event } = this.state;
        // All the routes under /organizations/:orgId/issues/:groupId have a defined props
        const { currentTab, isEventRoute } = routes[routes.length - 1].props;
        const baseUrl = isEventRoute && event
            ? `/organizations/${organization.slug}/issues/${group.id}/events/${event.id}/`
            : `/organizations/${organization.slug}/issues/${group.id}/`;
        return { currentTab, baseUrl };
    }
    updateReprocessingProgress() {
        const hasReprocessingV2Feature = this.hasReprocessingV2Feature();
        if (!hasReprocessingV2Feature) {
            return;
        }
        this.interval = setInterval(this.refetchGroup, 30000);
    }
    hasReprocessingV2Feature() {
        var _a;
        const { organization } = this.props;
        return (_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('reprocessing-v2');
    }
    getReprocessingNewRoute(data) {
        const { routes, location, params } = this.props;
        const { groupId } = params;
        const { id: nextGroupId } = data;
        const hasReprocessingV2Feature = this.hasReprocessingV2Feature();
        const reprocessingStatus = (0, utils_1.getGroupReprocessingStatus)(data);
        const { currentTab, baseUrl } = this.getCurrentRouteInfo(data);
        if (groupId !== nextGroupId) {
            if (hasReprocessingV2Feature) {
                // Redirects to the Activities tab
                if (reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
                    currentTab !== types_1.Tab.ACTIVITY) {
                    return {
                        pathname: `${baseUrl}${types_1.Tab.ACTIVITY}/`,
                        query: Object.assign(Object.assign({}, params), { groupId: nextGroupId }),
                    };
                }
            }
            return (0, recreateRoute_1.default)('', {
                routes,
                location,
                params: Object.assign(Object.assign({}, params), { groupId: nextGroupId }),
            });
        }
        if (hasReprocessingV2Feature) {
            if (reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSING &&
                currentTab !== types_1.Tab.DETAILS) {
                return {
                    pathname: baseUrl,
                    query: params,
                };
            }
            if (reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
                currentTab !== types_1.Tab.ACTIVITY &&
                currentTab !== types_1.Tab.USER_FEEDBACK) {
                return {
                    pathname: `${baseUrl}${types_1.Tab.ACTIVITY}/`,
                    query: params,
                };
            }
        }
        return undefined;
    }
    getGroupQuery() {
        const { environments } = this.props;
        // Note, we do not want to include the environment key at all if there are no environments
        const query = Object.assign(Object.assign({}, (environments ? { environment: environments } : {})), { expand: 'inbox', collapse: 'release' });
        return query;
    }
    getFetchDataRequestErrorType(status) {
        if (!status) {
            return null;
        }
        if (status === 404) {
            return constants_1.ERROR_TYPES.GROUP_NOT_FOUND;
        }
        if (status === 403) {
            return constants_1.ERROR_TYPES.MISSING_MEMBERSHIP;
        }
        return null;
    }
    handleRequestError(error) {
        Sentry.captureException(error);
        const errorType = this.getFetchDataRequestErrorType(error === null || error === void 0 ? void 0 : error.status);
        this.setState({
            loadingGroup: false,
            loading: false,
            error: true,
            errorType,
        });
    }
    fetchGroupReleases() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api } = this.props;
            const releases = yield api.requestPromise(this.groupReleaseEndpoint);
            groupStore_1.default.onPopulateReleases(this.props.params.groupId, releases);
        });
    }
    fetchData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, isGlobalSelectionReady, params } = this.props;
            // Need to wait for global selection store to be ready before making request
            if (!isGlobalSelectionReady) {
                return;
            }
            try {
                const eventPromise = this.canLoadEventEarly(this.props)
                    ? this.getEvent()
                    : undefined;
                const groupPromise = yield api.requestPromise(this.groupDetailsEndpoint, {
                    query: this.getGroupQuery(),
                });
                const [data] = yield Promise.all([groupPromise, eventPromise]);
                this.fetchGroupReleases();
                const reprocessingNewRoute = this.getReprocessingNewRoute(data);
                if (reprocessingNewRoute) {
                    react_router_1.browserHistory.push(reprocessingNewRoute);
                    return;
                }
                const project = data.project;
                (0, utils_1.markEventSeen)(api, params.orgId, project.slug, params.groupId);
                if (!project) {
                    Sentry.withScope(() => {
                        Sentry.captureException(new Error('Project not found'));
                    });
                }
                else {
                    const locationWithProject = Object.assign({}, this.props.location);
                    if (locationWithProject.query.project === undefined &&
                        locationWithProject.query._allp === undefined) {
                        // We use _allp as a temporary measure to know they came from the
                        // issue list page with no project selected (all projects included in
                        // filter).
                        //
                        // If it is not defined, we add the locked project id to the URL
                        // (this is because if someone navigates directly to an issue on
                        // single-project priveleges, then goes back - they were getting
                        // assigned to the first project).
                        //
                        // If it is defined, we do not so that our back button will bring us
                        // to the issue list page with no project selected instead of the
                        // locked project.
                        locationWithProject.query.project = project.id;
                    }
                    // We delete _allp from the URL to keep the hack a bit cleaner, but
                    // this is not an ideal solution and will ultimately be replaced with
                    // something smarter.
                    delete locationWithProject.query._allp;
                    react_router_1.browserHistory.replace(locationWithProject);
                }
                this.setState({ project, loadingGroup: false });
                groupStore_1.default.loadInitialData([data]);
            }
            catch (error) {
                this.handleRequestError(error);
            }
        });
    }
    onGroupChange(itemIds) {
        const id = this.props.params.groupId;
        if (itemIds.has(id)) {
            const group = groupStore_1.default.get(id);
            if (group) {
                // TODO(ts) This needs a better approach. issueActions is splicing attributes onto
                // group objects to cheat here.
                if (group.stale) {
                    this.fetchData();
                    return;
                }
                this.setState({
                    group,
                });
            }
        }
    }
    getTitle() {
        const { organization } = this.props;
        const { group } = this.state;
        const defaultTitle = 'Sentry';
        if (!group) {
            return defaultTitle;
        }
        const { title } = (0, events_1.getTitle)(group, organization === null || organization === void 0 ? void 0 : organization.features);
        const message = (0, events_1.getMessage)(group);
        const { project } = group;
        const eventDetails = `${organization.slug} - ${project.slug}`;
        if (title && message) {
            return `${title}: ${message} - ${eventDetails}`;
        }
        return `${title || message || defaultTitle} - ${eventDetails}`;
    }
    renderError() {
        const { projects, location } = this.props;
        const projectId = location.query.project;
        const project = projects.find(proj => proj.id === projectId);
        switch (this.state.errorType) {
            case constants_1.ERROR_TYPES.GROUP_NOT_FOUND:
                return (<loadingError_1.default message={(0, locale_1.t)('The issue you were looking for was not found.')}/>);
            case constants_1.ERROR_TYPES.MISSING_MEMBERSHIP:
                return (<missingProjectMembership_1.default organization={this.props.organization} project={project}/>);
            default:
                return <loadingError_1.default onRetry={this.remountComponent}/>;
        }
    }
    renderContent(project, group) {
        const { children, environments } = this.props;
        const { loadingEvent, eventError, event } = this.state;
        const { currentTab, baseUrl } = this.getCurrentRouteInfo(group);
        const groupReprocessingStatus = (0, utils_1.getGroupReprocessingStatus)(group);
        let childProps = {
            environments,
            group,
            project,
        };
        if (currentTab === types_1.Tab.DETAILS) {
            childProps = Object.assign(Object.assign({}, childProps), { event,
                loadingEvent,
                eventError,
                groupReprocessingStatus, onRetry: () => this.remountComponent() });
        }
        if (currentTab === types_1.Tab.TAGS) {
            childProps = Object.assign(Object.assign({}, childProps), { event, baseUrl });
        }
        return (<React.Fragment>
        <header_1.default groupReprocessingStatus={groupReprocessingStatus} project={project} event={event} group={group} currentTab={currentTab} baseUrl={baseUrl}/>
        {React.isValidElement(children)
                ? React.cloneElement(children, childProps)
                : children}
      </React.Fragment>);
    }
    renderPageContent() {
        var _a;
        const { error: isError, group, project, loading } = this.state;
        const isLoading = loading || (!group && !isError);
        if (isLoading) {
            return <loadingIndicator_1.default />;
        }
        if (isError) {
            return this.renderError();
        }
        const { organization } = this.props;
        return (<projects_1.default orgId={organization.slug} slugs={[(_a = project === null || project === void 0 ? void 0 : project.slug) !== null && _a !== void 0 ? _a : '']} data-test-id="group-projects-container">
        {({ projects, initiallyLoaded, fetchError }) => initiallyLoaded ? (fetchError ? (<loadingError_1.default message={(0, locale_1.t)('Error loading the specified project')}/>) : (
            // TODO(ts): Update renderContent function to deal with empty group
            this.renderContent(projects[0], group))) : (<loadingIndicator_1.default />)}
      </projects_1.default>);
    }
    render() {
        const { project } = this.state;
        return (<react_document_title_1.default title={this.getTitle()}>
        <globalSelectionHeader_1.default skipLoadLastUsed forceProject={project} showDateSelector={false} shouldForceProject lockedMessageSubject={(0, locale_1.t)('issue')} showIssueStreamLink showProjectSettingsLink>
          <organization_1.PageContent>{this.renderPageContent()}</organization_1.PageContent>
        </globalSelectionHeader_1.default>
      </react_document_title_1.default>);
    }
}
GroupDetails.childContextTypes = {
    group: sentryTypes_1.default.Group,
    location: prop_types_1.default.object,
};
exports.default = (0, withApi_1.default)(Sentry.withProfiler(GroupDetails));
//# sourceMappingURL=groupDetails.jsx.map