Object.defineProperty(exports, "__esModule", { value: true });
exports.SearchWrapper = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.SearchWrapper = (0, styled_1.default)('div') `
  display: flex;
  grid-template-columns: 1fr max-content;
  grid-gap: ${(0, space_1.default)(1.5)};
  margin-top: ${(0, space_1.default)(4)};
  margin-bottom: ${(0, space_1.default)(1.5)};
  position: relative;
`;
//# sourceMappingURL=defaultSearchBar.jsx.map