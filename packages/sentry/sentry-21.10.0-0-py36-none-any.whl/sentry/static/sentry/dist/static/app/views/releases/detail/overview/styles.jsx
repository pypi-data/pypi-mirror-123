Object.defineProperty(exports, "__esModule", { value: true });
exports.SectionHeading = exports.Wrapper = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.Wrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(3)};
`;
exports.SectionHeading = (0, styled_1.default)(styles_1.SectionHeading) `
  margin: 0 0 ${(0, space_1.default)(1.5)} 0;
`;
//# sourceMappingURL=styles.jsx.map