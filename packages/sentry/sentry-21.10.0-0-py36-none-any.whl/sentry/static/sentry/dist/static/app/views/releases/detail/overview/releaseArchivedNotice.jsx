Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
function ReleaseArchivedNotice({ onRestore, multi }) {
    return (<alert_1.default icon={<icons_1.IconInfo size="md"/>} type="warning">
      {multi
            ? (0, locale_1.t)('These releases have been archived.')
            : (0, locale_1.t)('This release has been archived.')}

      {!multi && onRestore && (<react_1.Fragment>
          {' '}
          <UnarchiveButton size="zero" priority="link" onClick={onRestore}>
            {(0, locale_1.t)('Restore this release')}
          </UnarchiveButton>
        </react_1.Fragment>)}
    </alert_1.default>);
}
const UnarchiveButton = (0, styled_1.default)(button_1.default) `
  font-size: inherit;
  text-decoration: underline;
  &,
  &:hover,
  &:focus,
  &:active {
    color: ${p => p.theme.textColor};
  }
`;
exports.default = ReleaseArchivedNotice;
//# sourceMappingURL=releaseArchivedNotice.jsx.map