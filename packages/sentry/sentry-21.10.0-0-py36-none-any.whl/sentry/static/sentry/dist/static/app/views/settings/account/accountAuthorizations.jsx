Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
class AccountAuthorizations extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleRevoke = authorization => {
            const oldData = this.state.data;
            this.setState(state => ({
                data: state.data.filter(({ id }) => id !== authorization.id),
            }), () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                try {
                    yield this.api.requestPromise('/api-authorizations/', {
                        method: 'DELETE',
                        data: { authorization: authorization.id },
                    });
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Saved changes'));
                }
                catch (_err) {
                    this.setState({
                        data: oldData,
                    });
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to save changes, please try again'));
                }
            }));
        };
    }
    getEndpoints() {
        return [['data', '/api-authorizations/']];
    }
    getTitle() {
        return 'Approved Applications';
    }
    renderBody() {
        const { data } = this.state;
        const isEmpty = data.length === 0;
        return (<div>
        <settingsPageHeader_1.default title="Authorized Applications"/>
        <Description>
          {(0, locale_1.tct)('You can manage your own applications via the [link:API dashboard].', {
                link: <link_1.default to="/settings/account/api/"/>,
            })}
        </Description>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Approved Applications')}</panels_1.PanelHeader>

          <panels_1.PanelBody>
            {isEmpty && (<emptyMessage_1.default>
                {(0, locale_1.t)("You haven't approved any third party applications.")}
              </emptyMessage_1.default>)}

            {!isEmpty && (<div>
                {data.map(authorization => (<PanelItemCenter key={authorization.id}>
                    <ApplicationDetails>
                      <ApplicationName>{authorization.application.name}</ApplicationName>
                      {authorization.homepageUrl && (<Url>
                          <externalLink_1.default href={authorization.homepageUrl}>
                            {authorization.homepageUrl}
                          </externalLink_1.default>
                        </Url>)}
                      <Scopes>{authorization.scopes.join(', ')}</Scopes>
                    </ApplicationDetails>
                    <button_1.default size="small" onClick={() => this.handleRevoke(authorization)} icon={<icons_1.IconDelete />}/>
                  </PanelItemCenter>))}
              </div>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
exports.default = AccountAuthorizations;
const Description = (0, styled_1.default)('p') `
  font-size: ${p => p.theme.fontSizeRelativeSmall};
  margin-bottom: ${(0, space_1.default)(4)};
`;
const PanelItemCenter = (0, styled_1.default)(panels_1.PanelItem) `
  align-items: center;
`;
const ApplicationDetails = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  flex-direction: column;
`;
const ApplicationName = (0, styled_1.default)('div') `
  font-weight: bold;
  margin-bottom: ${(0, space_1.default)(0.5)};
`;
/**
 * Intentionally wrap <a> so that it does not take up full width and cause
 * hit box issues
 */
const Url = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(0.5)};
  font-size: ${p => p.theme.fontSizeRelativeSmall};
`;
const Scopes = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeRelativeSmall};
`;
//# sourceMappingURL=accountAuthorizations.jsx.map