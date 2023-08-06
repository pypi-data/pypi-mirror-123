Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Item = (0, styled_1.default)(({ title, subtitle, children, className }) => (<listItem_1.default className={className}>
    {title}
    {subtitle && <small>{subtitle}</small>}
    <div>{children}</div>
  </listItem_1.default>)) `
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
`;
exports.default = Item;
//# sourceMappingURL=item.jsx.map