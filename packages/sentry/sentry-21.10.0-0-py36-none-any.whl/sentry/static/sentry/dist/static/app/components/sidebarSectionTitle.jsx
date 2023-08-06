Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
/**
 * Used to add a new subheading in a sidebar section.
 */
function SidebarSectionTitle(_a) {
    var { title, icon } = _a, props = (0, tslib_1.__rest)(_a, ["title", "icon"]);
    return (<Heading {...props}>
      {title}
      {icon && <IconWrapper>{icon}</IconWrapper>}
    </Heading>);
}
const Heading = (0, styled_1.default)('h6') `
  color: ${p => p.theme.gray400};
  display: flex;
  font-size: ${p => p.theme.fontSizeMedium};
  margin-bottom: ${(0, space_1.default)(1)};
`;
const IconWrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray200};
  margin-left: ${(0, space_1.default)(0.5)};
`;
exports.default = SidebarSectionTitle;
//# sourceMappingURL=sidebarSectionTitle.jsx.map