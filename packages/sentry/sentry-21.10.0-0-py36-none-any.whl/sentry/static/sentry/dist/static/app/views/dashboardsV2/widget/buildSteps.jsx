Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function BuildSteps({ children }) {
    return <StyledList symbol="colored-numeric">{children}</StyledList>;
}
exports.default = BuildSteps;
const StyledList = (0, styled_1.default)(list_1.default) `
  display: grid;
  grid-gap: ${(0, space_1.default)(4)};
  max-width: 100%;

  @media (min-width: ${p => p.theme.breakpoints[4]}) {
    max-width: 50%;
  }
`;
//# sourceMappingURL=buildSteps.jsx.map