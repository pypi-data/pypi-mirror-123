Object.defineProperty(exports, "__esModule", { value: true });
exports.RouteSource = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const flattenDepth_1 = (0, tslib_1.__importDefault)(require("lodash/flattenDepth"));
const createFuzzySearch_1 = require("app/utils/createFuzzySearch");
const replaceRouterParams_1 = (0, tslib_1.__importDefault)(require("app/utils/replaceRouterParams"));
const withLatestContext_1 = (0, tslib_1.__importDefault)(require("app/utils/withLatestContext"));
const navigationConfiguration_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/navigationConfiguration"));
const navigationConfiguration_2 = (0, tslib_1.__importDefault)(require("app/views/settings/organization/navigationConfiguration"));
const navigationConfiguration_3 = (0, tslib_1.__importDefault)(require("app/views/settings/project/navigationConfiguration"));
/**
 * navigation configuration can currently be either:
 *
 *  - an array of {name: string, items: Array<{NavItem}>} OR
 *  - a function that returns the above
 *    (some navigation items require additional context, e.g. a badge based on
 *    a `project` property)
 *
 * We need to go through all navigation configurations and get a flattened list
 * of all navigation item objects
 */
const mapFunc = (config, context = null) => (Array.isArray(config) ? config : context !== null ? config(context) : []).map(({ items }) => items.filter(({ show }) => typeof show === 'function' && context !== null ? show(context) : true));
class RouteSource extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            fuzzy: undefined,
        };
    }
    componentDidMount() {
        this.createSearch();
    }
    componentDidUpdate(prevProps) {
        if (prevProps.project === this.props.project &&
            prevProps.organization === this.props.organization) {
            return;
        }
        this.createSearch();
    }
    createSearch() {
        var _a, _b;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { project, organization } = this.props;
            const context = {
                project,
                organization,
                access: new Set((_a = organization === null || organization === void 0 ? void 0 : organization.access) !== null && _a !== void 0 ? _a : []),
                features: new Set((_b = project === null || project === void 0 ? void 0 : project.features) !== null && _b !== void 0 ? _b : []),
            };
            const searchMap = (0, flattenDepth_1.default)([
                mapFunc(navigationConfiguration_1.default, context),
                mapFunc(navigationConfiguration_3.default, context),
                mapFunc(navigationConfiguration_2.default, context),
            ], 2);
            const options = Object.assign(Object.assign({}, this.props.searchOptions), { keys: ['title', 'description'] });
            const fuzzy = yield (0, createFuzzySearch_1.createFuzzySearch)(searchMap !== null && searchMap !== void 0 ? searchMap : [], options);
            this.setState({ fuzzy });
        });
    }
    render() {
        var _a, _b;
        const { query, params, children } = this.props;
        const results = (_b = (_a = this.state.fuzzy) === null || _a === void 0 ? void 0 : _a.search(query).map((_a) => {
            var { item } = _a, rest = (0, tslib_1.__rest)(_a, ["item"]);
            return (Object.assign({ item: Object.assign(Object.assign({}, item), { sourceType: 'route', resultType: 'route', to: (0, replaceRouterParams_1.default)(item.path, params) }) }, rest));
        })) !== null && _b !== void 0 ? _b : [];
        return children({
            isLoading: this.state.fuzzy === undefined,
            results,
        });
    }
}
exports.RouteSource = RouteSource;
RouteSource.defaultProps = {
    searchOptions: {},
};
exports.default = (0, withLatestContext_1.default)(RouteSource);
//# sourceMappingURL=routeSource.jsx.map