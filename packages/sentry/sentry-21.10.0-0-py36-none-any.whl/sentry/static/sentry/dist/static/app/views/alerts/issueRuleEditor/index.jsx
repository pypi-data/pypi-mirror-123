Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const cloneDeep_1 = (0, tslib_1.__importDefault)(require("lodash/cloneDeep"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const indicator_1 = require("app/actionCreators/indicator");
const onboardingTasks_1 = require("app/actionCreators/onboardingTasks");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const teamSelector_1 = (0, tslib_1.__importDefault)(require("app/components/forms/teamSelector"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const loadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/loadingMask"));
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const analytics_1 = require("app/utils/analytics");
const environment_1 = require("app/utils/environment");
const isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const changeAlerts_1 = require("app/views/alerts/issueRuleEditor/constants/changeAlerts");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const ruleNodeList_1 = (0, tslib_1.__importDefault)(require("./ruleNodeList"));
const setupAlertIntegrationButton_1 = (0, tslib_1.__importDefault)(require("./setupAlertIntegrationButton"));
const FREQUENCY_OPTIONS = [
    { value: '5', label: (0, locale_1.t)('5 minutes') },
    { value: '10', label: (0, locale_1.t)('10 minutes') },
    { value: '30', label: (0, locale_1.t)('30 minutes') },
    { value: '60', label: (0, locale_1.t)('60 minutes') },
    { value: '180', label: (0, locale_1.t)('3 hours') },
    { value: '720', label: (0, locale_1.t)('12 hours') },
    { value: '1440', label: (0, locale_1.t)('24 hours') },
    { value: '10080', label: (0, locale_1.t)('1 week') },
    { value: '43200', label: (0, locale_1.t)('30 days') },
];
const ACTION_MATCH_OPTIONS = [
    { value: 'all', label: (0, locale_1.t)('all') },
    { value: 'any', label: (0, locale_1.t)('any') },
    { value: 'none', label: (0, locale_1.t)('none') },
];
const ACTION_MATCH_OPTIONS_MIGRATED = [
    { value: 'all', label: (0, locale_1.t)('all') },
    { value: 'any', label: (0, locale_1.t)('any') },
];
const defaultRule = {
    actionMatch: 'all',
    filterMatch: 'all',
    actions: [],
    conditions: [],
    filters: [],
    name: '',
    frequency: 30,
    environment: constants_1.ALL_ENVIRONMENTS_KEY,
};
const POLLING_MAX_TIME_LIMIT = 3 * 60000;
function isSavedAlertRule(rule) {
    var _a;
    return (_a = rule === null || rule === void 0 ? void 0 : rule.hasOwnProperty('id')) !== null && _a !== void 0 ? _a : false;
}
class IssueRuleEditor extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.pollHandler = (quitTime) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (Date.now() > quitTime) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Looking for that channel took too long :('));
                this.setState({ loading: false });
                return;
            }
            const { organization, project } = this.props;
            const { uuid } = this.state;
            const origRule = this.state.rule;
            try {
                const response = yield this.api.requestPromise(`/projects/${organization.slug}/${project.slug}/rule-task/${uuid}/`);
                const { status, rule, error } = response;
                if (status === 'pending') {
                    setTimeout(() => {
                        this.pollHandler(quitTime);
                    }, 1000);
                    return;
                }
                if (status === 'failed') {
                    this.setState({
                        detailedError: { actions: [error ? error : (0, locale_1.t)('An error occurred')] },
                        loading: false,
                    });
                    this.handleRuleSaveFailure((0, locale_1.t)('An error occurred'));
                }
                if (rule) {
                    const ruleId = isSavedAlertRule(origRule) ? `${origRule.id}/` : '';
                    const isNew = !ruleId;
                    this.handleRuleSuccess(isNew, rule);
                }
            }
            catch (_a) {
                this.handleRuleSaveFailure((0, locale_1.t)('An error occurred'));
                this.setState({ loading: false });
            }
        });
        this.handleRuleSuccess = (isNew, rule) => {
            const { organization, router } = this.props;
            this.setState({ detailedError: null, loading: false, rule });
            // The onboarding task will be completed on the server side when the alert
            // is created
            (0, onboardingTasks_1.updateOnboardingTask)(null, organization, {
                task: types_1.OnboardingTaskKey.ALERT_RULE,
                status: 'complete',
            });
            analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
            router.push(`/organizations/${organization.slug}/alerts/rules/`);
            (0, indicator_1.addSuccessMessage)(isNew ? (0, locale_1.t)('Created alert rule') : (0, locale_1.t)('Updated alert rule'));
        };
        this.handleSubmit = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { rule } = this.state;
            const ruleId = isSavedAlertRule(rule) ? `${rule.id}/` : '';
            const isNew = !ruleId;
            const { project, organization } = this.props;
            const endpoint = `/projects/${organization.slug}/${project.slug}/rules/${ruleId}`;
            if (rule && rule.environment === constants_1.ALL_ENVIRONMENTS_KEY) {
                delete rule.environment;
            }
            (0, indicator_1.addLoadingMessage)();
            try {
                const transaction = analytics_1.metric.startTransaction({ name: 'saveAlertRule' });
                transaction.setTag('type', 'issue');
                transaction.setTag('operation', isNew ? 'create' : 'edit');
                if (rule) {
                    for (const action of rule.actions) {
                        // Grab the last part of something like 'sentry.mail.actions.NotifyEmailAction'
                        const splitActionId = action.id.split('.');
                        const actionName = splitActionId[splitActionId.length - 1];
                        if (actionName === 'SlackNotifyServiceAction') {
                            transaction.setTag(actionName, true);
                        }
                    }
                    transaction.setData('actions', rule.actions);
                }
                const [data, , resp] = yield this.api.requestPromise(endpoint, {
                    includeAllArgs: true,
                    method: isNew ? 'POST' : 'PUT',
                    data: rule,
                });
                // if we get a 202 back it means that we have an async task
                // running to lookup and verify the channel id for Slack.
                if ((resp === null || resp === void 0 ? void 0 : resp.status) === 202) {
                    this.setState({ detailedError: null, loading: true, uuid: data.uuid });
                    this.fetchStatus();
                    (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Looking through all your channels...'));
                }
                else {
                    this.handleRuleSuccess(isNew, data);
                }
            }
            catch (err) {
                this.setState({
                    detailedError: err.responseJSON || { __all__: 'Unknown error' },
                    loading: false,
                });
                this.handleRuleSaveFailure((0, locale_1.t)('An error occurred'));
            }
        });
        this.handleDeleteRule = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { rule } = this.state;
            const ruleId = isSavedAlertRule(rule) ? `${rule.id}/` : '';
            const isNew = !ruleId;
            const { project, organization } = this.props;
            if (isNew) {
                return;
            }
            const endpoint = `/projects/${organization.slug}/${project.slug}/rules/${ruleId}`;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Deleting...'));
            try {
                yield this.api.requestPromise(endpoint, {
                    method: 'DELETE',
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Deleted alert rule'));
                react_router_1.browserHistory.replace((0, recreateRoute_1.default)('', Object.assign(Object.assign({}, this.props), { stepBack: -2 })));
            }
            catch (err) {
                this.setState({
                    detailedError: err.responseJSON || { __all__: 'Unknown error' },
                });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('There was a problem deleting the alert'));
            }
        });
        this.handleCancel = () => {
            const { organization, router } = this.props;
            router.push(`/organizations/${organization.slug}/alerts/rules/`);
        };
        this.hasError = (field) => {
            const { detailedError } = this.state;
            if (!detailedError) {
                return false;
            }
            return detailedError.hasOwnProperty(field);
        };
        this.handleEnvironmentChange = (val) => {
            // If 'All Environments' is selected the value should be null
            if (val === constants_1.ALL_ENVIRONMENTS_KEY) {
                this.handleChange('environment', null);
            }
            else {
                this.handleChange('environment', val);
            }
        };
        this.handleChange = (prop, val) => {
            this.setState(prevState => {
                const clonedState = (0, cloneDeep_1.default)(prevState);
                (0, set_1.default)(clonedState, `rule[${prop}]`, val);
                return Object.assign(Object.assign({}, clonedState), { detailedError: (0, omit_1.default)(prevState.detailedError, prop) });
            });
        };
        this.handlePropertyChange = (type, idx, prop, val) => {
            this.setState(prevState => {
                const clonedState = (0, cloneDeep_1.default)(prevState);
                (0, set_1.default)(clonedState, `rule[${type}][${idx}][${prop}]`, val);
                return clonedState;
            });
        };
        this.getInitialValue = (type, id) => {
            var _a, _b;
            const configuration = (_b = (_a = this.state.configs) === null || _a === void 0 ? void 0 : _a[type]) === null || _b === void 0 ? void 0 : _b.find(c => c.id === id);
            return (configuration === null || configuration === void 0 ? void 0 : configuration.formFields)
                ? Object.fromEntries(Object.entries(configuration.formFields)
                    // TODO(ts): Doesn't work if I cast formField as IssueAlertRuleFormField
                    .map(([key, formField]) => {
                    var _a, _b, _c;
                    return [
                        key,
                        (_a = formField === null || formField === void 0 ? void 0 : formField.initial) !== null && _a !== void 0 ? _a : (_c = (_b = formField === null || formField === void 0 ? void 0 : formField.choices) === null || _b === void 0 ? void 0 : _b[0]) === null || _c === void 0 ? void 0 : _c[0],
                    ];
                })
                    .filter(([, initial]) => !!initial))
                : {};
        };
        this.handleResetRow = (type, idx, prop, val) => {
            this.setState(prevState => {
                const clonedState = (0, cloneDeep_1.default)(prevState);
                // Set initial configuration, but also set
                const id = clonedState.rule[type][idx].id;
                const newRule = Object.assign(Object.assign({}, this.getInitialValue(type, id)), { id, [prop]: val });
                (0, set_1.default)(clonedState, `rule[${type}][${idx}]`, newRule);
                return clonedState;
            });
        };
        this.handleAddRow = (type, id) => {
            this.setState(prevState => {
                const clonedState = (0, cloneDeep_1.default)(prevState);
                // Set initial configuration
                const newRule = Object.assign(Object.assign({}, this.getInitialValue(type, id)), { id });
                const newTypeList = prevState.rule ? prevState.rule[type] : [];
                (0, set_1.default)(clonedState, `rule[${type}]`, [...newTypeList, newRule]);
                return clonedState;
            });
            const { organization, project } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'edit_alert_rule.add_row',
                eventName: 'Edit Alert Rule: Add Row',
                organization_id: organization.id,
                project_id: project.id,
                type,
                name: id,
            });
        };
        this.handleDeleteRow = (type, idx) => {
            this.setState(prevState => {
                const clonedState = (0, cloneDeep_1.default)(prevState);
                const newTypeList = prevState.rule ? prevState.rule[type] : [];
                if (prevState.rule) {
                    newTypeList.splice(idx, 1);
                }
                (0, set_1.default)(clonedState, `rule[${type}]`, newTypeList);
                return clonedState;
            });
        };
        this.handleAddCondition = (id) => this.handleAddRow('conditions', id);
        this.handleAddAction = (id) => this.handleAddRow('actions', id);
        this.handleAddFilter = (id) => this.handleAddRow('filters', id);
        this.handleDeleteCondition = (ruleIndex) => this.handleDeleteRow('conditions', ruleIndex);
        this.handleDeleteAction = (ruleIndex) => this.handleDeleteRow('actions', ruleIndex);
        this.handleDeleteFilter = (ruleIndex) => this.handleDeleteRow('filters', ruleIndex);
        this.handleChangeConditionProperty = (ruleIndex, prop, val) => this.handlePropertyChange('conditions', ruleIndex, prop, val);
        this.handleChangeActionProperty = (ruleIndex, prop, val) => this.handlePropertyChange('actions', ruleIndex, prop, val);
        this.handleChangeFilterProperty = (ruleIndex, prop, val) => this.handlePropertyChange('filters', ruleIndex, prop, val);
        this.handleResetCondition = (ruleIndex, prop, value) => this.handleResetRow('conditions', ruleIndex, prop, value);
        this.handleResetAction = (ruleIndex, prop, value) => this.handleResetRow('actions', ruleIndex, prop, value);
        this.handleResetFilter = (ruleIndex, prop, value) => this.handleResetRow('filters', ruleIndex, prop, value);
        this.handleValidateRuleName = () => {
            var _a;
            const isRuleNameEmpty = !((_a = this.state.rule) === null || _a === void 0 ? void 0 : _a.name.trim());
            if (!isRuleNameEmpty) {
                return;
            }
            this.setState(prevState => ({
                detailedError: Object.assign(Object.assign({}, prevState.detailedError), { name: [(0, locale_1.t)('Field Required')] }),
            }));
        };
        this.getTeamId = () => {
            const { rule } = this.state;
            const owner = rule === null || rule === void 0 ? void 0 : rule.owner;
            // ownership follows the format team:<id>, just grab the id
            return owner && owner.split(':')[1];
        };
        this.handleOwnerChange = ({ value }) => {
            const ownerValue = value && `team:${value}`;
            this.handleChange('owner', ownerValue);
        };
    }
    getTitle() {
        const { organization, project } = this.props;
        const { rule } = this.state;
        const ruleName = rule === null || rule === void 0 ? void 0 : rule.name;
        return (0, routeTitle_1.default)(ruleName ? (0, locale_1.t)('Alert %s', ruleName) : '', organization.slug, false, project === null || project === void 0 ? void 0 : project.slug);
    }
    getDefaultState() {
        var _a;
        const { teams, project } = this.props;
        const defaultState = Object.assign(Object.assign({}, super.getDefaultState()), { configs: null, detailedError: null, rule: Object.assign({}, defaultRule), environments: [], uuid: null });
        const projectTeamIds = new Set(project.teams.map(({ id }) => id));
        const userTeam = (_a = teams.find(({ isMember, id }) => !!isMember && projectTeamIds.has(id))) !== null && _a !== void 0 ? _a : null;
        defaultState.rule.owner = userTeam && `team:${userTeam.id}`;
        return defaultState;
    }
    getEndpoints() {
        const { ruleId, projectId, orgId } = this.props.params;
        const endpoints = [
            ['environments', `/projects/${orgId}/${projectId}/environments/`],
            ['configs', `/projects/${orgId}/${projectId}/rules/configuration/`],
        ];
        if (ruleId) {
            endpoints.push(['rule', `/projects/${orgId}/${projectId}/rules/${ruleId}/`]);
        }
        return endpoints;
    }
    onRequestSuccess({ stateKey, data }) {
        var _a, _b;
        if (stateKey === 'rule' && data.name) {
            (_b = (_a = this.props).onChangeTitle) === null || _b === void 0 ? void 0 : _b.call(_a, data.name);
        }
    }
    fetchStatus() {
        // pollHandler calls itself until it gets either a success
        // or failed status but we don't want to poll forever so we pass
        // in a hard stop time of 3 minutes before we bail.
        const quitTime = Date.now() + POLLING_MAX_TIME_LIMIT;
        setTimeout(() => {
            this.pollHandler(quitTime);
        }, 1000);
    }
    handleRuleSaveFailure(msg) {
        (0, indicator_1.addErrorMessage)(msg);
        analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
    }
    getConditions() {
        var _a, _b, _c, _d, _e;
        const { organization } = this.props;
        if (!organization.features.includes('change-alerts')) {
            return (_b = (_a = this.state.configs) === null || _a === void 0 ? void 0 : _a.conditions) !== null && _b !== void 0 ? _b : null;
        }
        return ((_e = (_d = (_c = this.state.configs) === null || _c === void 0 ? void 0 : _c.conditions) === null || _d === void 0 ? void 0 : _d.map(condition => changeAlerts_1.CHANGE_ALERT_CONDITION_IDS.includes(condition.id)
            ? Object.assign(Object.assign({}, condition), { label: changeAlerts_1.CHANGE_ALERT_PLACEHOLDERS_LABELS[condition.id] })
            : condition)) !== null && _e !== void 0 ? _e : null);
    }
    renderLoading() {
        return this.renderBody();
    }
    renderError() {
        return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
        {(0, locale_1.t)('Unable to access this alert rule -- check to make sure you have the correct permissions')}
      </alert_1.default>);
    }
    renderBody() {
        var _a, _b;
        const { project, organization, teams } = this.props;
        const { environments } = this.state;
        const environmentOptions = [
            {
                value: constants_1.ALL_ENVIRONMENTS_KEY,
                label: (0, locale_1.t)('All Environments'),
            },
            ...((_a = environments === null || environments === void 0 ? void 0 : environments.map(env => ({ value: env.name, label: (0, environment_1.getDisplayName)(env) }))) !== null && _a !== void 0 ? _a : []),
        ];
        const { rule, detailedError } = this.state;
        const { actions, filters, conditions, frequency, name } = rule || {};
        const environment = !rule || !rule.environment ? constants_1.ALL_ENVIRONMENTS_KEY : rule.environment;
        const userTeams = teams.filter(({ isMember }) => isMember).map(({ id }) => id);
        const ownerId = (_b = rule === null || rule === void 0 ? void 0 : rule.owner) === null || _b === void 0 ? void 0 : _b.split(':')[1];
        // check if superuser or if user is on the alert's team
        const canEdit = (0, isActiveSuperuser_1.isActiveSuperuser)() || (ownerId ? userTeams.includes(ownerId) : true);
        // Note `key` on `<Form>` below is so that on initial load, we show
        // the form with a loading mask on top of it, but force a re-render by using
        // a different key when we have fetched the rule so that form inputs are filled in
        return (<access_1.default access={['alerts:write']}>
        {({ hasAccess }) => {
                var _a, _b, _c, _d, _e;
                return (<StyledForm key={isSavedAlertRule(rule) ? rule.id : undefined} onCancel={this.handleCancel} onSubmit={this.handleSubmit} initialData={Object.assign(Object.assign({}, rule), { environment, frequency: `${frequency}` })} submitDisabled={!hasAccess || !canEdit} submitLabel={isSavedAlertRule(rule) ? (0, locale_1.t)('Save Rule') : (0, locale_1.t)('Save Rule')} extraButton={isSavedAlertRule(rule) ? (<confirm_1.default disabled={!hasAccess || !canEdit} priority="danger" confirmText={(0, locale_1.t)('Delete Rule')} onConfirm={this.handleDeleteRule} header={(0, locale_1.t)('Delete Rule')} message={(0, locale_1.t)('Are you sure you want to delete this rule?')}>
                  <button_1.default priority="danger" type="button">
                    {(0, locale_1.t)('Delete Rule')}
                  </button_1.default>
                </confirm_1.default>) : null}>
            <list_1.default symbol="colored-numeric">
              {this.state.loading && <SemiTransparentLoadingMask />}
              <StyledListItem>{(0, locale_1.t)('Add alert settings')}</StyledListItem>
              <panels_1.Panel>
                <panels_1.PanelBody>
                  <selectField_1.default className={(0, classnames_1.default)({
                        error: this.hasError('environment'),
                    })} label={(0, locale_1.t)('Environment')} help={(0, locale_1.t)('Choose an environment for these conditions to apply to')} placeholder={(0, locale_1.t)('Select an Environment')} clearable={false} name="environment" options={environmentOptions} onChange={val => this.handleEnvironmentChange(val)} disabled={!hasAccess || !canEdit}/>

                  <StyledField label={(0, locale_1.t)('Team')} help={(0, locale_1.t)('The team that can edit this alert.')} disabled={!hasAccess || !canEdit}>
                    <teamSelector_1.default value={this.getTeamId()} project={project} onChange={this.handleOwnerChange} teamFilter={(team) => team.isMember || team.id === ownerId} useId includeUnassigned disabled={!hasAccess || !canEdit}/>
                  </StyledField>

                  <StyledField label={(0, locale_1.t)('Alert name')} help={(0, locale_1.t)('Add a name for this alert')} error={(_a = detailedError === null || detailedError === void 0 ? void 0 : detailedError.name) === null || _a === void 0 ? void 0 : _a[0]} disabled={!hasAccess || !canEdit} required stacked>
                    <input_1.default type="text" name="name" value={name} placeholder={(0, locale_1.t)('My Rule Name')} onChange={(event) => this.handleChange('name', event.target.value)} onBlur={this.handleValidateRuleName} disabled={!hasAccess || !canEdit}/>
                  </StyledField>
                </panels_1.PanelBody>
              </panels_1.Panel>
              <SetConditionsListItem>
                {(0, locale_1.t)('Set conditions')}
                <setupAlertIntegrationButton_1.default projectSlug={project.slug} organization={organization}/>
              </SetConditionsListItem>
              <ConditionsPanel>
                <panels_1.PanelBody>
                  <Step>
                    <StepConnector />

                    <StepContainer>
                      <ChevronContainer>
                        <icons_1.IconChevron color="gray200" isCircled direction="right" size="sm"/>
                      </ChevronContainer>

                      <feature_1.default features={['projects:alert-filters']} project={project}>
                        {({ hasFeature }) => (<StepContent>
                            <StepLead>
                              {(0, locale_1.tct)('[when:When] an event is captured by Sentry and [selector] of the following happens', {
                            when: <Badge />,
                            selector: (<EmbeddedWrapper>
                                      <EmbeddedSelectField className={(0, classnames_1.default)({
                                    error: this.hasError('actionMatch'),
                                })} inline={false} styles={{
                                    control: provided => (Object.assign(Object.assign({}, provided), { minHeight: '20px', height: '20px' })),
                                }} isSearchable={false} isClearable={false} name="actionMatch" required flexibleControlStateSize options={hasFeature
                                    ? ACTION_MATCH_OPTIONS_MIGRATED
                                    : ACTION_MATCH_OPTIONS} onChange={val => this.handleChange('actionMatch', val)} disabled={!hasAccess || !canEdit}/>
                                    </EmbeddedWrapper>),
                        })}
                            </StepLead>
                            <ruleNodeList_1.default nodes={this.getConditions()} items={conditions !== null && conditions !== void 0 ? conditions : []} placeholder={hasFeature
                            ? (0, locale_1.t)('Add optional trigger...')
                            : (0, locale_1.t)('Add optional condition...')} onPropertyChange={this.handleChangeConditionProperty} onAddRow={this.handleAddCondition} onResetRow={this.handleResetCondition} onDeleteRow={this.handleDeleteCondition} organization={organization} project={project} disabled={!hasAccess || !canEdit} error={this.hasError('conditions') && (<StyledAlert type="error">
                                    {detailedError === null || detailedError === void 0 ? void 0 : detailedError.conditions[0]}
                                  </StyledAlert>)}/>
                          </StepContent>)}
                      </feature_1.default>
                    </StepContainer>
                  </Step>

                  <feature_1.default features={['organizations:alert-filters', 'projects:alert-filters']} organization={organization} project={project} requireAll={false}>
                    <Step>
                      <StepConnector />

                      <StepContainer>
                        <ChevronContainer>
                          <icons_1.IconChevron color="gray200" isCircled direction="right" size="sm"/>
                        </ChevronContainer>

                        <StepContent>
                          <StepLead>
                            {(0, locale_1.tct)('[if:If] [selector] of these filters match', {
                        if: <Badge />,
                        selector: (<EmbeddedWrapper>
                                  <EmbeddedSelectField className={(0, classnames_1.default)({
                                error: this.hasError('filterMatch'),
                            })} inline={false} styles={{
                                control: provided => (Object.assign(Object.assign({}, provided), { minHeight: '20px', height: '20px' })),
                            }} isSearchable={false} isClearable={false} name="filterMatch" required flexibleControlStateSize options={ACTION_MATCH_OPTIONS} onChange={val => this.handleChange('filterMatch', val)} disabled={!hasAccess || !canEdit}/>
                                </EmbeddedWrapper>),
                    })}
                          </StepLead>
                          <ruleNodeList_1.default nodes={(_c = (_b = this.state.configs) === null || _b === void 0 ? void 0 : _b.filters) !== null && _c !== void 0 ? _c : null} items={filters !== null && filters !== void 0 ? filters : []} placeholder={(0, locale_1.t)('Add optional filter...')} onPropertyChange={this.handleChangeFilterProperty} onAddRow={this.handleAddFilter} onResetRow={this.handleResetFilter} onDeleteRow={this.handleDeleteFilter} organization={organization} project={project} disabled={!hasAccess || !canEdit} error={this.hasError('filters') && (<StyledAlert type="error">
                                  {detailedError === null || detailedError === void 0 ? void 0 : detailedError.filters[0]}
                                </StyledAlert>)}/>
                        </StepContent>
                      </StepContainer>
                    </Step>
                  </feature_1.default>

                  <Step>
                    <StepContainer>
                      <ChevronContainer>
                        <icons_1.IconChevron isCircled color="gray200" direction="right" size="sm"/>
                      </ChevronContainer>
                      <StepContent>
                        <StepLead>
                          {(0, locale_1.tct)('[then:Then] perform these actions', {
                        then: <Badge />,
                    })}
                        </StepLead>

                        <ruleNodeList_1.default nodes={(_e = (_d = this.state.configs) === null || _d === void 0 ? void 0 : _d.actions) !== null && _e !== void 0 ? _e : null} selectType="grouped" items={actions !== null && actions !== void 0 ? actions : []} placeholder={(0, locale_1.t)('Add action...')} onPropertyChange={this.handleChangeActionProperty} onAddRow={this.handleAddAction} onResetRow={this.handleResetAction} onDeleteRow={this.handleDeleteAction} organization={organization} project={project} disabled={!hasAccess || !canEdit} error={this.hasError('actions') && (<StyledAlert type="error">
                                {detailedError === null || detailedError === void 0 ? void 0 : detailedError.actions[0]}
                              </StyledAlert>)}/>
                      </StepContent>
                    </StepContainer>
                  </Step>
                </panels_1.PanelBody>
              </ConditionsPanel>
              <StyledListItem>{(0, locale_1.t)('Set action interval')}</StyledListItem>
              <panels_1.Panel>
                <panels_1.PanelBody>
                  <selectField_1.default label={(0, locale_1.t)('Action Interval')} help={(0, locale_1.t)('Perform these actions once this often for an issue')} clearable={false} name="frequency" className={this.hasError('frequency') ? ' error' : ''} value={frequency} required options={FREQUENCY_OPTIONS} onChange={val => this.handleChange('frequency', val)} disabled={!hasAccess || !canEdit}/>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </list_1.default>
          </StyledForm>);
            }}
      </access_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)((0, withTeams_1.default)(IssueRuleEditor));
// TODO(ts): Understand why styled is not correctly inheriting props here
const StyledForm = (0, styled_1.default)(form_1.default) `
  position: relative;
`;
const ConditionsPanel = (0, styled_1.default)(panels_1.Panel) `
  padding-top: ${(0, space_1.default)(0.5)};
  padding-bottom: ${(0, space_1.default)(2)};
`;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin-bottom: 0;
`;
const StyledListItem = (0, styled_1.default)(listItem_1.default) `
  margin: ${(0, space_1.default)(2)} 0 ${(0, space_1.default)(1)} 0;
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
const SetConditionsListItem = (0, styled_1.default)(StyledListItem) `
  display: flex;
  justify-content: space-between;
`;
const Step = (0, styled_1.default)('div') `
  position: relative;
  display: flex;
  align-items: flex-start;
  margin: ${(0, space_1.default)(4)} ${(0, space_1.default)(4)} ${(0, space_1.default)(3)} ${(0, space_1.default)(1)};
`;
const StepContainer = (0, styled_1.default)('div') `
  position: relative;
  display: flex;
  align-items: flex-start;
  flex-grow: 1;
`;
const StepContent = (0, styled_1.default)('div') `
  flex-grow: 1;
`;
const StepConnector = (0, styled_1.default)('div') `
  position: absolute;
  height: 100%;
  top: 28px;
  left: 19px;
  border-right: 1px ${p => p.theme.gray300} dashed;
`;
const StepLead = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(0.5)};
`;
const ChevronContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1.5)};
`;
const Badge = (0, styled_1.default)('span') `
  display: inline-block;
  min-width: 56px;
  background-color: ${p => p.theme.purple300};
  padding: 0 ${(0, space_1.default)(0.75)};
  border-radius: ${p => p.theme.borderRadius};
  color: ${p => p.theme.white};
  text-transform: uppercase;
  text-align: center;
  font-size: ${p => p.theme.fontSizeMedium};
  font-weight: 600;
  line-height: 1.5;
`;
const EmbeddedWrapper = (0, styled_1.default)('div') `
  display: inline-block;
  margin: 0 ${(0, space_1.default)(0.5)};
  width: 80px;
`;
const EmbeddedSelectField = (0, styled_1.default)(selectField_1.default) `
  padding: 0;
  font-weight: normal;
  text-transform: none;
`;
const SemiTransparentLoadingMask = (0, styled_1.default)(loadingMask_1.default) `
  opacity: 0.6;
  z-index: 1; /* Needed so that it sits above form elements */
`;
const StyledField = (0, styled_1.default)(field_1.default) `
  :last-child {
    padding-bottom: ${(0, space_1.default)(2)};
  }
`;
//# sourceMappingURL=index.jsx.map