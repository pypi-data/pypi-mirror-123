Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const integrationUtil_1 = require("app/utils/integrationUtil");
class PluginDeprecationAlert extends react_1.Component {
    render() {
        const { organization, plugin } = this.props;
        // Short-circuit if not deprecated.
        if (!plugin.deprecationDate) {
            return <react_1.default.Fragment />;
        }
        const resource = plugin.altIsSentryApp ? 'sentry-apps' : 'integrations';
        const upgradeUrl = `/settings/${organization.slug}/${resource}/${plugin.firstPartyAlternative}/`;
        const queryParams = `?${plugin.altIsSentryApp ? '' : 'tab=configurations&'}referrer=directory_upgrade_now`;
        return (<div>
        <alert_1.default type="warning" icon={<icons_1.IconWarning size="sm"/>}>
          <span>{`This integration is being deprecated on ${plugin.deprecationDate}. Please upgrade to avoid any disruption.`}</span>
          <UpgradeNowButton href={`${upgradeUrl}${queryParams}`} size="xsmall" onClick={() => (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.resolve_now_clicked', {
                integration_type: 'plugin',
                integration: plugin.slug,
                organization,
            })}>
            {(0, locale_1.t)('Upgrade Now')}
          </UpgradeNowButton>
        </alert_1.default>
      </div>);
    }
}
const UpgradeNowButton = (0, styled_1.default)(button_1.default) `
  color: ${p => p.theme.subText};
  float: right;
`;
exports.default = PluginDeprecationAlert;
//# sourceMappingURL=pluginDeprecationAlert.jsx.map