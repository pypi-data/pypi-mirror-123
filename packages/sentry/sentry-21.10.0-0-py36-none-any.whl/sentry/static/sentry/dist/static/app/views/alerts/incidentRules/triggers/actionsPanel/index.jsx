Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const guid_1 = require("app/utils/guid");
const removeAtArrayIndex_1 = require("app/utils/removeAtArrayIndex");
const replaceAtArrayIndex_1 = require("app/utils/replaceAtArrayIndex");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const actionSpecificTargetSelector_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/triggers/actionsPanel/actionSpecificTargetSelector"));
const actionTargetSelector_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/triggers/actionsPanel/actionTargetSelector"));
const deleteActionButton_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/triggers/actionsPanel/deleteActionButton"));
const types_1 = require("app/views/alerts/incidentRules/types");
const sentryAppRuleModal_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/issueRuleEditor/sentryAppRuleModal"));
/**
 * When a new action is added, all of it's settings should be set to their default values.
 * @param actionConfig
 * @param dateCreated kept to maintain order of unsaved actions
 */
const getCleanAction = (actionConfig, dateCreated) => {
    return {
        unsavedId: (0, guid_1.uniqueId)(),
        unsavedDateCreated: dateCreated !== null && dateCreated !== void 0 ? dateCreated : new Date().toISOString(),
        type: actionConfig.type,
        targetType: actionConfig &&
            actionConfig.allowedTargetTypes &&
            actionConfig.allowedTargetTypes.length > 0
            ? actionConfig.allowedTargetTypes[0]
            : null,
        targetIdentifier: actionConfig.sentryAppId || '',
        inputChannelId: null,
        integrationId: actionConfig.integrationId,
        sentryAppId: actionConfig.sentryAppId,
        options: actionConfig.options || null,
    };
};
/**
 * Actions have a type (e.g. email, slack, etc), but only some have
 * an integrationId (e.g. email is null). This helper creates a unique
 * id based on the type and integrationId so that we know what action
 * a user's saved action corresponds to.
 */
const getActionUniqueKey = ({ type, integrationId, sentryAppId, }) => {
    if (integrationId) {
        return `${type}-${integrationId}`;
    }
    else if (sentryAppId) {
        return `${type}-${sentryAppId}`;
    }
    return type;
};
/**
 * Creates a human-friendly display name for the integration based on type and
 * server provided `integrationName`
 *
 * e.g. for slack we show that it is slack and the `integrationName` is the workspace name
 */
const getFullActionTitle = ({ type, integrationName, sentryAppName, status, }) => {
    if (sentryAppName) {
        if (status) {
            return `${sentryAppName} (${status})`;
        }
        return `${sentryAppName}`;
    }
    const label = types_1.ActionLabel[type];
    if (integrationName) {
        return `${label} - ${integrationName}`;
    }
    return label;
};
/**
 * Lists saved actions as well as control to add a new action
 */
class ActionsPanel extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.handleAddAction = () => {
            const { availableActions, onAdd } = this.props;
            const actionConfig = availableActions === null || availableActions === void 0 ? void 0 : availableActions[0];
            if (!actionConfig) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('There was a problem adding an action'));
                Sentry.captureException(new Error('Unable to add an action'));
                return;
            }
            const action = getCleanAction(actionConfig);
            // Add new actions to critical by default
            const triggerIndex = 0;
            onAdd(triggerIndex, action);
        };
        this.handleDeleteAction = (triggerIndex, index) => {
            const { triggers, onChange } = this.props;
            const { actions } = triggers[triggerIndex];
            onChange(triggerIndex, triggers, (0, removeAtArrayIndex_1.removeAtArrayIndex)(actions, index));
        };
        this.handleChangeActionLevel = (triggerIndex, index, value) => {
            const { triggers, onChange } = this.props;
            // Convert saved action to unsaved by removing id
            const _a = triggers[triggerIndex].actions[index], { id: _ } = _a, action = (0, tslib_1.__rest)(_a, ["id"]);
            action.unsavedId = (0, guid_1.uniqueId)();
            triggers[value.value].actions.push(action);
            onChange(value.value, triggers, triggers[value.value].actions);
            this.handleDeleteAction(triggerIndex, index);
        };
        this.handleChangeActionType = (triggerIndex, index, value) => {
            var _a;
            const { triggers, onChange, availableActions } = this.props;
            const { actions } = triggers[triggerIndex];
            const actionConfig = availableActions === null || availableActions === void 0 ? void 0 : availableActions.find(availableAction => getActionUniqueKey(availableAction) === value.value);
            if (!actionConfig) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('There was a problem changing an action'));
                Sentry.captureException(new Error('Unable to change an action type'));
                return;
            }
            const existingDateCreated = (_a = actions[index].dateCreated) !== null && _a !== void 0 ? _a : actions[index].unsavedDateCreated;
            const newAction = getCleanAction(actionConfig, existingDateCreated);
            onChange(triggerIndex, triggers, (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(actions, index, newAction));
        };
        this.handleChangeTarget = (triggerIndex, index, value) => {
            const { triggers, onChange } = this.props;
            const { actions } = triggers[triggerIndex];
            const newAction = Object.assign(Object.assign({}, actions[index]), { targetType: value.value, targetIdentifier: '' });
            onChange(triggerIndex, triggers, (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(actions, index, newAction));
        };
        /**
         * Update the Trigger's Action fields from the SentryAppRuleModal together
         * only after the user clicks "Save Changes".
         * @param formData Form data
         */
        this.updateParentFromSentryAppRule = (triggerIndex, actionIndex, formData) => {
            const { triggers, onChange } = this.props;
            const { actions } = triggers[triggerIndex];
            const newAction = Object.assign(Object.assign({}, actions[actionIndex]), formData);
            onChange(triggerIndex, triggers, (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(actions, actionIndex, newAction));
        };
    }
    handleChangeKey(triggerIndex, index, key, value) {
        const { triggers, onChange } = this.props;
        const { actions } = triggers[triggerIndex];
        const newAction = Object.assign(Object.assign({}, actions[index]), { [key]: value });
        onChange(triggerIndex, triggers, (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(actions, index, newAction));
    }
    render() {
        const { availableActions, currentProject, disabled, loading, organization, projects, triggers, } = this.props;
        const project = projects.find(({ slug }) => slug === currentProject);
        const items = availableActions === null || availableActions === void 0 ? void 0 : availableActions.map(availableAction => ({
            value: getActionUniqueKey(availableAction),
            label: getFullActionTitle(availableAction),
        }));
        const levels = [
            { value: 0, label: 'Critical Status' },
            { value: 1, label: 'Warning Status' },
        ];
        // Create single array of unsaved and saved trigger actions
        // Sorted by date created ascending
        const actions = triggers
            .flatMap((trigger, triggerIndex) => {
            return trigger.actions.map((action, actionIdx) => {
                var _a;
                const availableAction = availableActions === null || availableActions === void 0 ? void 0 : availableActions.find(a => getActionUniqueKey(a) === getActionUniqueKey(action));
                return {
                    dateCreated: new Date((_a = action.dateCreated) !== null && _a !== void 0 ? _a : action.unsavedDateCreated).getTime(),
                    triggerIndex,
                    action,
                    actionIdx,
                    availableAction,
                };
            });
        })
            .sort((a, b) => a.dateCreated - b.dateCreated);
        return (<react_1.Fragment>
        <PerformActionsListItem>
          {(0, locale_1.t)('Perform actions')}
          <AlertParagraph>
            {(0, locale_1.t)('When any of the thresholds above are met, perform an action such as sending an email or using an integration.')}
          </AlertParagraph>
        </PerformActionsListItem>
        {loading && <loadingIndicator_1.default />}
        {actions.map(({ action, actionIdx, triggerIndex, availableAction }) => {
                var _a, _b;
                return (<div key={(_a = action.id) !== null && _a !== void 0 ? _a : action.unsavedId}>
              <RuleRowContainer>
                <PanelItemGrid>
                  <PanelItemSelects>
                    <selectControl_1.default name="select-level" aria-label={(0, locale_1.t)('Select a status level')} isDisabled={disabled || loading} placeholder={(0, locale_1.t)('Select Level')} onChange={this.handleChangeActionLevel.bind(this, triggerIndex, actionIdx)} value={triggerIndex} options={levels}/>
                    <selectControl_1.default name="select-action" aria-label={(0, locale_1.t)('Select an Action')} isDisabled={disabled || loading} placeholder={(0, locale_1.t)('Select Action')} onChange={this.handleChangeActionType.bind(this, triggerIndex, actionIdx)} value={getActionUniqueKey(action)} options={items !== null && items !== void 0 ? items : []}/>

                    {availableAction && availableAction.allowedTargetTypes.length > 1 ? (<selectControl_1.default isDisabled={disabled || loading} value={action.targetType} options={(_b = availableAction === null || availableAction === void 0 ? void 0 : availableAction.allowedTargetTypes) === null || _b === void 0 ? void 0 : _b.map(allowedType => ({
                            value: allowedType,
                            label: types_1.TargetLabel[allowedType],
                        }))} onChange={this.handleChangeTarget.bind(this, triggerIndex, actionIdx)}/>) : availableAction &&
                        availableAction.type === 'sentry_app' &&
                        availableAction.settings ? (<button_1.default icon={<icons_1.IconSettings />} type="button" onClick={() => {
                            (0, modal_1.openModal)(deps => (<sentryAppRuleModal_1.default {...deps} 
                            // Using ! for keys that will exist for sentryapps
                            sentryAppInstallationUuid={availableAction.sentryAppInstallationUuid} config={availableAction.settings} appName={availableAction.sentryAppName} onSubmitSuccess={this.updateParentFromSentryAppRule.bind(this, triggerIndex, actionIdx)} resetValues={triggers[triggerIndex].actions[actionIdx] || {}}/>), { allowClickClose: false });
                        }}>
                        {(0, locale_1.t)('Settings')}
                      </button_1.default>) : null}
                    <actionTargetSelector_1.default action={action} availableAction={availableAction} disabled={disabled} loading={loading} onChange={this.handleChangeKey.bind(this, triggerIndex, actionIdx, 'targetIdentifier')} organization={organization} project={project}/>
                    <actionSpecificTargetSelector_1.default action={action} disabled={disabled} onChange={this.handleChangeKey.bind(this, triggerIndex, actionIdx, 'inputChannelId')}/>
                  </PanelItemSelects>
                  <deleteActionButton_1.default triggerIndex={triggerIndex} index={actionIdx} onClick={this.handleDeleteAction} disabled={disabled}/>
                </PanelItemGrid>
              </RuleRowContainer>
            </div>);
            })}
        <ActionSection>
          <button_1.default type="button" disabled={disabled || loading} icon={<icons_1.IconAdd isCircled color="gray300"/>} onClick={this.handleAddAction}>
            {(0, locale_1.t)('Add Action')}
          </button_1.default>
        </ActionSection>
      </react_1.Fragment>);
    }
}
const ActionsPanelWithSpace = (0, styled_1.default)(ActionsPanel) `
  margin-top: ${(0, space_1.default)(4)};
`;
const ActionSection = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(1)};
  margin-bottom: ${(0, space_1.default)(3)};
`;
const AlertParagraph = (0, styled_1.default)('p') `
  color: ${p => p.theme.subText};
  margin-bottom: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeLarge};
`;
const PanelItemGrid = (0, styled_1.default)(panels_1.PanelItem) `
  display: flex;
  align-items: center;
  border-bottom: 0;
  padding: ${(0, space_1.default)(1)};
`;
const PanelItemSelects = (0, styled_1.default)('div') `
  display: flex;
  width: 100%;
  margin-right: ${(0, space_1.default)(1)};
  > * {
    flex: 0 1 200px;

    &:not(:last-child) {
      margin-right: ${(0, space_1.default)(1)};
    }
  }
`;
const RuleRowContainer = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.backgroundSecondary};
  border-radius: ${p => p.theme.borderRadius};
  border: 1px ${p => p.theme.border} solid;
`;
const StyledListItem = (0, styled_1.default)(listItem_1.default) `
  margin: ${(0, space_1.default)(2)} 0 ${(0, space_1.default)(3)} 0;
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
const PerformActionsListItem = (0, styled_1.default)(StyledListItem) `
  margin-bottom: 0;
  line-height: 1.3;
`;
exports.default = (0, withOrganization_1.default)(ActionsPanelWithSpace);
//# sourceMappingURL=index.jsx.map