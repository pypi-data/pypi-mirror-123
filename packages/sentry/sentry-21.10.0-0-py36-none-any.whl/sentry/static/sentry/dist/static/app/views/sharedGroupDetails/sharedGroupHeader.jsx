Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const eventMessage_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventMessage"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const unhandledTag_1 = (0, tslib_1.__importStar)(require("../organizationGroupDetails/unhandledTag"));
const SharedGroupHeader = ({ group }) => (<Wrapper>
    <Details>
      <Title>{group.title}</Title>
      <unhandledTag_1.TagAndMessageWrapper>
        {group.isUnhandled && <unhandledTag_1.default />}
        <eventMessage_1.default message={group.culprit}/>
      </unhandledTag_1.TagAndMessageWrapper>
    </Details>
  </Wrapper>);
exports.default = SharedGroupHeader;
const Wrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(4)} ${(0, space_1.default)(3)} ${(0, space_1.default)(4)};
  border-bottom: ${p => `1px solid ${p.theme.border}`};
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);
  position: relative;
  margin: 0 0 ${(0, space_1.default)(3)};
`;
const Details = (0, styled_1.default)('div') `
  max-width: 960px;
  margin: 0 auto;
`;
// TODO(style): the color #161319 is not yet in the color object of the theme
const Title = (0, styled_1.default)('h3') `
  color: #161319;
  margin: 0 0 ${(0, space_1.default)(1)};
  overflow-wrap: break-word;
  line-height: 1.2;
  font-size: ${p => p.theme.fontSizeExtraLarge};
  @media (min-width: ${props => props.theme.breakpoints[0]}) {
    font-size: ${p => p.theme.headerFontSize};
    line-height: 1.1;
    ${overflowEllipsis_1.default};
  }
`;
//# sourceMappingURL=sharedGroupHeader.jsx.map