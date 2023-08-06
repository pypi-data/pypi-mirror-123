Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
// TODO(epurkhiser, jess): This should be moved into plugins.
const SUPPORTED_PROVIDERS = [
    {
        icon: <icons_1.IconGithub size="xs"/>,
        providerIds: ['github', 'integrations:github', 'integrations:github_enterprise'],
        commitUrl: ({ baseUrl, commitId }) => `${baseUrl}/commit/${commitId}`,
    },
    {
        icon: <icons_1.IconBitbucket size="xs"/>,
        providerIds: ['bitbucket', 'integrations:bitbucket'],
        commitUrl: ({ baseUrl, commitId }) => `${baseUrl}/commits/${commitId}`,
    },
    {
        icon: <icons_1.IconVsts size="xs"/>,
        providerIds: ['visualstudio', 'integrations:vsts'],
        commitUrl: ({ baseUrl, commitId }) => `${baseUrl}/commit/${commitId}`,
    },
    {
        icon: <icons_1.IconGitlab size="xs"/>,
        providerIds: ['gitlab', 'integrations:gitlab'],
        commitUrl: ({ baseUrl, commitId }) => `${baseUrl}/commit/${commitId}`,
    },
];
function CommitLink({ inline, commitId, repository }) {
    if (!commitId || !repository) {
        return <span>{(0, locale_1.t)('Unknown Commit')}</span>;
    }
    const shortId = (0, utils_1.getShortCommitHash)(commitId);
    const providerData = SUPPORTED_PROVIDERS.find(provider => {
        if (!repository.provider) {
            return false;
        }
        return provider.providerIds.includes(repository.provider.id);
    });
    if (providerData === undefined) {
        return <span>{shortId}</span>;
    }
    const commitUrl = repository.url &&
        providerData.commitUrl({
            commitId,
            baseUrl: repository.url,
        });
    return !inline ? (<button_1.default external href={commitUrl} size="small" icon={providerData.icon}>
      {shortId}
    </button_1.default>) : (<externalLink_1.default className="inline-commit" href={commitUrl}>
      {providerData.icon}
      {' ' + shortId}
    </externalLink_1.default>);
}
exports.default = CommitLink;
//# sourceMappingURL=commitLink.jsx.map