Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const noUnresolvedIssues_1 = (0, tslib_1.__importDefault)(require("./noUnresolvedIssues"));
/**
 * Component which is rendered when no groups/issues were found. This could
 * either be caused by having no first events, having resolved all issues, or
 * having no issues be returned from a query. This component will conditionally
 * render one of those states.
 */
class NoGroupsHandler extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            fetchingSentFirstEvent: true,
            sentFirstEvent: false,
            firstEventProjects: null,
        };
        /**
         * This is a bit hacky, but this is causing flakiness in frontend tests
         * `issueList/overview` is being unmounted during tests before the requests
         * in `this.fetchSentFirstEvent` are completed and causing this React warning:
         *
         * Warning: Can't perform a React state update on an unmounted component.
         * This is a no-op, but it indicates a memory leak in your application.
         * To fix, cancel all subscriptions and asynchronous tasks in the
         * componentWillUnmount method.
         *
         * This is something to revisit if we refactor API client
         */
        this._isMounted = false;
    }
    componentDidMount() {
        this.fetchSentFirstEvent();
        this._isMounted = true;
    }
    componentWillUnmount() {
        this._isMounted = false;
    }
    fetchSentFirstEvent() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({
                fetchingSentFirstEvent: true,
            });
            const { organization, selectedProjectIds, api } = this.props;
            let sentFirstEvent = false;
            let projects = [];
            // If no projects are selected, then we must check every project the user is a
            // member of and make sure there are no first events for all of the projects
            let firstEventQuery = {};
            const projectsQuery = { per_page: 1 };
            if (!selectedProjectIds || !selectedProjectIds.length) {
                firstEventQuery = { is_member: true };
            }
            else {
                firstEventQuery = { project: selectedProjectIds };
                projectsQuery.query = selectedProjectIds.map(id => `id:${id}`).join(' ');
            }
            [{ sentFirstEvent }, projects] = yield Promise.all([
                // checks to see if selection has sent a first event
                api.requestPromise(`/organizations/${organization.slug}/sent-first-event/`, {
                    query: firstEventQuery,
                }),
                // retrieves a single project to feed to the ErrorRobot from renderStreamBody
                api.requestPromise(`/organizations/${organization.slug}/projects/`, {
                    query: projectsQuery,
                }),
            ]);
            // See comment where this property is initialized
            // FIXME
            if (!this._isMounted) {
                return;
            }
            this.setState({
                fetchingSentFirstEvent: false,
                sentFirstEvent,
                firstEventProjects: projects,
            });
        });
    }
    renderLoading() {
        return <loadingIndicator_1.default />;
    }
    renderAwaitingEvents(projects) {
        const { organization, groupIds } = this.props;
        const project = projects && projects.length > 0 ? projects[0] : undefined;
        const sampleIssueId = groupIds.length > 0 ? groupIds[0] : undefined;
        const ErrorRobot = React.lazy(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/errorRobot'))));
        return (<React.Suspense fallback={<placeholder_1.default height="260px"/>}>
        <ErrorRobot org={organization} project={project} sampleIssueId={sampleIssueId} gradient/>
      </React.Suspense>);
    }
    renderEmpty() {
        const { emptyMessage } = this.props;
        return (<emptyStateWarning_1.default>
        <p>{emptyMessage !== null && emptyMessage !== void 0 ? emptyMessage : (0, locale_1.t)('Sorry, no issues match your filters.')}</p>
      </emptyStateWarning_1.default>);
    }
    render() {
        const { fetchingSentFirstEvent, sentFirstEvent, firstEventProjects } = this.state;
        const { query } = this.props;
        if (fetchingSentFirstEvent) {
            return this.renderLoading();
        }
        if (!sentFirstEvent) {
            return this.renderAwaitingEvents(firstEventProjects);
        }
        if (query === constants_1.DEFAULT_QUERY) {
            return <noUnresolvedIssues_1.default />;
        }
        return this.renderEmpty();
    }
}
exports.default = NoGroupsHandler;
//# sourceMappingURL=index.jsx.map