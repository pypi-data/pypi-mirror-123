Object.defineProperty(exports, "__esModule", { value: true });
exports.removeHistogramQueryStrings = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const queryString_1 = require("app/utils/queryString");
const constants_1 = require("./constants");
class Histogram extends React.Component {
    constructor() {
        super(...arguments);
        this.handleResetView = () => {
            const { location, zoomKeys } = this.props;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: removeHistogramQueryStrings(location, zoomKeys),
            });
        };
        this.handleFilterChange = (value) => {
            const { location, zoomKeys } = this.props;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, removeHistogramQueryStrings(location, zoomKeys)), { dataFilter: value }),
            });
        };
    }
    isZoomed() {
        const { location, zoomKeys } = this.props;
        return zoomKeys.map(key => location.query[key]).some(value => value !== undefined);
    }
    getActiveFilter() {
        const { location } = this.props;
        const dataFilter = location.query.dataFilter
            ? (0, queryString_1.decodeScalar)(location.query.dataFilter)
            : constants_1.FILTER_OPTIONS[0].value;
        return constants_1.FILTER_OPTIONS.find(item => item.value === dataFilter) || constants_1.FILTER_OPTIONS[0];
    }
    render() {
        const childrenProps = {
            isZoomed: this.isZoomed(),
            handleResetView: this.handleResetView,
            activeFilter: this.getActiveFilter(),
            handleFilterChange: this.handleFilterChange,
            filterOptions: constants_1.FILTER_OPTIONS,
        };
        return this.props.children(childrenProps);
    }
}
function removeHistogramQueryStrings(location, zoomKeys) {
    const query = Object.assign(Object.assign({}, location.query), { cursor: undefined });
    delete query.dataFilter;
    // reset all zoom parameters
    zoomKeys.forEach(key => delete query[key]);
    return query;
}
exports.removeHistogramQueryStrings = removeHistogramQueryStrings;
exports.default = Histogram;
//# sourceMappingURL=index.jsx.map