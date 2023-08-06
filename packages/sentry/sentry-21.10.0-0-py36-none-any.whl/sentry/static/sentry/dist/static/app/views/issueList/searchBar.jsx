Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const savedSearches_1 = require("app/actionCreators/savedSearches");
const smartSearchBar_1 = (0, tslib_1.__importDefault)(require("app/components/smartSearchBar"));
const actions_1 = require("app/components/smartSearchBar/actions");
const types_1 = require("app/components/smartSearchBar/types");
const locale_1 = require("app/locale");
const types_2 = require("app/types");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const SEARCH_ITEMS = [
    {
        title: (0, locale_1.t)('Tag'),
        desc: 'browser:"Chrome 34", has:browser',
        value: 'browser:',
        type: types_1.ItemType.DEFAULT,
    },
    {
        title: (0, locale_1.t)('Status'),
        desc: 'is:resolved, unresolved, ignored, assigned, unassigned',
        value: 'is:',
        type: types_1.ItemType.DEFAULT,
    },
    {
        title: (0, locale_1.t)('Time or Count'),
        desc: 'firstSeen, lastSeen, event.timestamp, timesSeen',
        value: 'firstSeen:',
        type: types_1.ItemType.DEFAULT,
    },
    {
        title: (0, locale_1.t)('Assigned'),
        desc: 'assigned, assigned_or_suggested:[me|[me, none]|user@example.com|#team-example]',
        value: 'assigned:',
        type: types_1.ItemType.DEFAULT,
    },
    {
        title: (0, locale_1.t)('Bookmarked By'),
        desc: 'bookmarks:[me|user@example.com]',
        value: 'bookmarks:',
        type: types_1.ItemType.DEFAULT,
    },
];
class IssueListSearchBar extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            defaultSearchItems: [SEARCH_ITEMS, []],
            recentSearches: [],
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.props.api.clear();
            const resp = yield this.getRecentSearches();
            this.setState({
                defaultSearchItems: [
                    SEARCH_ITEMS,
                    resp
                        ? resp.map(query => ({
                            desc: query,
                            value: query,
                            type: types_1.ItemType.RECENT_SEARCH,
                        }))
                        : [],
                ],
                recentSearches: resp,
            });
        });
        /**
         * @returns array of tag values that substring match `query`
         */
        this.getTagValues = (tag, query) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { tagValueLoader } = this.props;
            const values = yield tagValueLoader(tag.key, query);
            return values.map(({ value }) => value);
        });
        this.getRecentSearches = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            const { api, organization } = this.props;
            const recent = yield (0, savedSearches_1.fetchRecentSearches)(api, organization.slug, types_2.SavedSearchType.ISSUE);
            return (_a = recent === null || recent === void 0 ? void 0 : recent.map(({ query }) => query)) !== null && _a !== void 0 ? _a : [];
        });
        this.handleSavedRecentSearch = () => {
            // Reset recent searches
            this.fetchData();
        };
    }
    componentDidMount() {
        // Ideally, we would fetch on demand (e.g. when input gets focus)
        // but `<SmartSearchBar>` is a bit complicated and this is the easiest route
        this.fetchData();
    }
    render() {
        const _a = this.props, { tagValueLoader: _, savedSearch, sort, onSidebarToggle } = _a, props = (0, tslib_1.__rest)(_a, ["tagValueLoader", "savedSearch", "sort", "onSidebarToggle"]);
        const pinnedSearch = (savedSearch === null || savedSearch === void 0 ? void 0 : savedSearch.isPinned) ? savedSearch : undefined;
        return (<smartSearchBar_1.default searchSource="main_search" hasRecentSearches maxSearchItems={5} savedSearchType={types_2.SavedSearchType.ISSUE} onGetTagValues={this.getTagValues} defaultSearchItems={this.state.defaultSearchItems} onSavedRecentSearch={this.handleSavedRecentSearch} actionBarItems={[
                (0, actions_1.makePinSearchAction)({ sort, pinnedSearch }),
                (0, actions_1.makeSaveSearchAction)({ sort }),
                (0, actions_1.makeSearchBuilderAction)({ onSidebarToggle }),
            ]} {...props}/>);
    }
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(IssueListSearchBar));
//# sourceMappingURL=searchBar.jsx.map