Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorPanel = exports.DoubleHeaderContainer = exports.GridCellNumber = exports.GridCell = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.GridCell = (0, styled_1.default)('div') `
  font-size: 14px;
`;
exports.GridCellNumber = (0, styled_1.default)(exports.GridCell) `
  text-align: right;
  font-variant-numeric: tabular-nums;
`;
exports.DoubleHeaderContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)} ${(0, space_1.default)(1)} ${(0, space_1.default)(3)};
  grid-gap: ${(0, space_1.default)(3)};
`;
exports.ErrorPanel = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  align-items: center;

  flex: 1;
  flex-shrink: 0;
  overflow: hidden;
  height: 200px;
  position: relative;
  border-color: transparent;
  margin-bottom: 0;
`;
//# sourceMappingURL=styles.jsx.map