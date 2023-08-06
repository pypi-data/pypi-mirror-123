Object.defineProperty(exports, "__esModule", { value: true });
exports.StatNumber = exports.Description = exports.CardSectionHeading = exports.CardSummary = exports.CardSection = exports.Card = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const panels_1 = require("app/components/panels");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.Card = (0, styled_1.default)(panels_1.PanelItem) `
  display: grid;
  grid-template-columns: 325px minmax(100px, auto);
  padding: 0;
`;
exports.CardSection = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(3)};
`;
exports.CardSummary = (0, styled_1.default)(exports.CardSection) `
  position: relative;
  border-right: 1px solid ${p => p.theme.border};
  grid-column: 1/1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`;
exports.CardSectionHeading = (0, styled_1.default)(styles_1.SectionHeading) `
  margin: 0px;
`;
exports.Description = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.subText};
`;
exports.StatNumber = (0, styled_1.default)('div') `
  font-size: 32px;
`;
//# sourceMappingURL=styles.jsx.map