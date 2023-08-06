Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueDiff = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getStacktraceBody_1 = (0, tslib_1.__importDefault)(require("app/utils/getStacktraceBody"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const renderGroupingInfo_1 = (0, tslib_1.__importDefault)(require("./renderGroupingInfo"));
const defaultProps = {
    baseEventId: 'latest',
    targetEventId: 'latest',
};
class IssueDiff extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            groupingDiff: false,
            baseEvent: [],
            targetEvent: [],
            // `SplitDiffAsync` is an async-loaded component
            // This will eventually contain a reference to the exported component from `./splitDiff`
            SplitDiffAsync: undefined,
        };
        this.toggleDiffMode = () => {
            this.setState(state => ({ groupingDiff: !state.groupingDiff, loading: true }), this.fetchData);
        };
        this.fetchEventData = (issueId, eventId) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { orgId, project, api } = this.props;
            const { groupingDiff } = this.state;
            let paramEventId = eventId;
            if (eventId === 'latest') {
                const event = yield api.requestPromise(`/issues/${issueId}/events/latest/`);
                paramEventId = event.eventID;
            }
            if (groupingDiff) {
                const groupingInfo = yield api.requestPromise(`/projects/${orgId}/${project.slug}/events/${paramEventId}/grouping-info/`);
                return (0, renderGroupingInfo_1.default)(groupingInfo);
            }
            const event = yield api.requestPromise(`/projects/${orgId}/${project.slug}/events/${paramEventId}/`);
            return (0, getStacktraceBody_1.default)(event);
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    fetchData() {
        const { baseIssueId, targetIssueId, baseEventId, targetEventId } = this.props;
        // Fetch component and event data
        Promise.all([
            Promise.resolve().then(() => (0, tslib_1.__importStar)(require('../splitDiff'))),
            this.fetchEventData(baseIssueId, baseEventId !== null && baseEventId !== void 0 ? baseEventId : 'latest'),
            this.fetchEventData(targetIssueId, targetEventId !== null && targetEventId !== void 0 ? targetEventId : 'latest'),
        ])
            .then(([{ default: SplitDiffAsync }, baseEvent, targetEvent]) => {
            this.setState({
                SplitDiffAsync,
                baseEvent,
                targetEvent,
                loading: false,
            });
        })
            .catch(() => {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error loading events'));
        });
    }
    render() {
        const { className, project } = this.props;
        const { SplitDiffAsync: DiffComponent, loading, groupingDiff, baseEvent, targetEvent, } = this.state;
        const showDiffToggle = project.features.includes('similarity-view-v2');
        return (<StyledIssueDiff className={className} loading={loading}>
        {loading && <loadingIndicator_1.default />}
        {!loading && showDiffToggle && (<HeaderWrapper>
            <buttonBar_1.default merged active={groupingDiff ? 'grouping' : 'event'}>
              <button_1.default barId="event" size="small" onClick={this.toggleDiffMode}>
                {(0, locale_1.t)('Diff stack trace and message')}
              </button_1.default>
              <button_1.default barId="grouping" size="small" onClick={this.toggleDiffMode}>
                {(0, locale_1.t)('Diff grouping information')}
              </button_1.default>
            </buttonBar_1.default>
          </HeaderWrapper>)}
        {!loading &&
                DiffComponent &&
                baseEvent.map((value, i) => {
                    var _a;
                    return (<DiffComponent key={i} base={value} target={(_a = targetEvent[i]) !== null && _a !== void 0 ? _a : ''} type="words"/>);
                })}
      </StyledIssueDiff>);
    }
}
exports.IssueDiff = IssueDiff;
IssueDiff.defaultProps = defaultProps;
exports.default = (0, withApi_1.default)(IssueDiff);
const StyledIssueDiff = (0, styled_1.default)('div', {
    shouldForwardProp: p => typeof p === 'string' && (0, is_prop_valid_1.default)(p) && p !== 'loading',
}) `
  background-color: ${p => p.theme.backgroundSecondary};
  overflow: auto;
  padding: ${(0, space_1.default)(1)};
  flex: 1;
  display: flex;
  flex-direction: column;

  ${p => p.loading &&
    `
        background-color: ${p.theme.background};
        justify-content: center;
        align-items: center;
      `};
`;
const HeaderWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=index.jsx.map