Object.defineProperty(exports, "__esModule", { value: true });
exports.ChartContainer = exports.HeaderValue = exports.HeaderTitleLegend = exports.HeaderTitle = exports.ChartControls = exports.InlineContainer = exports.SectionValue = exports.SectionHeading = exports.SubHeading = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.SubHeading = (0, styled_1.default)('h3') `
  font-size: ${p => p.theme.fontSizeLarge};
  font-weight: normal;
  color: ${p => p.theme.textColor};
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
`;
exports.SectionHeading = (0, styled_1.default)('h4') `
  display: inline-grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  margin: ${(0, space_1.default)(1)} 0;
`;
exports.SectionValue = (0, styled_1.default)('span') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  margin-right: ${(0, space_1.default)(1)};
`;
exports.InlineContainer = (0, styled_1.default)('div') `
  display: grid;
  align-items: center;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-auto-flow: column;
    grid-column-gap: ${(0, space_1.default)(1)};
  }
`;
exports.ChartControls = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(3)};
  border-top: 1px solid ${p => p.theme.border};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
  }
`;
// Header element for charts within panels.
exports.HeaderTitle = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeLarge};
  color: ${p => p.theme.textColor};
  align-items: center;
`;
// Header element for charts within panels
// This header can be rendered while the chart is still loading
exports.HeaderTitleLegend = (0, styled_1.default)(exports.HeaderTitle) `
  background-color: ${p => p.theme.background};
  border-bottom-right-radius: ${p => p.theme.borderRadius};
  position: absolute;
  z-index: 1;
`;
// Used for rendering total value of a chart right below the HeaderTitleLegend
exports.HeaderValue = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: baseline;
  background-color: ${p => p.theme.background};
  position: absolute;
  top: 40px;
  z-index: 1;
  font-size: ${p => p.theme.headerFontSize};
`;
exports.ChartContainer = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)};
`;
//# sourceMappingURL=styles.jsx.map