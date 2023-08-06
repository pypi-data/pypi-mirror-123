Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const commitLink_1 = (0, tslib_1.__importDefault)(require("app/components/commitLink"));
const styles_1 = require("app/components/events/styles");
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
function renderReason(statusDetails, projectId, activities) {
    const actor = statusDetails.actor ? (<strong>
      <userAvatar_1.default user={statusDetails.actor} size={20} className="avatar"/>
      <span style={{ marginLeft: 5 }}>{statusDetails.actor.name}</span>
    </strong>) : null;
    const relevantActivity = activities.find(activity => activity.type === types_1.GroupActivityType.SET_RESOLVED_IN_RELEASE);
    const currentReleaseVersion = relevantActivity === null || relevantActivity === void 0 ? void 0 : relevantActivity.data.current_release_version;
    if (statusDetails.inNextRelease && statusDetails.actor) {
        return (0, locale_1.tct)('[actor] marked this issue as resolved in the upcoming release.', {
            actor,
        });
    }
    else if (statusDetails.inNextRelease) {
        return (0, locale_1.t)('This issue has been marked as resolved in the upcoming release.');
    }
    else if (statusDetails.inRelease && statusDetails.actor) {
        return currentReleaseVersion
            ? (0, locale_1.tct)('[actor] marked this issue as resolved in versions greater than [version].', {
                actor,
                version: (<version_1.default version={currentReleaseVersion} projectId={projectId} tooltipRawVersion/>),
            })
            : (0, locale_1.tct)('[actor] marked this issue as resolved in version [version].', {
                actor,
                version: (<version_1.default version={statusDetails.inRelease} projectId={projectId} tooltipRawVersion/>),
            });
    }
    else if (statusDetails.inRelease) {
        return currentReleaseVersion
            ? (0, locale_1.tct)('This issue has been marked as resolved in versions greater than [version].', {
                version: (<version_1.default version={currentReleaseVersion} projectId={projectId} tooltipRawVersion/>),
            })
            : (0, locale_1.tct)('This issue has been marked as resolved in version [version].', {
                version: (<version_1.default version={statusDetails.inRelease} projectId={projectId} tooltipRawVersion/>),
            });
    }
    else if (!!statusDetails.inCommit) {
        return (0, locale_1.tct)('This issue has been marked as resolved by [commit]', {
            commit: (<react_1.Fragment>
          <commitLink_1.default commitId={statusDetails.inCommit.id} repository={statusDetails.inCommit.repository}/>
          <StyledTimeSince date={statusDetails.inCommit.dateCreated}/>
        </react_1.Fragment>),
        });
    }
    return (0, locale_1.t)('This issue has been marked as resolved.');
}
function ResolutionBox({ statusDetails, projectId, activities = [] }) {
    return (<styles_1.BannerContainer priority="default">
      <styles_1.BannerSummary>
        <StyledIconCheckmark color="green300"/>
        <span>{renderReason(statusDetails, projectId, activities)}</span>
      </styles_1.BannerSummary>
    </styles_1.BannerContainer>);
}
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  color: ${p => p.theme.gray300};
  margin-left: ${(0, space_1.default)(0.5)};
  font-size: ${p => p.theme.fontSizeSmall};
`;
const StyledIconCheckmark = (0, styled_1.default)(icons_1.IconCheckmark) `
  /* override margin defined in BannerSummary */
  margin-top: 0 !important;
  align-self: center;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    margin-top: ${(0, space_1.default)(0.5)} !important;
    align-self: flex-start;
  }
`;
exports.default = ResolutionBox;
//# sourceMappingURL=resolutionBox.jsx.map