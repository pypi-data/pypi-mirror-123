Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectContext = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const members_1 = require("app/actionCreators/members");
const projects_1 = require("app/actionCreators/projects");
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const missingProjectMembership_1 = (0, tslib_1.__importDefault)(require("app/components/projects/missingProjectMembership"));
const locale_1 = require("app/locale");
const sentryTypes_1 = (0, tslib_1.__importDefault)(require("app/sentryTypes"));
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
var ErrorTypes;
(function (ErrorTypes) {
    ErrorTypes["MISSING_MEMBERSHIP"] = "MISSING_MEMBERSHIP";
    ErrorTypes["PROJECT_NOT_FOUND"] = "PROJECT_NOT_FOUND";
    ErrorTypes["UNKNOWN"] = "UNKNOWN";
})(ErrorTypes || (ErrorTypes = {}));
/**
 * Higher-order component that sets `project` as a child context
 * value to be accessed by child elements.
 *
 * Additionally delays rendering of children until project XHR has finished
 * and context is populated.
 */
class ProjectContext extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.docTitleRef = (0, react_1.createRef)();
        this.unsubscribeProjects = projectsStore_1.default.listen((projectIds) => this.onProjectChange(projectIds), undefined);
        this.unsubscribeMembers = memberListStore_1.default.listen((memberList) => this.setState({ memberList }), undefined);
    }
    getInitialState() {
        return {
            loading: true,
            error: false,
            errorType: null,
            memberList: [],
            project: null,
        };
    }
    getChildContext() {
        return {
            project: this.state.project,
        };
    }
    componentDidMount() {
        // Wait for withProjects to fetch projects before making request
        // Once loaded we can fetchData in componentDidUpdate
        const { loadingProjects } = this.props;
        if (!loadingProjects) {
            this.fetchData();
        }
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.projectId === this.props.projectId) {
            return;
        }
        if (!nextProps.skipReload) {
            this.remountComponent();
        }
    }
    componentDidUpdate(prevProps, prevState) {
        if (prevProps.projectId !== this.props.projectId) {
            this.fetchData();
        }
        // Project list has changed. Likely indicating that a new project has been
        // added. Re-fetch project details in case that the new project is the active
        // project.
        //
        // For now, only compare lengths. It is possible that project slugs within
        // the list could change, but it doesn't seem to be broken anywhere else at
        // the moment that would require deeper checks.
        if (prevProps.projects.length !== this.props.projects.length) {
            this.fetchData();
        }
        // Call forceUpdate() on <DocumentTitle/> if either project or organization
        // state has changed. This is because <DocumentTitle/>'s shouldComponentUpdate()
        // returns false unless props differ; meaning context changes for project/org
        // do NOT trigger renders for <DocumentTitle/> OR any subchildren. The end result
        // being that child elements that listen for context changes on project/org will
        // NOT update (without this hack).
        // See: https://github.com/gaearon/react-document-title/issues/35
        // intentionally shallow comparing references
        if (prevState.project !== this.state.project) {
            const docTitle = this.docTitleRef.current;
            if (!docTitle) {
                return;
            }
            docTitle.forceUpdate();
        }
    }
    componentWillUnmount() {
        this.unsubscribeMembers();
        this.unsubscribeProjects();
    }
    remountComponent() {
        this.setState(this.getInitialState());
    }
    getTitle() {
        var _a, _b;
        return (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.slug) !== null && _b !== void 0 ? _b : 'Sentry';
    }
    onProjectChange(projectIds) {
        if (!this.state.project) {
            return;
        }
        if (!projectIds.has(this.state.project.id)) {
            return;
        }
        this.setState({
            project: Object.assign({}, projectsStore_1.default.getById(this.state.project.id)),
        });
    }
    identifyProject() {
        const { projects, projectId } = this.props;
        const projectSlug = projectId;
        return projects.find(({ slug }) => slug === projectSlug) || null;
    }
    fetchData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { orgId, projectId, skipReload } = this.props;
            // we fetch core access/information from the global organization data
            const activeProject = this.identifyProject();
            const hasAccess = activeProject && activeProject.hasAccess;
            this.setState((state) => ({
                // if `skipReload` is true, then don't change loading state
                loading: skipReload ? state.loading : true,
                // we bind project initially, but it'll rebind
                project: activeProject,
            }));
            if (activeProject && hasAccess) {
                (0, projects_1.setActiveProject)(null);
                const projectRequest = this.props.api.requestPromise(`/projects/${orgId}/${projectId}/`);
                try {
                    const project = yield projectRequest;
                    this.setState({
                        loading: false,
                        project,
                        error: false,
                        errorType: null,
                    });
                    // assuming here that this means the project is considered the active project
                    (0, projects_1.setActiveProject)(project);
                }
                catch (error) {
                    this.setState({
                        loading: false,
                        error: false,
                        errorType: ErrorTypes.UNKNOWN,
                    });
                }
                (0, members_1.fetchOrgMembers)(this.props.api, orgId, [activeProject.id]);
                return;
            }
            // User is not a memberof the active project
            if (activeProject && !activeProject.isMember) {
                this.setState({
                    loading: false,
                    error: true,
                    errorType: ErrorTypes.MISSING_MEMBERSHIP,
                });
                return;
            }
            // There is no active project. This likely indicates either the project
            // *does not exist* or the project has not yet been added to the store.
            // Either way, make a request to check for existence of the project.
            try {
                yield this.props.api.requestPromise(`/projects/${orgId}/${projectId}/`);
            }
            catch (error) {
                this.setState({
                    loading: false,
                    error: true,
                    errorType: ErrorTypes.PROJECT_NOT_FOUND,
                });
            }
        });
    }
    renderBody() {
        const { children, organization } = this.props;
        const { error, errorType, loading, project } = this.state;
        if (loading) {
            return (<div className="loading-full-layout">
          <loadingIndicator_1.default />
        </div>);
        }
        if (!error && project) {
            return typeof children === 'function' ? children({ project }) : children;
        }
        switch (errorType) {
            case ErrorTypes.PROJECT_NOT_FOUND:
                // TODO(chrissy): use scale for margin values
                return (<div className="container">
            <div className="alert alert-block" style={{ margin: '30px 0 10px' }}>
              {(0, locale_1.t)('The project you were looking for was not found.')}
            </div>
          </div>);
            case ErrorTypes.MISSING_MEMBERSHIP:
                // TODO(dcramer): add various controls to improve this flow and break it
                // out into a reusable missing access error component
                return (<ErrorWrapper>
            <missingProjectMembership_1.default organization={organization} project={project}/>
          </ErrorWrapper>);
            default:
                return <loadingError_1.default onRetry={this.remountComponent}/>;
        }
    }
    render() {
        return (<react_document_title_1.default ref={this.docTitleRef} title={this.getTitle()}>
        {this.renderBody()}
      </react_document_title_1.default>);
    }
}
exports.ProjectContext = ProjectContext;
ProjectContext.childContextTypes = {
    project: sentryTypes_1.default.Project,
};
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withProjects_1.default)(ProjectContext)));
const ErrorWrapper = (0, styled_1.default)('div') `
  width: 100%;
  margin: ${(0, space_1.default)(2)} ${(0, space_1.default)(4)};
`;
//# sourceMappingURL=projectContext.jsx.map