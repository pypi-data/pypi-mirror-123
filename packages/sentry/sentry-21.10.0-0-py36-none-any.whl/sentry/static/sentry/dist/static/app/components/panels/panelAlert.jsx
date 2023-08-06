Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const DEFAULT_ICONS = {
    info: <icons_1.IconInfo size="md"/>,
    error: <icons_1.IconClose isCircled size="md"/>,
    warning: <icons_1.IconFlag size="md"/>,
    success: <icons_1.IconCheckmark isCircled size="md"/>,
};
// Margin bottom should probably be a different prop
const PanelAlert = (0, styled_1.default)((_a) => {
    var { icon } = _a, props = (0, tslib_1.__rest)(_a, ["icon"]);
    return (<alert_1.default {...props} icon={icon || DEFAULT_ICONS[props.type]} system/>);
}) `
  margin: 0 0 1px 0;
  padding: ${(0, space_1.default)(2)};
  border-radius: 0;
  box-shadow: none;

  &:last-child {
    border-bottom: none;
    margin: 0;
    border-radius: 0 0 4px 4px;
  }
`;
exports.default = PanelAlert;
//# sourceMappingURL=panelAlert.jsx.map