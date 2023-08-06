Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const BaseButton = (props) => (<button_1.default size="zero" {...props}/>);
const ActionButton = (0, styled_1.default)(BaseButton) `
  padding: ${p => (p.icon ? (0, space_1.default)(0.75) : '7px')} ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeSmall};
`;
exports.default = ActionButton;
//# sourceMappingURL=button.jsx.map