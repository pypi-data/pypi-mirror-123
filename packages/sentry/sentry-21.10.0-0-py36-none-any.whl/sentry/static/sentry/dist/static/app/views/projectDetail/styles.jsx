Object.defineProperty(exports, "__esModule", { value: true });
exports.SectionHeadingLink = exports.SectionHeadingWrapper = exports.SidebarSection = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.SidebarSection = (0, styled_1.default)('section') `
  margin-bottom: ${(0, space_1.default)(2)};

  ${styles_1.SectionHeading} {
    line-height: 1;
  }
`;
exports.SectionHeadingWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
`;
exports.SectionHeadingLink = (0, styled_1.default)(globalSelectionLink_1.default) `
  display: flex;
`;
//# sourceMappingURL=styles.jsx.map