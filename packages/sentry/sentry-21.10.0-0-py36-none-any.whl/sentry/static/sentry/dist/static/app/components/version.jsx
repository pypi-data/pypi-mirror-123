Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const Version = ({ version, organization, anchor = true, preserveGlobalSelection, tooltipRawVersion, withPackage, projectId, truncate, className, location, }) => {
    const versionToDisplay = (0, formatters_1.formatVersion)(version, withPackage);
    let releaseDetailProjectId;
    if (projectId) {
        // we can override preserveGlobalSelection's project id
        releaseDetailProjectId = projectId;
    }
    else if (!(organization === null || organization === void 0 ? void 0 : organization.features.includes('global-views'))) {
        // we need this for users without global-views, otherwise they might get `This release may not be in your selected project`
        releaseDetailProjectId = location === null || location === void 0 ? void 0 : location.query.project;
    }
    const renderVersion = () => {
        if (anchor && (organization === null || organization === void 0 ? void 0 : organization.slug)) {
            const props = {
                to: {
                    pathname: `/organizations/${organization === null || organization === void 0 ? void 0 : organization.slug}/releases/${encodeURIComponent(version)}/`,
                    query: releaseDetailProjectId ? { project: releaseDetailProjectId } : undefined,
                },
                className,
            };
            if (preserveGlobalSelection) {
                return (<globalSelectionLink_1.default {...props}>
            <VersionText truncate={truncate}>{versionToDisplay}</VersionText>
          </globalSelectionLink_1.default>);
            }
            else {
                return (<link_1.default {...props}>
            <VersionText truncate={truncate}>{versionToDisplay}</VersionText>
          </link_1.default>);
            }
        }
        return (<VersionText className={className} truncate={truncate}>
        {versionToDisplay}
      </VersionText>);
    };
    const renderTooltipContent = () => (<TooltipContent onClick={e => {
            e.stopPropagation();
        }}>
      <TooltipVersionWrapper>{version}</TooltipVersionWrapper>

      <clipboard_1.default value={version}>
        <TooltipClipboardIconWrapper>
          <icons_1.IconCopy size="xs" color="white"/>
        </TooltipClipboardIconWrapper>
      </clipboard_1.default>
    </TooltipContent>);
    const getPopperStyles = () => {
        // if the version name is not a hash (sha1 or sha265) and we are not on mobile, allow tooltip to be as wide as 500px
        if (/(^[a-f0-9]{40}$)|(^[a-f0-9]{64}$)/.test(version)) {
            return undefined;
        }
        return (0, react_1.css) `
      @media (min-width: ${theme_1.default.breakpoints[0]}) {
        max-width: 500px;
      }
    `;
    };
    return (<tooltip_1.default title={renderTooltipContent()} disabled={!tooltipRawVersion} isHoverable containerDisplayMode={truncate ? 'block' : 'inline-block'} popperStyle={getPopperStyles()}>
      {renderVersion()}
    </tooltip_1.default>);
};
// TODO(matej): try to wrap version with this when truncate prop is true (in separate PR)
// const VersionWrapper = styled('div')`
//   ${overflowEllipsis};
//   max-width: 100%;
//   width: auto;
//   display: inline-block;
// `;
const VersionText = (0, styled_1.default)('span') `
  ${p => p.truncate &&
    `max-width: 100%;
    display: block;
  overflow: hidden;
  font-variant-numeric: tabular-nums;
  text-overflow: ellipsis;
  white-space: nowrap;`}
`;
const TooltipContent = (0, styled_1.default)('span') `
  display: flex;
  align-items: center;
`;
const TooltipVersionWrapper = (0, styled_1.default)('span') `
  ${overflowEllipsis_1.default}
`;
const TooltipClipboardIconWrapper = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(0.5)};
  position: relative;
  bottom: -${(0, space_1.default)(0.25)};

  &:hover {
    cursor: pointer;
  }
`;
exports.default = (0, withOrganization_1.default)((0, react_router_1.withRouter)(Version));
//# sourceMappingURL=version.jsx.map