Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const BYE_URL = '/';
const leaveRedirect = () => (window.location.href = BYE_URL);
const Important = (0, styled_1.default)('div') `
  font-weight: bold;
  font-size: 1.2em;
`;
const GoodbyeModalContent = ({ Header, Body, Footer }) => (<div>
    <Header>{(0, locale_1.t)('Closing Account')}</Header>
    <Body>
      <textBlock_1.default>
        {(0, locale_1.t)('Your account has been deactivated and scheduled for removal.')}
      </textBlock_1.default>
      <textBlock_1.default>
        {(0, locale_1.t)('Thanks for using Sentry! We hope to see you again soon!')}
      </textBlock_1.default>
    </Body>
    <Footer>
      <button_1.default href={BYE_URL}>{(0, locale_1.t)('Goodbye')}</button_1.default>
    </Footer>
  </div>);
class AccountClose extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleChange = ({ slug }, isSingle, event) => {
            const checked = event.target.checked;
            // Can't unselect an org where you are the single owner
            if (isSingle) {
                return;
            }
            this.setState(state => {
                const set = state.orgsToRemove || new Set(this.singleOwnerOrgs);
                if (checked) {
                    set.add(slug);
                }
                else {
                    set.delete(slug);
                }
                return { orgsToRemove: set };
            });
        };
        this.handleRemoveAccount = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { orgsToRemove } = this.state;
            const orgs = orgsToRemove === null ? this.singleOwnerOrgs : Array.from(orgsToRemove);
            (0, indicator_1.addLoadingMessage)('Closing account\u2026');
            try {
                yield this.api.requestPromise('/users/me/', {
                    method: 'DELETE',
                    data: { organizations: orgs },
                });
                (0, modal_1.openModal)(GoodbyeModalContent, {
                    onClose: leaveRedirect,
                });
                // Redirect after 10 seconds
                setTimeout(leaveRedirect, 10000);
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)('Error closing account');
            }
        });
    }
    getEndpoints() {
        return [['organizations', '/organizations/?owner=1']];
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { orgsToRemove: null });
    }
    get singleOwnerOrgs() {
        var _a, _b;
        return (_b = (_a = this.state.organizations) === null || _a === void 0 ? void 0 : _a.filter(({ singleOwner }) => singleOwner)) === null || _b === void 0 ? void 0 : _b.map(({ organization }) => organization.slug);
    }
    renderBody() {
        const { organizations, orgsToRemove } = this.state;
        return (<div>
        <settingsPageHeader_1.default title="Close Account"/>

        <textBlock_1.default>
          {(0, locale_1.t)('This will permanently remove all associated data for your user')}.
        </textBlock_1.default>

        <alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          <Important>
            {(0, locale_1.t)('Closing your account is permanent and cannot be undone')}!
          </Important>
        </alert_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Remove the following organizations')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <panels_1.PanelAlert type="info">
              {(0, locale_1.t)('Ownership will remain with other organization owners if an organization is not deleted.')}
              <br />
              {(0, locale_1.tct)("Boxes which can't be unchecked mean that you are the only organization owner and the organization [strong:will be deleted].", { strong: <strong /> })}
            </panels_1.PanelAlert>

            {organizations === null || organizations === void 0 ? void 0 : organizations.map(({ organization, singleOwner }) => (<panels_1.PanelItem key={organization.slug}>
                <label>
                  <input style={{ marginRight: 6 }} type="checkbox" value={organization.slug} onChange={this.handleChange.bind(this, organization, singleOwner)} name="organizations" checked={orgsToRemove === null
                    ? singleOwner
                    : orgsToRemove.has(organization.slug)} disabled={singleOwner}/>
                  {organization.slug}
                </label>
              </panels_1.PanelItem>))}
          </panels_1.PanelBody>
        </panels_1.Panel>

        <confirm_1.default priority="danger" message={(0, locale_1.t)('This is permanent and cannot be undone, are you really sure you want to do this?')} onConfirm={this.handleRemoveAccount}>
          <button_1.default priority="danger">{(0, locale_1.t)('Close Account')}</button_1.default>
        </confirm_1.default>
      </div>);
    }
}
exports.default = AccountClose;
//# sourceMappingURL=accountClose.jsx.map