Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const fileChange_1 = (0, tslib_1.__importDefault)(require("app/components/fileChange"));
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
class FilesChanged extends asyncView_1.default {
    getTitle() {
        const { params, projectSlug } = this.props;
        const { orgId } = params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Files Changed - Release %s', (0, formatters_1.formatVersion)(params.release)), orgId, false, projectSlug);
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { fileList: [] });
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
        const { activeReleaseRepo: activeRepository, location, release, orgSlug } = this.props;
        const query = (0, utils_1.getQuery)({ location, activeRepository });
        return [
            [
                'fileList',
                `/organizations/${orgSlug}/releases/${encodeURIComponent(release)}/commitfiles/`,
                { query },
            ],
        ];
    }
    renderLoading() {
        return this.renderBody();
    }
    renderContent() {
        const { fileList, fileListPageLinks, loading } = this.state;
        const { activeReleaseRepo } = this.props;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (!fileList.length) {
            return (<emptyState_1.default>
          {!activeReleaseRepo
                    ? (0, locale_1.t)('There are no changed files associated with this release.')
                    : (0, locale_1.t)('There are no changed files associated with this release in the %s repository.', activeReleaseRepo.name)}
        </emptyState_1.default>);
        }
        const filesByRepository = (0, utils_1.getFilesByRepository)(fileList);
        const reposToRender = (0, utils_1.getReposToRender)(Object.keys(filesByRepository));
        return (<react_1.Fragment>
        {reposToRender.map(repoName => {
                const repoData = filesByRepository[repoName];
                const files = Object.keys(repoData);
                const fileCount = files.length;
                return (<panels_1.Panel key={repoName}>
              <panels_1.PanelHeader>
                <span>{repoName}</span>
                <span>{(0, locale_1.tn)('%s file changed', '%s files changed', fileCount)}</span>
              </panels_1.PanelHeader>
              <panels_1.PanelBody>
                {files.map(filename => {
                        const { authors } = repoData[filename];
                        return (<StyledFileChange key={filename} filename={filename} authors={Object.values(authors)}/>);
                    })}
              </panels_1.PanelBody>
            </panels_1.Panel>);
            })}
        <pagination_1.default pageLinks={fileListPageLinks}/>
      </react_1.Fragment>);
    }
    renderBody() {
        const { activeReleaseRepo, releaseRepos, router, location } = this.props;
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
exports.default = (0, withReleaseRepos_1.default)(FilesChanged);
const StyledFileChange = (0, styled_1.default)(fileChange_1.default) `
  border-radius: 0;
  border-left: none;
  border-right: none;
  border-top: none;
  :last-child {
    border: none;
    border-radius: 0;
  }
`;
//# sourceMappingURL=filesChanged.jsx.map