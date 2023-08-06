Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const savedSearchesStore_1 = (0, tslib_1.__importDefault)(require("app/stores/savedSearchesStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * Wrap a component with saved issue search data from the store.
 */
function withSavedSearches(WrappedComponent) {
    class WithSavedSearches extends React.Component {
        constructor() {
            super(...arguments);
            this.state = savedSearchesStore_1.default.get();
            this.unsubscribe = savedSearchesStore_1.default.listen((searchesState) => this.onUpdate(searchesState), undefined);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        onUpdate(newState) {
            this.setState(newState);
        }
        render() {
            const { params, location, savedSearchLoading, savedSearch: savedSearchProp, savedSearches: savedSearchesProp, } = this.props;
            const { searchId } = params;
            const { savedSearches, isLoading } = this.state;
            let savedSearch = null;
            // Switch to the current saved search or pinned result if available
            if (!isLoading && savedSearches) {
                if (searchId) {
                    const match = savedSearches.find(search => search.id === searchId);
                    savedSearch = match ? match : null;
                }
                // If there's no direct saved search being requested (via URL route)
                // *AND* there's no query in URL, then check if there is pinned search
                //
                // Note: Don't use pinned searches when there is an empty query (query === empty string)
                if (!savedSearch && typeof location.query.query === 'undefined') {
                    const pin = savedSearches.find(search => search.isPinned);
                    savedSearch = pin ? pin : null;
                }
            }
            return (<WrappedComponent {...this.props} savedSearches={savedSearchesProp !== null && savedSearchesProp !== void 0 ? savedSearchesProp : savedSearches} savedSearchLoading={savedSearchLoading !== null && savedSearchLoading !== void 0 ? savedSearchLoading : isLoading} savedSearch={savedSearchProp !== null && savedSearchProp !== void 0 ? savedSearchProp : savedSearch}/>);
        }
    }
    WithSavedSearches.displayName = `withSavedSearches(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithSavedSearches;
}
exports.default = withSavedSearches;
//# sourceMappingURL=withSavedSearches.jsx.map