Object.defineProperty(exports, "__esModule", { value: true });
exports.tableLayout = void 0;
const tslib_1 = require("tslib");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.tableLayout = `
  display: grid;
  grid-template-columns: auto 140px 140px;
  grid-gap ${(0, space_1.default)(1)};
  align-items: center;
`;
//# sourceMappingURL=utils.jsx.map