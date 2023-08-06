Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const kebabCase_1 = (0, tslib_1.__importDefault)(require("lodash/kebabCase"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const eventDataSection_1 = (0, tslib_1.__importStar)(require("app/components/events/eventDataSection"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function DataSection(_a) {
    var { title, description, children, className } = _a, props = (0, tslib_1.__rest)(_a, ["title", "description", "children", "className"]);
    const type = (0, kebabCase_1.default)(title);
    return (<StyledEventDataSection {...props} className={className} type={type} title={<TitleWrapper>
          <guideAnchor_1.default target={type} position="bottom">
            <Title>{title}</Title>
          </guideAnchor_1.default>
          <questionTooltip_1.default size="xs" position="top" title={description}/>
        </TitleWrapper>} wrapTitle={false}>
      {children}
    </StyledEventDataSection>);
}
exports.default = DataSection;
const TitleWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(2, max-content);
  grid-gap: ${(0, space_1.default)(0.5)};
  align-items: center;
  padding: ${(0, space_1.default)(0.75)} 0;
`;
const Title = (0, styled_1.default)('h3') `
  margin-bottom: 0;
  padding: 0 !important;
  height: 14px;
`;
const StyledEventDataSection = (0, styled_1.default)(eventDataSection_1.default) `
  ${eventDataSection_1.SectionContents} {
    flex: 1;
  }

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    && {
      padding: 0;
      border: 0;
    }
  }
`;
//# sourceMappingURL=dataSection.jsx.map