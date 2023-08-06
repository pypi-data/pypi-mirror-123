Object.defineProperty(exports, "__esModule", { value: true });
exports.Assembly = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const Assembly = ({ name, version, culture, publicKeyToken, filePath }) => (<AssemblyWrapper>
    <AssemblyInfo>
      <Caption>Assembly:</Caption>
      {name || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>{(0, locale_1.t)('Version')}:</Caption>
      {version || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>{(0, locale_1.t)('Culture')}:</Caption>
      {culture || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>PublicKeyToken:</Caption>
      {publicKeyToken || '-'}
    </AssemblyInfo>

    {filePath && (<FilePathInfo>
        <Caption>{(0, locale_1.t)('Path')}:</Caption>
        <tooltip_1.default title={filePath}>
          <textCopyInput_1.default rtl>{filePath}</textCopyInput_1.default>
        </tooltip_1.default>
      </FilePathInfo>)}
  </AssemblyWrapper>);
exports.Assembly = Assembly;
// TODO(ts): we should be able to delete these after disabling react/prop-types rule in tsx functional components
const AssemblyWrapper = (0, styled_1.default)('div') `
  font-size: 80%;
  display: flex;
  flex-wrap: wrap;
  color: ${p => p.theme.textColor};
  text-align: center;
  position: relative;
  padding: 0 ${(0, space_1.default)(3)} 0 ${(0, space_1.default)(3)};
`;
const AssemblyInfo = (0, styled_1.default)('div') `
  margin-right: 15px;
  margin-bottom: 5px;
`;
const Caption = (0, styled_1.default)('span') `
  margin-right: 5px;
  font-weight: bold;
`;
const FilePathInfo = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-bottom: 5px;
  input {
    width: 300px;
    height: 20px;
    padding-top: 0;
    padding-bottom: 0;
    line-height: 1.5;
    @media (max-width: ${theme_1.default.breakpoints[1]}) {
      width: auto;
    }
  }
  button > span {
    padding: 2px 5px;
  }
  svg {
    width: 11px;
    height: 11px;
  }
`;
//# sourceMappingURL=assembly.jsx.map