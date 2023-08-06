Object.defineProperty(exports, "__esModule", { value: true });
exports.HelpSource = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const global_search_1 = require("@sentry-internal/global-search");
const dompurify_1 = (0, tslib_1.__importDefault)(require("dompurify"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const parseHtmlMarks_1 = (0, tslib_1.__importDefault)(require("app/utils/parseHtmlMarks"));
const withLatestContext_1 = (0, tslib_1.__importDefault)(require("app/utils/withLatestContext"));
const MARK_TAGS = {
    highlightPreTag: '<mark>',
    highlightPostTag: '</mark>',
};
class HelpSource extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
            results: [],
        };
        this.search = new global_search_1.SentryGlobalSearch(['docs', 'help-center', 'develop', 'blog']);
        this.doSearch = (0, debounce_1.default)(this.unbouncedSearch, 300);
    }
    componentDidMount() {
        if (this.props.query !== undefined) {
            this.doSearch(this.props.query);
        }
    }
    componentDidUpdate(nextProps) {
        if (nextProps.query !== this.props.query) {
            this.doSearch(nextProps.query);
        }
    }
    unbouncedSearch(query) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ loading: true });
            const { platforms = [] } = this.props;
            const searchResults = yield this.search.query(query, {
                platforms: platforms.map(platform => { var _a; return (_a = (0, global_search_1.standardSDKSlug)(platform)) === null || _a === void 0 ? void 0 : _a.slug; }),
            });
            const results = mapSearchResults(searchResults);
            this.setState({ loading: false, results });
        });
    }
    render() {
        return this.props.children({
            isLoading: this.state.loading,
            results: this.state.results,
        });
    }
}
exports.HelpSource = HelpSource;
function mapSearchResults(results) {
    const items = [];
    results.forEach(section => {
        const sectionItems = section.hits.map(hit => {
            var _a, _b, _c;
            const title = (0, parseHtmlMarks_1.default)({
                key: 'title',
                htmlString: (_a = hit.title) !== null && _a !== void 0 ? _a : '',
                markTags: MARK_TAGS,
            });
            const description = (0, parseHtmlMarks_1.default)({
                key: 'description',
                htmlString: (_b = hit.text) !== null && _b !== void 0 ? _b : '',
                markTags: MARK_TAGS,
            });
            const item = Object.assign(Object.assign({}, hit), { sourceType: 'help', resultType: `help-${hit.site}`, title: dompurify_1.default.sanitize((_c = hit.title) !== null && _c !== void 0 ? _c : ''), extra: hit.context.context1, description: hit.text ? dompurify_1.default.sanitize(hit.text) : undefined, to: hit.url });
            return { item, matches: [title, description], score: 1 };
        });
        // The first element should indicate the section.
        if (sectionItems.length > 0) {
            sectionItems[0].item.sectionHeading = section.name;
            sectionItems[0].item.sectionCount = sectionItems.length;
            items.push(...sectionItems);
            return;
        }
        // If we didn't have any results for this section mark it as empty
        const emptyHeaderItem = {
            sourceType: 'help',
            resultType: `help-${section.site}`,
            title: `No results in ${section.name}`,
            sectionHeading: section.name,
            empty: true,
        };
        items.push({ item: emptyHeaderItem, score: 1 });
    });
    return items;
}
exports.default = (0, withLatestContext_1.default)((0, react_router_1.withRouter)(HelpSource));
//# sourceMappingURL=helpSource.jsx.map