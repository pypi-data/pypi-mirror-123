Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Header = (0, styled_1.default)(panels_1.PanelHeader) `
  border-top-left-radius: 0;
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
  font-size: ${p => p.theme.fontSizeSmall};
`;
exports.default = Header;
//# sourceMappingURL=header.jsx.map