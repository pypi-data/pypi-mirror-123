Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const groupingStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupingStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class MergedToolbar extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.listener = groupingStore_1.default.listen(data => this.onGroupChange(data), undefined);
        this.onGroupChange = updateObj => {
            const allowedKeys = [
                'unmergeLastCollapsed',
                'unmergeDisabled',
                'unmergeList',
                'enableFingerprintCompare',
            ];
            this.setState((0, pick_1.default)(updateObj, allowedKeys));
        };
        this.handleShowDiff = (event) => {
            const { groupId, project, orgId } = this.props;
            const { unmergeList } = this.state;
            const entries = unmergeList.entries();
            // `unmergeList` should only have 2 items in map
            if (unmergeList.size !== 2) {
                return;
            }
            // only need eventId, not fingerprint
            const [baseEventId, targetEventId] = Array.from(entries).map(([, eventId]) => eventId);
            (0, modal_1.openDiffModal)({
                targetIssueId: groupId,
                project,
                baseIssueId: groupId,
                orgId,
                baseEventId,
                targetEventId,
            });
            event.stopPropagation();
        };
    }
    getInitialState() {
        const { unmergeList, unmergeLastCollapsed, unmergeDisabled, enableFingerprintCompare } = groupingStore_1.default;
        return {
            enableFingerprintCompare,
            unmergeList,
            unmergeLastCollapsed,
            unmergeDisabled,
        };
    }
    componentWillUnmount() {
        var _a;
        (_a = this.listener) === null || _a === void 0 ? void 0 : _a.call(this);
    }
    render() {
        const { onUnmerge, onToggleCollapse } = this.props;
        const { unmergeList, unmergeLastCollapsed, unmergeDisabled, enableFingerprintCompare } = this.state;
        const unmergeCount = (unmergeList && unmergeList.size) || 0;
        return (<panels_1.PanelHeader hasButtons>
        <div>
          <confirm_1.default disabled={unmergeDisabled} onConfirm={onUnmerge} message={(0, locale_1.t)('These events will be unmerged and grouped into a new issue. Are you sure you want to unmerge these events?')}>
            <button_1.default size="small" title={(0, locale_1.tct)('Unmerging [unmergeCount] events', { unmergeCount })}>
              {(0, locale_1.t)('Unmerge')} ({unmergeCount || 0})
            </button_1.default>
          </confirm_1.default>

          <CompareButton size="small" disabled={!enableFingerprintCompare} onClick={this.handleShowDiff}>
            {(0, locale_1.t)('Compare')}
          </CompareButton>
        </div>
        <button_1.default size="small" onClick={onToggleCollapse}>
          {unmergeLastCollapsed ? (0, locale_1.t)('Expand All') : (0, locale_1.t)('Collapse All')}
        </button_1.default>
      </panels_1.PanelHeader>);
    }
}
exports.default = MergedToolbar;
const CompareButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=mergedToolbar.jsx.map