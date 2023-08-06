Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const sentryAppInstallations_1 = require("app/actionCreators/sentryAppInstallations");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const consolidatedScopes_1 = require("app/utils/consolidatedScopes");
const integrationUtil_1 = require("app/utils/integrationUtil");
const queryString_1 = require("app/utils/queryString");
const recordSentryAppInteraction_1 = require("app/utils/recordSentryAppInteraction");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const abstractIntegrationDetailedView_1 = (0, tslib_1.__importDefault)(require("./abstractIntegrationDetailedView"));
const SplitInstallationIdModal_1 = (0, tslib_1.__importDefault)(require("./SplitInstallationIdModal"));
class SentryAppDetailedView extends abstractIntegrationDetailedView_1.default {
    constructor() {
        super(...arguments);
        this.tabs = ['overview'];
        this.redirectUser = (install) => {
            const { organization } = this.props;
            const { sentryApp } = this.state;
            const queryParams = {
                installationId: install.uuid,
                code: install.code,
                orgSlug: organization.slug,
            };
            if (sentryApp.redirectUrl) {
                const redirectUrl = (0, queryString_1.addQueryParamsToExistingUrl)(sentryApp.redirectUrl, queryParams);
                window.location.assign(redirectUrl);
            }
        };
        this.handleInstall = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization } = this.props;
            const { sentryApp } = this.state;
            this.trackIntegrationAnalytics('integrations.installation_start', {
                integration_status: sentryApp.status,
            });
            // installSentryApp adds a message on failure
            const install = yield (0, sentryAppInstallations_1.installSentryApp)(this.api, organization.slug, sentryApp);
            // installation is complete if the status is installed
            if (install.status === 'installed') {
                this.trackIntegrationAnalytics('integrations.installation_complete', {
                    integration_status: sentryApp.status,
                });
            }
            if (!sentryApp.redirectUrl) {
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)(`${sentryApp.slug} successfully installed.`));
                this.setState({ appInstalls: [install, ...this.state.appInstalls] });
                // hack for split so we can show the install ID to users for them to copy
                // Will remove once the proper fix is in place
                if (['split', 'split-dev', 'split-testing'].includes(sentryApp.slug)) {
                    (0, modal_1.openModal)(({ closeModal }) => (<SplitInstallationIdModal_1.default installationId={install.uuid} closeModal={closeModal}/>));
                }
            }
            else {
                this.redirectUser(install);
            }
        });
        this.handleUninstall = (install) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                yield (0, sentryAppInstallations_1.uninstallSentryApp)(this.api, install);
                this.trackIntegrationAnalytics('integrations.uninstall_completed', {
                    integration_status: this.sentryApp.status,
                });
                const appInstalls = this.state.appInstalls.filter(i => i.app.slug !== this.sentryApp.slug);
                return this.setState({ appInstalls });
            }
            catch (error) {
                return (0, indicator_1.addErrorMessage)((0, locale_1.t)(`Unable to uninstall ${this.sentryApp.name}`));
            }
        });
        this.recordUninstallClicked = () => {
            const sentryApp = this.sentryApp;
            this.trackIntegrationAnalytics('integrations.uninstall_clicked', {
                integration_status: sentryApp.status,
            });
        };
    }
    getEndpoints() {
        const { organization, params: { integrationSlug }, } = this.props;
        return [
            ['sentryApp', `/sentry-apps/${integrationSlug}/`],
            ['featureData', `/sentry-apps/${integrationSlug}/features/`],
            ['appInstalls', `/organizations/${organization.slug}/sentry-app-installations/`],
        ];
    }
    onLoadAllEndpointsSuccess() {
        const { organization, params: { integrationSlug }, router, } = this.props;
        // redirect for internal integrations
        if (this.sentryApp.status === 'internal') {
            router.push(`/settings/${organization.slug}/developer-settings/${integrationSlug}/`);
            return;
        }
        super.onLoadAllEndpointsSuccess();
        (0, recordSentryAppInteraction_1.recordInteraction)(integrationSlug, 'sentry_app_viewed');
    }
    get integrationType() {
        return 'sentry_app';
    }
    get sentryApp() {
        return this.state.sentryApp;
    }
    get description() {
        return this.state.sentryApp.overview || '';
    }
    get author() {
        return this.sentryApp.author;
    }
    get resourceLinks() {
        // only show links for published sentry apps
        if (this.sentryApp.status !== 'published') {
            return [];
        }
        return [
            {
                title: 'Documentation',
                url: `https://docs.sentry.io/product/integrations/${this.integrationSlug}/`,
            },
        ];
    }
    get permissions() {
        return (0, consolidatedScopes_1.toPermissions)(this.sentryApp.scopes);
    }
    get installationStatus() {
        return (0, integrationUtil_1.getSentryAppInstallStatus)(this.install);
    }
    get integrationName() {
        return this.sentryApp.name;
    }
    get featureData() {
        return this.state.featureData;
    }
    get install() {
        return this.state.appInstalls.find(i => i.app.slug === this.sentryApp.slug);
    }
    renderPermissions() {
        const permissions = this.permissions;
        if (!Object.keys(permissions).some(scope => permissions[scope].length > 0)) {
            return null;
        }
        return (<PermissionWrapper>
        <Title>Permissions</Title>
        {permissions.read.length > 0 && (<Permission>
            <Indicator />
            <Text key="read">
              {(0, locale_1.tct)('[read] access to [resources] resources', {
                    read: <strong>Read</strong>,
                    resources: permissions.read.join(', '),
                })}
            </Text>
          </Permission>)}
        {permissions.write.length > 0 && (<Permission>
            <Indicator />
            <Text key="write">
              {(0, locale_1.tct)('[read] and [write] access to [resources] resources', {
                    read: <strong>Read</strong>,
                    write: <strong>Write</strong>,
                    resources: permissions.write.join(', '),
                })}
            </Text>
          </Permission>)}
        {permissions.admin.length > 0 && (<Permission>
            <Indicator />
            <Text key="admin">
              {(0, locale_1.tct)('[admin] access to [resources] resources', {
                    admin: <strong>Admin</strong>,
                    resources: permissions.admin.join(', '),
                })}
            </Text>
          </Permission>)}
      </PermissionWrapper>);
    }
    renderTopButton(disabledFromFeatures, userHasAccess) {
        const install = this.install;
        if (install) {
            return (<confirm_1.default disabled={!userHasAccess} message={(0, locale_1.tct)('Are you sure you want to remove the [slug] installation?', {
                    slug: this.integrationSlug,
                })} onConfirm={() => this.handleUninstall(install)} // called when the user confirms the action
             onConfirming={this.recordUninstallClicked} // called when the confirm modal opens
             priority="danger">
          <StyledUninstallButton size="small" data-test-id="sentry-app-uninstall">
            <icons_1.IconSubtract isCircled style={{ marginRight: (0, space_1.default)(0.75) }}/>
            {(0, locale_1.t)('Uninstall')}
          </StyledUninstallButton>
        </confirm_1.default>);
        }
        if (userHasAccess) {
            return (<InstallButton data-test-id="install-button" disabled={disabledFromFeatures} onClick={() => this.handleInstall()} priority="primary" size="small" style={{ marginLeft: (0, space_1.default)(1) }}>
          {(0, locale_1.t)('Accept & Install')}
        </InstallButton>);
        }
        return this.renderRequestIntegrationButton();
    }
    // no configurations for sentry apps
    renderConfigurations() {
        return null;
    }
}
const Text = (0, styled_1.default)('p') `
  margin: 0px 6px;
`;
const Permission = (0, styled_1.default)('div') `
  display: flex;
`;
const PermissionWrapper = (0, styled_1.default)('div') `
  padding-bottom: ${(0, space_1.default)(2)};
`;
const Title = (0, styled_1.default)('p') `
  margin-bottom: ${(0, space_1.default)(1)};
  font-weight: bold;
`;
const Indicator = (0, styled_1.default)(p => <circleIndicator_1.default size={7} {...p}/>) `
  margin-top: 3px;
  color: ${p => p.theme.success};
`;
const InstallButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
const StyledUninstallButton = (0, styled_1.default)(button_1.default) `
  color: ${p => p.theme.gray300};
  background: ${p => p.theme.background};

  border: ${p => `1px solid ${p.theme.gray300}`};
  box-sizing: border-box;
  box-shadow: 0px 2px 1px rgba(0, 0, 0, 0.08);
  border-radius: 4px;
`;
exports.default = (0, withOrganization_1.default)(SentryAppDetailedView);
//# sourceMappingURL=sentryAppDetailedView.jsx.map