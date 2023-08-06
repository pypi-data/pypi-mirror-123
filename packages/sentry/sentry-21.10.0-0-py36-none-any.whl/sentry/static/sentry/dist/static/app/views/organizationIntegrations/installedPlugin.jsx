Object.defineProperty(exports, "__esModule", { value: true });
exports.InstalledPlugin = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class InstalledPlugin extends react_1.Component {
    constructor() {
        super(...arguments);
        this.pluginUpdate = (data, method = 'POST') => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, projectItem, plugin } = this.props;
            // no try/catch so the caller will have to have it
            yield this.props.api.requestPromise(`/projects/${organization.slug}/${projectItem.projectSlug}/plugins/${plugin.id}/`, {
                method,
                data,
            });
        });
        this.updatePluginEnableStatus = (enabled) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (enabled) {
                yield this.pluginUpdate({ enabled });
            }
            else {
                yield this.pluginUpdate({}, 'DELETE');
            }
        });
        this.handleReset = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Removing...'));
                yield this.pluginUpdate({ reset: true });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Configuration was removed'));
                this.props.onResetConfiguration(this.projectId);
                this.props.trackIntegrationAnalytics('integrations.uninstall_completed');
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove configuration'));
            }
        });
        this.handleUninstallClick = () => {
            this.props.trackIntegrationAnalytics('integrations.uninstall_clicked');
        };
        this.toggleEnablePlugin = (projectId, status = true) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Enabling...'));
                yield this.updatePluginEnableStatus(status);
                (0, indicator_1.addSuccessMessage)(status ? (0, locale_1.t)('Configuration was enabled.') : (0, locale_1.t)('Configuration was disabled.'));
                this.props.onPluginEnableStatusChange(projectId, status);
                this.props.trackIntegrationAnalytics(status ? 'integrations.enabled' : 'integrations.disabled');
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)(status
                    ? (0, locale_1.t)('Unable to enable configuration.')
                    : (0, locale_1.t)('Unable to disable configuration.'));
            }
        });
    }
    get projectId() {
        return this.props.projectItem.projectId;
    }
    getConfirmMessage() {
        return (<react_1.Fragment>
        <alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {(0, locale_1.t)('Deleting this installation will disable the integration for this project and remove any configurations.')}
        </alert_1.default>
      </react_1.Fragment>);
    }
    get projectForBadge() {
        // this function returns the project as needed for the ProjectBadge component
        const { projectItem } = this.props;
        return {
            slug: projectItem.projectSlug,
            platform: projectItem.projectPlatform ? projectItem.projectPlatform : undefined,
        };
    }
    render() {
        const { className, plugin, organization, projectItem } = this.props;
        return (<Container>
        <access_1.default access={['org:integrations']}>
          {({ hasAccess }) => (<IntegrationFlex className={className}>
              <IntegrationItemBox>
                <projectBadge_1.default project={this.projectForBadge}/>
              </IntegrationItemBox>
              <div>
                {<StyledButton borderless icon={<icons_1.IconSettings />} disabled={!hasAccess} to={`/settings/${organization.slug}/projects/${projectItem.projectSlug}/plugins/${plugin.id}/`} data-test-id="integration-configure-button">
                    {(0, locale_1.t)('Configure')}
                  </StyledButton>}
              </div>
              <div>
                <confirm_1.default priority="danger" onConfirming={this.handleUninstallClick} disabled={!hasAccess} confirmText="Delete Installation" onConfirm={() => this.handleReset()} message={this.getConfirmMessage()}>
                  <StyledButton disabled={!hasAccess} borderless icon={<icons_1.IconDelete />} data-test-id="integration-remove-button">
                    {(0, locale_1.t)('Uninstall')}
                  </StyledButton>
                </confirm_1.default>
              </div>
              <switchButton_1.default isActive={projectItem.enabled} toggle={() => this.toggleEnablePlugin(projectItem.projectId, !projectItem.enabled)} isDisabled={!hasAccess}/>
            </IntegrationFlex>)}
        </access_1.default>
      </Container>);
    }
}
exports.InstalledPlugin = InstalledPlugin;
exports.default = (0, withApi_1.default)(InstalledPlugin);
const Container = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
  border: 1px solid ${p => p.theme.border};
  border-bottom: none;
  background-color: ${p => p.theme.background};

  &:last-child {
    border-bottom: 1px solid ${p => p.theme.border};
  }
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  color: ${p => p.theme.gray300};
`;
const IntegrationFlex = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const IntegrationItemBox = (0, styled_1.default)('div') `
  flex: 1;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  min-width: 0;
`;
//# sourceMappingURL=installedPlugin.jsx.map