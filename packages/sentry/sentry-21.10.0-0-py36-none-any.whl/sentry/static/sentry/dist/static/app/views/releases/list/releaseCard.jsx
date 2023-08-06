Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const panels_1 = require("app/components/panels");
const releaseStats_1 = (0, tslib_1.__importDefault)(require("app/components/releaseStats"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const releaseHealth_1 = (0, tslib_1.__importDefault)(require("./releaseHealth"));
function getReleaseProjectId(release, selection) {
    // if a release has only one project
    if (release.projects.length === 1) {
        return release.projects[0].id;
    }
    // if only one project is selected in global header and release has it (second condition will prevent false positives like -1)
    if (selection.projects.length === 1 &&
        release.projects.map(p => p.id).includes(selection.projects[0])) {
        return selection.projects[0];
    }
    // project selector on release detail page will pick it up
    return undefined;
}
const ReleaseCard = ({ release, organization, activeDisplay, location, reloading, selection, showHealthPlaceholders, isTopRelease, getHealthData, showReleaseAdoptionStages, }) => {
    const { version, commitCount, lastDeploy, dateCreated, versionInfo } = release;
    return (<StyledPanel reloading={reloading ? 1 : 0}>
      <ReleaseInfo>
        <ReleaseInfoHeader>
          <globalSelectionLink_1.default to={{
            pathname: `/organizations/${organization.slug}/releases/${encodeURIComponent(version)}/`,
            query: { project: getReleaseProjectId(release, selection) },
        }}>
            <guideAnchor_1.default disabled={!isTopRelease} target="release_version">
              <VersionWrapper>
                <StyledVersion version={version} tooltipRawVersion anchor={false}/>
              </VersionWrapper>
            </guideAnchor_1.default>
          </globalSelectionLink_1.default>
          {commitCount > 0 && <releaseStats_1.default release={release} withHeading={false}/>}
        </ReleaseInfoHeader>
        <ReleaseInfoSubheader>
          {(versionInfo === null || versionInfo === void 0 ? void 0 : versionInfo.package) && (<PackageName ellipsisDirection="left">{versionInfo.package}</PackageName>)}
          <timeSince_1.default date={(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) || dateCreated}/>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) && ` \u007C ${lastDeploy.environment}`}
        </ReleaseInfoSubheader>
      </ReleaseInfo>

      <ReleaseProjects>
        <releaseHealth_1.default release={release} organization={organization} activeDisplay={activeDisplay} location={location} showPlaceholders={showHealthPlaceholders} reloading={reloading} selection={selection} isTopRelease={isTopRelease} getHealthData={getHealthData} showReleaseAdoptionStages={showReleaseAdoptionStages}/>
      </ReleaseProjects>
    </StyledPanel>);
};
const VersionWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const StyledVersion = (0, styled_1.default)(version_1.default) `
  ${overflowEllipsis_1.default};
`;
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  opacity: ${p => (p.reloading ? 0.5 : 1)};
  pointer-events: ${p => (p.reloading ? 'none' : 'auto')};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    display: flex;
  }
`;
const ReleaseInfo = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
  flex-shrink: 0;

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    border-right: 1px solid ${p => p.theme.border};
    min-width: 260px;
    width: 22%;
    max-width: 300px;
  }
`;
const ReleaseInfoSubheader = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.gray400};
`;
const PackageName = (0, styled_1.default)(textOverflow_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.textColor};
`;
const ReleaseProjects = (0, styled_1.default)('div') `
  border-top: 1px solid ${p => p.theme.border};
  flex-grow: 1;
  display: grid;

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    border-top: none;
  }
`;
const ReleaseInfoHeader = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  display: grid;
  grid-template-columns: minmax(0, 1fr) max-content;
  grid-gap: ${(0, space_1.default)(2)};
  align-items: center;
`;
exports.default = ReleaseCard;
//# sourceMappingURL=releaseCard.jsx.map