Object.defineProperty(exports, "__esModule", { value: true });
exports.PerformanceLayoutBodyRow = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
/**
 * Common performance layouts
 */
exports.PerformanceLayoutBodyRow = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr;
  grid-column-gap: ${(0, space_1.default)(2)};
  grid-row-gap: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    ${p => p.columns
    ? `
    grid-template-columns: repeat(${p.columns}, 1fr);
    `
    : `
    grid-template-columns: repeat(auto-fit, minmax(${p.minSize}px, 1fr));
    `}
  }
`;
//# sourceMappingURL=index.jsx.map