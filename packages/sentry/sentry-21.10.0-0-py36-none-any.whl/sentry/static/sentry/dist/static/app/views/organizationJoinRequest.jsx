Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const narrowLayout_1 = (0, tslib_1.__importDefault)(require("app/components/narrowLayout"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const emailField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/emailField"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
class OrganizationJoinRequest extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            submitSuccess: null,
        };
        this.handleSubmitSuccess = () => {
            this.setState({ submitSuccess: true });
        };
        this.handleCancel = e => {
            e.preventDefault();
            const { orgId } = this.props.params;
            window.location.assign(`/auth/login/${orgId}/`);
        };
    }
    componentDidMount() {
        const { orgId } = this.props.params;
        (0, analytics_1.trackAdhocEvent)({
            eventKey: 'join_request.viewed',
            org_slug: orgId,
        });
    }
    handleSubmitError() {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Request to join failed'));
    }
    render() {
        const { orgId } = this.props.params;
        const { submitSuccess } = this.state;
        if (submitSuccess) {
            return (<narrowLayout_1.default maxWidth="550px">
          <SuccessModal>
            <StyledIconMegaphone size="5em"/>
            <StyledHeader>{(0, locale_1.t)('Request Sent')}</StyledHeader>
            <StyledText>{(0, locale_1.t)('Your request to join has been sent.')}</StyledText>
            <ReceiveEmailMessage>
              {(0, locale_1.tct)('You will receive an email when your request is approved.', { orgId })}
            </ReceiveEmailMessage>
          </SuccessModal>
        </narrowLayout_1.default>);
        }
        return (<narrowLayout_1.default maxWidth="650px">
        <StyledIconMegaphone size="5em"/>
        <StyledHeader>{(0, locale_1.t)('Request to Join')}</StyledHeader>
        <StyledText>
          {(0, locale_1.tct)('Ask the admins if you can join the [orgId] organization.', {
                orgId,
            })}
        </StyledText>
        <form_1.default requireChanges apiEndpoint={`/organizations/${orgId}/join-request/`} apiMethod="POST" submitLabel={(0, locale_1.t)('Request to Join')} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onCancel={this.handleCancel}>
          <StyledEmailField name="email" inline={false} label={(0, locale_1.t)('Email Address')} placeholder="name@example.com"/>
        </form_1.default>
      </narrowLayout_1.default>);
    }
}
const SuccessModal = (0, styled_1.default)('div') `
  display: grid;
  justify-items: center;
  text-align: center;
  padding-top: 10px;
  padding-bottom: ${(0, space_1.default)(4)};
`;
const StyledIconMegaphone = (0, styled_1.default)(icons_1.IconMegaphone) `
  padding-bottom: ${(0, space_1.default)(3)};
`;
const StyledHeader = (0, styled_1.default)('h3') `
  margin-bottom: ${(0, space_1.default)(1)};
`;
const StyledText = (0, styled_1.default)('p') `
  margin-bottom: 0;
`;
const ReceiveEmailMessage = (0, styled_1.default)(StyledText) `
  max-width: 250px;
`;
const StyledEmailField = (0, styled_1.default)(emailField_1.default) `
  padding-top: ${(0, space_1.default)(2)};
  padding-left: 0;
`;
exports.default = OrganizationJoinRequest;
//# sourceMappingURL=organizationJoinRequest.jsx.map