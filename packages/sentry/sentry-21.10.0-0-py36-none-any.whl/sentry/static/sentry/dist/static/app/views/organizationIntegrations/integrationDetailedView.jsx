Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const abstractIntegrationDetailedView_1 = (0, tslib_1.__importDefault)(require("./abstractIntegrationDetailedView"));
const addIntegrationButton_1 = (0, tslib_1.__importDefault)(require("./addIntegrationButton"));
const installedIntegration_1 = (0, tslib_1.__importDefault)(require("./installedIntegration"));
class IntegrationDetailedView extends abstractIntegrationDetailedView_1.default {
    constructor() {
        super(...arguments);
        this.onInstall = (integration) => {
            // send the user to the configure integration view for that integration
            const { orgId } = this.props.params;
            this.props.router.push(`/settings/${orgId}/integrations/${integration.provider.key}/${integration.id}/`);
        };
        this.onRemove = (integration) => {
            const { orgId } = this.props.params;
            const origIntegrations = [...this.state.configurations];
            const integrations = this.state.configurations.filter(i => i.id !== integration.id);
            this.setState({ configurations: integrations });
            const options = {
                method: 'DELETE',
                error: () => {
                    this.setState({ configurations: origIntegrations });
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to remove Integration'));
                },
            };
            this.api.request(`/organizations/${orgId}/integrations/${integration.id}/`, options);
        };
        this.onDisable = (integration) => {
            let url;
            const [domainName, orgName] = integration.domainName.split('/');
            if (integration.accountType === 'User') {
                url = `https://${domainName}/settings/installations/`;
            }
            else {
                url = `https://${domainName}/organizations/${orgName}/settings/installations/`;
            }
            window.open(url, '_blank');
        };
        this.handleExternalInstall = () => {
            this.trackIntegrationAnalytics('integrations.installation_start');
        };
    }
    getEndpoints() {
        const { orgId, integrationSlug } = this.props.params;
        return [
            [
                'information',
                `/organizations/${orgId}/config/integrations/?provider_key=${integrationSlug}`,
            ],
            [
                'configurations',
                `/organizations/${orgId}/integrations/?provider_key=${integrationSlug}&includeConfig=0`,
            ],
        ];
    }
    get integrationType() {
        return 'first_party';
    }
    get provider() {
        return this.state.information.providers[0];
    }
    get description() {
        return this.metadata.description;
    }
    get author() {
        return this.metadata.author;
    }
    get alerts() {
        const provider = this.provider;
        const metadata = this.metadata;
        // The server response for integration installations includes old icon CSS classes
        // We map those to the currently in use values to their react equivalents
        // and fallback to IconFlag just in case.
        const alerts = (metadata.aspects.alerts || []).map(item => {
            switch (item.icon) {
                case 'icon-warning':
                case 'icon-warning-sm':
                    return Object.assign(Object.assign({}, item), { icon: <icons_1.IconWarning /> });
                default:
                    return Object.assign(Object.assign({}, item), { icon: <icons_1.IconFlag /> });
            }
        });
        if (!provider.canAdd && metadata.aspects.externalInstall) {
            alerts.push({
                type: 'warning',
                icon: <icons_1.IconOpen />,
                text: metadata.aspects.externalInstall.noticeText,
            });
        }
        return alerts;
    }
    get resourceLinks() {
        const metadata = this.metadata;
        return [
            { url: metadata.source_url, title: 'View Source' },
            { url: metadata.issue_url, title: 'Report Issue' },
        ];
    }
    get metadata() {
        return this.provider.metadata;
    }
    get isEnabled() {
        return this.state.configurations.length > 0;
    }
    get installationStatus() {
        return this.isEnabled ? 'Installed' : 'Not Installed';
    }
    get integrationName() {
        return this.provider.name;
    }
    get featureData() {
        return this.metadata.features;
    }
    renderTopButton(disabledFromFeatures, userHasAccess) {
        const { organization } = this.props;
        const provider = this.provider;
        const { metadata } = provider;
        const size = 'small';
        const priority = 'primary';
        const buttonProps = {
            style: { marginBottom: (0, space_1.default)(1) },
            size,
            priority,
            'data-test-id': 'install-button',
            disabled: disabledFromFeatures,
            organization,
        };
        if (!userHasAccess) {
            return this.renderRequestIntegrationButton();
        }
        if (provider.canAdd) {
            return (<addIntegrationButton_1.default provider={provider} onAddIntegration={this.onInstall} analyticsParams={{
                    view: 'integrations_directory_integration_detail',
                    already_installed: this.installationStatus !== 'Not Installed',
                }} {...buttonProps}/>);
        }
        if (metadata.aspects.externalInstall) {
            return (<button_1.default icon={<icons_1.IconOpen />} href={metadata.aspects.externalInstall.url} onClick={this.handleExternalInstall} external {...buttonProps}>
          {metadata.aspects.externalInstall.buttonText}
        </button_1.default>);
        }
        // This should never happen but we can't return undefined without some refactoring.
        return <react_1.Fragment />;
    }
    renderConfigurations() {
        const { configurations } = this.state;
        const { organization } = this.props;
        const provider = this.provider;
        if (!configurations.length) {
            return this.renderEmptyConfigurations();
        }
        const alertText = (0, integrationUtil_1.getAlertText)(configurations);
        return (<react_1.Fragment>
        {alertText && (<alert_1.default type="warning" icon={<icons_1.IconFlag size="sm"/>}>
            {alertText}
          </alert_1.default>)}
        {configurations.map(integration => (<InstallWrapper key={integration.id}>
            <installedIntegration_1.default organization={organization} provider={provider} integration={integration} onRemove={this.onRemove} onDisable={this.onDisable} data-test-id={integration.id} trackIntegrationAnalytics={this.trackIntegrationAnalytics} requiresUpgrade={!!alertText}/>
          </InstallWrapper>))}
      </react_1.Fragment>);
    }
}
const InstallWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
  border: 1px solid ${p => p.theme.border};
  border-bottom: none;
  background-color: ${p => p.theme.background};

  &:last-child {
    border-bottom: 1px solid ${p => p.theme.border};
  }
`;
exports.default = (0, withOrganization_1.default)(IntegrationDetailedView);
//# sourceMappingURL=integrationDetailedView.jsx.map