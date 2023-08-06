Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const stacktrace_1 = require("app/types/stacktrace");
const CrashActions = ({ hasHierarchicalGrouping, stackView, stackType, stacktrace, thread, exception, platform, onChange, }) => {
    var _a, _b;
    const hasSystemFrames = (stacktrace === null || stacktrace === void 0 ? void 0 : stacktrace.hasSystemFrames) ||
        !!((_a = exception === null || exception === void 0 ? void 0 : exception.values) === null || _a === void 0 ? void 0 : _a.find(value => { var _a; return !!((_a = value.stacktrace) === null || _a === void 0 ? void 0 : _a.hasSystemFrames); }));
    const hasMinified = !stackType
        ? false
        : !!((_b = exception === null || exception === void 0 ? void 0 : exception.values) === null || _b === void 0 ? void 0 : _b.find(value => value.rawStacktrace)) || !!(thread === null || thread === void 0 ? void 0 : thread.rawStacktrace);
    const notify = (options) => {
        if (onChange) {
            onChange(options);
        }
    };
    const setStackType = (type) => () => {
        notify({ stackType: type });
    };
    const setStackView = (view) => () => {
        notify({ stackView: view });
    };
    const getOriginalButtonLabel = () => {
        if (platform === 'javascript' || platform === 'node') {
            return (0, locale_1.t)('Original');
        }
        return (0, locale_1.t)('Symbolicated');
    };
    const getMinifiedButtonLabel = () => {
        if (platform === 'javascript' || platform === 'node') {
            return (0, locale_1.t)('Minified');
        }
        return (0, locale_1.t)('Unsymbolicated');
    };
    return (<ButtonGroupWrapper>
      <buttonBar_1.default active={stackView} merged>
        {hasSystemFrames && (<button_1.default barId={stacktrace_1.STACK_VIEW.APP} size="xsmall" onClick={setStackView(stacktrace_1.STACK_VIEW.APP)} title={hasHierarchicalGrouping
                ? (0, locale_1.t)('The stack trace only shows application frames and frames responsible for grouping this issue')
                : undefined}>
            {hasHierarchicalGrouping ? (0, locale_1.t)('Most Relevant') : (0, locale_1.t)('App Only')}
          </button_1.default>)}
        <button_1.default barId={stacktrace_1.STACK_VIEW.FULL} size="xsmall" onClick={setStackView(stacktrace_1.STACK_VIEW.FULL)}>
          {(0, locale_1.t)('Full')}
        </button_1.default>
        <button_1.default barId={stacktrace_1.STACK_VIEW.RAW} onClick={setStackView(stacktrace_1.STACK_VIEW.RAW)} size="xsmall">
          {(0, locale_1.t)('Raw')}
        </button_1.default>
      </buttonBar_1.default>
      {hasMinified && (<buttonBar_1.default active={stackType} merged>
          <button_1.default barId={stacktrace_1.STACK_TYPE.ORIGINAL} size="xsmall" onClick={setStackType(stacktrace_1.STACK_TYPE.ORIGINAL)}>
            {getOriginalButtonLabel()}
          </button_1.default>
          <button_1.default barId={stacktrace_1.STACK_TYPE.MINIFIED} size="xsmall" onClick={setStackType(stacktrace_1.STACK_TYPE.MINIFIED)}>
            {getMinifiedButtonLabel()}
          </button_1.default>
        </buttonBar_1.default>)}
    </ButtonGroupWrapper>);
};
exports.default = CrashActions;
const ButtonGroupWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
  > * {
    padding: ${(0, space_1.default)(0.5)} 0;
  }
  > *:not(:last-child) {
    margin-right: ${(0, space_1.default)(1)};
  }
`;
//# sourceMappingURL=crashActions.jsx.map