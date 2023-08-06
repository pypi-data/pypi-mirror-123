Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function BuildStep({ title, description, children }) {
    return (<StyledListItem>
      <Header>
        <Description>{title}</Description>
        <SubDescription>{description}</SubDescription>
      </Header>
      <Content>{children}</Content>
    </StyledListItem>);
}
exports.default = BuildStep;
const StyledListItem = (0, styled_1.default)(listItem_1.default) `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
`;
const Description = (0, styled_1.default)('h4') `
  font-weight: 400;
  margin-bottom: 0;
`;
const SubDescription = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeMedium};
`;
const Header = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(0.5)};
`;
const Content = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr max-content;
`;
//# sourceMappingURL=buildStep.jsx.map