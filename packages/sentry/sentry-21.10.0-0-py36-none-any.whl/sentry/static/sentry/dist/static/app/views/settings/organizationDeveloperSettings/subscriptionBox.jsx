Object.defineProperty(exports, "__esModule", { value: true });
exports.SubscriptionBox = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const constants_1 = require("app/views/settings/organizationDeveloperSettings/constants");
class SubscriptionBox extends React.Component {
    constructor() {
        super(...arguments);
        this.onChange = (evt) => {
            const checked = evt.target.checked;
            const { resource } = this.props;
            this.props.onChange(resource, checked);
        };
    }
    render() {
        const { resource, organization, webhookDisabled, checked } = this.props;
        const features = new Set(organization.features);
        let disabled = this.props.disabledFromPermissions || webhookDisabled;
        let message = `Must have at least 'Read' permissions enabled for ${resource}`;
        if (resource === 'error' && !features.has('integrations-event-hooks')) {
            disabled = true;
            message =
                'Your organization does not have access to the error subscription resource.';
        }
        if (webhookDisabled) {
            message = 'Cannot enable webhook subscription without specifying a webhook url';
        }
        return (<React.Fragment>
        <SubscriptionGridItemWrapper key={resource}>
          <tooltip_1.default disabled={!disabled} title={message}>
            <SubscriptionGridItem disabled={disabled}>
              <SubscriptionInfo>
                <SubscriptionTitle>{(0, locale_1.t)(`${resource}`)}</SubscriptionTitle>
                <SubscriptionDescription>
                  {(0, locale_1.t)(`${constants_1.DESCRIPTIONS[resource]}`)}
                </SubscriptionDescription>
              </SubscriptionInfo>
              <checkbox_1.default key={`${resource}${checked}`} disabled={disabled} id={resource} value={resource} checked={checked} onChange={this.onChange}/>
            </SubscriptionGridItem>
          </tooltip_1.default>
        </SubscriptionGridItemWrapper>
      </React.Fragment>);
    }
}
exports.SubscriptionBox = SubscriptionBox;
SubscriptionBox.defaultProps = {
    webhookDisabled: false,
};
exports.default = (0, withOrganization_1.default)(SubscriptionBox);
const SubscriptionInfo = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
`;
const SubscriptionGridItem = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background: ${p => p.theme.backgroundSecondary};
  opacity: ${({ disabled }) => (disabled ? 0.3 : 1)};
  border-radius: 3px;
  flex: 1;
  padding: 12px;
  height: 100%;
`;
const SubscriptionGridItemWrapper = (0, styled_1.default)('div') `
  padding: 12px;
  width: 33%;
`;
const SubscriptionDescription = (0, styled_1.default)('div') `
  font-size: 12px;
  line-height: 1;
  color: ${p => p.theme.gray300};
  white-space: nowrap;
`;
const SubscriptionTitle = (0, styled_1.default)('div') `
  font-size: 16px;
  line-height: 1;
  color: ${p => p.theme.textColor};
  white-space: nowrap;
  margin-bottom: 5px;
`;
//# sourceMappingURL=subscriptionBox.jsx.map