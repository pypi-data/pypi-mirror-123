Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const MenuItem = (0, styled_1.default)('div') `
  font-size: 14px;
  ${overflowEllipsis_1.default};
`;
exports.default = MenuItem;
//# sourceMappingURL=menuItem.jsx.map