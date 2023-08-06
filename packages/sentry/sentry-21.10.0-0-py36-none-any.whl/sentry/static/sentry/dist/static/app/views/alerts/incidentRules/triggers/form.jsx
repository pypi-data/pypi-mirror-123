Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const members_1 = require("app/actionCreators/members");
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withConfig_1 = (0, tslib_1.__importDefault)(require("app/utils/withConfig"));
const thresholdControl_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/triggers/thresholdControl"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const utils_1 = require("../../utils");
const types_1 = require("../types");
class TriggerForm extends React.PureComponent {
    constructor() {
        super(...arguments);
        /**
         * Handler for threshold changes coming from slider or chart.
         * Needs to sync state with the form.
         */
        this.handleChangeThreshold = (value) => {
            const { onChange, trigger } = this.props;
            onChange(Object.assign(Object.assign({}, trigger), { alertThreshold: value.threshold }), { alertThreshold: value.threshold });
        };
    }
    render() {
        const { disabled, error, trigger, isCritical, thresholdType, comparisonType, fieldHelp, triggerLabel, placeholder, onThresholdTypeChange, } = this.props;
        return (<field_1.default label={triggerLabel} help={fieldHelp} required={isCritical} error={error && error.alertThreshold}>
        <thresholdControl_1.default disabled={disabled} disableThresholdType={!isCritical} type={trigger.label} thresholdType={thresholdType} threshold={trigger.alertThreshold} comparisonType={comparisonType} placeholder={placeholder} onChange={this.handleChangeThreshold} onThresholdTypeChange={onThresholdTypeChange}/>
      </field_1.default>);
    }
}
class TriggerFormContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.handleChangeTrigger = (triggerIndex) => (trigger, changeObj) => {
            const { onChange } = this.props;
            onChange(triggerIndex, trigger, changeObj);
        };
        this.handleChangeResolveTrigger = (trigger, _) => {
            const { onResolveThresholdChange } = this.props;
            onResolveThresholdChange(trigger.alertThreshold);
        };
    }
    componentDidMount() {
        const { api, organization } = this.props;
        (0, members_1.fetchOrgMembers)(api, organization.slug);
    }
    getThresholdUnits(aggregate, comparisonType) {
        if (aggregate.includes('duration') || aggregate.includes('measurements')) {
            return 'ms';
        }
        if ((0, utils_1.isSessionAggregate)(aggregate) ||
            comparisonType === types_1.AlertRuleComparisonType.CHANGE) {
            return '%';
        }
        return '';
    }
    getCriticalThresholdPlaceholder(aggregate, comparisonType) {
        if (aggregate.includes('failure_rate')) {
            return '0.05';
        }
        if ((0, utils_1.isSessionAggregate)(aggregate)) {
            return '97';
        }
        if (comparisonType === types_1.AlertRuleComparisonType.CHANGE) {
            return '100';
        }
        return '300';
    }
    render() {
        const { api, config, disabled, errors, organization, triggers, thresholdType, comparisonType, aggregate, resolveThreshold, projects, onThresholdTypeChange, } = this.props;
        const resolveTrigger = {
            label: 'resolve',
            alertThreshold: resolveThreshold,
            actions: [],
        };
        const thresholdUnits = this.getThresholdUnits(aggregate, comparisonType);
        return (<React.Fragment>
        {triggers.map((trigger, index) => {
                const isCritical = index === 0;
                // eslint-disable-next-line no-use-before-define
                const TriggerIndicator = isCritical ? CriticalIndicator : WarningIndicator;
                return (<TriggerForm key={index} api={api} config={config} disabled={disabled} error={errors && errors.get(index)} trigger={trigger} thresholdType={thresholdType} comparisonType={comparisonType} aggregate={aggregate} resolveThreshold={resolveThreshold} organization={organization} projects={projects} triggerIndex={index} isCritical={isCritical} fieldHelp={(0, locale_1.tct)('The threshold[units] that will activate the [severity] status.', {
                        severity: isCritical ? (0, locale_1.t)('critical') : (0, locale_1.t)('warning'),
                        units: thresholdUnits ? ` (${thresholdUnits})` : '',
                    })} triggerLabel={<React.Fragment>
                  <TriggerIndicator size={12}/>
                  {isCritical ? (0, locale_1.t)('Critical') : (0, locale_1.t)('Warning')}
                </React.Fragment>} placeholder={isCritical
                        ? `${this.getCriticalThresholdPlaceholder(aggregate, comparisonType)}${comparisonType === types_1.AlertRuleComparisonType.COUNT
                            ? thresholdUnits
                            : ''}`
                        : (0, locale_1.t)('None')} onChange={this.handleChangeTrigger(index)} onThresholdTypeChange={onThresholdTypeChange}/>);
            })}
        <TriggerForm api={api} config={config} disabled={disabled} error={errors && errors.get(2)} trigger={resolveTrigger} 
        // Flip rule thresholdType to opposite
        thresholdType={+!thresholdType} comparisonType={comparisonType} aggregate={aggregate} resolveThreshold={resolveThreshold} organization={organization} projects={projects} triggerIndex={2} isCritical={false} fieldHelp={(0, locale_1.tct)('The threshold[units] that will activate the resolved status.', {
                units: thresholdUnits ? ` (${thresholdUnits})` : '',
            })} triggerLabel={<React.Fragment>
              <ResolvedIndicator size={12}/>
              {(0, locale_1.t)('Resolved')}
            </React.Fragment>} placeholder={(0, locale_1.t)('Automatic')} onChange={this.handleChangeResolveTrigger} onThresholdTypeChange={onThresholdTypeChange}/>
      </React.Fragment>);
    }
}
const CriticalIndicator = (0, styled_1.default)(circleIndicator_1.default) `
  background: ${p => p.theme.red300};
  margin-right: ${(0, space_1.default)(1)};
`;
const WarningIndicator = (0, styled_1.default)(circleIndicator_1.default) `
  background: ${p => p.theme.yellow300};
  margin-right: ${(0, space_1.default)(1)};
`;
const ResolvedIndicator = (0, styled_1.default)(circleIndicator_1.default) `
  background: ${p => p.theme.green300};
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = (0, withConfig_1.default)((0, withApi_1.default)(TriggerFormContainer));
//# sourceMappingURL=form.jsx.map