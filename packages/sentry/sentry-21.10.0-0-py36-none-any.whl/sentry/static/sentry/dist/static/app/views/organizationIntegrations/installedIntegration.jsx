Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const addIntegrationButton_1 = (0, tslib_1.__importDefault)(require("./addIntegrationButton"));
const integrationItem_1 = (0, tslib_1.__importDefault)(require("./integrationItem"));
class InstalledIntegration extends React.Component {
    constructor() {
        super(...arguments);
        this.handleUninstallClick = () => {
            this.props.trackIntegrationAnalytics('integrations.uninstall_clicked');
        };
    }
    getRemovalBodyAndText(aspects) {
        if (aspects && aspects.removal_dialog) {
            return {
                body: aspects.removal_dialog.body,
                actionText: aspects.removal_dialog.actionText,
            };
        }
        else {
            return {
                body: (0, locale_1.t)('Deleting this integration will remove any project associated data. This action cannot be undone. Are you sure you want to delete this integration?'),
                actionText: (0, locale_1.t)('Delete'),
            };
        }
    }
    handleRemove(integration) {
        this.props.onRemove(integration);
        this.props.trackIntegrationAnalytics('integrations.uninstall_completed');
    }
    get removeConfirmProps() {
        const { integration } = this.props;
        const { body, actionText } = this.getRemovalBodyAndText(integration.provider.aspects);
        const message = (<React.Fragment>
        <alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {(0, locale_1.t)('Deleting this integration has consequences!')}
        </alert_1.default>
        {body}
      </React.Fragment>);
        return {
            message,
            confirmText: actionText,
            onConfirm: () => this.handleRemove(integration),
        };
    }
    get disableConfirmProps() {
        const { integration } = this.props;
        const { body, actionText } = integration.provider.aspects.disable_dialog || {};
        const message = (<React.Fragment>
        <alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {(0, locale_1.t)('This integration cannot be removed in Sentry')}
        </alert_1.default>
        {body}
      </React.Fragment>);
        return {
            message,
            confirmText: actionText,
            onConfirm: () => this.props.onDisable(integration),
        };
    }
    render() {
        const { className, integration, organization, provider, requiresUpgrade } = this.props;
        const removeConfirmProps = integration.status === 'active' && integration.provider.canDisable
            ? this.disableConfirmProps
            : this.removeConfirmProps;
        return (<access_1.default access={['org:integrations']}>
        {({ hasAccess }) => (<IntegrationFlex key={integration.id} className={className}>
            <IntegrationItemBox>
              <integrationItem_1.default integration={integration}/>
            </IntegrationItemBox>
            <div>
              <tooltip_1.default disabled={hasAccess} position="left" title={(0, locale_1.t)('You must be an organization owner, manager or admin to configure')}>
                {requiresUpgrade && (<addIntegrationButton_1.default analyticsParams={{
                        view: 'integrations_directory_integration_detail',
                        already_installed: true,
                    }} buttonText={(0, locale_1.t)('Update Now')} data-test-id="integration-upgrade-button" disabled={!(hasAccess && integration.status === 'active')} icon={<icons_1.IconWarning />} onAddIntegration={() => { }} organization={organization} provider={provider} priority="primary" size="small"/>)}
                <StyledButton borderless icon={<icons_1.IconSettings />} disabled={!(hasAccess && integration.status === 'active')} to={`/settings/${organization.slug}/integrations/${provider.key}/${integration.id}/`} data-test-id="integration-configure-button">
                  {(0, locale_1.t)('Configure')}
                </StyledButton>
              </tooltip_1.default>
            </div>
            <div>
              <tooltip_1.default disabled={hasAccess} title={(0, locale_1.t)('You must be an organization owner, manager or admin to uninstall')}>
                <confirm_1.default priority="danger" onConfirming={this.handleUninstallClick} disabled={!hasAccess} {...removeConfirmProps}>
                  <StyledButton disabled={!hasAccess} borderless icon={<icons_1.IconDelete />} data-test-id="integration-remove-button">
                    {(0, locale_1.t)('Uninstall')}
                  </StyledButton>
                </confirm_1.default>
              </tooltip_1.default>
            </div>

            <StyledIntegrationStatus status={integration.status}/>
          </IntegrationFlex>)}
      </access_1.default>);
    }
}
exports.default = InstalledIntegration;
const StyledButton = (0, styled_1.default)(button_1.default) `
  color: ${p => p.theme.gray300};
`;
const IntegrationFlex = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const IntegrationItemBox = (0, styled_1.default)('div') `
  flex: 1;
`;
const IntegrationStatus = (props) => {
    const theme = (0, react_1.useTheme)();
    const { status } = props, p = (0, tslib_1.__rest)(props, ["status"]);
    const color = status === 'active' ? theme.success : theme.gray300;
    const titleText = status === 'active'
        ? (0, locale_1.t)('This Integration can be disabled by clicking the Uninstall button')
        : (0, locale_1.t)('This Integration has been disconnected from the external provider');
    return (<tooltip_1.default title={titleText}>
      <div {...p}>
        <circleIndicator_1.default size={6} color={color}/>
        <IntegrationStatusText>{`${status === 'active' ? (0, locale_1.t)('enabled') : (0, locale_1.t)('disabled')}`}</IntegrationStatusText>
      </div>
    </tooltip_1.default>);
};
const StyledIntegrationStatus = (0, styled_1.default)(IntegrationStatus) `
  display: flex;
  align-items: center;
  color: ${p => p.theme.gray300};
  font-weight: light;
  text-transform: capitalize;
  &:before {
    content: '|';
    color: ${p => p.theme.gray200};
    margin-right: ${(0, space_1.default)(1)};
    font-weight: normal;
  }
`;
const IntegrationStatusText = (0, styled_1.default)('div') `
  margin: 0 ${(0, space_1.default)(0.75)} 0 ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=installedIntegration.jsx.map