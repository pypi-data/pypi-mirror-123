Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const prop_types_1 = (0, tslib_1.__importDefault)(require("prop-types"));
const api_1 = require("app/api");
const asyncComponentSearchInput_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponentSearchInput"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const permissionDenied_1 = (0, tslib_1.__importDefault)(require("app/views/permissionDenied"));
const routeError_1 = (0, tslib_1.__importDefault)(require("app/views/routeError"));
/**
 * Wraps methods on the AsyncComponent to catch errors and set the `error`
 * state on error.
 */
function wrapErrorHandling(component, fn) {
    return (...args) => {
        try {
            return fn(...args);
        }
        catch (error) {
            // eslint-disable-next-line no-console
            console.error(error);
            setTimeout(() => {
                throw error;
            });
            component.setState({ error });
            return null;
        }
    };
}
class AsyncComponent extends React.Component {
    constructor(props, context) {
        super(props, context);
        // Override this flag to have the component reload it's state when the window
        // becomes visible again. This will set the loading and reloading state, but
        // will not render a loading state during reloading.
        //
        // eslint-disable-next-line react/sort-comp
        this.reloadOnVisible = false;
        // When enabling reloadOnVisible, this flag may be used to turn on and off
        // the reloading. This is useful if your component only needs to reload when
        // becoming visible during certain states.
        //
        // eslint-disable-next-line react/sort-comp
        this.shouldReloadOnVisible = false;
        // This affects how the component behaves when `remountComponent` is called
        // By default, the component gets put back into a "loading" state when re-fetching data.
        // If this is true, then when we fetch data, the original ready component remains mounted
        // and it will need to handle any additional "reloading" states
        this.shouldReload = false;
        // should `renderError` render the `detail` attribute of a 400 error
        this.shouldRenderBadRequests = false;
        this.api = new api_1.Client();
        // Check if we should measure render time for this component
        this.markShouldMeasure = ({ remainingRequests, error, } = {}) => {
            if (!this._measurement.hasMeasured) {
                this._measurement.finished = remainingRequests === 0;
                this._measurement.error = error || this._measurement.error;
            }
        };
        this.remountComponent = () => {
            if (this.shouldReload) {
                this.reloadData();
            }
            else {
                this.setState(this.getDefaultState(), this.fetchData);
            }
        };
        this.visibilityReloader = () => this.shouldReloadOnVisible &&
            !this.state.loading &&
            !document.hidden &&
            this.reloadData();
        this.fetchData = (extraState) => {
            const endpoints = this.getEndpoints();
            if (!endpoints.length) {
                this.setState({ loading: false, error: false });
                return;
            }
            // Cancel any in flight requests
            this.api.clear();
            this.setState(Object.assign({ loading: true, error: false, remainingRequests: endpoints.length }, extraState));
            endpoints.forEach(([stateKey, endpoint, params, options]) => {
                options = options || {};
                // If you're using nested async components/views make sure to pass the
                // props through so that the child component has access to props.location
                const locationQuery = (this.props.location && this.props.location.query) || {};
                let query = (params && params.query) || {};
                // If paginate option then pass entire `query` object to API call
                // It should only be expecting `query.cursor` for pagination
                if ((options.paginate || locationQuery.cursor) && !options.disableEntireQuery) {
                    query = Object.assign(Object.assign({}, locationQuery), query);
                }
                this.api.request(endpoint, Object.assign(Object.assign({ method: 'GET' }, params), { query, success: (data, _, resp) => {
                        this.handleRequestSuccess({ stateKey, data, resp }, true);
                    }, error: error => {
                        // Allow endpoints to fail
                        // allowError can have side effects to handle the error
                        if (options.allowError && options.allowError(error)) {
                            error = null;
                        }
                        this.handleError(error, [stateKey, endpoint, params, options]);
                    } }));
            });
        };
        this.fetchData = wrapErrorHandling(this, this.fetchData.bind(this));
        this.render = wrapErrorHandling(this, this.render.bind(this));
        this.state = this.getDefaultState();
        this._measurement = {
            hasMeasured: false,
        };
        if (props.routes && props.routes) {
            analytics_1.metric.mark({ name: `async-component-${(0, getRouteStringFromRoutes_1.default)(props.routes)}` });
        }
    }
    UNSAFE_componentWillMount() {
        this.api = new api_1.Client();
        this.fetchData();
        if (this.reloadOnVisible) {
            document.addEventListener('visibilitychange', this.visibilityReloader);
        }
    }
    // Compatibility shim for child classes that call super on this hook.
    UNSAFE_componentWillReceiveProps(_newProps, _newContext) { }
    componentDidUpdate(prevProps, prevContext) {
        const isRouterInContext = !!prevContext.router;
        const isLocationInProps = prevProps.location !== undefined;
        const currentLocation = isLocationInProps
            ? this.props.location
            : isRouterInContext
                ? this.context.router.location
                : null;
        const prevLocation = isLocationInProps
            ? prevProps.location
            : isRouterInContext
                ? prevContext.router.location
                : null;
        if (!(currentLocation && prevLocation)) {
            return;
        }
        // Take a measurement from when this component is initially created until it finishes it's first
        // set of API requests
        if (!this._measurement.hasMeasured &&
            this._measurement.finished &&
            this.props.routes) {
            const routeString = (0, getRouteStringFromRoutes_1.default)(this.props.routes);
            analytics_1.metric.measure({
                name: 'app.component.async-component',
                start: `async-component-${routeString}`,
                data: {
                    route: routeString,
                    error: this._measurement.error,
                },
            });
            this._measurement.hasMeasured = true;
        }
        // Re-fetch data when router params change.
        if (!(0, isEqual_1.default)(this.props.params, prevProps.params) ||
            currentLocation.search !== prevLocation.search ||
            currentLocation.state !== prevLocation.state) {
            this.remountComponent();
        }
    }
    componentWillUnmount() {
        this.api.clear();
        document.removeEventListener('visibilitychange', this.visibilityReloader);
    }
    // XXX: can't call this getInitialState as React whines
    getDefaultState() {
        const endpoints = this.getEndpoints();
        const state = {
            // has all data finished requesting?
            loading: true,
            // is the component reload
            reloading: false,
            // is there an error loading ANY data?
            error: false,
            errors: {},
        };
        endpoints.forEach(([stateKey, _endpoint]) => {
            state[stateKey] = null;
        });
        return state;
    }
    reloadData() {
        this.fetchData({ reloading: true });
    }
    onRequestSuccess(_resp /* {stateKey, data, resp} */) {
        // Allow children to implement this
    }
    onRequestError(_resp, _args) {
        // Allow children to implement this
    }
    onLoadAllEndpointsSuccess() {
        // Allow children to implement this
    }
    handleRequestSuccess({ stateKey, data, resp }, initialRequest) {
        this.setState(prevState => {
            const state = {
                [stateKey]: data,
                // TODO(billy): This currently fails if this request is retried by SudoModal
                [`${stateKey}PageLinks`]: resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link'),
            };
            if (initialRequest) {
                state.remainingRequests = prevState.remainingRequests - 1;
                state.loading = prevState.remainingRequests > 1;
                state.reloading = prevState.reloading && state.loading;
                this.markShouldMeasure({ remainingRequests: state.remainingRequests });
            }
            return state;
        }, () => {
            // if everything is loaded and we don't have an error, call the callback
            if (this.state.remainingRequests === 0 && !this.state.error) {
                this.onLoadAllEndpointsSuccess();
            }
        });
        this.onRequestSuccess({ stateKey, data, resp });
    }
    handleError(error, args) {
        const [stateKey] = args;
        if (error && error.responseText) {
            Sentry.addBreadcrumb({
                message: error.responseText,
                category: 'xhr',
                level: Sentry.Severity.Error,
            });
        }
        this.setState(prevState => {
            const loading = prevState.remainingRequests > 1;
            const state = {
                [stateKey]: null,
                errors: Object.assign(Object.assign({}, prevState.errors), { [stateKey]: error }),
                error: prevState.error || !!error,
                remainingRequests: prevState.remainingRequests - 1,
                loading,
                reloading: prevState.reloading && loading,
            };
            this.markShouldMeasure({ remainingRequests: state.remainingRequests, error: true });
            return state;
        });
        this.onRequestError(error, args);
    }
    /**
     * @deprecated use getEndpoints
     */
    getEndpointParams() {
        // eslint-disable-next-line no-console
        console.warn('getEndpointParams is deprecated');
        return {};
    }
    /**
     * @deprecated use getEndpoints
     */
    getEndpoint() {
        // eslint-disable-next-line no-console
        console.warn('getEndpoint is deprecated');
        return null;
    }
    /**
     * Return a list of endpoint queries to make.
     *
     * return [
     *   ['stateKeyName', '/endpoint/', {optional: 'query params'}, {options}]
     * ]
     */
    getEndpoints() {
        const endpoint = this.getEndpoint();
        if (!endpoint) {
            return [];
        }
        return [['data', endpoint, this.getEndpointParams()]];
    }
    renderSearchInput(_a) {
        var { stateKey, url } = _a, props = (0, tslib_1.__rest)(_a, ["stateKey", "url"]);
        const [firstEndpoint] = this.getEndpoints() || [null];
        const stateKeyOrDefault = stateKey || (firstEndpoint && firstEndpoint[0]);
        const urlOrDefault = url || (firstEndpoint && firstEndpoint[1]);
        return (<asyncComponentSearchInput_1.default url={urlOrDefault} {...props} api={this.api} onSuccess={(data, resp) => {
                this.handleRequestSuccess({ stateKey: stateKeyOrDefault, data, resp });
            }} onError={() => {
                this.renderError(new Error('Error with AsyncComponentSearchInput'));
            }}/>);
    }
    renderLoading() {
        return <loadingIndicator_1.default />;
    }
    renderError(error, disableLog = false, disableReport = false) {
        const { errors } = this.state;
        // 401s are captured by SudoModal, but may be passed back to AsyncComponent if they close the modal without identifying
        const unauthorizedErrors = Object.values(errors).find(resp => resp && resp.status === 401);
        // Look through endpoint results to see if we had any 403s, means their role can not access resource
        const permissionErrors = Object.values(errors).find(resp => resp && resp.status === 403);
        // If all error responses have status code === 0, then show error message but don't
        // log it to sentry
        const shouldLogSentry = !!Object.values(errors).find(resp => resp && resp.status !== 0) || disableLog;
        if (unauthorizedErrors) {
            return (<loadingError_1.default message={(0, locale_1.t)('You are not authorized to access this resource.')}/>);
        }
        if (permissionErrors) {
            return <permissionDenied_1.default />;
        }
        if (this.shouldRenderBadRequests) {
            const badRequests = Object.values(errors)
                .filter(resp => resp && resp.status === 400 && resp.responseJSON && resp.responseJSON.detail)
                .map(resp => resp.responseJSON.detail);
            if (badRequests.length) {
                return <loadingError_1.default message={[...new Set(badRequests)].join('\n')}/>;
            }
        }
        return (<routeError_1.default error={error} disableLogSentry={!shouldLogSentry} disableReport={disableReport}/>);
    }
    shouldRenderLoading() {
        const { loading, reloading } = this.state;
        return loading && (!this.shouldReload || !reloading);
    }
    renderComponent() {
        return this.shouldRenderLoading()
            ? this.renderLoading()
            : this.state.error
                ? this.renderError(new Error('Unable to load all required endpoints'))
                : this.renderBody();
    }
    /**
     * Renders once all endpoints have been loaded
     */
    renderBody() {
        // Allow children to implement this
        throw new Error('Not implemented');
    }
    render() {
        return this.renderComponent();
    }
}
exports.default = AsyncComponent;
AsyncComponent.contextTypes = {
    router: prop_types_1.default.object,
};
//# sourceMappingURL=asyncComponent.jsx.map