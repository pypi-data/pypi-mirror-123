Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icon_1 = (0, tslib_1.__importDefault)(require("./icon"));
function Type({ type, color, description, error }) {
    return (<Wrapper error={error}>
      <tooltip_1.default title={description} disabled={!description}>
        <IconWrapper color={color}>
          <icon_1.default type={type}/>
        </IconWrapper>
      </tooltip_1.default>
    </Wrapper>);
}
exports.default = Type;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  position: relative;
  :before {
    content: '';
    display: block;
    width: 1px;
    top: 0;
    bottom: 0;
    left: 50%;
    transform: translate(-50%);
    position: absolute;
    background: ${p => (p.error ? p.theme.red300 : p.theme.innerBorder)};
  }
`;
const IconWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  color: ${p => p.theme.white};
  background: ${p => { var _a; return (_a = p.theme[p.color]) !== null && _a !== void 0 ? _a : p.color; }};
  box-shadow: ${p => p.theme.dropShadowLightest};
  position: relative;
`;
//# sourceMappingURL=index.jsx.map