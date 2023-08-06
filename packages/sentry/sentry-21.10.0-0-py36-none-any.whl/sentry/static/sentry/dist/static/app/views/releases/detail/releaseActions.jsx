Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const release_1 = require("app/actionCreators/release");
const api_1 = require("app/api");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const navigationButtonGroup_1 = (0, tslib_1.__importDefault)(require("app/components/navigationButtonGroup"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const formatters_1 = require("app/utils/formatters");
const utils_1 = require("../utils");
function ReleaseActions({ location, organization, projectSlug, release, releaseMeta, refetchData, }) {
    function handleArchive() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                yield (0, release_1.archiveRelease)(new api_1.Client(), {
                    orgSlug: organization.slug,
                    projectSlug,
                    releaseVersion: release.version,
                });
                react_router_1.browserHistory.push(`/organizations/${organization.slug}/releases/`);
            }
            catch (_a) {
                // do nothing, action creator is already displaying error message
            }
        });
    }
    function handleRestore() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                yield (0, release_1.restoreRelease)(new api_1.Client(), {
                    orgSlug: organization.slug,
                    projectSlug,
                    releaseVersion: release.version,
                });
                refetchData();
            }
            catch (_a) {
                // do nothing, action creator is already displaying error message
            }
        });
    }
    function getProjectList() {
        const maxVisibleProjects = 5;
        const visibleProjects = releaseMeta.projects.slice(0, maxVisibleProjects);
        const numberOfCollapsedProjects = releaseMeta.projects.length - visibleProjects.length;
        return (<React.Fragment>
        {visibleProjects.map(project => (<projectBadge_1.default key={project.slug} project={project} avatarSize={18}/>))}
        {numberOfCollapsedProjects > 0 && (<span>
            <tooltip_1.default title={release.projects
                    .slice(maxVisibleProjects)
                    .map(p => p.slug)
                    .join(', ')}>
              + {(0, locale_1.tn)('%s other project', '%s other projects', numberOfCollapsedProjects)}
            </tooltip_1.default>
          </span>)}
      </React.Fragment>);
    }
    function getModalHeader(title) {
        return (<h4>
        <textOverflow_1.default>{title}</textOverflow_1.default>
      </h4>);
    }
    function getModalMessage(message) {
        return (<React.Fragment>
        {message}

        <ProjectsWrapper>{getProjectList()}</ProjectsWrapper>

        {(0, locale_1.t)('Are you sure you want to do this?')}
      </React.Fragment>);
    }
    function replaceReleaseUrl(toRelease) {
        return toRelease
            ? {
                pathname: location.pathname
                    .replace(encodeURIComponent(release.version), toRelease)
                    .replace(release.version, toRelease),
                query: Object.assign(Object.assign({}, location.query), { activeRepo: undefined }),
            }
            : '';
    }
    function handleNavigationClick(direction) {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: `release_detail.pagination`,
            eventName: `Release Detail: Pagination`,
            organization_id: parseInt(organization.id, 10),
            direction,
        });
    }
    const { nextReleaseVersion, prevReleaseVersion, firstReleaseVersion, lastReleaseVersion, } = release.currentProjectMeta;
    return (<buttonBar_1.default gap={1}>
      <navigationButtonGroup_1.default hasPrevious={!!prevReleaseVersion} hasNext={!!nextReleaseVersion} links={[
            replaceReleaseUrl(firstReleaseVersion),
            replaceReleaseUrl(prevReleaseVersion),
            replaceReleaseUrl(nextReleaseVersion),
            replaceReleaseUrl(lastReleaseVersion),
        ]} onOldestClick={() => handleNavigationClick('oldest')} onOlderClick={() => handleNavigationClick('older')} onNewerClick={() => handleNavigationClick('newer')} onNewestClick={() => handleNavigationClick('newest')}/>
      <StyledDropdownLink caret={false} anchorRight={window.innerWidth > 992} title={<ActionsButton icon={<icons_1.IconEllipsis />} label={(0, locale_1.t)('Actions')}/>}>
        {(0, utils_1.isReleaseArchived)(release) ? (<confirm_1.default onConfirm={handleRestore} header={getModalHeader((0, locale_1.tct)('Restore Release [release]', {
                release: (0, formatters_1.formatVersion)(release.version),
            }))} message={getModalMessage((0, locale_1.tn)('You are restoring this release for the following project:', 'By restoring this release, you are also restoring it for the following projects:', releaseMeta.projects.length))} cancelText={(0, locale_1.t)('Nevermind')} confirmText={(0, locale_1.t)('Restore')}>
            <menuItem_1.default>{(0, locale_1.t)('Restore')}</menuItem_1.default>
          </confirm_1.default>) : (<confirm_1.default onConfirm={handleArchive} header={getModalHeader((0, locale_1.tct)('Archive Release [release]', {
                release: (0, formatters_1.formatVersion)(release.version),
            }))} message={getModalMessage((0, locale_1.tn)('You are archiving this release for the following project:', 'By archiving this release, you are also archiving it for the following projects:', releaseMeta.projects.length))} cancelText={(0, locale_1.t)('Nevermind')} confirmText={(0, locale_1.t)('Archive')}>
            <menuItem_1.default>{(0, locale_1.t)('Archive')}</menuItem_1.default>
          </confirm_1.default>)}
      </StyledDropdownLink>
    </buttonBar_1.default>);
}
const ActionsButton = (0, styled_1.default)(button_1.default) `
  width: 40px;
  height: 40px;
  padding: 0;
`;
const StyledDropdownLink = (0, styled_1.default)(dropdownLink_1.default) `
  & + .dropdown-menu {
    top: 50px !important;
  }
`;
const ProjectsWrapper = (0, styled_1.default)('div') `
  margin: ${(0, space_1.default)(2)} 0 ${(0, space_1.default)(2)} ${(0, space_1.default)(2)};
  display: grid;
  gap: ${(0, space_1.default)(0.5)};
  img {
    border: none !important;
    box-shadow: none !important;
  }
`;
exports.default = ReleaseActions;
//# sourceMappingURL=releaseActions.jsx.map