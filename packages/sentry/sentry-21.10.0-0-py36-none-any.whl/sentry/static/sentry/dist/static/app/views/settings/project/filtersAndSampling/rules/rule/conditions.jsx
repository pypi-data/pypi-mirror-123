Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dynamicSampling_1 = require("app/types/dynamicSampling");
const utils_1 = require("../../utils");
function Conditions({ condition }) {
    function getConvertedValue(value) {
        var _a, _b;
        if (Array.isArray(value)) {
            return (<react_1.Fragment>
          {[...value].map((v, index) => {
                    var _a, _b;
                    return (<react_1.Fragment key={v}>
              <Value>{(_b = (_a = utils_1.LEGACY_BROWSER_LIST[v]) === null || _a === void 0 ? void 0 : _a.title) !== null && _b !== void 0 ? _b : v}</Value>
              {index !== value.length - 1 && <Separator>{'\u002C'}</Separator>}
            </react_1.Fragment>);
                })}
        </react_1.Fragment>);
        }
        return <Value>{(_b = (_a = utils_1.LEGACY_BROWSER_LIST[String(value)]) === null || _a === void 0 ? void 0 : _a.title) !== null && _b !== void 0 ? _b : String(value)}</Value>;
    }
    switch (condition.op) {
        case dynamicSampling_1.DynamicSamplingConditionOperator.AND: {
            const { inner } = condition;
            if (!inner.length) {
                return <Label>{(0, locale_1.t)('All')}</Label>;
            }
            return (<Wrapper>
          {inner.map(({ value, name }, index) => (<div key={index}>
              <Label>{(0, utils_1.getInnerNameLabel)(name)}</Label>
              {getConvertedValue(value)}
            </div>))}
        </Wrapper>);
        }
        default: {
            Sentry.captureException(new Error('Unknown dynamic sampling condition operator'));
            return null; // this shall not happen
        }
    }
}
exports.default = Conditions;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
`;
const Label = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(1)};
`;
const Value = (0, styled_1.default)('span') `
  word-break: break-all;
  white-space: pre-wrap;
  color: ${p => p.theme.gray300};
`;
const Separator = (0, styled_1.default)(Value) `
  padding-right: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=conditions.jsx.map