Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textField"));
const DOCS_LINK = 'https://docs.sentry.io/product/integrations/notification-incidents/slack/#team-notifications';
const NOTIFICATION_PROVIDERS = ['slack'];
class TeamNotificationSettings extends asyncView_1.default {
    getTitle() {
        return 'Team Notification Settings';
    }
    getEndpoints() {
        const { organization, team } = this.props;
        return [
            [
                'teamDetails',
                `/teams/${organization.slug}/${team.slug}/`,
                { query: { expand: ['externalTeams'] } },
            ],
            [
                'integrations',
                `/organizations/${organization.slug}/integrations/`,
                { query: { includeConfig: 0 } },
            ],
        ];
    }
    renderBody() {
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Notifications')}</panels_1.PanelHeader>
        <panels_1.PanelBody>{this.renderPanelBody()}</panels_1.PanelBody>
      </panels_1.Panel>);
    }
    renderPanelBody() {
        const { teamDetails, integrations } = this.state;
        const notificationIntegrations = integrations.filter(integration => NOTIFICATION_PROVIDERS.includes(integration.provider.key));
        if (!notificationIntegrations.length) {
            return (<emptyMessage_1.default>
          {(0, locale_1.t)('No Notification Integrations have been installed yet.')}
        </emptyMessage_1.default>);
        }
        const externalTeams = (teamDetails.externalTeams || []).filter(externalTeam => NOTIFICATION_PROVIDERS.includes(externalTeam.provider));
        if (!externalTeams.length) {
            return (<emptyMessage_1.default>
          <div>{(0, locale_1.t)('No teams have been linked yet.')}</div>
          <NotDisabledSubText>
            {(0, locale_1.tct)('Head over to Slack and type [code] to get started. [link].', {
                    code: <code>/sentry link team</code>,
                    link: <externalLink_1.default href={DOCS_LINK}>{(0, locale_1.t)('Learn more')}</externalLink_1.default>,
                })}
          </NotDisabledSubText>
        </emptyMessage_1.default>);
        }
        const integrationsById = Object.fromEntries(notificationIntegrations.map(integration => [integration.id, integration]));
        return externalTeams.map(externalTeam => (<textField_1.default disabled key={externalTeam.id} label={<div>
            <NotDisabledText>
              {(0, utils_1.toTitleCase)(externalTeam.provider)}:
              {integrationsById[externalTeam.integrationId].name}
            </NotDisabledText>
            <NotDisabledSubText>
              {(0, locale_1.tct)('Unlink this channel in Slack with [code]. [link].', {
                    code: <code>/sentry unlink team</code>,
                    link: <externalLink_1.default href={DOCS_LINK}>{(0, locale_1.t)('Learn more')}</externalLink_1.default>,
                })}
            </NotDisabledSubText>
          </div>} name="externalName" value={externalTeam.externalName}/>));
    }
}
exports.default = (0, withOrganization_1.default)(TeamNotificationSettings);
const NotDisabledText = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  line-height: ${(0, space_1.default)(2)};
`;
const NotDisabledSubText = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeRelativeSmall};
  line-height: 1.4;
  margin-top: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=teamNotifications.jsx.map