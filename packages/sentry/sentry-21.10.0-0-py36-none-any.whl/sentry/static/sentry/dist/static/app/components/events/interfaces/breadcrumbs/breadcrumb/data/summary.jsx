Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const contextData_1 = (0, tslib_1.__importDefault)(require("app/components/contextData"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function Summary({ kvData, children }) {
    if (!kvData || !Object.keys(kvData).length) {
        if (!children) {
            return <div />;
        }
        return (<Wrapper>
        <StyledCode>{children}</StyledCode>
      </Wrapper>);
    }
    return (<Wrapper>
      {children && <StyledCode>{children}</StyledCode>}
      <ContextDataWrapper>
        <contextData_1.default data={kvData} withAnnotatedText/>
      </ContextDataWrapper>
    </Wrapper>);
}
exports.default = Summary;
const Wrapper = (0, styled_1.default)('div') `
  word-break: break-all;
  font-size: ${p => p.theme.fontSizeSmall};
  font-family: ${p => p.theme.text.familyMono};
  display: grid;
  grid-gap: ${(0, space_1.default)(0.5)};
  overflow: hidden;
`;
const ContextDataWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1)};
  background: ${p => p.theme.backgroundSecondary};
  border-radius: ${p => p.theme.borderRadius};
  overflow: hidden;

  pre {
    background: ${p => p.theme.backgroundSecondary};
    margin: 0;
    padding: 0;
    overflow: hidden;
    overflow-y: auto;
    max-height: 100%;
  }
`;
const StyledCode = (0, styled_1.default)('code') `
  font-size: inherit;
  white-space: pre-wrap;
  background: none;
  padding: 0;
  > * {
    vertical-align: middle;
  }
`;
//# sourceMappingURL=summary.jsx.map