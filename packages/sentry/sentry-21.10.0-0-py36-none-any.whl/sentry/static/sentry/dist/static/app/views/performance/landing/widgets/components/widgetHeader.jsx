Object.defineProperty(exports, "__esModule", { value: true });
exports.WidgetHeader = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function WidgetHeader(props) {
    const { title, titleTooltip, subtitle, HeaderActions } = props;
    return (<WidgetHeaderContainer>
      <TitleContainer>
        <StyledHeaderTitleLegend data-test-id="performance-widget-title">
          {title}
          <questionTooltip_1.default position="top" size="sm" title={titleTooltip}/>
        </StyledHeaderTitleLegend>
        <div>{subtitle ? subtitle : null}</div>
      </TitleContainer>

      {HeaderActions && (<HeaderActionsContainer>
          {HeaderActions && <HeaderActions {...props}/>}
        </HeaderActionsContainer>)}
    </WidgetHeaderContainer>);
}
exports.WidgetHeader = WidgetHeader;
const StyledHeaderTitleLegend = (0, styled_1.default)(styles_1.HeaderTitleLegend) `
  position: relative;
  z-index: initial;
`;
const TitleContainer = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
`;
const WidgetHeaderContainer = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
`;
const HeaderActionsContainer = (0, styled_1.default)('div') `
  display: flex;
  gap: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=widgetHeader.jsx.map