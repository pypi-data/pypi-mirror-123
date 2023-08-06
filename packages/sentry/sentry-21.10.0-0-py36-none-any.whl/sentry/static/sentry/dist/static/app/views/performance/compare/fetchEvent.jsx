Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class FetchEvent extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isLoading: true,
            tableFetchID: undefined,
            error: null,
            event: undefined,
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        const orgSlugChanged = prevProps.orgSlug !== this.props.orgSlug;
        const eventSlugChanged = prevProps.eventSlug !== this.props.eventSlug;
        if (!this.state.isLoading && (orgSlugChanged || eventSlugChanged)) {
            this.fetchData();
        }
    }
    fetchData() {
        const { orgSlug, eventSlug } = this.props;
        // note: eventSlug is of the form <project-slug>:<event-id>
        const url = `/organizations/${orgSlug}/events/${eventSlug}/`;
        const tableFetchID = Symbol('tableFetchID');
        this.setState({ isLoading: true, tableFetchID });
        this.props.api
            .requestPromise(url, {
            method: 'GET',
        })
            .then(data => {
            if (this.state.tableFetchID !== tableFetchID) {
                // invariant: a different request was initiated after this request
                return;
            }
            this.setState({
                isLoading: false,
                tableFetchID: undefined,
                error: null,
                event: data,
            });
        })
            .catch(err => {
            var _a, _b;
            this.setState({
                isLoading: false,
                tableFetchID: undefined,
                error: (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : null,
                event: undefined,
            });
        });
    }
    render() {
        const { isLoading, error, event } = this.state;
        const childrenProps = {
            isLoading,
            error,
            event,
        };
        return this.props.children(childrenProps);
    }
}
exports.default = (0, withApi_1.default)(FetchEvent);
//# sourceMappingURL=fetchEvent.jsx.map