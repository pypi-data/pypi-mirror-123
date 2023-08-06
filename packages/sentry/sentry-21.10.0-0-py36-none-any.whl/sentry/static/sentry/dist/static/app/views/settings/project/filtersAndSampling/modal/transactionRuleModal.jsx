Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const checkboxFancy_1 = (0, tslib_1.__importDefault)(require("app/components/checkboxFancy/checkboxFancy"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dynamicSampling_1 = require("app/types/dynamicSampling");
const utils_1 = require("app/utils");
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const utils_2 = require("../utils");
const ruleModal_1 = (0, tslib_1.__importDefault)(require("./ruleModal"));
const utils_3 = require("./utils");
function TransactionRuleModal(_a) {
    var { rule, errorRules, transactionRules } = _a, props = (0, tslib_1.__rest)(_a, ["rule", "errorRules", "transactionRules"]);
    const theme = (0, react_2.useTheme)();
    const [tracing, setTracing] = (0, react_1.useState)(rule ? rule.type === dynamicSampling_1.DynamicSamplingRuleType.TRACE : true);
    const [isTracingDisabled, setIsTracingDisabled] = (0, react_1.useState)(!!(rule === null || rule === void 0 ? void 0 : rule.condition.inner.length));
    function handleChange({ conditions, }) {
        setIsTracingDisabled(!!conditions.length);
    }
    function handleSubmit({ sampleRate, conditions, submitRules, }) {
        if (!(0, utils_1.defined)(sampleRate)) {
            return;
        }
        const newRule = {
            // All new/updated rules must have id equal to 0
            id: 0,
            type: tracing ? dynamicSampling_1.DynamicSamplingRuleType.TRACE : dynamicSampling_1.DynamicSamplingRuleType.TRANSACTION,
            condition: {
                op: dynamicSampling_1.DynamicSamplingConditionOperator.AND,
                inner: !conditions.length ? [] : conditions.map(utils_3.getNewCondition),
            },
            sampleRate: sampleRate / 100,
        };
        const newTransactionRules = rule
            ? transactionRules.map(transactionRule => (0, isEqual_1.default)(transactionRule, rule) ? newRule : transactionRule)
            : [...transactionRules, newRule];
        const [transactionTraceRules, individualTransactionRules] = (0, partition_1.default)(newTransactionRules, transactionRule => transactionRule.type === dynamicSampling_1.DynamicSamplingRuleType.TRACE);
        const newRules = [
            ...errorRules,
            ...transactionTraceRules,
            ...individualTransactionRules,
        ];
        const currentRuleIndex = newRules.findIndex(newR => newR === newRule);
        submitRules(newRules, currentRuleIndex);
    }
    return (<ruleModal_1.default {...props} title={rule ? (0, locale_1.t)('Edit Transaction Sampling Rule') : (0, locale_1.t)('Add Transaction Sampling Rule')} emptyMessage={(0, locale_1.t)('Apply sampling rate to all transactions')} conditionCategories={tracing
            ? [
                [dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE, (0, locale_1.t)('Release')],
                [dynamicSampling_1.DynamicSamplingInnerName.TRACE_ENVIRONMENT, (0, locale_1.t)('Environment')],
                [dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_ID, (0, locale_1.t)('User Id')],
                [dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_SEGMENT, (0, locale_1.t)('User Segment')],
                [dynamicSampling_1.DynamicSamplingInnerName.TRACE_TRANSACTION, (0, locale_1.t)('Transaction')],
            ]
            : [
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE, (0, locale_1.t)('Release')],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT, (0, locale_1.t)('Environment')],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_ID, (0, locale_1.t)('User Id')],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_SEGMENT, (0, locale_1.t)('User Segment')],
                [
                    dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS,
                    (0, locale_1.t)('Browser Extensions'),
                ],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST, (0, locale_1.t)('Localhost')],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER, (0, locale_1.t)('Legacy Browser')],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS, (0, locale_1.t)('Web Crawlers')],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_IP_ADDRESSES, (0, locale_1.t)('IP Address')],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_CSP, (0, locale_1.t)('Content Security Policy')],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_ERROR_MESSAGES, (0, locale_1.t)('Error Message')],
                [dynamicSampling_1.DynamicSamplingInnerName.EVENT_TRANSACTION, (0, locale_1.t)('Transaction')],
            ]} rule={rule} onSubmit={handleSubmit} onChange={handleChange} extraFields={<field_1.default label={(0, locale_1.t)('Tracing')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
          <tooltip_1.default title={(0, locale_1.t)('This field can only be edited if there are no match conditions')} disabled={!isTracingDisabled} popperStyle={(0, react_2.css) `
              @media (min-width: ${theme.breakpoints[0]}) {
                max-width: 370px;
              }
            `}>
            <TracingWrapper onClick={isTracingDisabled ? undefined : () => setTracing(!tracing)}>
              <StyledCheckboxFancy isChecked={tracing} isDisabled={isTracingDisabled}/>
              {(0, locale_1.tct)('Include all related transactions by trace ID. This can span across multiple projects. All related errors will remain. [link:Learn more about tracing].', {
                link: (<externalLink_1.default href={utils_2.DYNAMIC_SAMPLING_DOC_LINK} onClick={event => event.stopPropagation()}/>),
            })}
            </TracingWrapper>
          </tooltip_1.default>
        </field_1.default>}/>);
}
exports.default = TransactionRuleModal;
const TracingWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  cursor: ${p => (p.onClick ? 'pointer' : 'not-allowed')};
`;
const StyledCheckboxFancy = (0, styled_1.default)(checkboxFancy_1.default) `
  margin-top: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=transactionRuleModal.jsx.map