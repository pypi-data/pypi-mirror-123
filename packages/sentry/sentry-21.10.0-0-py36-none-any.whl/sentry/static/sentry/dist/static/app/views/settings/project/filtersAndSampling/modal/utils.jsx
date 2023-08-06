Object.defineProperty(exports, "__esModule", { value: true });
exports.getNewCondition = exports.getMatchFieldPlaceholder = exports.isLegacyBrowser = exports.Transaction = exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const locale_1 = require("app/locale");
const dynamicSampling_1 = require("app/types/dynamicSampling");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const utils_1 = require("../utils");
exports.modalCss = (0, react_1.css) `
  [role='document'] {
    overflow: initial;
  }

  @media (min-width: ${theme_1.default.breakpoints[0]}) {
    width: 100%;
    max-width: 700px;
  }
`;
var Transaction;
(function (Transaction) {
    Transaction["ALL"] = "all";
    Transaction["MATCH_CONDITIONS"] = "match-conditions";
})(Transaction = exports.Transaction || (exports.Transaction = {}));
function isLegacyBrowser(maybe) {
    return maybe.every(m => !!utils_1.LEGACY_BROWSER_LIST[m]);
}
exports.isLegacyBrowser = isLegacyBrowser;
function getMatchFieldPlaceholder(category) {
    switch (category) {
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER:
            return (0, locale_1.t)('Match all selected legacy browsers below');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS:
            return (0, locale_1.t)('Match all browser extensions');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST:
            return (0, locale_1.t)('Match all localhosts');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS:
            return (0, locale_1.t)('Match all web crawlers');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_ID:
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_ID:
            return (0, locale_1.t)('ex. 4711 (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_SEGMENT:
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_SEGMENT:
            return (0, locale_1.t)('ex. paid, common (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_ENVIRONMENT:
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT:
            return (0, locale_1.t)('ex. prod, dev');
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE:
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE:
            return (0, locale_1.t)('ex. 1*, [I3].[0-9].*');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_IP_ADDRESSES:
            return (0, locale_1.t)('ex. 127.0.0.1 or 10.0.0.0/8 (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_CSP:
            return (0, locale_1.t)('ex. file://*, example.com (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_ERROR_MESSAGES:
            return (0, locale_1.t)('ex. TypeError* (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_TRANSACTION:
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_TRANSACTION:
            return (0, locale_1.t)('ex. "page-load"');
        default:
            Sentry.captureException(new Error('Unknown dynamic sampling condition inner name'));
            return ''; // this shall never happen
    }
}
exports.getMatchFieldPlaceholder = getMatchFieldPlaceholder;
function getNewCondition(condition) {
    var _a, _b;
    // DynamicSamplingConditionLogicalInnerEqBoolean
    if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS ||
        condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS ||
        condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST) {
        return {
            op: dynamicSampling_1.DynamicSamplingInnerOperator.EQUAL,
            name: condition.category,
            value: true,
        };
    }
    // DynamicSamplingConditionLogicalInnerCustom
    if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER) {
        return {
            op: dynamicSampling_1.DynamicSamplingInnerOperator.CUSTOM,
            name: condition.category,
            value: (_a = condition.legacyBrowsers) !== null && _a !== void 0 ? _a : [],
        };
    }
    const newValue = ((_b = condition.match) !== null && _b !== void 0 ? _b : '')
        .split('\n')
        .filter(match => !!match.trim())
        .map(match => match.trim());
    if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_IP_ADDRESSES ||
        condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_ERROR_MESSAGES ||
        condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_CSP) {
        return {
            op: dynamicSampling_1.DynamicSamplingInnerOperator.CUSTOM,
            name: condition.category,
            value: newValue,
        };
    }
    // DynamicSamplingConditionLogicalInnerGlob
    if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE ||
        condition.category === dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE ||
        condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_TRANSACTION ||
        condition.category === dynamicSampling_1.DynamicSamplingInnerName.TRACE_TRANSACTION) {
        return {
            op: dynamicSampling_1.DynamicSamplingInnerOperator.GLOB_MATCH,
            name: condition.category,
            value: newValue,
        };
    }
    // DynamicSamplingConditionLogicalInnerEq
    if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_ID ||
        condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_ID) {
        return {
            op: dynamicSampling_1.DynamicSamplingInnerOperator.EQUAL,
            name: condition.category,
            value: newValue,
            options: {
                ignoreCase: false,
            },
        };
    }
    // DynamicSamplingConditionLogicalInnerEq
    return {
        op: dynamicSampling_1.DynamicSamplingInnerOperator.EQUAL,
        name: condition.category,
        value: newValue,
        options: {
            ignoreCase: true,
        },
    };
}
exports.getNewCondition = getNewCondition;
//# sourceMappingURL=utils.jsx.map