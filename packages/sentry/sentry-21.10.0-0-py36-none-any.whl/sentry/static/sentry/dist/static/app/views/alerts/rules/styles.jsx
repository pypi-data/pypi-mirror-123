Object.defineProperty(exports, "__esModule", { value: true });
exports.TableLayout = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const TableLayout = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 60px 1.5fr 1fr 1fr 1fr 92px;
  grid-column-gap: ${(0, space_1.default)(1.5)};
  width: 100%;
  align-items: center;
`;
exports.TableLayout = TableLayout;
//# sourceMappingURL=styles.jsx.map