Object.defineProperty(exports, "__esModule", { value: true });
exports.displayExperimentalSpaAlert = exports.displayDeployPreviewAlert = void 0;
const tslib_1 = require("tslib");
const alertActions_1 = (0, tslib_1.__importDefault)(require("app/actions/alertActions"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
function displayDeployPreviewAlert() {
    if (!constants_1.DEPLOY_PREVIEW_CONFIG) {
        return;
    }
    const { branch, commitSha, githubOrg, githubRepo } = constants_1.DEPLOY_PREVIEW_CONFIG;
    const repoUrl = `https://github.com/${githubOrg}/${githubRepo}`;
    const commitLink = (<externalLink_1.default href={`${repoUrl}/commit/${commitSha}`}>
      {(0, locale_1.t)('%s@%s', `${githubOrg}/${githubRepo}`, commitSha.slice(0, 6))}
    </externalLink_1.default>);
    const branchLink = (<externalLink_1.default href={`${repoUrl}/tree/${branch}`}>{branch}</externalLink_1.default>);
    alertActions_1.default.addAlert({
        id: 'deploy-preview',
        message: (0, locale_1.tct)('You are viewing a frontend deploy preview of [commitLink] ([branchLink])', { commitLink, branchLink }),
        type: 'warning',
        neverExpire: true,
        noDuplicates: true,
    });
}
exports.displayDeployPreviewAlert = displayDeployPreviewAlert;
function displayExperimentalSpaAlert() {
    if (!constants_1.EXPERIMENTAL_SPA) {
        return;
    }
    alertActions_1.default.addAlert({
        id: 'develop-proxy',
        message: (0, locale_1.t)('You are developing against production Sentry API, please BE CAREFUL, as your changes will affect production data.'),
        type: 'warning',
        neverExpire: true,
        noDuplicates: true,
    });
}
exports.displayExperimentalSpaAlert = displayExperimentalSpaAlert;
//# sourceMappingURL=deployPreview.jsx.map