Object.defineProperty(exports, "__esModule", { value: true });
exports.DataExport = exports.ExportQueryType = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const indicator_1 = require("app/actionCreators/indicator");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
// NOTE: Coordinate with other ExportQueryType (src/sentry/data_export/base.py)
var ExportQueryType;
(function (ExportQueryType) {
    ExportQueryType["IssuesByTag"] = "Issues-by-Tag";
    ExportQueryType["Discover"] = "Discover";
})(ExportQueryType = exports.ExportQueryType || (exports.ExportQueryType = {}));
class DataExport extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.initialState;
        this.resetState = () => {
            this.setState(this.initialState);
        };
        this.startDataExport = () => {
            const { api, organization: { slug }, payload: { queryType, queryInfo }, } = this.props;
            this.setState({ inProgress: true });
            api
                .requestPromise(`/organizations/${slug}/data-export/`, {
                includeAllArgs: true,
                method: 'POST',
                data: {
                    query_type: queryType,
                    query_info: queryInfo,
                },
            })
                .then(([_data, _, response]) => {
                (0, indicator_1.addSuccessMessage)((response === null || response === void 0 ? void 0 : response.status) === 201
                    ? (0, locale_1.t)("Sit tight. We'll shoot you an email when your data is ready for download.")
                    : (0, locale_1.t)("It looks like we're already working on it. Sit tight, we'll email you."));
            })
                .catch(err => {
                var _a, _b;
                const message = (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : "We tried our hardest, but we couldn't export your data. Give it another go.";
                (0, indicator_1.addErrorMessage)((0, locale_1.t)(message));
                this.setState({ inProgress: false });
            });
        };
    }
    componentDidUpdate({ payload: prevPayload }) {
        const { payload } = this.props;
        if (!(0, isEqual_1.default)(prevPayload, payload))
            this.resetState();
    }
    get initialState() {
        return {
            inProgress: false,
        };
    }
    render() {
        const { inProgress } = this.state;
        const { children, disabled, icon } = this.props;
        return (<feature_1.default features={['organizations:discover-query']}>
        {inProgress ? (<button_1.default size="small" priority="default" title="You can get on with your life. We'll email you when your data's ready." {...this.props} disabled icon={icon}>
            {(0, locale_1.t)("We're working on it...")}
          </button_1.default>) : (<button_1.default onClick={(0, debounce_1.default)(this.startDataExport, 500)} disabled={disabled || false} size="small" priority="default" title="Put your data to work. Start your export and we'll email you when it's finished." icon={icon} {...this.props}>
            {children ? children : (0, locale_1.t)('Export All to CSV')}
          </button_1.default>)}
      </feature_1.default>);
    }
}
exports.DataExport = DataExport;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(DataExport));
//# sourceMappingURL=dataExport.jsx.map