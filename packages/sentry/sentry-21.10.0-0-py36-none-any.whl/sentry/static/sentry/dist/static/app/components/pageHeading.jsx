Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const PageHeading = (0, styled_1.default)('h1') `
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.headerFontSize};
  line-height: ${p => p.theme.headerFontSize};
  font-weight: normal;
  margin: 0;
  margin-bottom: ${p => p.withMargins && (0, space_1.default)(3)};
  margin-top: ${p => p.withMargins && (0, space_1.default)(1)};
`;
exports.default = PageHeading;
//# sourceMappingURL=pageHeading.jsx.map