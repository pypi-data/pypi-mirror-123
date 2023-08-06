Object.defineProperty(exports, "__esModule", { value: true });
exports.HeaderTitle = exports.PageHeader = exports.PageContent = void 0;
const tslib_1 = require("tslib");
// Shared styles for the new org level pages with global project/env/time selection
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.PageContent = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(4)} ${(0, space_1.default)(3)};
  margin-bottom: -20px; /* <footer> has margin-top: 20px; */

  /* No footer at smallest breakpoint */
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    margin-bottom: 0;
  }
`;
exports.PageHeader = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(2)};
  min-height: 32px;
`;
exports.HeaderTitle = (0, styled_1.default)('h4') `
  flex: 1;
  font-size: ${p => p.theme.headerFontSize};
  line-height: ${p => p.theme.headerFontSize};
  font-weight: normal;
  color: ${p => p.theme.textColor};
  margin: 0;
`;
//# sourceMappingURL=organization.jsx.map