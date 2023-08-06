Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const thirds_1 = require("app/components/layouts/thirds");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withRepositories_1 = (0, tslib_1.__importDefault)(require("app/utils/withRepositories"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const _1 = require(".");
function withReleaseRepos(WrappedComponent) {
    class WithReleaseRepos extends React.Component {
        constructor() {
            super(...arguments);
            this.state = {
                releaseRepos: [],
                isLoading: true,
            };
        }
        componentDidMount() {
            this.fetchReleaseRepos();
        }
        componentDidUpdate(prevProps, prevState) {
            var _a, _b;
            if (this.props.params.release !== prevProps.params.release ||
                (!!prevProps.repositoriesLoading && !this.props.repositoriesLoading)) {
                this.fetchReleaseRepos();
                return;
            }
            if (prevState.releaseRepos.length !== this.state.releaseRepos.length ||
                ((_a = prevProps.location.query) === null || _a === void 0 ? void 0 : _a.activeRepo) !== ((_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.activeRepo)) {
                this.setActiveReleaseRepo(this.props);
            }
        }
        setActiveReleaseRepo(props) {
            var _a, _b;
            const { releaseRepos, activeReleaseRepo } = this.state;
            if (!releaseRepos.length) {
                return;
            }
            const activeCommitRepo = (_a = props.location.query) === null || _a === void 0 ? void 0 : _a.activeRepo;
            if (!activeCommitRepo) {
                this.setState({
                    activeReleaseRepo: (_b = releaseRepos[0]) !== null && _b !== void 0 ? _b : null,
                });
                return;
            }
            if (activeCommitRepo === (activeReleaseRepo === null || activeReleaseRepo === void 0 ? void 0 : activeReleaseRepo.name)) {
                return;
            }
            const matchedRepository = releaseRepos.find(commitRepo => commitRepo.name === activeCommitRepo);
            if (matchedRepository) {
                this.setState({
                    activeReleaseRepo: matchedRepository,
                });
                return;
            }
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('The repository you were looking for was not found.'));
        }
        fetchReleaseRepos() {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const { params, api, repositories, repositoriesLoading } = this.props;
                if (repositoriesLoading === undefined || repositoriesLoading === true) {
                    return;
                }
                if (!(repositories === null || repositories === void 0 ? void 0 : repositories.length)) {
                    this.setState({ isLoading: false });
                    return;
                }
                const { release, orgId } = params;
                const { project } = this.context;
                this.setState({ isLoading: true });
                try {
                    const releasePath = encodeURIComponent(release);
                    const releaseRepos = yield api.requestPromise(`/projects/${orgId}/${project.slug}/releases/${releasePath}/repositories/`);
                    this.setState({ releaseRepos, isLoading: false });
                    this.setActiveReleaseRepo(this.props);
                }
                catch (error) {
                    Sentry.captureException(error);
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occured while trying to fetch the repositories of the release: %s', release));
                }
            });
        }
        render() {
            const { isLoading, activeReleaseRepo, releaseRepos } = this.state;
            const { repositoriesLoading, repositories, params, router, location, organization } = this.props;
            if (isLoading || repositoriesLoading) {
                return <loadingIndicator_1.default />;
            }
            const noRepositoryOrgRelatedFound = !(repositories === null || repositories === void 0 ? void 0 : repositories.length);
            if (noRepositoryOrgRelatedFound) {
                const { orgId } = params;
                return (<thirds_1.Body>
            <thirds_1.Main fullWidth>
              <panels_1.Panel dashedBorder>
                <emptyMessage_1.default icon={<icons_1.IconCommit size="xl"/>} title={(0, locale_1.t)('Releases are better with commit data!')} description={(0, locale_1.t)('Connect a repository to see commit info, files changed, and authors involved in future releases.')} action={<button_1.default priority="primary" to={`/settings/${orgId}/repos/`}>
                      {(0, locale_1.t)('Connect a repository')}
                    </button_1.default>}/>
              </panels_1.Panel>
            </thirds_1.Main>
          </thirds_1.Body>);
            }
            const noReleaseReposFound = !releaseRepos.length;
            if (noReleaseReposFound) {
                return (<thirds_1.Body>
            <thirds_1.Main fullWidth>
              <panels_1.Panel dashedBorder>
                <emptyMessage_1.default icon={<icons_1.IconCommit size="xl"/>} title={(0, locale_1.t)('Releases are better with commit data!')} description={(0, locale_1.t)('No commits associated with this release have been found.')}/>
              </panels_1.Panel>
            </thirds_1.Main>
          </thirds_1.Body>);
            }
            if (activeReleaseRepo === undefined) {
                return <loadingIndicator_1.default />;
            }
            const { release } = params;
            const orgSlug = organization.slug;
            return (<WrappedComponent {...this.props} orgSlug={orgSlug} projectSlug={this.context.project.slug} release={release} router={router} location={location} releaseRepos={releaseRepos} activeReleaseRepo={activeReleaseRepo}/>);
        }
    }
    WithReleaseRepos.displayName = `withReleaseRepos(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    WithReleaseRepos.contextType = _1.ReleaseContext;
    return (0, withApi_1.default)((0, withOrganization_1.default)((0, withRepositories_1.default)(WithReleaseRepos)));
}
exports.default = withReleaseRepos;
//# sourceMappingURL=withReleaseRepos.jsx.map