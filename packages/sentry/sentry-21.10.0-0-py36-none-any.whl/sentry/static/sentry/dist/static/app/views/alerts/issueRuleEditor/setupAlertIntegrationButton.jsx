Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const pluginIcon_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/pluginIcon"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
/**
 * This component renders a button to Set up an alert integration (just Slack for now)
 * if the project has no alerting integrations setup already.
 */
class SetupAlertIntegrationButton extends asyncComponent_1.default {
    getEndpoints() {
        const { projectSlug, organization } = this.props;
        return [
            [
                'detailedProject',
                `/projects/${organization.slug}/${projectSlug}/?expand=hasAlertIntegration`,
            ],
        ];
    }
    renderLoading() {
        return null;
    }
    // if there is an error, just show nothing
    renderError() {
        return null;
    }
    renderBody() {
        const { organization } = this.props;
        const { detailedProject } = this.state;
        // don't render anything if we don't have the project yet or if an alert integration
        // is installed
        if (!detailedProject || detailedProject.hasAlertIntegrationInstalled) {
            return null;
        }
        const config = configStore_1.default.getConfig();
        // link to docs to set up Slack for on-prem folks
        const referrerQuery = '?referrer=issue-alert-builder';
        const buttonProps = config.isOnPremise
            ? {
                href: `https://develop.sentry.dev/integrations/slack/${referrerQuery}`,
            }
            : {
                to: `/settings/${organization.slug}/integrations/slack/${referrerQuery}`,
            };
        // TOOD(Steve): need to use the Tooltip component because adding a title to the button
        // puts the tooltip in the upper left hand corner of the page instead of the button
        return (<tooltip_1.default title={(0, locale_1.t)('Send Alerts to Slack. Install the integration now.')}>
        <button_1.default size="small" icon={<pluginIcon_1.default pluginId="slack" size={16}/>} {...buttonProps}>
          {(0, locale_1.t)('Set Up Slack Now')}
        </button_1.default>
      </tooltip_1.default>);
    }
}
exports.default = SetupAlertIntegrationButton;
//# sourceMappingURL=setupAlertIntegrationButton.jsx.map