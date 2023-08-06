Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
const queryString_1 = require("app/utils/queryString");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const sourceMapsArtifactRow_1 = (0, tslib_1.__importDefault)(require("./sourceMapsArtifactRow"));
class ProjectSourceMapsDetail extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSearch = (query) => {
            const { location, router } = this.props;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query }) }));
        };
        this.handleArtifactDelete = (id) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Removing artifact\u2026'));
            try {
                yield this.api.requestPromise(`${this.getArtifactsUrl()}${id}/`, {
                    method: 'DELETE',
                });
                this.fetchData();
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Artifact removed.'));
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove artifact. Please try again.'));
            }
        });
        this.handleArchiveDelete = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { orgId, projectId, name } = this.props.params;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Removing artifacts\u2026'));
            try {
                yield this.api.requestPromise(`/projects/${orgId}/${projectId}/files/source-maps/`, {
                    method: 'DELETE',
                    query: { name },
                });
                this.fetchData();
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Artifacts removed.'));
            }
            catch (_b) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove artifacts. Please try again.'));
            }
        });
    }
    getTitle() {
        const { projectId, name } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Archive %s', (0, formatters_1.formatVersion)(name)), projectId, false);
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { artifacts: [] });
    }
    getEndpoints() {
        return [['artifacts', this.getArtifactsUrl(), { query: { query: this.getQuery() } }]];
    }
    getArtifactsUrl() {
        const { orgId, projectId, name } = this.props.params;
        return `/projects/${orgId}/${projectId}/releases/${encodeURIComponent(name)}/files/`;
    }
    getQuery() {
        const { query } = this.props.location.query;
        return (0, queryString_1.decodeScalar)(query);
    }
    getEmptyMessage() {
        if (this.getQuery()) {
            return (0, locale_1.t)('There are no artifacts that match your search.');
        }
        return (0, locale_1.t)('There are no artifacts in this archive.');
    }
    renderLoading() {
        return this.renderBody();
    }
    renderArtifacts() {
        const { organization } = this.props;
        const { artifacts } = this.state;
        const artifactApiUrl = this.api.baseUrl + this.getArtifactsUrl();
        if (!artifacts.length) {
            return null;
        }
        return artifacts.map(artifact => {
            return (<sourceMapsArtifactRow_1.default key={artifact.id} artifact={artifact} onDelete={this.handleArtifactDelete} downloadUrl={`${artifactApiUrl}${artifact.id}/?download=1`} downloadRole={organization.debugFilesRole}/>);
        });
    }
    renderBody() {
        const { loading, artifacts, artifactsPageLinks } = this.state;
        const { name, orgId } = this.props.params;
        const { project } = this.props;
        return (<react_1.Fragment>
        <StyledSettingsPageHeader title={<Title>
              {(0, locale_1.t)('Archive')}&nbsp;
              <textOverflow_1.default>
                <version_1.default version={name} tooltipRawVersion anchor={false} truncate/>
              </textOverflow_1.default>
            </Title>} action={<StyledButtonBar gap={1}>
              <ReleaseButton to={`/organizations/${orgId}/releases/${encodeURIComponent(name)}/?project=${project.id}`}>
                {(0, locale_1.t)('Go to Release')}
              </ReleaseButton>
              <access_1.default access={['project:releases']}>
                {({ hasAccess }) => (<tooltip_1.default disabled={hasAccess} title={(0, locale_1.t)('You do not have permission to delete artifacts.')}>
                    <confirm_1.default message={(0, locale_1.t)('Are you sure you want to remove all artifacts in this archive?')} onConfirm={this.handleArchiveDelete} disabled={!hasAccess}>
                      <button_1.default icon={<icons_1.IconDelete size="sm"/>} title={(0, locale_1.t)('Remove All Artifacts')} label={(0, locale_1.t)('Remove All Artifacts')} disabled={!hasAccess}/>
                    </confirm_1.default>
                  </tooltip_1.default>)}
              </access_1.default>

              <searchBar_1.default placeholder={(0, locale_1.t)('Filter artifacts')} onSearch={this.handleSearch} query={this.getQuery()}/>
            </StyledButtonBar>}/>

        <StyledPanelTable headers={[
                (0, locale_1.t)('Artifact'),
                <SizeColumn key="size">{(0, locale_1.t)('File Size')}</SizeColumn>,
                '',
            ]} emptyMessage={this.getEmptyMessage()} isEmpty={artifacts.length === 0} isLoading={loading}>
          {this.renderArtifacts()}
        </StyledPanelTable>
        <pagination_1.default pageLinks={artifactsPageLinks}/>
      </react_1.Fragment>);
    }
}
const StyledSettingsPageHeader = (0, styled_1.default)(settingsPageHeader_1.default) `
  /*
    ugly selector to make header work on mobile
    we can refactor this once we start making other settings more responsive
  */
  > div {
    @media (max-width: ${p => p.theme.breakpoints[2]}) {
      display: block;
    }
    > div {
      min-width: 0;
      @media (max-width: ${p => p.theme.breakpoints[2]}) {
        margin-bottom: ${(0, space_1.default)(2)};
      }
    }
  }
`;
const Title = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  justify-content: flex-start;
`;
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  grid-template-columns: minmax(220px, 1fr) max-content 120px;
`;
const ReleaseButton = (0, styled_1.default)(button_1.default) `
  white-space: nowrap;
`;
const SizeColumn = (0, styled_1.default)('div') `
  text-align: right;
`;
exports.default = ProjectSourceMapsDetail;
//# sourceMappingURL=index.jsx.map