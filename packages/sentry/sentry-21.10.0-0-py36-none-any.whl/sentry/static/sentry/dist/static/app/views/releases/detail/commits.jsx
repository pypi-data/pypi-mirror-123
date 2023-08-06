Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const commitRow_1 = (0, tslib_1.__importDefault)(require("app/components/commitRow"));
const thirds_1 = require("app/components/layouts/thirds");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const formatters_1 = require("app/utils/formatters");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyState_1 = (0, tslib_1.__importDefault)(require("./emptyState"));
const repositorySwitcher_1 = (0, tslib_1.__importDefault)(require("./repositorySwitcher"));
const utils_1 = require("./utils");
const withReleaseRepos_1 = (0, tslib_1.__importDefault)(require("./withReleaseRepos"));
class Commits extends asyncView_1.default {
    getTitle() {
        const { params, projectSlug } = this.props;
        const { orgId } = params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Commits - Release %s', (0, formatters_1.formatVersion)(params.release)), orgId, false, projectSlug);
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { commits: [] });
    }
    componentDidUpdate(prevProps, prevContext) {
        var _a, _b;
        if (((_a = prevProps.activeReleaseRepo) === null || _a === void 0 ? void 0 : _a.name) !== ((_b = this.props.activeReleaseRepo) === null || _b === void 0 ? void 0 : _b.name)) {
            this.remountComponent();
            return;
        }
        super.componentDidUpdate(prevProps, prevContext);
    }
    getEndpoints() {
        const { projectSlug, activeReleaseRepo: activeRepository, location, orgSlug, release, } = this.props;
        const query = (0, utils_1.getQuery)({ location, activeRepository });
        return [
            [
                'commits',
                `/projects/${orgSlug}/${projectSlug}/releases/${encodeURIComponent(release)}/commits/`,
                { query },
            ],
        ];
    }
    renderLoading() {
        return this.renderBody();
    }
    renderContent() {
        const { commits, commitsPageLinks, loading } = this.state;
        const { activeReleaseRepo } = this.props;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (!commits.length) {
            return (<emptyState_1.default>
          {!activeReleaseRepo
                    ? (0, locale_1.t)('There are no commits associated with this release.')
                    : (0, locale_1.t)('There are no commits associated with this release in the %s repository.', activeReleaseRepo.name)}
        </emptyState_1.default>);
        }
        const commitsByRepository = (0, utils_1.getCommitsByRepository)(commits);
        const reposToRender = (0, utils_1.getReposToRender)(Object.keys(commitsByRepository));
        return (<react_1.Fragment>
        {reposToRender.map(repoName => {
                var _a;
                return (<panels_1.Panel key={repoName}>
            <panels_1.PanelHeader>{repoName}</panels_1.PanelHeader>
            <panels_1.PanelBody>
              {(_a = commitsByRepository[repoName]) === null || _a === void 0 ? void 0 : _a.map(commit => (<commitRow_1.default key={commit.id} commit={commit}/>))}
            </panels_1.PanelBody>
          </panels_1.Panel>);
            })}
        <pagination_1.default pageLinks={commitsPageLinks}/>
      </react_1.Fragment>);
    }
    renderBody() {
        const { location, router, activeReleaseRepo, releaseRepos } = this.props;
        return (<react_1.Fragment>
        {releaseRepos.length > 1 && (<repositorySwitcher_1.default repositories={releaseRepos} activeRepository={activeReleaseRepo} location={location} router={router}/>)}
        {this.renderContent()}
      </react_1.Fragment>);
    }
    renderComponent() {
        return (<thirds_1.Body>
        <thirds_1.Main fullWidth>{super.renderComponent()}</thirds_1.Main>
      </thirds_1.Body>);
    }
}
exports.default = (0, withReleaseRepos_1.default)(Commits);
//# sourceMappingURL=commits.jsx.map