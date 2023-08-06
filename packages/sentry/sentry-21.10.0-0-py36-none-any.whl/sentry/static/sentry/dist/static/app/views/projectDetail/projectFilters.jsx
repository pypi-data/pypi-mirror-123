Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const guideAnchor_1 = require("app/components/assistant/guideAnchor");
const smartSearchBar_1 = (0, tslib_1.__importDefault)(require("app/components/smartSearchBar"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const supportedTags = {
    'release.version': {
        key: 'release.version',
        name: 'release.version',
    },
    'release.build': {
        key: 'release.build',
        name: 'release.build',
    },
    'release.package': {
        key: 'release.package',
        name: 'release.package',
    },
    'release.stage': {
        key: 'release.stage',
        name: 'release.stage',
        predefined: true,
        values: constants_1.RELEASE_ADOPTION_STAGES,
    },
    release: {
        key: 'release',
        name: 'release',
    },
};
function ProjectFilters({ query, tagValueLoader, onSearch }) {
    const getTagValues = (tag, currentQuery) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const values = yield tagValueLoader(tag.key, currentQuery);
        return values.map(({ value }) => value);
    });
    return (<guideAnchor_1.GuideAnchor target="releases_search" position="bottom">
      <smartSearchBar_1.default searchSource="project_filters" query={query} placeholder={(0, locale_1.t)('Search by release version, build, package, or stage')} maxSearchItems={5} hasRecentSearches={false} supportedTags={supportedTags} onSearch={onSearch} onGetTagValues={getTagValues}/>
    </guideAnchor_1.GuideAnchor>);
}
exports.default = ProjectFilters;
//# sourceMappingURL=projectFilters.jsx.map