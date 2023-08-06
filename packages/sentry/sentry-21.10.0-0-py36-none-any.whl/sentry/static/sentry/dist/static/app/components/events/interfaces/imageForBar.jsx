Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const functionName_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/frame/functionName"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const ImageForBar = ({ frame, onShowAllImages }) => {
    const handleShowAllImages = () => {
        onShowAllImages('');
    };
    return (<Wrapper>
      <MatchedFunctionWrapper>
        <MatchedFunctionCaption>{(0, locale_1.t)('Image for: ')}</MatchedFunctionCaption>
        <functionName_1.default frame={frame}/>
      </MatchedFunctionWrapper>
      <ResetAddressFilterCaption onClick={handleShowAllImages}>
        {(0, locale_1.t)('Show all images')}
      </ResetAddressFilterCaption>
    </Wrapper>);
};
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(2)};
  background: ${p => p.theme.backgroundSecondary};
  border-bottom: 1px solid ${p => p.theme.border};
  font-weight: 700;
  code {
    color: ${p => p.theme.blue300};
    font-size: ${p => p.theme.fontSizeSmall};
    background: ${p => p.theme.backgroundSecondary};
  }
  a {
    color: ${p => p.theme.blue300};
    &:hover {
      text-decoration: underline;
    }
  }
`;
const MatchedFunctionWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: baseline;
`;
const MatchedFunctionCaption = (0, styled_1.default)('span') `
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 400;
  color: ${p => p.theme.gray300};
  flex-shrink: 0;
`;
const ResetAddressFilterCaption = (0, styled_1.default)('a') `
  display: flex;
  flex-shrink: 0;
  padding-left: ${(0, space_1.default)(0.5)};
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 400;
  color: ${p => p.theme.gray300} !important;
  &:hover {
    color: ${p => p.theme.gray300} !important;
  }
`;
exports.default = ImageForBar;
//# sourceMappingURL=imageForBar.jsx.map