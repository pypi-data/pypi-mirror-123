Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupMergedView = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const queryString = (0, tslib_1.__importStar)(require("query-string"));
const groupingActions_1 = (0, tslib_1.__importDefault)(require("app/actions/groupingActions"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const groupingStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupingStore"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const mergedList_1 = (0, tslib_1.__importDefault)(require("./mergedList"));
class GroupMergedView extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            mergedItems: [],
            loading: true,
            error: false,
            query: this.props.location.query.query || '',
        };
        this.onGroupingChange = ({ mergedItems, mergedLinks, loading, error }) => {
            if (mergedItems) {
                this.setState({
                    mergedItems,
                    mergedLinks,
                    loading: typeof loading !== 'undefined' ? loading : false,
                    error: typeof error !== 'undefined' ? error : false,
                });
            }
        };
        this.listener = groupingStore_1.default.listen(this.onGroupingChange, undefined);
        this.fetchData = () => {
            groupingActions_1.default.fetch([
                {
                    endpoint: this.getEndpoint(),
                    dataKey: 'merged',
                    queryParams: this.props.location.query,
                },
            ]);
        };
        this.handleUnmerge = () => {
            groupingActions_1.default.unmerge({
                groupId: this.props.params.groupId,
                loadingMessage: (0, locale_1.t)('Unmerging events\u2026'),
                successMessage: (0, locale_1.t)('Events successfully queued for unmerging.'),
                errorMessage: (0, locale_1.t)('Unable to queue events for unmerging.'),
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.params.groupId !== this.props.params.groupId ||
            nextProps.location.search !== this.props.location.search) {
            const queryParams = nextProps.location.query;
            this.setState({
                query: queryParams.query,
            }, this.fetchData);
        }
    }
    componentWillUnmount() {
        (0, callIfFunction_1.callIfFunction)(this.listener);
    }
    getEndpoint() {
        const { params, location } = this.props;
        const { groupId } = params;
        const queryParams = Object.assign(Object.assign({}, location.query), { limit: 50, query: this.state.query });
        return `/issues/${groupId}/hashes/?${queryString.stringify(queryParams)}`;
    }
    render() {
        const { project, params } = this.props;
        const { groupId } = params;
        const { loading: isLoading, error, mergedItems, mergedLinks } = this.state;
        const isError = error && !isLoading;
        const isLoadedSuccessfully = !isError && !isLoading;
        return (<react_1.Fragment>
        <alert_1.default type="warning">
          {(0, locale_1.t)('This is an experimental feature. Data may not be immediately available while we process unmerges.')}
        </alert_1.default>

        {isLoading && <loadingIndicator_1.default />}
        {isError && (<loadingError_1.default message={(0, locale_1.t)('Unable to load merged events, please try again later')} onRetry={this.fetchData}/>)}

        {isLoadedSuccessfully && (<mergedList_1.default project={project} fingerprints={mergedItems} pageLinks={mergedLinks} groupId={groupId} onUnmerge={this.handleUnmerge} onToggleCollapse={groupingActions_1.default.toggleCollapseFingerprints}/>)}
      </react_1.Fragment>);
    }
}
exports.GroupMergedView = GroupMergedView;
exports.default = (0, withOrganization_1.default)(GroupMergedView);
//# sourceMappingURL=index.jsx.map