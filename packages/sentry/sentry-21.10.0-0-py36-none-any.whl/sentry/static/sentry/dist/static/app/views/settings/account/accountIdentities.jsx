Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const account_1 = require("app/actionCreators/account");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const ENDPOINT = '/users/me/social-identities/';
class AccountIdentities extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleDisconnect = (identity) => {
            const { identities } = this.state;
            this.setState(state => {
                var _a;
                const newIdentities = (_a = state.identities) === null || _a === void 0 ? void 0 : _a.filter(({ id }) => id !== identity.id);
                return {
                    identities: newIdentities !== null && newIdentities !== void 0 ? newIdentities : [],
                };
            }, () => (0, account_1.disconnectIdentity)(identity).catch(() => {
                this.setState({
                    identities,
                });
            }));
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { identities: [] });
    }
    getEndpoints() {
        return [['identities', ENDPOINT]];
    }
    getTitle() {
        return (0, locale_1.t)('Identities');
    }
    renderBody() {
        var _a;
        return (<div>
        <settingsPageHeader_1.default title="Identities"/>
        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Identities')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            {!((_a = this.state.identities) === null || _a === void 0 ? void 0 : _a.length) ? (<emptyMessage_1.default>
                {(0, locale_1.t)('There are no identities associated with this account')}
              </emptyMessage_1.default>) : (this.state.identities.map(identity => (<IdentityPanelItem key={identity.id}>
                  <div>{identity.providerLabel}</div>

                  <button_1.default size="small" onClick={this.handleDisconnect.bind(this, identity)}>
                    {(0, locale_1.t)('Disconnect')}
                  </button_1.default>
                </IdentityPanelItem>)))}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
const IdentityPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  align-items: center;
  justify-content: space-between;
`;
exports.default = AccountIdentities;
//# sourceMappingURL=accountIdentities.jsx.map