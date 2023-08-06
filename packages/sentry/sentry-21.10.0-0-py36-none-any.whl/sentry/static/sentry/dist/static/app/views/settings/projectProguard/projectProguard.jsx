Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const projectProguardRow_1 = (0, tslib_1.__importDefault)(require("./projectProguardRow"));
class ProjectProguard extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = (id) => {
            const { orgId, projectId } = this.props.params;
            this.setState({
                loading: true,
            });
            this.api.request(`/projects/${orgId}/${projectId}/files/dsyms/?id=${encodeURIComponent(id)}`, {
                method: 'DELETE',
                complete: () => this.fetchData(),
            });
        };
        this.handleSearch = (query) => {
            const { location, router } = this.props;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query }) }));
        };
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('ProGuard Mappings'), projectId, false);
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { mappings: [] });
    }
    getEndpoints() {
        const { params, location } = this.props;
        const { orgId, projectId } = params;
        const endpoints = [
            [
                'mappings',
                `/projects/${orgId}/${projectId}/files/dsyms/`,
                { query: { query: location.query.query, file_formats: 'proguard' } },
            ],
        ];
        return endpoints;
    }
    getQuery() {
        const { query } = this.props.location.query;
        return typeof query === 'string' ? query : undefined;
    }
    getEmptyMessage() {
        if (this.getQuery()) {
            return (0, locale_1.t)('There are no mappings that match your search.');
        }
        return (0, locale_1.t)('There are no mappings for this project.');
    }
    renderLoading() {
        return this.renderBody();
    }
    renderMappings() {
        const { mappings } = this.state;
        const { organization, params } = this.props;
        const { orgId, projectId } = params;
        if (!(mappings === null || mappings === void 0 ? void 0 : mappings.length)) {
            return null;
        }
        return mappings.map(mapping => {
            const downloadUrl = `${this.api.baseUrl}/projects/${orgId}/${projectId}/files/dsyms/?id=${encodeURIComponent(mapping.id)}`;
            return (<projectProguardRow_1.default mapping={mapping} downloadUrl={downloadUrl} onDelete={this.handleDelete} downloadRole={organization.debugFilesRole} key={mapping.id}/>);
        });
    }
    renderBody() {
        const { loading, mappings, mappingsPageLinks } = this.state;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('ProGuard Mappings')} action={<searchBar_1.default placeholder={(0, locale_1.t)('Filter mappings')} onSearch={this.handleSearch} query={this.getQuery()} width="280px"/>}/>

        <textBlock_1.default>
          {(0, locale_1.tct)(`ProGuard mapping files are used to convert minified classes, methods and field names into a human readable format. To learn more about proguard mapping files, [link: read the docs].`, {
                link: (<externalLink_1.default href="https://docs.sentry.io/platforms/android/proguard/"/>),
            })}
        </textBlock_1.default>

        <StyledPanelTable headers={[
                (0, locale_1.t)('Mapping'),
                <SizeColumn key="size">{(0, locale_1.t)('File Size')}</SizeColumn>,
                '',
            ]} emptyMessage={this.getEmptyMessage()} isEmpty={(mappings === null || mappings === void 0 ? void 0 : mappings.length) === 0} isLoading={loading}>
          {this.renderMappings()}
        </StyledPanelTable>
        <pagination_1.default pageLinks={mappingsPageLinks}/>
      </react_1.Fragment>);
    }
}
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  grid-template-columns: minmax(220px, 1fr) max-content 120px;
`;
const SizeColumn = (0, styled_1.default)('div') `
  text-align: right;
`;
exports.default = ProjectProguard;
//# sourceMappingURL=projectProguard.jsx.map