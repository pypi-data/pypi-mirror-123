Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function EventTitleError() {
    return (<Wrapper>
      <Title>{(0, locale_1.t)('<unknown>')}</Title>
      <ErrorMessage>{(0, locale_1.t)('There was an error rendering the title')}</ErrorMessage>
    </Wrapper>);
}
exports.default = EventTitleError;
const Wrapper = (0, styled_1.default)('span') `
  display: flex;
  flex-wrap: wrap;
`;
const Title = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
const ErrorMessage = (0, styled_1.default)('span') `
  color: ${p => p.theme.alert.error.iconColor};
  background: ${p => p.theme.alert.error.backgroundLight};
  font-size: ${p => p.theme.fontSizeMedium};
  padding: 0 ${(0, space_1.default)(0.5)};
  border-radius: ${p => p.theme.borderRadius};
  display: flex;
  align-items: center;
`;
//# sourceMappingURL=eventTitleError.jsx.map