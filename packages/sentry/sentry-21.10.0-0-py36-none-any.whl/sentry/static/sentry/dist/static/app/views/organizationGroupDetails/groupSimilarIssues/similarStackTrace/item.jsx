Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const modal_1 = require("app/actionCreators/modal");
const groupingActions_1 = (0, tslib_1.__importDefault)(require("app/actions/groupingActions"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const eventOrGroupExtraDetails_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupExtraDetails"));
const eventOrGroupHeader_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupHeader"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const panels_1 = require("app/components/panels");
const scoreBar_1 = (0, tslib_1.__importDefault)(require("app/components/scoreBar"));
const similarScoreCard_1 = (0, tslib_1.__importDefault)(require("app/components/similarScoreCard"));
const locale_1 = require("app/locale");
const groupingStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupingStore"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const initialState = { visible: true, checked: false, busy: false };
class Item extends React.Component {
    constructor() {
        super(...arguments);
        this.state = initialState;
        this.listener = groupingStore_1.default.listen(data => this.onGroupChange(data), undefined);
        this.handleToggle = () => {
            const { issue } = this.props;
            // clicking anywhere in the row will toggle the checkbox
            if (!this.state.busy) {
                groupingActions_1.default.toggleMerge(issue.id);
            }
        };
        this.handleShowDiff = (event) => {
            const { orgId, groupId: baseIssueId, issue, project } = this.props;
            const { id: targetIssueId } = issue;
            (0, modal_1.openDiffModal)({ baseIssueId, targetIssueId, project, orgId });
            event.stopPropagation();
        };
        this.handleCheckClick = () => {
            // noop to appease React warnings
            // This is controlled via row click instead of only Checkbox
        };
        this.onGroupChange = ({ mergeState }) => {
            if (!mergeState) {
                return;
            }
            const { issue } = this.props;
            const stateForId = mergeState.has(issue.id) && mergeState.get(issue.id);
            if (!stateForId) {
                return;
            }
            Object.keys(stateForId).forEach(key => {
                if (stateForId[key] === this.state[key]) {
                    return;
                }
                this.setState(prevState => (Object.assign(Object.assign({}, prevState), { [key]: stateForId[key] })));
            });
        };
    }
    componentWillUnmount() {
        (0, callIfFunction_1.callIfFunction)(this.listener);
    }
    render() {
        const { aggregate, scoresByInterface, issue, v2 } = this.props;
        const { visible, busy } = this.state;
        const similarInterfaces = v2 ? ['similarity'] : ['exception', 'message'];
        if (!visible) {
            return null;
        }
        const cx = (0, classnames_1.default)('group', {
            isResolved: issue.status === 'resolved',
            busy,
        });
        return (<StyledPanelItem data-test-id="similar-item-row" className={cx} onClick={this.handleToggle}>
        <Details>
          <checkbox_1.default id={issue.id} value={issue.id} checked={this.state.checked} onChange={this.handleCheckClick}/>
          <EventDetails>
            <eventOrGroupHeader_1.default data={issue} includeLink size="normal"/>
            <eventOrGroupExtraDetails_1.default data={Object.assign(Object.assign({}, issue), { lastSeen: '' })} showAssignee/>
          </EventDetails>

          <Diff>
            <button_1.default onClick={this.handleShowDiff} size="small">
              {(0, locale_1.t)('Diff')}
            </button_1.default>
          </Diff>
        </Details>

        <Columns>
          <StyledCount value={issue.count}/>

          {similarInterfaces.map(interfaceName => {
                const avgScore = aggregate === null || aggregate === void 0 ? void 0 : aggregate[interfaceName];
                const scoreList = (scoresByInterface === null || scoresByInterface === void 0 ? void 0 : scoresByInterface[interfaceName]) || [];
                // Check for valid number (and not NaN)
                const scoreValue = typeof avgScore === 'number' && !Number.isNaN(avgScore) ? avgScore : 0;
                return (<Column key={interfaceName}>
                <hovercard_1.default body={scoreList.length && <similarScoreCard_1.default scoreList={scoreList}/>}>
                  <scoreBar_1.default vertical score={Math.round(scoreValue * 5)}/>
                </hovercard_1.default>
              </Column>);
            })}
        </Columns>
      </StyledPanelItem>);
    }
}
const Details = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};

  display: grid;
  gap: ${(0, space_1.default)(1)};
  grid-template-columns: max-content auto max-content;
  margin-left: ${(0, space_1.default)(2)};

  input[type='checkbox'] {
    margin: 0;
  }
`;
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  padding: ${(0, space_1.default)(1)} 0;
`;
const Columns = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  flex-shrink: 0;
  min-width: 300px;
  width: 300px;
`;
const columnStyle = (0, react_1.css) `
  flex: 1;
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  padding: ${(0, space_1.default)(0.5)} 0;
`;
const Column = (0, styled_1.default)('div') `
  ${columnStyle}
`;
const StyledCount = (0, styled_1.default)(count_1.default) `
  ${columnStyle}
  font-variant-numeric: tabular-nums;
`;
const Diff = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-right: ${(0, space_1.default)(0.25)};
`;
const EventDetails = (0, styled_1.default)('div') `
  flex: 1;
  ${overflowEllipsis_1.default};
`;
exports.default = Item;
//# sourceMappingURL=item.jsx.map