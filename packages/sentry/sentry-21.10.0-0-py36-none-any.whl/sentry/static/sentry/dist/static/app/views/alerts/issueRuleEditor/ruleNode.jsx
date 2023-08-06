Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const platformCategories_1 = require("app/data/platformCategories");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const alerts_1 = require("app/types/alerts");
const memberTeamFields_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/issueRuleEditor/memberTeamFields"));
const sentryAppRuleModal_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/issueRuleEditor/sentryAppRuleModal"));
const ticketRuleModal_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/issueRuleEditor/ticketRuleModal"));
const issueAlertOptions_1 = require("app/views/projectInstall/issueAlertOptions");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
class RuleNode extends React.Component {
    constructor() {
        super(...arguments);
        this.handleDelete = () => {
            const { index, onDelete } = this.props;
            onDelete(index);
        };
        this.handleMemberTeamChange = (data) => {
            const { index, onPropertyChange } = this.props;
            onPropertyChange(index, 'targetType', `${data.targetType}`);
            onPropertyChange(index, 'targetIdentifier', `${data.targetIdentifier}`);
        };
        this.getChoiceField = (name, fieldConfig) => {
            const { data, disabled, index, onPropertyChange, onReset } = this.props;
            // Select the first item on this list
            // If it's not yet defined, call onPropertyChange to make sure the value is set on state
            let initialVal;
            if (data) {
                if (data[name] === undefined && !!fieldConfig.choices.length) {
                    initialVal = fieldConfig.initial
                        ? `${fieldConfig.initial}`
                        : `${fieldConfig.choices[0][0]}`;
                }
                else {
                    initialVal = `${data[name]}`;
                }
            }
            // All `value`s are cast to string
            // There are integrations that give the form field choices with the value as number, but
            // when the integration configuration gets saved, it gets saved and returned as a string
            const options = fieldConfig.choices.map(([value, label]) => ({
                value: `${value}`,
                label,
            }));
            const handleChange = ({ value }) => {
                if (fieldConfig.resetsForm) {
                    onReset(index, name, value);
                }
                else {
                    onPropertyChange(index, name, value);
                }
            };
            return (<InlineSelectControl isClearable={false} name={name} value={initialVal} styles={{
                    control: provided => (Object.assign(Object.assign({}, provided), { minHeight: '28px', height: '28px' })),
                }} disabled={disabled} options={options} onChange={handleChange}/>);
        };
        this.getTextField = (name, fieldConfig) => {
            var _a;
            const { data, index, onPropertyChange, disabled } = this.props;
            return (<InlineInput type="text" name={name} value={(_a = (data && data[name])) !== null && _a !== void 0 ? _a : ''} placeholder={`${fieldConfig.placeholder}`} disabled={disabled} onChange={(e) => onPropertyChange(index, name, e.target.value)}/>);
        };
        this.getNumberField = (name, fieldConfig) => {
            var _a;
            const { data, index, onPropertyChange, disabled } = this.props;
            return (<InlineNumberInput type="number" name={name} value={(_a = (data && data[name])) !== null && _a !== void 0 ? _a : ''} placeholder={`${fieldConfig.placeholder}`} disabled={disabled} onChange={(e) => onPropertyChange(index, name, e.target.value)}/>);
        };
        this.getMailActionFields = (_, __) => {
            const { data, organization, project, disabled } = this.props;
            const isInitialized = (data === null || data === void 0 ? void 0 : data.targetType) !== undefined && `${data.targetType}`.length > 0;
            return (<memberTeamFields_1.default disabled={disabled} project={project} organization={organization} loading={!isInitialized} ruleData={data} onChange={this.handleMemberTeamChange} options={[
                    { value: alerts_1.MailActionTargetType.IssueOwners, label: (0, locale_1.t)('Issue Owners') },
                    { value: alerts_1.MailActionTargetType.Team, label: (0, locale_1.t)('Team') },
                    { value: alerts_1.MailActionTargetType.Member, label: (0, locale_1.t)('Member') },
                ]} memberValue={alerts_1.MailActionTargetType.Member} teamValue={alerts_1.MailActionTargetType.Team}/>);
        };
        this.getAssigneeFilterFields = (_, __) => {
            const { data, organization, project, disabled } = this.props;
            const isInitialized = (data === null || data === void 0 ? void 0 : data.targetType) !== undefined && `${data.targetType}`.length > 0;
            return (<memberTeamFields_1.default disabled={disabled} project={project} organization={organization} loading={!isInitialized} ruleData={data} onChange={this.handleMemberTeamChange} options={[
                    { value: alerts_1.AssigneeTargetType.Unassigned, label: (0, locale_1.t)('No One') },
                    { value: alerts_1.AssigneeTargetType.Team, label: (0, locale_1.t)('Team') },
                    { value: alerts_1.AssigneeTargetType.Member, label: (0, locale_1.t)('Member') },
                ]} memberValue={alerts_1.AssigneeTargetType.Member} teamValue={alerts_1.AssigneeTargetType.Team}/>);
        };
        this.getField = (name, fieldConfig) => {
            const getFieldTypes = {
                choice: this.getChoiceField,
                number: this.getNumberField,
                string: this.getTextField,
                mailAction: this.getMailActionFields,
                assignee: this.getAssigneeFilterFields,
            };
            return getFieldTypes[fieldConfig.type](name, fieldConfig);
        };
        /**
         * Update all the AlertRuleAction's fields from the TicketRuleModal together
         * only after the user clicks "Apply Changes".
         * @param formData Form data
         * @param fetchedFieldOptionsCache Object
         */
        this.updateParentFromTicketRule = (formData, fetchedFieldOptionsCache) => {
            const { index, onPropertyChange } = this.props;
            // We only know the choices after the form loads.
            formData.dynamic_form_fields = (formData.dynamic_form_fields || []).map(field => {
                // Overwrite the choices because the user's pick is in this list.
                if (field.name in formData &&
                    (fetchedFieldOptionsCache === null || fetchedFieldOptionsCache === void 0 ? void 0 : fetchedFieldOptionsCache.hasOwnProperty(field.name))) {
                    field.choices = fetchedFieldOptionsCache[field.name];
                }
                return field;
            });
            for (const [name, value] of Object.entries(formData)) {
                onPropertyChange(index, name, value);
            }
        };
        /**
         * Update all the AlertRuleAction's fields from the SentryAppRuleModal together
         * only after the user clicks "Save Changes".
         * @param formData Form data
         */
        this.updateParentFromSentryAppRule = (formData) => {
            const { index, onPropertyChange } = this.props;
            for (const [name, value] of Object.entries(formData)) {
                onPropertyChange(index, name, value);
            }
        };
    }
    renderRow() {
        const { data, node } = this.props;
        if (!node) {
            return (<Separator>
          This node failed to render. It may have migrated to another section of the alert
          conditions
        </Separator>);
        }
        const { label, formFields } = node;
        const parts = label.split(/({\w+})/).map((part, i) => {
            if (!/^{\w+}$/.test(part)) {
                return <Separator key={i}>{part}</Separator>;
            }
            const key = part.slice(1, -1);
            // If matcher is "is set" or "is not set", then we do not want to show the value input
            // because it is not required
            if (key === 'value' && data && (data.match === 'is' || data.match === 'ns')) {
                return null;
            }
            return (<Separator key={key}>
          {formFields && formFields.hasOwnProperty(key)
                    ? this.getField(key, formFields[key])
                    : part}
        </Separator>);
        });
        const [title, ...inputs] = parts;
        // We return this so that it can be a grid
        return (<React.Fragment>
        {title}
        {inputs}
      </React.Fragment>);
    }
    conditionallyRenderHelpfulBanner() {
        const { data, project, organization } = this.props;
        if (data.id === issueAlertOptions_1.EVENT_FREQUENCY_PERCENT_CONDITION) {
            if (!project.platform || !platformCategories_1.releaseHealth.includes(project.platform)) {
                return (<MarginlessAlert type="error">
            {(0, locale_1.tct)("This project doesn't support sessions. [link:View supported platforms]", {
                        link: (<externalLink_1.default href="https://docs.sentry.io/product/releases/health/setup/"/>),
                    })}
          </MarginlessAlert>);
            }
            return (<MarginlessAlert type="warning">
          {(0, locale_1.tct)('Percent of sessions affected is approximated by the ratio of the issue frequency to the number of sessions in the project. [link:Learn more.]', {
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/alerts/create-alerts/issue-alert-config/"/>),
                })}
        </MarginlessAlert>);
        }
        if (data.id === 'sentry.integrations.slack.notify_action.SlackNotifyServiceAction') {
            return (<MarginlessAlert type="warning">
          {(0, locale_1.tct)('Having rate limiting problems? Enter a channel or user ID. Read more [rateLimiting].', {
                    rateLimiting: (<externalLink_1.default href="https://docs.sentry.io/product/integrations/notification-incidents/slack/#rate-limiting-error">
                  {(0, locale_1.t)('here')}
                </externalLink_1.default>),
                })}
        </MarginlessAlert>);
        }
        /**
         * Would prefer to check if data is of `IssueAlertRuleAction` type, however we can't do typechecking at runtime as
         * user defined types are erased through transpilation.
         * Instead, we apply duck typing semantics here.
         * See: https://stackoverflow.com/questions/51528780/typescript-check-typeof-against-custom-type
         */
        if (!(data === null || data === void 0 ? void 0 : data.targetType) || data.id !== 'sentry.mail.actions.NotifyEmailAction') {
            return null;
        }
        switch (data.targetType) {
            case alerts_1.MailActionTargetType.IssueOwners:
                return (<MarginlessAlert type="warning">
            {(0, locale_1.tct)('If there are no matching [issueOwners], ownership is determined by the [ownershipSettings].', {
                        issueOwners: (<externalLink_1.default href="https://docs.sentry.io/product/error-monitoring/issue-owners/">
                    {(0, locale_1.t)('issue owners')}
                  </externalLink_1.default>),
                        ownershipSettings: (<externalLink_1.default href={`/settings/${organization.slug}/projects/${project.slug}/ownership/`}>
                    {(0, locale_1.t)('ownership settings')}
                  </externalLink_1.default>),
                    })}
          </MarginlessAlert>);
            case alerts_1.MailActionTargetType.Team:
                return null;
            case alerts_1.MailActionTargetType.Member:
                return null;
            default:
                return null;
        }
    }
    isSchemaConfig(formFields) {
        return !formFields ? false : formFields.uri !== undefined;
    }
    render() {
        const { data, disabled, index, node, organization } = this.props;
        const { actionType, id, sentryAppInstallationUuid } = node || {};
        const ticketRule = actionType === 'ticket';
        const sentryAppRule = actionType === 'sentryapp' && sentryAppInstallationUuid;
        const isNew = id === issueAlertOptions_1.EVENT_FREQUENCY_PERCENT_CONDITION;
        return (<RuleRowContainer>
        <RuleRow>
          <Rule>
            {isNew && <StyledFeatureBadge type="new"/>}
            {data && <input type="hidden" name="id" value={data.id}/>}
            {this.renderRow()}
            {ticketRule && node && (<button_1.default size="small" icon={<icons_1.IconSettings size="xs"/>} type="button" onClick={() => (0, modal_1.openModal)(deps => (<ticketRuleModal_1.default {...deps} formFields={node.formFields || {}} link={node.link} ticketType={node.ticketType} instance={data} index={index} onSubmitAction={this.updateParentFromTicketRule} organization={organization}/>))}>
                {(0, locale_1.t)('Issue Link Settings')}
              </button_1.default>)}
            {sentryAppRule && node && (<button_1.default size="small" icon={<icons_1.IconSettings size="xs"/>} type="button" onClick={() => {
                    (0, modal_1.openModal)(deps => (<sentryAppRuleModal_1.default {...deps} sentryAppInstallationUuid={sentryAppInstallationUuid} config={node.formFields} appName={node.prompt} onSubmitSuccess={this.updateParentFromSentryAppRule} resetValues={data}/>), { allowClickClose: false });
                }}>
                {(0, locale_1.t)('Settings')}
              </button_1.default>)}
          </Rule>
          <DeleteButton disabled={disabled} label={(0, locale_1.t)('Delete Node')} onClick={this.handleDelete} type="button" size="small" icon={<icons_1.IconDelete />}/>
        </RuleRow>
        {this.conditionallyRenderHelpfulBanner()}
      </RuleRowContainer>);
    }
}
exports.default = RuleNode;
const InlineInput = (0, styled_1.default)(input_1.default) `
  width: auto;
  height: 28px;
`;
const InlineNumberInput = (0, styled_1.default)(input_1.default) `
  width: 90px;
  height: 28px;
`;
const InlineSelectControl = (0, styled_1.default)(selectControl_1.default) `
  width: 180px;
`;
const Separator = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(1)};
  padding-top: ${(0, space_1.default)(0.5)};
  padding-bottom: ${(0, space_1.default)(0.5)};
`;
const RuleRow = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(1)};
`;
const RuleRowContainer = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.backgroundSecondary};
  border-radius: ${p => p.theme.borderRadius};
  border: 1px ${p => p.theme.innerBorder} solid;
`;
const Rule = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  flex: 1;
  flex-wrap: wrap;
`;
const DeleteButton = (0, styled_1.default)(button_1.default) `
  flex-shrink: 0;
`;
const MarginlessAlert = (0, styled_1.default)(alert_1.default) `
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  border-width: 0;
  border-top: 1px ${p => p.theme.innerBorder} solid;
  margin: 0;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeSmall};
`;
const StyledFeatureBadge = (0, styled_1.default)(featureBadge_1.default) `
  margin: 0 ${(0, space_1.default)(1)} 0 0;
`;
//# sourceMappingURL=ruleNode.jsx.map