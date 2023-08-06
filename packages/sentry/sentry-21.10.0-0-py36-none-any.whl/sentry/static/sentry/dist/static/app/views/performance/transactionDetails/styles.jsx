Object.defineProperty(exports, "__esModule", { value: true });
exports.SectionSubtext = exports.MetaData = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function MetaData({ headingText, tooltipText, bodyText, subtext, badge, }) {
    return (<HeaderInfo>
      <StyledSectionHeading>
        {headingText}
        <questionTooltip_1.default position="top" size="sm" containerDisplayMode="block" title={tooltipText}/>
        {badge && <StyledFeatureBadge type={badge}/>}
      </StyledSectionHeading>
      <SectionBody>{bodyText}</SectionBody>
      <exports.SectionSubtext>{subtext}</exports.SectionSubtext>
    </HeaderInfo>);
}
exports.MetaData = MetaData;
const HeaderInfo = (0, styled_1.default)('div') `
  height: 78px;
`;
const StyledSectionHeading = (0, styled_1.default)(styles_1.SectionHeading) `
  margin: 0;
`;
const SectionBody = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  padding: ${(0, space_1.default)(0.5)} 0;
  max-height: 32px;
`;
const StyledFeatureBadge = (0, styled_1.default)(featureBadge_1.default) `
  margin: 0;
`;
exports.SectionSubtext = (0, styled_1.default)('div') `
  color: ${p => (p.type === 'error' ? p.theme.error : p.theme.subText)};
  font-size: ${p => p.theme.fontSizeMedium};
`;
//# sourceMappingURL=styles.jsx.map