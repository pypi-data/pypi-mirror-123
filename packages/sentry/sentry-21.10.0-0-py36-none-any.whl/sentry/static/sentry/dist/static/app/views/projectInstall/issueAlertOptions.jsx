Object.defineProperty(exports, "__esModule", { value: true });
exports.EVENT_FREQUENCY_PERCENT_CONDITION = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const radioGroup_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/radioGroup"));
var MetricValues;
(function (MetricValues) {
    MetricValues[MetricValues["ERRORS"] = 0] = "ERRORS";
    MetricValues[MetricValues["USERS"] = 1] = "USERS";
})(MetricValues || (MetricValues = {}));
var Actions;
(function (Actions) {
    Actions[Actions["ALERT_ON_EVERY_ISSUE"] = 0] = "ALERT_ON_EVERY_ISSUE";
    Actions[Actions["CUSTOMIZED_ALERTS"] = 1] = "CUSTOMIZED_ALERTS";
    Actions[Actions["CREATE_ALERT_LATER"] = 2] = "CREATE_ALERT_LATER";
})(Actions || (Actions = {}));
const UNIQUE_USER_FREQUENCY_CONDITION = 'sentry.rules.conditions.event_frequency.EventUniqueUserFrequencyCondition';
const EVENT_FREQUENCY_CONDITION = 'sentry.rules.conditions.event_frequency.EventFrequencyCondition';
const NOTIFY_EVENT_ACTION = 'sentry.rules.actions.notify_event.NotifyEventAction';
exports.EVENT_FREQUENCY_PERCENT_CONDITION = 'sentry.rules.conditions.event_frequency.EventFrequencyPercentCondition';
const METRIC_CONDITION_MAP = {
    [MetricValues.ERRORS]: EVENT_FREQUENCY_CONDITION,
    [MetricValues.USERS]: UNIQUE_USER_FREQUENCY_CONDITION,
};
const DEFAULT_PLACEHOLDER_VALUE = '10';
function getConditionFrom(interval, metricValue, threshold) {
    let condition;
    switch (metricValue) {
        case MetricValues.ERRORS:
            condition = EVENT_FREQUENCY_CONDITION;
            break;
        case MetricValues.USERS:
            condition = UNIQUE_USER_FREQUENCY_CONDITION;
            break;
        default:
            throw new RangeError('Supplied metric value is not handled');
    }
    return {
        interval,
        id: condition,
        value: threshold,
    };
}
function unpackConditions(conditions) {
    var _a;
    const equalityReducer = (acc, curr) => {
        if (!acc || !curr || !(0, isEqual_1.default)(acc, curr)) {
            return null;
        }
        return acc;
    };
    const intervalChoices = conditions
        .map(condition => { var _a, _b; return (_b = (_a = condition.formFields) === null || _a === void 0 ? void 0 : _a.interval) === null || _b === void 0 ? void 0 : _b.choices; })
        .reduce(equalityReducer);
    return { intervalChoices, interval: (_a = intervalChoices === null || intervalChoices === void 0 ? void 0 : intervalChoices[0]) === null || _a === void 0 ? void 0 : _a[0] };
}
class IssueAlertOptions extends asyncComponent_1.default {
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { conditions: [], intervalChoices: [], alertSetting: Actions.CREATE_ALERT_LATER.toString(), metric: MetricValues.ERRORS, interval: '', threshold: '' });
    }
    getAvailableMetricChoices() {
        return [
            [MetricValues.ERRORS, (0, locale_1.t)('occurrences of')],
            [MetricValues.USERS, (0, locale_1.t)('users affected by')],
        ].filter(valueDescriptionPair => {
            var _a, _b;
            const [value] = valueDescriptionPair;
            return (_b = (_a = this.state.conditions) === null || _a === void 0 ? void 0 : _a.some) === null || _b === void 0 ? void 0 : _b.call(_a, object => (object === null || object === void 0 ? void 0 : object.id) === METRIC_CONDITION_MAP[value]);
        });
    }
    getIssueAlertsChoices(hasProperlyLoadedConditions) {
        const options = [
            [Actions.CREATE_ALERT_LATER.toString(), (0, locale_1.t)("I'll create my own alerts later")],
            [Actions.ALERT_ON_EVERY_ISSUE.toString(), (0, locale_1.t)('Alert me on every new issue')],
        ];
        if (hasProperlyLoadedConditions) {
            options.push([
                Actions.CUSTOMIZED_ALERTS.toString(),
                <CustomizeAlertsGrid key={Actions.CUSTOMIZED_ALERTS} onClick={e => {
                        // XXX(epurkhiser): The `e.preventDefault` here is needed to stop
                        // propagation of the click up to the label, causing it to focus
                        // the radio input and lose focus on the select.
                        e.preventDefault();
                        const alertSetting = Actions.CUSTOMIZED_ALERTS.toString();
                        this.setStateAndUpdateParents({ alertSetting });
                    }}>
          {(0, locale_1.t)('When there are more than')}
          <InlineInput type="number" min="0" name="" placeholder={DEFAULT_PLACEHOLDER_VALUE} value={this.state.threshold} onChange={threshold => this.setStateAndUpdateParents({ threshold: threshold.target.value })} data-test-id="range-input"/>
          <InlineSelectControl value={this.state.metric} choices={this.getAvailableMetricChoices()} onChange={metric => this.setStateAndUpdateParents({ metric: metric.value })} data-test-id="metric-select-control"/>
          {(0, locale_1.t)('a unique error in')}
          <InlineSelectControl value={this.state.interval} choices={this.state.intervalChoices} onChange={interval => this.setStateAndUpdateParents({ interval: interval.value })} data-test-id="interval-select-control"/>
        </CustomizeAlertsGrid>,
            ]);
        }
        return options.map(([choiceValue, node]) => [
            choiceValue,
            <RadioItemWrapper key={choiceValue}>{node}</RadioItemWrapper>,
        ]);
    }
    getUpdatedData() {
        let defaultRules;
        let shouldCreateCustomRule;
        const alertSetting = parseInt(this.state.alertSetting, 10);
        switch (alertSetting) {
            case Actions.ALERT_ON_EVERY_ISSUE:
                defaultRules = true;
                shouldCreateCustomRule = false;
                break;
            case Actions.CREATE_ALERT_LATER:
                defaultRules = false;
                shouldCreateCustomRule = false;
                break;
            case Actions.CUSTOMIZED_ALERTS:
                defaultRules = false;
                shouldCreateCustomRule = true;
                break;
            default:
                throw new RangeError('Supplied alert creation action is not handled');
        }
        return {
            defaultRules,
            shouldCreateCustomRule,
            name: 'Send a notification for new issues',
            conditions: this.state.interval.length > 0 && this.state.threshold.length > 0
                ? [
                    getConditionFrom(this.state.interval, this.state.metric, this.state.threshold),
                ]
                : undefined,
            actions: [{ id: NOTIFY_EVENT_ACTION }],
            actionMatch: 'all',
            frequency: 5,
        };
    }
    setStateAndUpdateParents(state, callback) {
        this.setState(state, () => {
            callback === null || callback === void 0 ? void 0 : callback();
            this.props.onChange(this.getUpdatedData());
        });
    }
    getEndpoints() {
        return [['conditions', `/projects/${this.props.organization.slug}/rule-conditions/`]];
    }
    onLoadAllEndpointsSuccess() {
        var _a, _b;
        const conditions = (_b = (_a = this.state.conditions) === null || _a === void 0 ? void 0 : _a.filter) === null || _b === void 0 ? void 0 : _b.call(_a, object => Object.values(METRIC_CONDITION_MAP).includes(object === null || object === void 0 ? void 0 : object.id));
        if (!conditions || conditions.length === 0) {
            this.setStateAndUpdateParents({
                conditions: undefined,
            });
            return;
        }
        const { intervalChoices, interval } = unpackConditions(conditions);
        if (!intervalChoices || !interval) {
            Sentry.withScope(scope => {
                scope.setExtra('props', this.props);
                scope.setExtra('state', this.state);
                Sentry.captureException(new Error('Interval choices or sent from API endpoint is inconsistent or empty'));
            });
            this.setStateAndUpdateParents({
                conditions: undefined,
            });
            return;
        }
        this.setStateAndUpdateParents({
            conditions,
            intervalChoices,
            interval,
        });
    }
    renderBody() {
        var _a;
        const issueAlertOptionsChoices = this.getIssueAlertsChoices(((_a = this.state.conditions) === null || _a === void 0 ? void 0 : _a.length) > 0);
        return (<React.Fragment>
        <PageHeadingWithTopMargins withMargins>
          {(0, locale_1.t)('Set your default alert settings')}
        </PageHeadingWithTopMargins>
        <RadioGroupWithPadding choices={issueAlertOptionsChoices} label={(0, locale_1.t)('Options for creating an alert')} onChange={alertSetting => this.setStateAndUpdateParents({ alertSetting })} value={this.state.alertSetting}/>
      </React.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(IssueAlertOptions);
const CustomizeAlertsGrid = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(5, max-content);
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
`;
const InlineInput = (0, styled_1.default)(input_1.default) `
  width: 80px;
`;
const InlineSelectControl = (0, styled_1.default)(selectControl_1.default) `
  width: 160px;
`;
const RadioGroupWithPadding = (0, styled_1.default)(radioGroup_1.default) `
  padding: ${(0, space_1.default)(3)} 0;
  margin-bottom: 50px;
  box-shadow: 0 -1px 0 rgba(0, 0, 0, 0.1);
`;
const PageHeadingWithTopMargins = (0, styled_1.default)(pageHeading_1.default) `
  margin-top: 65px;
`;
const RadioItemWrapper = (0, styled_1.default)('div') `
  min-height: 35px;
  display: flex;
  flex-direction: column;
  justify-content: center;
`;
//# sourceMappingURL=issueAlertOptions.jsx.map