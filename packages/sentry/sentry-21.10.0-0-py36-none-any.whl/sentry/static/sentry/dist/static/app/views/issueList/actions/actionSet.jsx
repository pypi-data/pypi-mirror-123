Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const actionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/actionLink"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const ignore_1 = (0, tslib_1.__importDefault)(require("app/components/actions/ignore"));
const menuItemActionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuItemActionLink"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const resolveActions_1 = (0, tslib_1.__importDefault)(require("./resolveActions"));
const reviewAction_1 = (0, tslib_1.__importDefault)(require("./reviewAction"));
const utils_1 = require("./utils");
function ActionSet({ orgSlug, queryCount, query, allInQuerySelected, anySelected, multiSelected, issues, onUpdate, onShouldConfirm, onDelete, onMerge, selectedProjectSlug, }) {
    const numIssues = issues.size;
    const confirm = (0, utils_1.getConfirm)(numIssues, allInQuerySelected, query, queryCount);
    const label = (0, utils_1.getLabel)(numIssues, allInQuerySelected);
    // merges require a single project to be active in an org context
    // selectedProjectSlug is null when 0 or >1 projects are selected.
    const mergeDisabled = !(multiSelected && selectedProjectSlug);
    const selectedIssues = [...issues].map(groupStore_1.default.get);
    const canMarkReviewed = anySelected && (allInQuerySelected || selectedIssues.some(issue => !!(issue === null || issue === void 0 ? void 0 : issue.inbox)));
    return (<Wrapper>
      {selectedProjectSlug ? (<projects_1.default orgId={orgSlug} slugs={[selectedProjectSlug]}>
          {({ projects, initiallyLoaded, fetchError }) => {
                const selectedProject = projects[0];
                return (<resolveActions_1.default onShouldConfirm={onShouldConfirm} onUpdate={onUpdate} anySelected={anySelected} orgSlug={orgSlug} params={{
                        hasReleases: selectedProject.hasOwnProperty('features')
                            ? selectedProject.features.includes('releases')
                            : false,
                        latestRelease: selectedProject.hasOwnProperty('latestRelease')
                            ? selectedProject.latestRelease
                            : undefined,
                        projectId: selectedProject.slug,
                        confirm,
                        label,
                        loadingProjects: !initiallyLoaded,
                        projectFetchError: !!fetchError,
                    }}/>);
            }}
        </projects_1.default>) : (<resolveActions_1.default onShouldConfirm={onShouldConfirm} onUpdate={onUpdate} anySelected={anySelected} orgSlug={orgSlug} params={{
                hasReleases: false,
                latestRelease: null,
                projectId: null,
                confirm,
                label,
            }}/>)}

      <ignore_1.default onUpdate={onUpdate} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.IGNORE)} confirmMessage={confirm(utils_1.ConfirmAction.IGNORE, true)} confirmLabel={label('ignore')} disabled={!anySelected}/>
      <guideAnchor_1.default target="inbox_guide_review" position="bottom">
        <div className="hidden-sm hidden-xs">
          <reviewAction_1.default disabled={!canMarkReviewed} onUpdate={onUpdate}/>
        </div>
      </guideAnchor_1.default>
      <div className="hidden-md hidden-sm hidden-xs">
        <actionLink_1.default type="button" disabled={mergeDisabled} onAction={onMerge} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.MERGE)} message={confirm(utils_1.ConfirmAction.MERGE, false)} confirmLabel={label('merge')} title={(0, locale_1.t)('Merge Selected Issues')}>
          {(0, locale_1.t)('Merge')}
        </actionLink_1.default>
      </div>

      <dropdownLink_1.default key="actions" customTitle={<button_1.default label={(0, locale_1.t)('Open more issue actions')} icon={<icons_1.IconEllipsis size="xs"/>}/>}>
        <menuItemActionLink_1.default className="hidden-lg hidden-xl" disabled={mergeDisabled} onAction={onMerge} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.MERGE)} message={confirm(utils_1.ConfirmAction.MERGE, false)} confirmLabel={label('merge')} title={(0, locale_1.t)('Merge Selected Issues')}>
          {(0, locale_1.t)('Merge')}
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default className="hidden-md hidden-lg hidden-xl" disabled={!canMarkReviewed} onAction={() => onUpdate({ inbox: false })} title={(0, locale_1.t)('Mark Reviewed')}>
          {(0, locale_1.t)('Mark Reviewed')}
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default disabled={!anySelected} onAction={() => onUpdate({ isBookmarked: true })} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.BOOKMARK)} message={confirm(utils_1.ConfirmAction.BOOKMARK, false)} confirmLabel={label('bookmark')} title={(0, locale_1.t)('Add to Bookmarks')}>
          {(0, locale_1.t)('Add to Bookmarks')}
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default disabled={!anySelected} onAction={() => onUpdate({ isBookmarked: false })} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.UNBOOKMARK)} message={confirm('remove', false, ' from your bookmarks')} confirmLabel={label('remove', ' from your bookmarks')} title={(0, locale_1.t)('Remove from Bookmarks')}>
          {(0, locale_1.t)('Remove from Bookmarks')}
        </menuItemActionLink_1.default>

        <menuItemActionLink_1.default disabled={!anySelected} onAction={() => onUpdate({ status: types_1.ResolutionStatus.UNRESOLVED })} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.UNRESOLVE)} message={confirm(utils_1.ConfirmAction.UNRESOLVE, true)} confirmLabel={label('unresolve')} title={(0, locale_1.t)('Set status to: Unresolved')}>
          {(0, locale_1.t)('Set status to: Unresolved')}
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default disabled={!anySelected} onAction={onDelete} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.DELETE)} message={confirm(utils_1.ConfirmAction.DELETE, false)} confirmLabel={label('delete')} title={(0, locale_1.t)('Delete Issues')}>
          {(0, locale_1.t)('Delete Issues')}
        </menuItemActionLink_1.default>
      </dropdownLink_1.default>
    </Wrapper>);
}
exports.default = ActionSet;
const Wrapper = (0, styled_1.default)('div') `
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    width: 66.66%;
  }
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    width: 50%;
  }
  flex: 1;
  margin: 0 ${(0, space_1.default)(1)};
  display: grid;
  gap: ${(0, space_1.default)(0.5)};
  grid-auto-flow: column;
  justify-content: flex-start;
  white-space: nowrap;
`;
//# sourceMappingURL=actionSet.jsx.map