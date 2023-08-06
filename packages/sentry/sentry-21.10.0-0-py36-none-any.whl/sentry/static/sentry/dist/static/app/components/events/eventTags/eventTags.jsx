Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const pills_1 = (0, tslib_1.__importDefault)(require("app/components/pills"));
const utils_1 = require("app/utils");
const eventTagsPill_1 = (0, tslib_1.__importDefault)(require("./eventTagsPill"));
const EventTags = ({ event: { tags = [] }, organization, projectId, location }) => {
    if (!tags.length) {
        return null;
    }
    const orgSlug = organization.slug;
    const streamPath = `/organizations/${orgSlug}/issues/`;
    const releasesPath = `/organizations/${orgSlug}/releases/`;
    return (<pills_1.default>
      {tags.map((tag, index) => (<eventTagsPill_1.default key={!(0, utils_1.defined)(tag.key) ? `tag-pill-${index}` : tag.key} tag={tag} projectId={projectId} organization={organization} query={(0, utils_1.generateQueryWithTag)(location.query, tag)} streamPath={streamPath} releasesPath={releasesPath}/>))}
    </pills_1.default>);
};
exports.default = EventTags;
//# sourceMappingURL=eventTags.jsx.map