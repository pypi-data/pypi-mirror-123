Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const queryString_1 = require("app/utils/queryString");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const sourceMapsArchiveRow_1 = (0, tslib_1.__importDefault)(require("./sourceMapsArchiveRow"));
class ProjectSourceMaps extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSearch = (query) => {
            const { location, router } = this.props;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query }) }));
        };
        this.handleDelete = (name) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Removing artifacts\u2026'));
            try {
                yield this.api.requestPromise(this.getArchivesUrl(), {
                    method: 'DELETE',
                    query: { name },
                });
                this.fetchData();
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Artifacts removed.'));
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove artifacts. Please try again.'));
            }
        });
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Source Maps'), projectId, false);
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { archives: [] });
    }
    getEndpoints() {
        return [['archives', this.getArchivesUrl(), { query: { query: this.getQuery() } }]];
    }
    getArchivesUrl() {
        const { orgId, projectId } = this.props.params;
        return `/projects/${orgId}/${projectId}/files/source-maps/`;
    }
    getQuery() {
        const { query } = this.props.location.query;
        return (0, queryString_1.decodeScalar)(query);
    }
    getEmptyMessage() {
        if (this.getQuery()) {
            return (0, locale_1.t)('There are no archives that match your search.');
        }
        return (0, locale_1.t)('There are no archives for this project.');
    }
    renderLoading() {
        return this.renderBody();
    }
    renderArchives() {
        const { archives } = this.state;
        const { params } = this.props;
        const { orgId, projectId } = params;
        if (!archives.length) {
            return null;
        }
        return archives.map(a => {
            return (<sourceMapsArchiveRow_1.default key={a.name} archive={a} orgId={orgId} projectId={projectId} onDelete={this.handleDelete}/>);
        });
    }
    renderBody() {
        const { loading, archives, archivesPageLinks } = this.state;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Source Maps')} action={<searchBar_1.default placeholder={(0, locale_1.t)('Filter Archives')} onSearch={this.handleSearch} query={this.getQuery()} width="280px"/>}/>

        <textBlock_1.default>
          {(0, locale_1.tct)(`These source map archives help Sentry identify where to look when Javascript is minified. By providing this information, you can get better context for your stack traces when debugging. To learn more about source maps, [link: read the docs].`, {
                link: (<externalLink_1.default href="https://docs.sentry.io/platforms/javascript/sourcemaps/"/>),
            })}
        </textBlock_1.default>

        <StyledPanelTable headers={[
                (0, locale_1.t)('Archive'),
                <ArtifactsColumn key="artifacts">{(0, locale_1.t)('Artifacts')}</ArtifactsColumn>,
                (0, locale_1.t)('Type'),
                (0, locale_1.t)('Date Created'),
                '',
            ]} emptyMessage={this.getEmptyMessage()} isEmpty={archives.length === 0} isLoading={loading}>
          {this.renderArchives()}
        </StyledPanelTable>
        <pagination_1.default pageLinks={archivesPageLinks}/>
      </react_1.Fragment>);
    }
}
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  grid-template-columns:
    minmax(120px, 1fr) max-content minmax(85px, max-content) minmax(265px, max-content)
    75px;
`;
const ArtifactsColumn = (0, styled_1.default)('div') `
  text-align: right;
  padding-right: ${(0, space_1.default)(1.5)};
  margin-right: ${(0, space_1.default)(0.25)};
`;
exports.default = ProjectSourceMaps;
//# sourceMappingURL=index.jsx.map