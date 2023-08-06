Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
class SearchSources extends React.Component {
    // `allSources` will be an array of all result objects from each source
    renderResults(allSources) {
        const { children } = this.props;
        // loading means if any result has `isLoading` OR any result is null
        const isLoading = !!allSources.find(arg => arg.isLoading || arg.results === null);
        const foundResults = isLoading
            ? []
            : (0, flatten_1.default)(allSources.map(({ results }) => results || [])).sort((a, b) => a.score - b.score);
        const hasAnyResults = !!foundResults.length;
        return children({
            isLoading,
            results: foundResults,
            hasAnyResults,
        });
    }
    renderSources(sources, results, idx) {
        if (idx >= sources.length) {
            return this.renderResults(results);
        }
        const Source = sources[idx];
        return (<Source {...this.props}>
        {(args) => {
                // Mutate the array instead of pushing because we don't know how often
                // this child function will be called and pushing will cause duplicate
                // results to be pushed for all calls down the chain.
                results[idx] = args;
                return this.renderSources(sources, results, idx + 1);
            }}
      </Source>);
    }
    render() {
        const { sources } = this.props;
        return this.renderSources(sources, new Array(sources.length), 0);
    }
}
exports.default = SearchSources;
//# sourceMappingURL=index.jsx.map