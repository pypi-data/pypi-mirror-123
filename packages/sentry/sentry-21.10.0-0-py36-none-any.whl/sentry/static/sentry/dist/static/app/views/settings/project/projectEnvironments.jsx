Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectEnvironments = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const listLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/listLink"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const panels_1 = require("app/components/panels");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const environment_1 = require("app/utils/environment");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
class ProjectEnvironments extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            project: null,
            environments: null,
            isLoading: true,
        };
        // Toggle visibility of environment
        this.toggleEnv = (env, shouldHide) => {
            const { orgId, projectId } = this.props.params;
            this.props.api.request(`/projects/${orgId}/${projectId}/environments/${(0, environment_1.getUrlRoutingName)(env)}/`, {
                method: 'PUT',
                data: {
                    name: env.name,
                    isHidden: shouldHide,
                },
                success: () => {
                    (0, indicator_1.addSuccessMessage)((0, locale_1.tct)('Updated [environment]', {
                        environment: (0, environment_1.getDisplayName)(env),
                    }));
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)((0, locale_1.tct)('Unable to update [environment]', {
                        environment: (0, environment_1.getDisplayName)(env),
                    }));
                },
                complete: this.fetchData.bind(this),
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if (this.props.location.pathname.endsWith('hidden/') !==
            prevProps.location.pathname.endsWith('hidden/')) {
            this.fetchData();
        }
    }
    fetchData() {
        const isHidden = this.props.location.pathname.endsWith('hidden/');
        if (!this.state.isLoading) {
            this.setState({ isLoading: true });
        }
        const { orgId, projectId } = this.props.params;
        this.props.api.request(`/projects/${orgId}/${projectId}/environments/`, {
            query: {
                visibility: isHidden ? 'hidden' : 'visible',
            },
            success: environments => {
                this.setState({ environments, isLoading: false });
            },
        });
    }
    fetchProjectDetails() {
        const { orgId, projectId } = this.props.params;
        this.props.api.request(`/projects/${orgId}/${projectId}/`, {
            success: project => {
                this.setState({ project });
            },
        });
    }
    renderEmpty() {
        const isHidden = this.props.location.pathname.endsWith('hidden/');
        const message = isHidden
            ? (0, locale_1.t)("You don't have any hidden environments.")
            : (0, locale_1.t)("You don't have any environments yet.");
        return <emptyMessage_1.default>{message}</emptyMessage_1.default>;
    }
    /**
     * Renders rows for "system" environments:
     * - "All Environments"
     * - "No Environment"
     *
     */
    renderAllEnvironmentsSystemRow() {
        // Not available in "Hidden" tab
        const isHidden = this.props.location.pathname.endsWith('hidden/');
        if (isHidden) {
            return null;
        }
        return (<EnvironmentRow name={constants_1.ALL_ENVIRONMENTS_KEY} environment={{
                id: constants_1.ALL_ENVIRONMENTS_KEY,
                name: constants_1.ALL_ENVIRONMENTS_KEY,
                displayName: constants_1.ALL_ENVIRONMENTS_KEY,
            }} isSystemRow/>);
    }
    renderEnvironmentList(envs) {
        const isHidden = this.props.location.pathname.endsWith('hidden/');
        const buttonText = isHidden ? (0, locale_1.t)('Show') : (0, locale_1.t)('Hide');
        return (<react_1.Fragment>
        {this.renderAllEnvironmentsSystemRow()}
        {envs.map(env => (<EnvironmentRow key={env.id} name={env.name} environment={env} isHidden={isHidden} onHide={this.toggleEnv} actionText={buttonText} shouldShowAction/>))}
      </react_1.Fragment>);
    }
    renderBody() {
        const { environments, isLoading } = this.state;
        if (isLoading) {
            return <loadingIndicator_1.default />;
        }
        return (<panels_1.PanelBody>
        {(environments === null || environments === void 0 ? void 0 : environments.length)
                ? this.renderEnvironmentList(environments)
                : this.renderEmpty()}
      </panels_1.PanelBody>);
    }
    render() {
        const { routes, params, location } = this.props;
        const isHidden = location.pathname.endsWith('hidden/');
        const baseUrl = (0, recreateRoute_1.default)('', { routes, params, stepBack: -1 });
        return (<div>
        <sentryDocumentTitle_1.default title={(0, locale_1.t)('Environments')} projectSlug={params.projectId}/>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Manage Environments')} tabs={<navTabs_1.default underlined>
              <listLink_1.default to={baseUrl} index isActive={() => !isHidden}>
                {(0, locale_1.t)('Environments')}
              </listLink_1.default>
              <listLink_1.default to={`${baseUrl}hidden/`} index isActive={() => isHidden}>
                {(0, locale_1.t)('Hidden')}
              </listLink_1.default>
            </navTabs_1.default>}/>
        <permissionAlert_1.default />

        <panels_1.Panel>
          <panels_1.PanelHeader>{isHidden ? (0, locale_1.t)('Hidden') : (0, locale_1.t)('Active Environments')}</panels_1.PanelHeader>
          {this.renderBody()}
        </panels_1.Panel>
      </div>);
    }
}
exports.ProjectEnvironments = ProjectEnvironments;
function EnvironmentRow({ environment, name, onHide, shouldShowAction = false, isSystemRow = false, isHidden = false, actionText = '', }) {
    return (<EnvironmentItem>
      <Name>{isSystemRow ? (0, locale_1.t)('All Environments') : name}</Name>
      <access_1.default access={['project:write']}>
        {({ hasAccess }) => (<react_1.Fragment>
            {shouldShowAction && onHide && (<EnvironmentButton size="xsmall" disabled={!hasAccess} onClick={() => onHide(environment, !isHidden)}>
                {actionText}
              </EnvironmentButton>)}
          </react_1.Fragment>)}
      </access_1.default>
    </EnvironmentItem>);
}
const EnvironmentItem = (0, styled_1.default)(panels_1.PanelItem) `
  align-items: center;
  justify-content: space-between;
`;
const Name = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const EnvironmentButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(0.5)};
`;
exports.default = (0, withApi_1.default)(ProjectEnvironments);
//# sourceMappingURL=projectEnvironments.jsx.map