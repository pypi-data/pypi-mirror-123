Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const resolve_1 = (0, tslib_1.__importDefault)(require("app/components/actions/resolve"));
const utils_1 = require("./utils");
function ResolveActionsContainer({ params, orgSlug, anySelected, onShouldConfirm, onUpdate, }) {
    const { hasReleases, latestRelease, projectId, confirm, label, loadingProjects, projectFetchError, } = params;
    // resolve requires a single project to be active in an org context
    // projectId is null when 0 or >1 projects are selected.
    const resolveDisabled = Boolean(!anySelected || projectFetchError);
    const resolveDropdownDisabled = Boolean(!anySelected || !projectId || loadingProjects || projectFetchError);
    return (<resolve_1.default hasRelease={hasReleases} latestRelease={latestRelease} orgSlug={orgSlug} projectSlug={projectId} onUpdate={onUpdate} shouldConfirm={onShouldConfirm(utils_1.ConfirmAction.RESOLVE)} confirmMessage={confirm('resolve', true)} confirmLabel={label('resolve')} disabled={resolveDisabled} disableDropdown={resolveDropdownDisabled} projectFetchError={projectFetchError}/>);
}
exports.default = ResolveActionsContainer;
//# sourceMappingURL=resolveActions.jsx.map