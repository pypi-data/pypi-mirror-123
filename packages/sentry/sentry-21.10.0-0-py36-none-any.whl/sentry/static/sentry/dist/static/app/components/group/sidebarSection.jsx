Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Heading = (0, styled_1.default)('h5') `
  display: flex;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(2)};
  font-size: ${p => p.theme.fontSizeMedium};

  &:after {
    flex: 1;
    display: block;
    content: '';
    border-top: 1px solid ${p => p.theme.innerBorder};
    margin-left: ${(0, space_1.default)(1)};
  }
`;
const Subheading = (0, styled_1.default)('h6') `
  color: ${p => p.theme.gray300};
  display: flex;
  font-size: ${p => p.theme.fontSizeExtraSmall};
  text-transform: uppercase;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(1)};
`;
/**
 * Used to add a new section in Issue Details' sidebar.
 */
function SidebarSection(_a) {
    var { title, children, secondary } = _a, props = (0, tslib_1.__rest)(_a, ["title", "children", "secondary"]);
    const HeaderComponent = secondary ? Subheading : Heading;
    return (<React.Fragment>
      <HeaderComponent {...props}>{title}</HeaderComponent>
      <SectionContent secondary={secondary}>{children}</SectionContent>
    </React.Fragment>);
}
const SectionContent = (0, styled_1.default)('div') `
  margin-bottom: ${p => (p.secondary ? (0, space_1.default)(2) : (0, space_1.default)(3))};
`;
exports.default = SidebarSection;
//# sourceMappingURL=sidebarSection.jsx.map