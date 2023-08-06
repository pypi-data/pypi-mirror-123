Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const sortBy_1 = (0, tslib_1.__importDefault)(require("lodash/sortBy"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const repositoryProjectPathConfigForm_1 = (0, tslib_1.__importDefault)(require("app/components/repositoryProjectPathConfigForm"));
const repositoryProjectPathConfigRow_1 = (0, tslib_1.__importStar)(require("app/components/repositoryProjectPathConfigRow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
class IntegrationCodeMappings extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = (pathConfig) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization } = this.props;
            const endpoint = `/organizations/${organization.slug}/code-mappings/${pathConfig.id}/`;
            try {
                yield this.api.requestPromise(endpoint, {
                    method: 'DELETE',
                });
                // remove config and update state
                let { pathConfigs } = this.state;
                pathConfigs = pathConfigs.filter(config => config.id !== pathConfig.id);
                this.setState({ pathConfigs });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Deletion successful'));
            }
            catch (err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.tct)('[status]: [text]', {
                    status: err.statusText,
                    text: err.responseText,
                }));
            }
        });
        this.handleSubmitSuccess = (pathConfig) => {
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_complete_setup', {
                setup_type: 'manual',
                view: 'integration_configuration_detail',
                provider: this.props.integration.provider.key,
                organization: this.props.organization,
            });
            let { pathConfigs } = this.state;
            pathConfigs = pathConfigs.filter(config => config.id !== pathConfig.id);
            // our getter handles the order of the configs
            pathConfigs = pathConfigs.concat([pathConfig]);
            this.setState({ pathConfigs });
            this.setState({ pathConfig: undefined });
        };
        this.openModal = (pathConfig) => {
            const { organization, projects, integration } = this.props;
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_start_setup', {
                setup_type: 'manual',
                view: 'integration_configuration_detail',
                provider: this.props.integration.provider.key,
                organization: this.props.organization,
            });
            (0, modal_1.openModal)(({ Body, Header, closeModal }) => (<react_1.Fragment>
        <Header closeButton>{(0, locale_1.t)('Configure code path mapping')}</Header>
        <Body>
          <repositoryProjectPathConfigForm_1.default organization={organization} integration={integration} projects={projects} repos={this.repos} onSubmitSuccess={config => {
                    this.handleSubmitSuccess(config);
                    closeModal();
                }} existingConfig={pathConfig} onCancel={closeModal}/>
        </Body>
      </react_1.Fragment>));
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { pathConfigs: [], repos: [] });
    }
    get integrationId() {
        return this.props.integration.id;
    }
    get pathConfigs() {
        // we want to sort by the project slug and the
        // id of the config
        return (0, sortBy_1.default)(this.state.pathConfigs, [
            ({ projectSlug }) => projectSlug,
            ({ id }) => parseInt(id, 10),
        ]);
    }
    get repos() {
        // endpoint doesn't support loading only the repos for this integration
        // but most people only have one source code repo so this should be fine
        return this.state.repos.filter(repo => repo.integrationId === this.integrationId);
    }
    getEndpoints() {
        const orgSlug = this.props.organization.slug;
        return [
            [
                'pathConfigs',
                `/organizations/${orgSlug}/code-mappings/`,
                { query: { integrationId: this.integrationId } },
            ],
            ['repos', `/organizations/${orgSlug}/repos/`, { query: { status: 'active' } }],
        ];
    }
    getMatchingProject(pathConfig) {
        return this.props.projects.find(project => project.id === pathConfig.projectId);
    }
    componentDidMount() {
        const { referrer } = qs.parse(window.location.search) || {};
        // We don't start new session if the user was coming from choosing
        // the manual setup option flow from the issue details page
        const startSession = referrer === 'stacktrace-issue-details' ? false : true;
        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.code_mappings_viewed', {
            integration: this.props.integration.provider.key,
            integration_type: 'first_party',
            organization: this.props.organization,
        }, { startSession });
    }
    renderBody() {
        const pathConfigs = this.pathConfigs;
        const { integration } = this.props;
        return (<react_1.Fragment>
        <textBlock_1.default>
          {(0, locale_1.tct)(`Code Mappings are used to map stack trace file paths to source code file paths. These mappings are the basis for features like Stack Trace Linking. To learn more, [link: read the docs].`, {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/integrations/source-code-mgmt/gitlab/#stack-trace-linking"/>),
            })}
        </textBlock_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader disablePadding hasButtons>
            <HeaderLayout>
              <repositoryProjectPathConfigRow_1.NameRepoColumn>{(0, locale_1.t)('Code Mappings')}</repositoryProjectPathConfigRow_1.NameRepoColumn>
              <repositoryProjectPathConfigRow_1.InputPathColumn>{(0, locale_1.t)('Stack Trace Root')}</repositoryProjectPathConfigRow_1.InputPathColumn>
              <repositoryProjectPathConfigRow_1.OutputPathColumn>{(0, locale_1.t)('Source Code Root')}</repositoryProjectPathConfigRow_1.OutputPathColumn>

              <access_1.default access={['org:integrations']}>
                {({ hasAccess }) => (<repositoryProjectPathConfigRow_1.ButtonColumn>
                    <tooltip_1.default title={(0, locale_1.t)('You must be an organization owner, manager or admin to edit or remove a code mapping.')} disabled={hasAccess}>
                      <AddButton data-test-id="add-mapping-button" onClick={() => this.openModal()} size="xsmall" icon={<icons_1.IconAdd size="xs" isCircled/>} disabled={!hasAccess}>
                        {(0, locale_1.t)('Add Code Mapping')}
                      </AddButton>
                    </tooltip_1.default>
                  </repositoryProjectPathConfigRow_1.ButtonColumn>)}
              </access_1.default>
            </HeaderLayout>
          </panels_1.PanelHeader>
          <panels_1.PanelBody>
            {pathConfigs.length === 0 && (<emptyMessage_1.default icon={(0, integrationUtil_1.getIntegrationIcon)(integration.provider.key, 'lg')} action={<button_1.default href={`https://docs.sentry.io/product/integrations/${integration.provider.key}/#stack-trace-linking`} size="small" onClick={() => {
                        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_docs_clicked', {
                            view: 'integration_configuration_detail',
                            provider: this.props.integration.provider.key,
                            organization: this.props.organization,
                        });
                    }}>
                    View Documentation
                  </button_1.default>}>
                Set up stack trace linking by adding a code mapping.
              </emptyMessage_1.default>)}
            {pathConfigs
                .map(pathConfig => {
                const project = this.getMatchingProject(pathConfig);
                // this should never happen since our pathConfig would be deleted
                // if project was deleted
                if (!project) {
                    return null;
                }
                return (<ConfigPanelItem key={pathConfig.id}>
                    <Layout>
                      <repositoryProjectPathConfigRow_1.default pathConfig={pathConfig} project={project} onEdit={this.openModal} onDelete={this.handleDelete}/>
                    </Layout>
                  </ConfigPanelItem>);
            })
                .filter(item => !!item)}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = (0, withProjects_1.default)((0, withOrganization_1.default)(IntegrationCodeMappings));
const AddButton = (0, styled_1.default)(button_1.default) ``;
const Layout = (0, styled_1.default)('div') `
  display: grid;
  grid-column-gap: ${(0, space_1.default)(1)};
  width: 100%;
  align-items: center;
  grid-template-columns: 4.5fr 2.5fr 2.5fr 1.6fr;
  grid-template-areas: 'name-repo input-path output-path button';
`;
const HeaderLayout = (0, styled_1.default)(Layout) `
  align-items: center;
  margin: 0;
  margin-left: ${(0, space_1.default)(2)};
`;
const ConfigPanelItem = (0, styled_1.default)(panels_1.PanelItem) ``;
//# sourceMappingURL=integrationCodeMappings.jsx.map