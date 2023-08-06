Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class CreateTeamAccessRequest extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            createBusy: false,
        };
        this.handleClick = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, memberId, orgId, teamId, closeModal } = this.props;
            this.setState({ createBusy: true });
            try {
                yield api.requestPromise(`/organizations/${orgId}/members/${memberId}/teams/${teamId}/`, {
                    method: 'POST',
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Team request sent for approval'));
            }
            catch (err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to send team request'));
            }
            this.setState({ createBusy: false });
            closeModal();
        });
    }
    render() {
        const { Body, Footer, closeModal, teamId } = this.props;
        return (<react_1.Fragment>
        <Body>
          {(0, locale_1.tct)('You do not have permission to add members to the #[team] team, but we will send a request to your organization admins for approval.', { team: teamId })}
        </Body>
        <Footer>
          <ButtonGroup>
            <button_1.default onClick={closeModal}>{(0, locale_1.t)('Cancel')}</button_1.default>
            <button_1.default priority="primary" onClick={this.handleClick} busy={this.state.createBusy} autoFocus>
              {(0, locale_1.t)('Continue')}
            </button_1.default>
          </ButtonGroup>
        </Footer>
      </react_1.Fragment>);
    }
}
const ButtonGroup = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content max-content;
  grid-gap: ${(0, space_1.default)(1)};
`;
exports.default = (0, withApi_1.default)(CreateTeamAccessRequest);
//# sourceMappingURL=teamAccessRequestModal.jsx.map