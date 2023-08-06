Object.defineProperty(exports, "__esModule", { value: true });
exports.GridCell = exports.Grid = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Grid = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  grid-template-columns: 30px 2.5fr 4fr 0fr 40px;
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 40px 2.5fr 3.5fr 105px 40px;
  }
`;
exports.Grid = Grid;
const GridCell = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
`;
exports.GridCell = GridCell;
//# sourceMappingURL=styles.jsx.map