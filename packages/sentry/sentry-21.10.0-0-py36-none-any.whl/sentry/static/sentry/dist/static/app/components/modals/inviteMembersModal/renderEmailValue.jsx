Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_select_1 = require("react-select");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function renderEmailValue(status, valueProps) {
    const { children } = valueProps, props = (0, tslib_1.__rest)(valueProps, ["children"]);
    const error = status && status.error;
    const emailLabel = status === undefined ? (children) : (<tooltip_1.default disabled={!error} title={error}>
        <EmailLabel>
          {children}
          {!status.sent && !status.error && <SendingIndicator />}
          {status.error && <icons_1.IconWarning size="10px"/>}
          {status.sent && <icons_1.IconCheckmark size="10px" color="success"/>}
        </EmailLabel>
      </tooltip_1.default>);
    return (<react_select_1.components.MultiValue {...props}>{emailLabel}</react_select_1.components.MultiValue>);
}
const EmailLabel = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(0.5)};
  align-items: center;
`;
const SendingIndicator = (0, styled_1.default)(loadingIndicator_1.default) `
  margin: 0;
  .loading-indicator {
    border-width: 2px;
  }
`;
SendingIndicator.defaultProps = {
    hideMessage: true,
    size: 14,
};
exports.default = renderEmailValue;
//# sourceMappingURL=renderEmailValue.jsx.map