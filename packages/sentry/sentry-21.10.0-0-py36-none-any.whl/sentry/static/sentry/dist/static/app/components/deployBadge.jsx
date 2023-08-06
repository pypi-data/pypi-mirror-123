Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const DeployBadge = ({ deploy, orgSlug, projectId, version, className }) => {
    const shouldLinkToIssues = !!orgSlug && !!version;
    const badge = (<tag_1.default className={className} type="highlight" icon={shouldLinkToIssues && <icons_1.IconOpen />} textMaxWidth={80} tooltipText={shouldLinkToIssues ? (0, locale_1.t)('Open In Issues') : undefined}>
      {deploy.environment}
    </tag_1.default>);
    if (!shouldLinkToIssues) {
        return badge;
    }
    return (<link_1.default to={{
            pathname: `/organizations/${orgSlug}/issues/`,
            query: {
                project: projectId !== null && projectId !== void 0 ? projectId : null,
                environment: deploy.environment,
                query: new tokenizeSearch_1.MutableSearch([`release:${version}`]).formatString(),
            },
        }}>
      {badge}
    </link_1.default>);
};
exports.default = DeployBadge;
//# sourceMappingURL=deployBadge.jsx.map