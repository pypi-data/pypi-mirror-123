Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const hovercard_1 = require("app/components/hovercard");
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const versionHoverCard_1 = (0, tslib_1.__importDefault)(require("app/components/versionHoverCard"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
class SeenInfo extends React.Component {
    shouldComponentUpdate(nextProps) {
        var _a;
        const { date, release } = this.props;
        return (release === null || release === void 0 ? void 0 : release.version) !== ((_a = nextProps.release) === null || _a === void 0 ? void 0 : _a.version) || date !== nextProps.date;
    }
    getReleaseTrackingUrl() {
        const { organization, projectSlug } = this.props;
        const orgSlug = organization.slug;
        return `/settings/${orgSlug}/projects/${projectSlug}/release-tracking/`;
    }
    render() {
        const { date, dateGlobal, environment, release, organization, projectSlug, projectId } = this.props;
        return (<HovercardWrapper>
        <StyledHovercard header={<div>
              <TimeSinceWrapper>
                {(0, locale_1.t)('Any Environment')}
                <timeSince_1.default date={dateGlobal} disabledAbsoluteTooltip/>
              </TimeSinceWrapper>
              {environment && (<TimeSinceWrapper>
                  {(0, utils_1.toTitleCase)(environment)}
                  {date ? (<timeSince_1.default date={date} disabledAbsoluteTooltip/>) : (<span>{(0, locale_1.t)('N/A')}</span>)}
                </TimeSinceWrapper>)}
            </div>} body={date ? (<StyledDateTime date={date}/>) : (<NoEnvironment>{(0, locale_1.t)(`N/A for ${environment}`)}</NoEnvironment>)} position="top" tipColor={theme_1.default.gray500}>
          <DateWrapper>
            {date ? (<TooltipWrapper>
                <StyledTimeSince date={date} disabledAbsoluteTooltip/>
              </TooltipWrapper>) : dateGlobal && environment === '' ? (<React.Fragment>
                <timeSince_1.default date={dateGlobal} disabledAbsoluteTooltip/>
                <StyledTimeSince date={dateGlobal} disabledAbsoluteTooltip/>
              </React.Fragment>) : (<NoDateTime>{(0, locale_1.t)('N/A')}</NoDateTime>)}
          </DateWrapper>
        </StyledHovercard>
        <DateWrapper>
          {(0, utils_1.defined)(release) ? (<React.Fragment>
              {(0, locale_1.t)('in release ')}
              <versionHoverCard_1.default organization={organization} projectSlug={projectSlug} releaseVersion={release.version}>
                <span>
                  <version_1.default version={release.version} projectId={projectId}/>
                </span>
              </versionHoverCard_1.default>
            </React.Fragment>) : null}
        </DateWrapper>
      </HovercardWrapper>);
    }
}
const dateTimeCss = p => (0, react_1.css) `
  color: ${p.theme.gray300};
  font-size: ${p.theme.fontSizeMedium};
  display: flex;
  justify-content: center;
`;
const HovercardWrapper = (0, styled_1.default)('div') `
  display: flex;
`;
const DateWrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
  ${overflowEllipsis_1.default};
`;
const StyledDateTime = (0, styled_1.default)(dateTime_1.default) `
  ${dateTimeCss};
`;
const NoEnvironment = (0, styled_1.default)('div') `
  ${dateTimeCss};
`;
const NoDateTime = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
const TooltipWrapper = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(0.25)};
  svg {
    margin-right: ${(0, space_1.default)(0.5)};
    position: relative;
    top: 1px;
  }
`;
const TimeSinceWrapper = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  margin-bottom: ${(0, space_1.default)(0.5)};
  display: flex;
  justify-content: space-between;
`;
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};
`;
const StyledHovercard = (0, styled_1.default)(hovercard_1.Hovercard) `
  width: 250px;
  font-weight: normal;
  border: 1px solid ${p => p.theme.gray500};
  background: ${p => p.theme.gray500};
  ${hovercard_1.Header} {
    font-weight: normal;
    color: ${p => p.theme.white};
    background: ${p => p.theme.gray500};
    border-bottom: 1px solid ${p => p.theme.gray400};
  }
  ${hovercard_1.Body} {
    padding: ${(0, space_1.default)(1.5)};
  }
`;
exports.default = SeenInfo;
//# sourceMappingURL=seenInfo.jsx.map