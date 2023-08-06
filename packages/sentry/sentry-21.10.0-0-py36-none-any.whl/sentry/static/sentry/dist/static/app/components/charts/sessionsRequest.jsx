Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const omitBy_1 = (0, tslib_1.__importDefault)(require("lodash/omitBy"));
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const sessions_1 = require("app/utils/sessions");
const propNamesToIgnore = ['api', 'children', 'organization'];
const omitIgnoredProps = (props) => (0, omitBy_1.default)(props, (_value, key) => propNamesToIgnore.includes(key));
class SessionsRequest extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            reloading: false,
            errored: false,
            response: null,
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a, _b;
            const { api, isDisabled, shouldFilterSessionsInTimeWindow } = this.props;
            if (isDisabled) {
                return;
            }
            this.setState(state => ({
                reloading: state.response !== null,
                errored: false,
            }));
            try {
                const response = yield api.requestPromise(this.path, {
                    query: this.baseQueryParams,
                });
                this.setState({
                    reloading: false,
                    response: shouldFilterSessionsInTimeWindow
                        ? (0, sessions_1.filterSessionsInTimeWindow)(response, this.baseQueryParams.start, this.baseQueryParams.end)
                        : response,
                });
            }
            catch (error) {
                (0, indicator_1.addErrorMessage)((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : (0, locale_1.t)('Error loading health data'));
                this.setState({
                    reloading: false,
                    errored: true,
                });
            }
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if ((0, isEqual_1.default)(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    }
    get path() {
        const { organization } = this.props;
        return `/organizations/${organization.slug}/sessions/`;
    }
    get baseQueryParams() {
        const { project, environment, field, statsPeriod, start, end, query, groupBy, interval, organization, } = this.props;
        return {
            project,
            environment,
            field,
            statsPeriod,
            query,
            groupBy,
            start,
            end,
            interval: interval
                ? interval
                : (0, sessions_1.getSessionsInterval)({ start, end, period: statsPeriod }, { highFidelity: organization.features.includes('minute-resolution-sessions') }),
        };
    }
    render() {
        const { reloading, errored, response } = this.state;
        const { children } = this.props;
        const loading = response === null;
        return children({
            loading,
            reloading,
            errored,
            response,
        });
    }
}
exports.default = SessionsRequest;
//# sourceMappingURL=sessionsRequest.jsx.map