Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const qs = (0, tslib_1.__importStar)(require("query-string"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
/**
 * A modified link used for navigating between organization level pages that
 * will keep the global selection values (projects, environments, time) in the
 * querystring when navigating if it's present
 *
 * Falls back to <a> if there is no router present.
 */
class GlobalSelectionLink extends React.Component {
    render() {
        const { location, to } = this.props;
        const globalQuery = (0, utils_1.extractSelectionParameters)(location === null || location === void 0 ? void 0 : location.query);
        const hasGlobalQuery = Object.keys(globalQuery).length > 0;
        const query = typeof to === 'object' && to.query ? Object.assign(Object.assign({}, globalQuery), to.query) : globalQuery;
        if (location) {
            const toWithGlobalQuery = hasGlobalQuery
                ? typeof to === 'string'
                    ? { pathname: to, query }
                    : Object.assign(Object.assign({}, to), { query })
                : {};
            const routerProps = hasGlobalQuery
                ? Object.assign(Object.assign({}, this.props), { to: toWithGlobalQuery }) : Object.assign(Object.assign({}, this.props), { to });
            return <link_1.default {...routerProps}>{this.props.children}</link_1.default>;
        }
        let queryStringObject = {};
        if (typeof to === 'object' && to.search) {
            queryStringObject = qs.parse(to.search);
        }
        queryStringObject = Object.assign(Object.assign({}, queryStringObject), globalQuery);
        if (typeof to === 'object' && to.query) {
            queryStringObject = Object.assign(Object.assign({}, queryStringObject), to.query);
        }
        const url = (typeof to === 'string' ? to : to.pathname) + '?' + qs.stringify(queryStringObject);
        return (<a {...this.props} href={url}>
        {this.props.children}
      </a>);
    }
}
exports.default = (0, react_router_1.withRouter)(GlobalSelectionLink);
//# sourceMappingURL=globalSelectionLink.jsx.map