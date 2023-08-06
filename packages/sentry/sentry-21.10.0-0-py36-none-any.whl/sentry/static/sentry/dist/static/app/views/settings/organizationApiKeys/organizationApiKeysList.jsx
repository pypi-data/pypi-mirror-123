Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const autoSelectText_1 = (0, tslib_1.__importDefault)(require("app/components/autoSelectText"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const linkWithConfirmation_1 = (0, tslib_1.__importDefault)(require("app/components/links/linkWithConfirmation"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const input_1 = require("app/styles/input");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
function OrganizationApiKeysList({ params, routes, keys, busy, loading, onAddApiKey, onRemove, }) {
    const hasKeys = keys && keys.length;
    const action = (<button_1.default priority="primary" size="small" icon={<icons_1.IconAdd size="xs" isCircled/>} busy={busy} disabled={busy} onClick={onAddApiKey}>
      {(0, locale_1.t)('New API Key')}
    </button_1.default>);
    return (<div>
      <settingsPageHeader_1.default title={(0, locale_1.t)('API Keys')} action={action}/>

      <textBlock_1.default>
        {(0, locale_1.tct)(`API keys grant access to the [api:developer web API].
          If you're looking to configure a Sentry client, you'll need a
          client key which is available in your project settings.`, {
            api: <externalLink_1.default href="https://docs.sentry.io/api/"/>,
        })}
      </textBlock_1.default>

      <alertLink_1.default to="/settings/account/api/auth-tokens/" priority="info">
        {(0, locale_1.tct)('Until Sentry supports OAuth, you might want to switch to using [tokens:Auth Tokens] instead.', {
            tokens: <u />,
        })}
      </alertLink_1.default>

      <panels_1.PanelTable isLoading={loading} isEmpty={!hasKeys} emptyMessage={(0, locale_1.t)('No API keys for this organization')} headers={[(0, locale_1.t)('Name'), (0, locale_1.t)('Key'), (0, locale_1.t)('Actions')]}>
        {keys &&
            keys.map(({ id, key, label }) => {
                const apiDetailsUrl = (0, recreateRoute_1.default)(`${id}/`, {
                    params,
                    routes,
                });
                return (<react_1.Fragment key={key}>
                <Cell>
                  <link_1.default to={apiDetailsUrl}>{label}</link_1.default>
                </Cell>

                <div>
                  <AutoSelectTextInput readOnly>{key}</AutoSelectTextInput>
                </div>

                <Cell>
                  <linkWithConfirmation_1.default aria-label={(0, locale_1.t)('Remove API Key')} className="btn btn-default btn-sm" onConfirm={() => onRemove(id)} message={(0, locale_1.t)('Are you sure you want to remove this API key?')} title={(0, locale_1.t)('Remove API Key?')}>
                    <icons_1.IconDelete size="xs" css={{ position: 'relative', top: '2px' }}/>
                  </linkWithConfirmation_1.default>
                </Cell>
              </react_1.Fragment>);
            })}
      </panels_1.PanelTable>
    </div>);
}
const Cell = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const AutoSelectTextInput = (0, styled_1.default)(autoSelectText_1.default) `
  ${p => (0, input_1.inputStyles)(p)}
`;
exports.default = OrganizationApiKeysList;
//# sourceMappingURL=organizationApiKeysList.jsx.map