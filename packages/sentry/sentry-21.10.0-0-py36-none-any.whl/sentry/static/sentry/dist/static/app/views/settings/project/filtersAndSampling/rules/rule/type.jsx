Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const locale_1 = require("app/locale");
const dynamicSampling_1 = require("app/types/dynamicSampling");
function Type({ type }) {
    switch (type) {
        case dynamicSampling_1.DynamicSamplingRuleType.ERROR:
            return <ErrorLabel>{(0, locale_1.t)('Errors only')}</ErrorLabel>;
        case dynamicSampling_1.DynamicSamplingRuleType.TRANSACTION:
            return <TransactionLabel>{(0, locale_1.t)('Individual transactions')}</TransactionLabel>;
        case dynamicSampling_1.DynamicSamplingRuleType.TRACE:
            return <TransactionLabel>{(0, locale_1.t)('Transaction traces')}</TransactionLabel>;
        default: {
            Sentry.captureException(new Error('Unknown dynamic sampling rule type'));
            return null; // this shall never happen
        }
    }
}
exports.default = Type;
const ErrorLabel = (0, styled_1.default)('div') `
  color: ${p => p.theme.pink300};
  white-space: pre-wrap;
`;
const TransactionLabel = (0, styled_1.default)(ErrorLabel) `
  color: ${p => p.theme.linkColor};
`;
//# sourceMappingURL=type.jsx.map