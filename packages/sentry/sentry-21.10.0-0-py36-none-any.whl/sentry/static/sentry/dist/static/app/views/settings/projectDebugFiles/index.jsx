Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
const debugFileRow_1 = (0, tslib_1.__importDefault)(require("./debugFileRow"));
const externalSources_1 = (0, tslib_1.__importDefault)(require("./externalSources"));
class ProjectDebugSymbols extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = (id) => {
            const { orgId, projectId } = this.props.params;
            this.setState({
                loading: true,
            });
            this.api.request(`/projects/${orgId}/${projectId}/files/dsyms/?id=${id}`, {
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
        return (0, routeTitle_1.default)((0, locale_1.t)('Debug Files'), projectId, false);
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { project: this.props.project, showDetails: false });
    }
    getEndpoints() {
        const { organization, params, location } = this.props;
        const { builtinSymbolSources } = this.state || {};
        const { orgId, projectId } = params;
        const { query } = location.query;
        const endpoints = [
            [
                'debugFiles',
                `/projects/${orgId}/${projectId}/files/dsyms/`,
                {
                    query: {
                        query,
                        file_formats: [
                            'breakpad',
                            'macho',
                            'elf',
                            'pe',
                            'pdb',
                            'sourcebundle',
                            'wasm',
                            'bcsymbolmap',
                            'uuidmap',
                        ],
                    },
                },
            ],
        ];
        if (!builtinSymbolSources && organization.features.includes('symbol-sources')) {
            endpoints.push(['builtinSymbolSources', '/builtin-symbol-sources/', {}]);
        }
        return endpoints;
    }
    fetchProject() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params } = this.props;
            const { orgId, projectId } = params;
            try {
                const updatedProject = yield this.api.requestPromise(`/projects/${orgId}/${projectId}/`);
                projectActions_1.default.updateSuccess(updatedProject);
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occured while fetching project data'));
            }
        });
    }
    getQuery() {
        const { query } = this.props.location.query;
        return typeof query === 'string' ? query : undefined;
    }
    getEmptyMessage() {
        if (this.getQuery()) {
            return (0, locale_1.t)('There are no debug symbols that match your search.');
        }
        return (0, locale_1.t)('There are no debug symbols for this project.');
    }
    renderLoading() {
        return this.renderBody();
    }
    renderDebugFiles() {
        const { debugFiles, showDetails } = this.state;
        const { organization, params } = this.props;
        const { orgId, projectId } = params;
        if (!(debugFiles === null || debugFiles === void 0 ? void 0 : debugFiles.length)) {
            return null;
        }
        return debugFiles.map(debugFile => {
            const downloadUrl = `${this.api.baseUrl}/projects/${orgId}/${projectId}/files/dsyms/?id=${debugFile.id}`;
            return (<debugFileRow_1.default debugFile={debugFile} showDetails={showDetails} downloadUrl={downloadUrl} downloadRole={organization.debugFilesRole} onDelete={this.handleDelete} key={debugFile.id}/>);
        });
    }
    renderBody() {
        var _a;
        const { organization, project, router, location } = this.props;
        const { loading, showDetails, builtinSymbolSources, debugFiles, debugFilesPageLinks } = this.state;
        const { features } = organization;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Debug Information Files')}/>

        <textBlock_1.default>
          {(0, locale_1.t)(`
            Debug information files are used to convert addresses and minified
            function names from native crash reports into function names and
            locations.
          `)}
        </textBlock_1.default>

        {features.includes('symbol-sources') && (<react_1.Fragment>
            <permissionAlert_1.default />
            <externalSources_1.default api={this.api} location={location} router={router} projSlug={project.slug} organization={organization} customRepositories={(project.symbolSources
                    ? JSON.parse(project.symbolSources)
                    : [])} builtinSymbolSources={(_a = project.builtinSymbolSources) !== null && _a !== void 0 ? _a : []} builtinSymbolSourceOptions={builtinSymbolSources !== null && builtinSymbolSources !== void 0 ? builtinSymbolSources : []}/>
          </react_1.Fragment>)}

        <Wrapper>
          <textBlock_1.default noMargin>{(0, locale_1.t)('Uploaded debug information files')}</textBlock_1.default>
          <Filters>
            <Label>
              <checkbox_1.default checked={showDetails} onChange={e => {
                this.setState({ showDetails: e.target.checked });
            }}/>
              {(0, locale_1.t)('show details')}
            </Label>

            <searchBar_1.default placeholder={(0, locale_1.t)('Search DIFs')} onSearch={this.handleSearch} query={this.getQuery()}/>
          </Filters>
        </Wrapper>

        <StyledPanelTable headers={[
                (0, locale_1.t)('Debug ID'),
                (0, locale_1.t)('Information'),
                <Actions key="actions">{(0, locale_1.t)('Actions')}</Actions>,
            ]} emptyMessage={this.getEmptyMessage()} isEmpty={(debugFiles === null || debugFiles === void 0 ? void 0 : debugFiles.length) === 0} isLoading={loading}>
          {this.renderDebugFiles()}
        </StyledPanelTable>
        <pagination_1.default pageLinks={debugFilesPageLinks}/>
      </react_1.Fragment>);
    }
}
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  grid-template-columns: 37% 1fr auto;
`;
const Actions = (0, styled_1.default)('div') `
  text-align: right;
`;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto 1fr;
  grid-gap: ${(0, space_1.default)(4)};
  align-items: center;
  margin-top: ${(0, space_1.default)(4)};
  margin-bottom: ${(0, space_1.default)(1)};
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
  }
`;
const Filters = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: min-content minmax(200px, 400px);
  align-items: center;
  justify-content: flex-end;
  grid-gap: ${(0, space_1.default)(2)};
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: min-content 1fr;
  }
`;
const Label = (0, styled_1.default)('label') `
  font-weight: normal;
  display: flex;
  margin-bottom: 0;
  white-space: nowrap;
  input {
    margin-top: 0;
    margin-right: ${(0, space_1.default)(1)};
  }
`;
exports.default = ProjectDebugSymbols;
//# sourceMappingURL=index.jsx.map