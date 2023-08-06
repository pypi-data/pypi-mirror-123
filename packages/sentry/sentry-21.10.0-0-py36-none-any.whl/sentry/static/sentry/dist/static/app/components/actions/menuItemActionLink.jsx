Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const actionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/actionLink"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
function MenuItemActionLink(_a) {
    var { className } = _a, props = (0, tslib_1.__rest)(_a, ["className"]);
    return (<menuItem_1.default noAnchor withBorder disabled={props.disabled} className={className}>
      <InnerActionLink {...props}/>
    </menuItem_1.default>);
}
const InnerActionLink = (0, styled_1.default)(actionLink_1.default) `
  color: ${p => p.theme.textColor};
  ${overflowEllipsis_1.default}
  &:hover {
    color: ${p => p.theme.textColor};
  }

  .dropdown-menu > li > &,
  .dropdown-menu > span > li > & {
    &.disabled:hover {
      background: ${p => p.theme.white};
      color: #7a8188;
    }
  }
`;
exports.default = MenuItemActionLink;
//# sourceMappingURL=menuItemActionLink.jsx.map