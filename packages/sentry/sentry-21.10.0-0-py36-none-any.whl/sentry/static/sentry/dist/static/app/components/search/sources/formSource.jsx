Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const formSearch_1 = require("app/actionCreators/formSearch");
const formSearchStore_1 = (0, tslib_1.__importDefault)(require("app/stores/formSearchStore"));
const createFuzzySearch_1 = require("app/utils/createFuzzySearch");
const replaceRouterParams_1 = (0, tslib_1.__importDefault)(require("app/utils/replaceRouterParams"));
class FormSource extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            fuzzy: null,
        };
    }
    componentDidMount() {
        this.createSearch(this.props.searchMap);
    }
    componentDidUpdate(prevProps) {
        if (this.props.searchMap !== prevProps.searchMap) {
            this.createSearch(this.props.searchMap);
        }
    }
    createSearch(searchMap) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({
                fuzzy: yield (0, createFuzzySearch_1.createFuzzySearch)(searchMap || [], Object.assign(Object.assign({}, this.props.searchOptions), { keys: ['title', 'description'] })),
            });
        });
    }
    render() {
        const { searchMap, query, params, children } = this.props;
        let results = [];
        if (this.state.fuzzy) {
            const rawResults = this.state.fuzzy.search(query);
            results = rawResults.map(value => {
                const { item } = value, rest = (0, tslib_1.__rest)(value, ["item"]);
                return Object.assign({ item: Object.assign(Object.assign({}, item), { sourceType: 'field', resultType: 'field', to: `${(0, replaceRouterParams_1.default)(item.route, params)}#${encodeURIComponent(item.field.name)}` }) }, rest);
            });
        }
        return children({
            isLoading: searchMap === null,
            results,
        });
    }
}
FormSource.defaultProps = {
    searchOptions: {},
};
class FormSourceContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            searchMap: formSearchStore_1.default.get(),
        };
        this.unsubscribe = formSearchStore_1.default.listen((searchMap) => this.setState({ searchMap }), undefined);
    }
    componentDidMount() {
        // Loads form fields
        (0, formSearch_1.loadSearchMap)();
    }
    componentWillUnmount() {
        this.unsubscribe();
    }
    render() {
        return <FormSource searchMap={this.state.searchMap} {...this.props}/>;
    }
}
exports.default = (0, react_router_1.withRouter)(FormSourceContainer);
//# sourceMappingURL=formSource.jsx.map