Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const iconDownload_1 = require("app/icons/iconDownload");
const iconRefresh_1 = require("app/icons/iconRefresh");
const iconWarning_1 = require("app/icons/iconWarning");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function Status({ details, onEditRepository, onRevalidateItunesSession }) {
    const theme = (0, react_1.useTheme)();
    if (!details) {
        return <placeholder_1.default height="14px"/>;
    }
    const { pendingDownloads, promptItunesSession, appstoreCredentialsValid, lastCheckedBuilds, } = details !== null && details !== void 0 ? details : {};
    if (promptItunesSession) {
        return (<Wrapper color={theme.red300} onClick={onRevalidateItunesSession}>
        <StyledTooltip title={(0, locale_1.t)('Revalidate your iTunes session')} containerDisplayMode="inline-flex">
          <iconWarning_1.IconWarning size="sm"/>
        </StyledTooltip>
        {(0, locale_1.t)('iTunes Authentication required')}
      </Wrapper>);
    }
    if (appstoreCredentialsValid === false) {
        return (<Wrapper color={theme.red300} onClick={onEditRepository}>
        <StyledTooltip title={(0, locale_1.t)('Recheck your App Store Credentials')} containerDisplayMode="inline-flex">
          <iconWarning_1.IconWarning size="sm"/>
        </StyledTooltip>
        {(0, locale_1.t)('Credentials are invalid')}
      </Wrapper>);
    }
    if (pendingDownloads) {
        return (<Wrapper color={theme.gray400}>
        <IconWrapper>
          <iconDownload_1.IconDownload size="sm"/>
        </IconWrapper>
        {(0, locale_1.tn)('%s build pending', '%s builds pending', pendingDownloads)}
      </Wrapper>);
    }
    if (lastCheckedBuilds) {
        return (<Wrapper color={theme.gray400}>
        <IconWrapper>
          <iconRefresh_1.IconRefresh size="sm"/>
        </IconWrapper>
        <timeSince_1.default date={lastCheckedBuilds}/>
      </Wrapper>);
    }
    return null;
}
exports.default = Status;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(2, max-content);
  align-items: center;
  grid-gap: ${(0, space_1.default)(0.75)};
  color: ${p => p.color};
  font-size: ${p => p.theme.fontSizeMedium};
  height: 14px;
  ${p => p.onClick && `cursor: pointer`};
`;
const StyledTooltip = (0, styled_1.default)(tooltip_1.default) `
  margin-top: -5px;
  height: 14px;
`;
const IconWrapper = (0, styled_1.default)('div') `
  margin-top: -5px;
  height: 14px;
`;
//# sourceMappingURL=status.jsx.map