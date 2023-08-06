Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getPadding = ({ disablePadding, hasButtons }) => (0, react_1.css) `
  padding: ${hasButtons ? (0, space_1.default)(1) : (0, space_1.default)(2)} ${disablePadding ? 0 : (0, space_1.default)(2)};
  padding-right: ${hasButtons ? (0, space_1.default)(1) : null};
`;
const PanelHeader = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: ${p => (p.lightText ? p.theme.gray300 : p.theme.gray400)};
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 600;
  text-transform: uppercase;
  border-bottom: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius} ${p => p.theme.borderRadius} 0 0;
  background: ${p => p.theme.backgroundSecondary};
  line-height: 1;
  position: relative;
  ${getPadding};
`;
exports.default = PanelHeader;
//# sourceMappingURL=panelHeader.jsx.map