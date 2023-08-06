Object.defineProperty(exports, "__esModule", { value: true });
exports.ApiTokens = void 0;
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const apiTokenRow_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/apiTokenRow"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
class ApiTokens extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleRemoveToken = (token) => {
            (0, indicator_1.addLoadingMessage)();
            const oldTokenList = this.state.tokenList;
            this.setState(state => {
                var _a, _b;
                return ({
                    tokenList: (_b = (_a = state.tokenList) === null || _a === void 0 ? void 0 : _a.filter(tk => tk.token !== token.token)) !== null && _b !== void 0 ? _b : [],
                });
            }, () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                try {
                    yield this.api.requestPromise('/api-tokens/', {
                        method: 'DELETE',
                        data: { token: token.token },
                    });
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Removed token'));
                }
                catch (_err) {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove token. Please try again.'));
                    this.setState({
                        tokenList: oldTokenList,
                    });
                }
            }));
        };
    }
    getTitle() {
        return (0, locale_1.t)('API Tokens');
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { tokenList: [] });
    }
    getEndpoints() {
        return [['tokenList', '/api-tokens/']];
    }
    renderBody() {
        var _a;
        const { organization } = this.props;
        const { tokenList } = this.state;
        const isEmpty = !Array.isArray(tokenList) || tokenList.length === 0;
        const action = (<button_1.default priority="primary" size="small" to="/settings/account/api/auth-tokens/new-token/" data-test-id="create-token">
        {(0, locale_1.t)('Create New Token')}
      </button_1.default>);
        return (<div>
        <settingsPageHeader_1.default title="Auth Tokens" action={action}/>
        <alertLink_1.default to={`/settings/${(_a = organization === null || organization === void 0 ? void 0 : organization.slug) !== null && _a !== void 0 ? _a : ''}/developer-settings/new-internal`}>
          {(0, locale_1.t)("Auth Tokens are tied to the logged in user, meaning they'll stop working if the user leaves the organization! We suggest using internal integrations to create/manage tokens tied to the organization instead.")}
        </alertLink_1.default>
        <textBlock_1.default>
          {(0, locale_1.t)("Authentication tokens allow you to perform actions against the Sentry API on behalf of your account. They're the easiest way to get started using the API.")}
        </textBlock_1.default>
        <textBlock_1.default>
          {(0, locale_1.tct)('For more information on how to use the web API, see our [link:documentation].', {
                link: <externalLink_1.default href="https://docs.sentry.io/api/"/>,
            })}
        </textBlock_1.default>
        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Auth Token')}</panels_1.PanelHeader>

          <panels_1.PanelBody>
            {isEmpty && (<emptyMessage_1.default>
                {(0, locale_1.t)("You haven't created any authentication tokens yet.")}
              </emptyMessage_1.default>)}

            {tokenList === null || tokenList === void 0 ? void 0 : tokenList.map(token => (<apiTokenRow_1.default key={token.token} token={token} onRemove={this.handleRemoveToken}/>))}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
exports.ApiTokens = ApiTokens;
exports.default = (0, withOrganization_1.default)(ApiTokens);
//# sourceMappingURL=apiTokens.jsx.map