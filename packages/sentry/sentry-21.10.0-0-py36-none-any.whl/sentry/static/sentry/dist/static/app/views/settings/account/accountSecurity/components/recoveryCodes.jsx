Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const RecoveryCodes = ({ className, isEnrolled, codes, onRegenerateBackupCodes, }) => {
    const printCodes = () => {
        // eslint-disable-next-line dot-notation
        const iframe = window.frames['printable'];
        iframe.document.write(codes.join('<br>'));
        iframe.print();
        iframe.document.close();
    };
    if (!isEnrolled || !codes) {
        return null;
    }
    const formattedCodes = codes.join(' \n');
    return (<CodeContainer className={className}>
      <panels_1.PanelHeader hasButtons>
        {(0, locale_1.t)('Unused Codes')}

        <Actions>
          <clipboard_1.default hideUnsupported value={formattedCodes}>
            <button_1.default size="small" label={(0, locale_1.t)('copy')}>
              <icons_1.IconCopy />
            </button_1.default>
          </clipboard_1.default>
          <button_1.default size="small" onClick={printCodes} label={(0, locale_1.t)('print')}>
            <icons_1.IconPrint />
          </button_1.default>
          <button_1.default size="small" download="sentry-recovery-codes.txt" href={`data:text/plain;charset=utf-8,${formattedCodes}`} label={(0, locale_1.t)('download')}>
            <icons_1.IconDownload />
          </button_1.default>
          <confirm_1.default onConfirm={onRegenerateBackupCodes} message={(0, locale_1.t)('Are you sure you want to regenerate recovery codes? Your old codes will no longer work.')}>
            <button_1.default priority="danger" size="small">
              {(0, locale_1.t)('Regenerate Codes')}
            </button_1.default>
          </confirm_1.default>
        </Actions>
      </panels_1.PanelHeader>
      <panels_1.PanelBody>
        <panels_1.PanelAlert type="warning">
          {(0, locale_1.t)('Make sure to save a copy of your recovery codes and store them in a safe place.')}
        </panels_1.PanelAlert>
        <div>{!!codes.length && codes.map(code => <Code key={code}>{code}</Code>)}</div>
        {!codes.length && (<emptyMessage_1.default>{(0, locale_1.t)('You have no more recovery codes to use')}</emptyMessage_1.default>)}
      </panels_1.PanelBody>
      <iframe name="printable" style={{ display: 'none' }}/>
    </CodeContainer>);
};
exports.default = RecoveryCodes;
const CodeContainer = (0, styled_1.default)(panels_1.Panel) `
  margin-top: ${(0, space_1.default)(4)};
`;
const Actions = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
`;
const Code = (0, styled_1.default)(panels_1.PanelItem) `
  font-family: ${p => p.theme.text.familyMono};
  padding: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=recoveryCodes.jsx.map