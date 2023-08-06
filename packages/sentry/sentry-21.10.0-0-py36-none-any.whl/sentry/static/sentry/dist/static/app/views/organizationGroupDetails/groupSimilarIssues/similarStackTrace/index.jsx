Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const queryString = (0, tslib_1.__importStar)(require("query-string"));
const groupingActions_1 = (0, tslib_1.__importDefault)(require("app/actions/groupingActions"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const groupingStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupingStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const list_1 = (0, tslib_1.__importDefault)(require("./list"));
class SimilarStackTrace extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            similarItems: [],
            filteredSimilarItems: [],
            similarLinks: null,
            loading: true,
            error: false,
            v2: false,
        };
        this.onGroupingChange = ({ mergedParent, similarItems, similarLinks, filteredSimilarItems, loading, error, }) => {
            if (similarItems) {
                this.setState({
                    similarItems,
                    similarLinks,
                    filteredSimilarItems,
                    loading: loading !== null && loading !== void 0 ? loading : false,
                    error: error !== null && error !== void 0 ? error : false,
                });
                return;
            }
            if (!mergedParent) {
                return;
            }
            if (mergedParent !== this.props.params.groupId) {
                const { params } = this.props;
                // Merge success, since we can't specify target, we need to redirect to new parent
                react_router_1.browserHistory.push(`/organizations/${params.orgId}/issues/${mergedParent}/similar/`);
                return;
            }
            return;
        };
        this.listener = groupingStore_1.default.listen(this.onGroupingChange, undefined);
        this.handleMerge = () => {
            const { params, location } = this.props;
            const query = location.query;
            if (!params) {
                return;
            }
            // You need at least 1 similarItem OR filteredSimilarItems to be able to merge,
            // so `firstIssue` should always exist from one of those lists.
            //
            // Similar issues API currently does not return issues across projects,
            // so we can assume that the first issues project slug is the project in
            // scope
            const [firstIssue] = this.state.similarItems.length
                ? this.state.similarItems
                : this.state.filteredSimilarItems;
            groupingActions_1.default.merge({
                params,
                query,
                projectId: firstIssue.issue.project.slug,
            });
        };
        this.toggleSimilarityVersion = () => {
            this.setState(prevState => ({ v2: !prevState.v2 }), this.fetchData);
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.params.groupId !== this.props.params.groupId ||
            nextProps.location.search !== this.props.location.search) {
            this.fetchData();
        }
    }
    componentWillUnmount() {
        (0, callIfFunction_1.callIfFunction)(this.listener);
    }
    fetchData() {
        const { params, location } = this.props;
        this.setState({ loading: true, error: false });
        const reqs = [];
        if (this.hasSimilarityFeature()) {
            const version = this.state.v2 ? '2' : '1';
            reqs.push({
                endpoint: `/issues/${params.groupId}/similar/?${queryString.stringify(Object.assign(Object.assign({}, location.query), { limit: 50, version }))}`,
                dataKey: 'similar',
            });
        }
        groupingActions_1.default.fetch(reqs);
    }
    hasSimilarityV2Feature() {
        return this.props.project.features.includes('similarity-view-v2');
    }
    hasSimilarityFeature() {
        return this.props.project.features.includes('similarity-view');
    }
    render() {
        const { params, project } = this.props;
        const { orgId, groupId } = params;
        const { similarItems, filteredSimilarItems, loading, error, v2, similarLinks } = this.state;
        const hasV2 = this.hasSimilarityV2Feature();
        const isLoading = loading;
        const isError = error && !isLoading;
        const isLoadedSuccessfully = !isError && !isLoading;
        const hasSimilarItems = this.hasSimilarityFeature() &&
            (similarItems.length >= 0 || filteredSimilarItems.length >= 0) &&
            isLoadedSuccessfully;
        return (<React.Fragment>
        <alert_1.default type="warning">
          {(0, locale_1.t)('This is an experimental feature. Data may not be immediately available while we process merges.')}
        </alert_1.default>
        <HeaderWrapper>
          <Title>{(0, locale_1.t)('Issues with a similar stack trace')}</Title>
          {hasV2 && (<buttonBar_1.default merged active={v2 ? 'new' : 'old'}>
              <button_1.default barId="old" size="small" onClick={this.toggleSimilarityVersion}>
                {(0, locale_1.t)('Old Algorithm')}
              </button_1.default>
              <button_1.default barId="new" size="small" onClick={this.toggleSimilarityVersion}>
                {(0, locale_1.t)('New Algorithm')}
              </button_1.default>
            </buttonBar_1.default>)}
        </HeaderWrapper>
        {isLoading && <loadingIndicator_1.default />}
        {isError && (<loadingError_1.default message={(0, locale_1.t)('Unable to load similar issues, please try again later')} onRetry={this.fetchData}/>)}
        {hasSimilarItems && (<list_1.default items={similarItems} filteredItems={filteredSimilarItems} onMerge={this.handleMerge} orgId={orgId} project={project} groupId={groupId} pageLinks={similarLinks} v2={v2}/>)}
      </React.Fragment>);
    }
}
exports.default = SimilarStackTrace;
const Title = (0, styled_1.default)('h4') `
  margin-bottom: 0;
`;
const HeaderWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=index.jsx.map