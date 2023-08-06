Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const MenuHeader = (0, styled_1.default)(menuItem_1.default) `
  text-transform: uppercase;
  font-weight: 600;
  color: ${p => p.theme.gray400};
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  padding: ${(0, space_1.default)(1)};
`;
MenuHeader.defaultProps = {
    header: true,
};
exports.default = MenuHeader;
//# sourceMappingURL=menuHeader.jsx.map