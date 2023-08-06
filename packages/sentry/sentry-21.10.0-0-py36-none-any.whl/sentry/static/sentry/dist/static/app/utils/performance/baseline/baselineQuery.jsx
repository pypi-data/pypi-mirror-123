Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class BaselineQuery extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            isLoading: true,
            fetchID: undefined,
            error: null,
            results: null,
        };
        this.shouldRefetchData = (prevProps) => {
            const thisAPIPayload = this.generatePayload(this.props.eventView);
            const otherAPIPayload = this.generatePayload(prevProps.eventView);
            return !(0, isEqual_1.default)(thisAPIPayload, otherAPIPayload);
        };
        this.fetchData = () => {
            const { eventView, orgSlug } = this.props;
            if (!eventView.isValid()) {
                return;
            }
            const url = `/organizations/${orgSlug}/event-baseline/`;
            const fetchID = Symbol('fetchID');
            this.setState({ isLoading: true, fetchID });
            this.props.api
                .requestPromise(url, {
                method: 'GET',
                query: Object.assign(Object.assign({}, eventView.getGlobalSelectionQuery()), { query: eventView.query }),
            })
                .then(data => {
                if (this.state.fetchID !== fetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                this.setState({
                    isLoading: false,
                    fetchID: undefined,
                    error: null,
                    results: data,
                });
            })
                .catch(err => {
                var _a, _b;
                this.setState({
                    isLoading: false,
                    fetchID: undefined,
                    error: (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : null,
                    results: null,
                });
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        // Reload data if we aren't already loading,
        const refetchCondition = !this.state.isLoading && this.shouldRefetchData(prevProps);
        if (refetchCondition) {
            this.fetchData();
        }
    }
    generatePayload(eventView) {
        return Object.assign(Object.assign({}, eventView.getGlobalSelectionQuery()), { query: eventView.query });
    }
    render() {
        const { isLoading, error, results } = this.state;
        const childrenProps = {
            isLoading,
            error,
            results,
        };
        return this.props.children(childrenProps);
    }
}
exports.default = (0, withApi_1.default)(BaselineQuery);
//# sourceMappingURL=baselineQuery.jsx.map