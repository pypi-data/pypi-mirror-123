Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const tags_1 = require("app/actionCreators/tags");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const locale_1 = require("app/locale");
const indicatorStore_1 = (0, tslib_1.__importDefault)(require("app/stores/indicatorStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
const ruleNameOwnerForm_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/ruleNameOwnerForm"));
const triggers_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/triggers"));
const chart_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/triggers/chart"));
const getEventTypeFilter_1 = require("app/views/alerts/incidentRules/utils/getEventTypeFilter");
const hasThresholdValue_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/utils/hasThresholdValue"));
const options_1 = require("app/views/alerts/wizard/options");
const utils_2 = require("app/views/alerts/wizard/utils");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const actions_1 = require("../actions");
const constants_1 = require("../constants");
const ruleConditionsForm_1 = (0, tslib_1.__importDefault)(require("../ruleConditionsForm"));
const types_1 = require("../types");
const POLLING_MAX_TIME_LIMIT = 3 * 60000;
const isEmpty = (str) => str === '' || !(0, utils_1.defined)(str);
class RuleFormContainer extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.resetPollingState = (loadingSlackIndicator) => {
            indicatorStore_1.default.remove(loadingSlackIndicator);
            this.setState({ loading: false, uuid: undefined });
        };
        this.pollHandler = (model, quitTime, loadingSlackIndicator) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (Date.now() > quitTime) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Looking for that channel took too long :('));
                this.resetPollingState(loadingSlackIndicator);
                return;
            }
            const { organization, project, onSubmitSuccess, params: { ruleId }, } = this.props;
            const { uuid } = this.state;
            try {
                const response = yield this.api.requestPromise(`/projects/${organization.slug}/${project.slug}/alert-rule-task/${uuid}/`);
                const { status, alertRule, error } = response;
                if (status === 'pending') {
                    setTimeout(() => {
                        this.pollHandler(model, quitTime, loadingSlackIndicator);
                    }, 1000);
                    return;
                }
                this.resetPollingState(loadingSlackIndicator);
                if (status === 'failed') {
                    this.handleRuleSaveFailure(error);
                }
                if (alertRule) {
                    (0, indicator_1.addSuccessMessage)(ruleId ? (0, locale_1.t)('Updated alert rule') : (0, locale_1.t)('Created alert rule'));
                    if (onSubmitSuccess) {
                        onSubmitSuccess(alertRule, model);
                    }
                }
            }
            catch (_a) {
                this.handleRuleSaveFailure((0, locale_1.t)('An error occurred'));
                this.resetPollingState(loadingSlackIndicator);
            }
        });
        /**
         * Checks to see if threshold is valid given target value, and state of
         * inverted threshold as well as the *other* threshold
         *
         * @param type The threshold type to be updated
         * @param value The new threshold value
         */
        this.isValidTrigger = (triggerIndex, trigger, errors, resolveThreshold) => {
            const { alertThreshold } = trigger;
            const { thresholdType } = this.state;
            // If value and/or other value is empty
            // then there are no checks to perform against
            if (!(0, hasThresholdValue_1.default)(alertThreshold) || !(0, hasThresholdValue_1.default)(resolveThreshold)) {
                return true;
            }
            // If this is alert threshold and not inverted, it can't be below resolve
            // If this is alert threshold and inverted, it can't be above resolve
            // If this is resolve threshold and not inverted, it can't be above resolve
            // If this is resolve threshold and inverted, it can't be below resolve
            // Since we're comparing non-inclusive thresholds here (>, <), we need
            // to modify the values when we compare. An example of why:
            // Alert > 0, resolve < 1. This means that we want to alert on values
            // of 1 or more, and resolve on values of 0 or less. This is valid, but
            // without modifying the values, this boundary case will fail.
            const isValid = thresholdType === types_1.AlertRuleThresholdType.BELOW
                ? alertThreshold - 1 <= resolveThreshold + 1
                : alertThreshold + 1 >= resolveThreshold - 1;
            const otherErrors = errors.get(triggerIndex) || {};
            if (isValid) {
                return true;
            }
            // Not valid... let's figure out an error message
            const isBelow = thresholdType === types_1.AlertRuleThresholdType.BELOW;
            let errorMessage = '';
            if (typeof resolveThreshold !== 'number') {
                errorMessage = isBelow
                    ? (0, locale_1.t)('Resolution threshold must be greater than alert')
                    : (0, locale_1.t)('Resolution threshold must be less than alert');
            }
            else {
                errorMessage = isBelow
                    ? (0, locale_1.t)('Alert threshold must be less than resolution')
                    : (0, locale_1.t)('Alert threshold must be greater than resolution');
            }
            errors.set(triggerIndex, Object.assign(Object.assign({}, otherErrors), { alertThreshold: errorMessage }));
            return false;
        };
        this.handleFieldChange = (name, value) => {
            if (['dataset', 'eventTypes', 'timeWindow', 'environment', 'aggregate'].includes(name)) {
                this.setState({ [name]: value });
            }
        };
        // We handle the filter update outside of the fieldChange handler since we
        // don't want to update the filter on every input change, just on blurs and
        // searches.
        this.handleFilterUpdate = (query) => {
            const { organization, sessionId } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'alert_builder.filter',
                eventName: 'Alert Builder: Filter',
                query,
                organization_id: organization.id,
                session_id: sessionId,
            });
            this.setState({ query });
        };
        this.handleSubmit = (_data, _onSubmitSuccess, _onSubmitError, _e, model) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _b;
            // This validates all fields *except* for Triggers
            const validRule = model.validateForm();
            // Validate Triggers
            const triggerErrors = this.validateTriggers();
            const validTriggers = Array.from(triggerErrors).length === 0;
            if (!validTriggers) {
                this.setState(state => ({
                    triggerErrors: new Map([...triggerErrors, ...state.triggerErrors]),
                }));
            }
            if (!validRule || !validTriggers) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Alert not valid'));
                return;
            }
            const { organization, params, rule, onSubmitSuccess, location, sessionId } = this.props;
            const { ruleId } = this.props.params;
            const { resolveThreshold, triggers, thresholdType, comparisonDelta, uuid } = this.state;
            // Remove empty warning trigger
            const sanitizedTriggers = triggers.filter(trigger => trigger.label !== 'warning' || !isEmpty(trigger.alertThreshold));
            // form model has all form state data, however we use local state to keep
            // track of the list of triggers (and actions within triggers)
            const loadingIndicator = indicatorStore_1.default.addMessage((0, locale_1.t)('Saving your alert rule, hold on...'), 'loading');
            try {
                const transaction = analytics_1.metric.startTransaction({ name: 'saveAlertRule' });
                transaction.setTag('type', 'metric');
                transaction.setTag('operation', !rule.id ? 'create' : 'edit');
                for (const trigger of sanitizedTriggers) {
                    for (const action of trigger.actions) {
                        if (action.type === 'slack') {
                            transaction.setTag(action.type, true);
                        }
                    }
                }
                transaction.setData('actions', sanitizedTriggers);
                this.setState({ loading: true });
                const [data, , resp] = yield (0, actions_1.addOrUpdateRule)(this.api, organization.slug, params.projectId, Object.assign(Object.assign(Object.assign({}, rule), model.getTransformedData()), { triggers: sanitizedTriggers, resolveThreshold: isEmpty(resolveThreshold) ? null : resolveThreshold, thresholdType,
                    comparisonDelta }), {
                    referrer: (_b = location === null || location === void 0 ? void 0 : location.query) === null || _b === void 0 ? void 0 : _b.referrer,
                    sessionId,
                });
                // if we get a 202 back it means that we have an async task
                // running to lookup and verify the channel id for Slack.
                if ((resp === null || resp === void 0 ? void 0 : resp.status) === 202) {
                    // if we have a uuid in state, no need to start a new polling cycle
                    if (!uuid) {
                        this.setState({ loading: true, uuid: data.uuid });
                        this.fetchStatus(model);
                    }
                }
                else {
                    indicatorStore_1.default.remove(loadingIndicator);
                    this.setState({ loading: false });
                    (0, indicator_1.addSuccessMessage)(ruleId ? (0, locale_1.t)('Updated alert rule') : (0, locale_1.t)('Created alert rule'));
                    if (onSubmitSuccess) {
                        onSubmitSuccess(data, model);
                    }
                }
            }
            catch (err) {
                indicatorStore_1.default.remove(loadingIndicator);
                this.setState({ loading: false });
                const errors = (err === null || err === void 0 ? void 0 : err.responseJSON)
                    ? Array.isArray(err === null || err === void 0 ? void 0 : err.responseJSON)
                        ? err === null || err === void 0 ? void 0 : err.responseJSON
                        : Object.values(err === null || err === void 0 ? void 0 : err.responseJSON)
                    : [];
                const apiErrors = errors.length > 0 ? `: ${errors.join(', ')}` : '';
                this.handleRuleSaveFailure((0, locale_1.t)('Unable to save alert%s', apiErrors));
            }
        });
        /**
         * Callback for when triggers change
         *
         * Re-validate triggers on every change and reset indicators when no errors
         */
        this.handleChangeTriggers = (triggers, triggerIndex) => {
            this.setState(state => {
                let triggerErrors = state.triggerErrors;
                const newTriggerErrors = this.validateTriggers(triggers, state.thresholdType, state.resolveThreshold, triggerIndex);
                triggerErrors = newTriggerErrors;
                if (Array.from(newTriggerErrors).length === 0) {
                    (0, indicator_1.clearIndicators)();
                }
                return { triggers, triggerErrors };
            });
        };
        this.handleThresholdTypeChange = (thresholdType) => {
            const { triggers } = this.state;
            const triggerErrors = this.validateTriggers(triggers, thresholdType);
            this.setState(state => ({
                thresholdType,
                triggerErrors: new Map([...triggerErrors, ...state.triggerErrors]),
            }));
        };
        this.handleResolveThresholdChange = (resolveThreshold) => {
            this.setState(state => {
                const triggerErrors = this.validateTriggers(state.triggers, state.thresholdType, resolveThreshold);
                if (Array.from(triggerErrors).length === 0) {
                    (0, indicator_1.clearIndicators)();
                }
                return { resolveThreshold, triggerErrors };
            });
        };
        this.handleComparisonTypeChange = (value) => {
            const comparisonDelta = value === types_1.AlertRuleComparisonType.COUNT ? undefined : this.state.comparisonDelta;
            this.setState({ comparisonType: value, comparisonDelta });
        };
        this.handleComparisonDeltaChange = (value) => {
            this.setState({ comparisonDelta: value });
        };
        this.handleDeleteRule = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params } = this.props;
            const { orgId, projectId, ruleId } = params;
            try {
                yield this.api.requestPromise(`/projects/${orgId}/${projectId}/alert-rules/${ruleId}/`, {
                    method: 'DELETE',
                });
                this.goBack();
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error deleting rule'));
            }
        });
        this.handleRuleSaveFailure = (msg) => {
            (0, indicator_1.addErrorMessage)(msg);
            analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
        };
        this.handleCancel = () => {
            this.goBack();
        };
    }
    componentDidMount() {
        const { organization, project } = this.props;
        // SearchBar gets its tags from Reflux.
        (0, tags_1.fetchOrganizationTags)(this.api, organization.slug, [project.id]);
    }
    getDefaultState() {
        var _a;
        const { rule } = this.props;
        const triggersClone = [...rule.triggers];
        // Warning trigger is removed if it is blank when saving
        if (triggersClone.length !== 2) {
            triggersClone.push((0, constants_1.createDefaultTrigger)('warning'));
        }
        return Object.assign(Object.assign({}, super.getDefaultState()), { dataset: rule.dataset, eventTypes: rule.eventTypes, aggregate: rule.aggregate, query: rule.query || '', timeWindow: rule.timeWindow, environment: rule.environment || null, triggerErrors: new Map(), availableActions: null, triggers: triggersClone, resolveThreshold: rule.resolveThreshold, thresholdType: rule.thresholdType, comparisonDelta: (_a = rule.comparisonDelta) !== null && _a !== void 0 ? _a : undefined, comparisonType: !rule.comparisonDelta
                ? types_1.AlertRuleComparisonType.COUNT
                : types_1.AlertRuleComparisonType.CHANGE, projects: [this.props.project], owner: rule.owner });
    }
    getEndpoints() {
        const { orgId } = this.props.params;
        // TODO(incidents): This is temporary until new API endpoints
        // We should be able to just fetch the rule if rule.id exists
        return [
            ['availableActions', `/organizations/${orgId}/alert-rules/available-actions/`],
        ];
    }
    goBack() {
        const { router } = this.props;
        const { orgId } = this.props.params;
        router.push(`/organizations/${orgId}/alerts/rules/`);
    }
    fetchStatus(model) {
        const loadingSlackIndicator = indicatorStore_1.default.addMessage((0, locale_1.t)('Looking for your slack channel (this can take a while)'), 'loading');
        // pollHandler calls itself until it gets either a success
        // or failed status but we don't want to poll forever so we pass
        // in a hard stop time of 3 minutes before we bail.
        const quitTime = Date.now() + POLLING_MAX_TIME_LIMIT;
        setTimeout(() => {
            this.pollHandler(model, quitTime, loadingSlackIndicator);
        }, 1000);
    }
    validateFieldInTrigger({ errors, triggerIndex, field, message, isValid }) {
        // If valid, reset error for fieldName
        if (isValid()) {
            const _a = errors.get(triggerIndex) || {}, _b = field, _validatedField = _a[_b], otherErrors = (0, tslib_1.__rest)(_a, [typeof _b === "symbol" ? _b : _b + ""]);
            if (Object.keys(otherErrors).length > 0) {
                errors.set(triggerIndex, otherErrors);
            }
            else {
                errors.delete(triggerIndex);
            }
            return errors;
        }
        if (!errors.has(triggerIndex)) {
            errors.set(triggerIndex, {});
        }
        const currentErrors = errors.get(triggerIndex);
        errors.set(triggerIndex, Object.assign(Object.assign({}, currentErrors), { [field]: message }));
        return errors;
    }
    /**
     * Validate triggers
     *
     * @return Returns true if triggers are valid
     */
    validateTriggers(triggers = this.state.triggers, thresholdType = this.state.thresholdType, resolveThreshold = this.state.resolveThreshold, changedTriggerIndex) {
        var _a, _b;
        const triggerErrors = new Map();
        const requiredFields = ['label', 'alertThreshold'];
        triggers.forEach((trigger, triggerIndex) => {
            requiredFields.forEach(field => {
                // check required fields
                this.validateFieldInTrigger({
                    errors: triggerErrors,
                    triggerIndex,
                    isValid: () => {
                        if (trigger.label === 'critical') {
                            return !isEmpty(trigger[field]);
                        }
                        // If warning trigger has actions, it must have a value
                        return trigger.actions.length === 0 || !isEmpty(trigger[field]);
                    },
                    field,
                    message: (0, locale_1.t)('Field is required'),
                });
            });
            // Check thresholds
            this.isValidTrigger(changedTriggerIndex !== null && changedTriggerIndex !== void 0 ? changedTriggerIndex : triggerIndex, trigger, triggerErrors, resolveThreshold);
        });
        // If we have 2 triggers, we need to make sure that the critical and warning
        // alert thresholds are valid (e.g. if critical is above x, warning must be less than x)
        const criticalTriggerIndex = triggers.findIndex(({ label }) => label === 'critical');
        const warningTriggerIndex = criticalTriggerIndex ^ 1;
        const criticalTrigger = triggers[criticalTriggerIndex];
        const warningTrigger = triggers[warningTriggerIndex];
        const isEmptyWarningThreshold = isEmpty(warningTrigger.alertThreshold);
        const warningThreshold = (_a = warningTrigger.alertThreshold) !== null && _a !== void 0 ? _a : 0;
        const criticalThreshold = (_b = criticalTrigger.alertThreshold) !== null && _b !== void 0 ? _b : 0;
        const hasError = thresholdType === types_1.AlertRuleThresholdType.ABOVE
            ? warningThreshold > criticalThreshold
            : warningThreshold < criticalThreshold;
        if (hasError && !isEmptyWarningThreshold) {
            [criticalTriggerIndex, warningTriggerIndex].forEach(index => {
                var _a;
                const otherErrors = (_a = triggerErrors.get(index)) !== null && _a !== void 0 ? _a : {};
                triggerErrors.set(index, Object.assign(Object.assign({}, otherErrors), { alertThreshold: thresholdType === types_1.AlertRuleThresholdType.BELOW
                        ? (0, locale_1.t)('Warning threshold must be greater than critical alert')
                        : (0, locale_1.t)('Warning threshold must be less than critical alert') }));
            });
        }
        return triggerErrors;
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        var _a;
        const { organization, ruleId, rule, params, onSubmitSuccess, project, userTeamIds, isCustomMetric, } = this.props;
        const { query, timeWindow, triggers, aggregate, environment, thresholdType, comparisonDelta, comparisonType, resolveThreshold, loading, eventTypes, dataset, } = this.state;
        const eventTypeFilter = (0, getEventTypeFilter_1.getEventTypeFilter)(this.state.dataset, eventTypes);
        const queryWithTypeFilter = `${query} ${eventTypeFilter}`.trim();
        const chartProps = {
            organization,
            projects: this.state.projects,
            triggers,
            query: dataset === types_1.Dataset.SESSIONS ? query : queryWithTypeFilter,
            aggregate,
            timeWindow,
            environment,
            resolveThreshold,
            thresholdType,
            comparisonDelta,
            comparisonType,
        };
        const alertType = (0, utils_2.getAlertTypeFromAggregateDataset)({ aggregate, dataset });
        const wizardBuilderChart = (<chart_1.default {...chartProps} header={<ChartHeader>
            <AlertName>{options_1.AlertWizardAlertNames[alertType]}</AlertName>
            {dataset !== types_1.Dataset.SESSIONS && (<AlertInfo>
                {aggregate} | event.type:{eventTypes === null || eventTypes === void 0 ? void 0 : eventTypes.join(',')}
              </AlertInfo>)}
          </ChartHeader>}/>);
        const ownerId = (_a = rule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        const canEdit = (0, isActiveSuperuser_1.isActiveSuperuser)() || (ownerId ? userTeamIds.includes(ownerId) : true);
        const triggerForm = (hasAccess) => (<triggers_1.default disabled={!hasAccess || !canEdit} projects={this.state.projects} errors={this.state.triggerErrors} triggers={triggers} aggregate={aggregate} resolveThreshold={resolveThreshold} thresholdType={thresholdType} comparisonType={comparisonType} currentProject={params.projectId} organization={organization} ruleId={ruleId} availableActions={this.state.availableActions} onChange={this.handleChangeTriggers} onThresholdTypeChange={this.handleThresholdTypeChange} onResolveThresholdChange={this.handleResolveThresholdChange}/>);
        const ruleNameOwnerForm = (hasAccess) => (<ruleNameOwnerForm_1.default disabled={!hasAccess || !canEdit} project={project}/>);
        return (<access_1.default access={['alerts:write']}>
        {({ hasAccess }) => (<form_1.default apiMethod={ruleId ? 'PUT' : 'POST'} apiEndpoint={`/organizations/${organization.slug}/alert-rules/${ruleId ? `${ruleId}/` : ''}`} submitDisabled={!hasAccess || loading || !canEdit} initialData={{
                    name: rule.name || '',
                    dataset: rule.dataset,
                    eventTypes: rule.eventTypes,
                    aggregate: rule.aggregate,
                    query: rule.query || '',
                    timeWindow: rule.timeWindow,
                    environment: rule.environment || null,
                    owner: rule.owner,
                }} saveOnBlur={false} onSubmit={this.handleSubmit} onSubmitSuccess={onSubmitSuccess} onCancel={this.handleCancel} onFieldChange={this.handleFieldChange} extraButton={!!rule.id ? (<confirm_1.default disabled={!hasAccess || !canEdit} message={(0, locale_1.t)('Are you sure you want to delete this alert rule?')} header={(0, locale_1.t)('Delete Alert Rule?')} priority="danger" confirmText={(0, locale_1.t)('Delete Rule')} onConfirm={this.handleDeleteRule}>
                  <button_1.default type="button" priority="danger">
                    {(0, locale_1.t)('Delete Rule')}
                  </button_1.default>
                </confirm_1.default>) : null} submitLabel={(0, locale_1.t)('Save Rule')}>
            <list_1.default symbol="colored-numeric">
              <ruleConditionsForm_1.default api={this.api} projectSlug={params.projectId} organization={organization} disabled={!hasAccess || !canEdit} thresholdChart={wizardBuilderChart} onFilterSearch={this.handleFilterUpdate} allowChangeEventTypes={isCustomMetric || dataset === types_1.Dataset.ERRORS} alertType={isCustomMetric ? 'custom' : alertType} dataset={dataset} comparisonType={comparisonType} comparisonDelta={comparisonDelta} onComparisonTypeChange={this.handleComparisonTypeChange} onComparisonDeltaChange={this.handleComparisonDeltaChange}/>
              <AlertListItem>{(0, locale_1.t)('Set thresholds to trigger alert')}</AlertListItem>
              {triggerForm(hasAccess)}
              <StyledListItem>{(0, locale_1.t)('Add a rule name and team')}</StyledListItem>
              {ruleNameOwnerForm(hasAccess)}
            </list_1.default>
          </form_1.default>)}
      </access_1.default>);
    }
}
const StyledListItem = (0, styled_1.default)(listItem_1.default) `
  margin: ${(0, space_1.default)(2)} 0 ${(0, space_1.default)(1)} 0;
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
const AlertListItem = (0, styled_1.default)(StyledListItem) `
  margin-top: 0;
`;
const ChartHeader = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(3)} 0 ${(0, space_1.default)(3)};
`;
const AlertName = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  font-weight: normal;
  color: ${p => p.theme.textColor};
`;
const AlertInfo = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  font-family: ${p => p.theme.text.familyMono};
  font-weight: normal;
  color: ${p => p.theme.subText};
`;
exports.default = RuleFormContainer;
//# sourceMappingURL=index.jsx.map