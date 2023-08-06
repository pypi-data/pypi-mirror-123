Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const locale_1 = require("app/locale");
const dynamicSampling_1 = require("app/types/dynamicSampling");
const utils_1 = require("app/utils");
const ruleModal_1 = (0, tslib_1.__importDefault)(require("./ruleModal"));
const utils_2 = require("./utils");
function ErrorRuleModal(_a) {
    var { rule, errorRules, transactionRules } = _a, props = (0, tslib_1.__rest)(_a, ["rule", "errorRules", "transactionRules"]);
    function handleSubmit({ sampleRate, conditions, submitRules, }) {
        if (!(0, utils_1.defined)(sampleRate)) {
            return;
        }
        const newRule = {
            // All new/updated rules must have id equal to 0
            id: 0,
            type: dynamicSampling_1.DynamicSamplingRuleType.ERROR,
            condition: {
                op: dynamicSampling_1.DynamicSamplingConditionOperator.AND,
                inner: !conditions.length ? [] : conditions.map(utils_2.getNewCondition),
            },
            sampleRate: sampleRate / 100,
        };
        const newRules = rule
            ? [
                ...errorRules.map(errorRule => (0, isEqual_1.default)(errorRule, rule) ? newRule : errorRule),
                ...transactionRules,
            ]
            : [...errorRules, newRule, ...transactionRules];
        const currentRuleIndex = newRules.findIndex(newR => newR === newRule);
        submitRules(newRules, currentRuleIndex);
    }
    return (<ruleModal_1.default {...props} title={rule ? (0, locale_1.t)('Edit Error Sampling Rule') : (0, locale_1.t)('Add Error Sampling Rule')} emptyMessage={(0, locale_1.t)('Apply sampling rate to all errors')} conditionCategories={[
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE, (0, locale_1.t)('Release')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT, (0, locale_1.t)('Environment')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_ID, (0, locale_1.t)('User Id')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_SEGMENT, (0, locale_1.t)('User Segment')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS, (0, locale_1.t)('Browser Extensions')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST, (0, locale_1.t)('Localhost')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER, (0, locale_1.t)('Legacy Browser')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS, (0, locale_1.t)('Web Crawlers')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_IP_ADDRESSES, (0, locale_1.t)('IP Address')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_CSP, (0, locale_1.t)('Content Security Policy')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_ERROR_MESSAGES, (0, locale_1.t)('Error Message')],
            [dynamicSampling_1.DynamicSamplingInnerName.EVENT_TRANSACTION, (0, locale_1.t)('Transaction')],
        ]} rule={rule} onSubmit={handleSubmit}/>);
}
exports.default = ErrorRuleModal;
//# sourceMappingURL=errorRuleModal.jsx.map