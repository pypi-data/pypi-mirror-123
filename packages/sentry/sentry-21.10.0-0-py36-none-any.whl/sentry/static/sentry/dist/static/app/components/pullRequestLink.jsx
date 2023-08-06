Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
function renderIcon(repo) {
    if (!repo.provider) {
        return null;
    }
    const { id } = repo.provider;
    const providerId = id.includes(':') ? id.split(':').pop() : id;
    switch (providerId) {
        case 'github':
            return <icons_1.IconGithub size="xs"/>;
        case 'gitlab':
            return <icons_1.IconGitlab size="xs"/>;
        case 'bitbucket':
            return <icons_1.IconBitbucket size="xs"/>;
        default:
            return null;
    }
}
const PullRequestLink = ({ pullRequest, repository, inline }) => {
    const displayId = `${repository.name} #${pullRequest.id}: ${pullRequest.title}`;
    return pullRequest.externalUrl ? (<externalLink_1.default className={inline ? 'inline-commit' : 'btn btn-default btn-sm'} href={pullRequest.externalUrl}>
      {renderIcon(repository)}
      {inline ? '' : ' '}
      {displayId}
    </externalLink_1.default>) : (<span>{displayId}</span>);
};
exports.default = PullRequestLink;
//# sourceMappingURL=pullRequestLink.jsx.map