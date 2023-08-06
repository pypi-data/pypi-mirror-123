Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const progressRing_1 = (0, tslib_1.__importDefault)(require("app/components/progressRing"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function ProgressHeader({ allTasks, completedTasks }) {
    const theme = (0, react_1.useTheme)();
    return (<Container>
      <StyledProgressRing size={80} barWidth={8} text={allTasks.length - completedTasks.length} animateText value={(completedTasks.length / allTasks.length) * 100} progressEndcaps="round" backgroundColor={theme.gray100} textCss={() => (0, react_1.css) `
          font-size: 26px;
          color: ${theme.textColor};
        `}/>
      <HeaderTitle>{(0, locale_1.t)('Quick Start')}</HeaderTitle>
      <Description>
        {(0, locale_1.t)("Take full advantage of Sentry's powerful monitoring features.")}
      </Description>
    </Container>);
}
exports.default = ProgressHeader;
const Container = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: min-content 1fr;
  grid-template-rows: min-content 1fr;
  grid-column-gap: ${(0, space_1.default)(2)};
  margin: 90px ${(0, space_1.default)(4)} 0 ${(0, space_1.default)(4)};
`;
const StyledProgressRing = (0, styled_1.default)(progressRing_1.default) `
  grid-column: 1/2;
  grid-row: 1/3;
`;
const HeaderTitle = (0, styled_1.default)('h3') `
  margin: 0;
  grid-column: 2/3;
  grid-row: 1/2;
`;
const Description = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  grid-column: 2/3;
  grid-row: 2/3;
`;
//# sourceMappingURL=progressHeader.jsx.map