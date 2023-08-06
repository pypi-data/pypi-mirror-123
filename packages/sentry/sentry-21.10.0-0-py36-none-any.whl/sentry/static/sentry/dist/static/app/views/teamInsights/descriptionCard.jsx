Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function DescriptionCard({ title, description, children }) {
    return (<Wrapper>
      <LeftPanel>
        <Title>{title}</Title>
        <Description>{description}</Description>
      </LeftPanel>
      <RightPanel>{children}</RightPanel>
    </Wrapper>);
}
exports.default = DescriptionCard;
const Wrapper = (0, styled_1.default)('div') `
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius};
  display: flex;
  margin-bottom: ${(0, space_1.default)(3)};
  flex-direction: column;

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    flex-direction: row;
  }
`;
const LeftPanel = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    max-width: 250px;
    border-right: 1px solid ${p => p.theme.border};
    border-bottom: 0;
  }
`;
const Title = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeLarge};
  margin: 0 0 ${(0, space_1.default)(0.5)};
`;
const Description = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
`;
const RightPanel = (0, styled_1.default)('div') `
  flex-grow: 1;
`;
//# sourceMappingURL=descriptionCard.jsx.map