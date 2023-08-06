Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function OnboardingPanel({ className, image, children }) {
    return (<panels_1.Panel className={className}>
      <Container>
        <IlloBox>{image}</IlloBox>
        <StyledBox>{children}</StyledBox>
      </Container>
    </panels_1.Panel>);
}
const Container = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(3)};
  position: relative;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: flex;
    align-items: center;
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
    min-height: 300px;
    max-width: 1000px;
    margin: 0 auto;
  }

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    min-height: 350px;
  }
`;
const StyledBox = (0, styled_1.default)('div') `
  z-index: 1;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    flex: 2;
  }
`;
const IlloBox = (0, styled_1.default)(StyledBox) `
  position: relative;
  min-height: 100px;
  max-width: 300px;
  margin: ${(0, space_1.default)(2)} auto;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    flex: 1;
    margin: ${(0, space_1.default)(3)};
    max-width: auto;
  }
`;
exports.default = OnboardingPanel;
//# sourceMappingURL=onboardingPanel.jsx.map