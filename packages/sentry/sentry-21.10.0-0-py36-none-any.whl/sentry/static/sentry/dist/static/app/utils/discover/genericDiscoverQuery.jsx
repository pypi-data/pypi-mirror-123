Object.defineProperty(exports, "__esModule", { value: true });
exports.doDiscoverQuery = exports.GenericDiscoverQuery = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const locale_1 = require("app/locale");
const eventView_1 = require("app/utils/discover/eventView");
const performanceEventViewContext_1 = require("app/utils/performance/contexts/performanceEventViewContext");
const useOrganization_1 = require("../useOrganization");
/**
 * Generic component for discover queries
 */
class _GenericDiscoverQuery extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isLoading: true,
            tableFetchID: undefined,
            error: null,
            tableData: null,
            pageLinks: null,
        };
        this._shouldRefetchData = (prevProps) => {
            const thisAPIPayload = this.getPayload(this.props);
            const otherAPIPayload = this.getPayload(prevProps);
            return (!(0, eventView_1.isAPIPayloadSimilar)(thisAPIPayload, otherAPIPayload) ||
                prevProps.limit !== this.props.limit ||
                prevProps.route !== this.props.route ||
                prevProps.cursor !== this.props.cursor);
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            const { api, beforeFetch, afterFetch, didFetch, eventView, orgSlug, route, limit, cursor, setError, noPagination, referrer, } = this.props;
            if (!eventView.isValid()) {
                return;
            }
            const url = `/organizations/${orgSlug}/${route}/`;
            const tableFetchID = Symbol(`tableFetchID`);
            const apiPayload = this.getPayload(this.props);
            this.setState({ isLoading: true, tableFetchID });
            setError === null || setError === void 0 ? void 0 : setError(undefined);
            if (limit) {
                apiPayload.per_page = limit;
            }
            if (noPagination) {
                apiPayload.noPagination = noPagination;
            }
            if (cursor) {
                apiPayload.cursor = cursor;
            }
            if (referrer) {
                apiPayload.referrer = referrer;
            }
            beforeFetch === null || beforeFetch === void 0 ? void 0 : beforeFetch(api);
            // clear any inflight requests since they are now stale
            api.clear();
            try {
                const [data, , resp] = yield doDiscoverQuery(api, url, apiPayload);
                if (this.state.tableFetchID !== tableFetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                const tableData = afterFetch ? afterFetch(data, this.props) : data;
                didFetch === null || didFetch === void 0 ? void 0 : didFetch(tableData);
                this.setState(prevState => {
                    var _a;
                    return ({
                        isLoading: false,
                        tableFetchID: undefined,
                        error: null,
                        pageLinks: (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : prevState.pageLinks,
                        tableData,
                    });
                });
            }
            catch (err) {
                const error = ((_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) || (0, locale_1.t)('An unknown error occurred.');
                this.setState({
                    isLoading: false,
                    tableFetchID: undefined,
                    error,
                    tableData: null,
                });
                if (setError) {
                    setError(error);
                }
            }
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        // Reload data if the payload changes
        const refetchCondition = this._shouldRefetchData(prevProps);
        // or if we've moved from an invalid view state to a valid one,
        const eventViewValidation = prevProps.eventView.isValid() === false && this.props.eventView.isValid();
        const shouldRefetchExternal = this.props.shouldRefetchData
            ? this.props.shouldRefetchData(prevProps, this.props)
            : false;
        if (refetchCondition || eventViewValidation || shouldRefetchExternal) {
            this.fetchData();
        }
    }
    getPayload(props) {
        if (this.props.getRequestPayload) {
            return this.props.getRequestPayload(props);
        }
        return props.eventView.getEventsAPIPayload(props.location);
    }
    render() {
        const { isLoading, error, tableData, pageLinks } = this.state;
        const childrenProps = {
            isLoading,
            error,
            tableData,
            pageLinks,
        };
        const children = this.props.children; // Explicitly setting type due to issues with generics and React's children
        return children === null || children === void 0 ? void 0 : children(childrenProps);
    }
}
// Shim to allow us to use generic discover query or any specialization with or without passing org slug or eventview, which are now contexts.
// This will help keep tests working and we can remove extra uses of context-provided props and update tests as we go.
function GenericDiscoverQuery(props) {
    var _a, _b;
    const orgSlug = (_a = props.orgSlug) !== null && _a !== void 0 ? _a : (0, useOrganization_1.useOrgSlug)();
    const eventView = (_b = props.eventView) !== null && _b !== void 0 ? _b : (0, performanceEventViewContext_1.usePerformanceEventView)();
    const _props = Object.assign(Object.assign({}, props), { orgSlug,
        eventView });
    return <_GenericDiscoverQuery {..._props}/>;
}
exports.GenericDiscoverQuery = GenericDiscoverQuery;
function doDiscoverQuery(api, url, params) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        return api.requestPromise(url, {
            method: 'GET',
            includeAllArgs: true,
            query: Object.assign({}, params),
        });
    });
}
exports.doDiscoverQuery = doDiscoverQuery;
exports.default = GenericDiscoverQuery;
//# sourceMappingURL=genericDiscoverQuery.jsx.map