Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class OrganizationAccessRequests extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            accessRequestBusy: {},
        };
        this.handleApprove = (id, e) => {
            e.stopPropagation();
            this.handleAction({
                id,
                isApproved: true,
                successMessage: (0, locale_1.t)('Team request approved'),
                errorMessage: (0, locale_1.t)('Error approving team request'),
            });
        };
        this.handleDeny = (id, e) => {
            e.stopPropagation();
            this.handleAction({
                id,
                isApproved: false,
                successMessage: (0, locale_1.t)('Team request denied'),
                errorMessage: (0, locale_1.t)('Error denying team request'),
            });
        };
    }
    handleAction({ id, isApproved, successMessage, errorMessage }) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, orgId, onRemoveAccessRequest } = this.props;
            this.setState(state => ({
                accessRequestBusy: Object.assign(Object.assign({}, state.accessRequestBusy), { [id]: true }),
            }));
            try {
                yield api.requestPromise(`/organizations/${orgId}/access-requests/${id}/`, {
                    method: 'PUT',
                    data: { isApproved },
                });
                onRemoveAccessRequest(id, isApproved);
                (0, indicator_1.addSuccessMessage)(successMessage);
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)(errorMessage);
            }
            this.setState(state => ({
                accessRequestBusy: Object.assign(Object.assign({}, state.accessRequestBusy), { [id]: false }),
            }));
        });
    }
    render() {
        const { requestList } = this.props;
        const { accessRequestBusy } = this.state;
        if (!requestList || !requestList.length) {
            return null;
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Pending Team Requests')}</panels_1.PanelHeader>

        <panels_1.PanelBody>
          {requestList.map(({ id, member, team, requester }) => {
                const memberName = member.user &&
                    (member.user.name || member.user.email || member.user.username);
                const requesterName = requester && (requester.name || requester.email || requester.username);
                return (<StyledPanelItem key={id}>
                <div data-test-id="request-message">
                  {requesterName
                        ? (0, locale_1.tct)('[requesterName] requests to add [name] to the [team] team.', {
                            requesterName,
                            name: <strong>{memberName}</strong>,
                            team: <strong>#{team.slug}</strong>,
                        })
                        : (0, locale_1.tct)('[name] requests access to the [team] team.', {
                            name: <strong>{memberName}</strong>,
                            team: <strong>#{team.slug}</strong>,
                        })}
                </div>
                <div>
                  <StyledButton priority="primary" size="small" onClick={e => this.handleApprove(id, e)} busy={accessRequestBusy[id]}>
                    {(0, locale_1.t)('Approve')}
                  </StyledButton>
                  <button_1.default busy={accessRequestBusy[id]} onClick={e => this.handleDeny(id, e)} size="small">
                    {(0, locale_1.t)('Deny')}
                  </button_1.default>
                </div>
              </StyledPanelItem>);
            })}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  display: grid;
  grid-template-columns: auto max-content;
  grid-gap: ${(0, space_1.default)(2)};
  align-items: center;
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = (0, withApi_1.default)(OrganizationAccessRequests);
//# sourceMappingURL=organizationAccessRequests.jsx.map