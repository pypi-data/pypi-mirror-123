Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueListActions = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const uniq_1 = (0, tslib_1.__importDefault)(require("lodash/uniq"));
const group_1 = require("app/actionCreators/group");
const indicator_1 = require("app/actionCreators/indicator");
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const locale_1 = require("app/locale");
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const selectedGroupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/selectedGroupStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const actionSet_1 = (0, tslib_1.__importDefault)(require("./actionSet"));
const headers_1 = (0, tslib_1.__importDefault)(require("./headers"));
const utils_1 = require("./utils");
class IssueListActions extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            anySelected: false,
            multiSelected: false,
            pageSelected: false,
            allInQuerySelected: false,
            selectedIds: new Set(),
        };
        this.listener = selectedGroupStore_1.default.listen(() => this.handleSelectedGroupChange(), undefined);
        this.handleSelectStatsPeriod = (period) => {
            return this.props.onSelectStatsPeriod(period);
        };
        this.handleApplyToAll = () => {
            this.setState({ allInQuerySelected: true });
        };
        this.handleUpdate = (data) => {
            const { selection, api, organization, query, onMarkReviewed } = this.props;
            const orgId = organization.slug;
            this.actionSelectedGroups(itemIds => {
                (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
                if ((data === null || data === void 0 ? void 0 : data.inbox) === false) {
                    onMarkReviewed === null || onMarkReviewed === void 0 ? void 0 : onMarkReviewed(itemIds !== null && itemIds !== void 0 ? itemIds : []);
                }
                // If `itemIds` is undefined then it means we expect to bulk update all items
                // that match the query.
                //
                // We need to always respect the projects selected in the global selection header:
                // * users with no global views requires a project to be specified
                // * users with global views need to be explicit about what projects the query will run against
                const projectConstraints = { project: selection.projects };
                (0, group_1.bulkUpdate)(api, Object.assign(Object.assign({ orgId,
                    itemIds,
                    data,
                    query, environment: selection.environments }, projectConstraints), selection.datetime), {
                    complete: () => {
                        (0, indicator_1.clearIndicators)();
                    },
                });
            });
        };
        this.handleDelete = () => {
            const { selection, api, organization, query, onDelete } = this.props;
            const orgId = organization.slug;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Removing events\u2026'));
            this.actionSelectedGroups(itemIds => {
                (0, group_1.bulkDelete)(api, Object.assign({ orgId,
                    itemIds,
                    query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                    complete: () => {
                        (0, indicator_1.clearIndicators)();
                        onDelete();
                    },
                });
            });
        };
        this.handleMerge = () => {
            const { selection, api, organization, query } = this.props;
            const orgId = organization.slug;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Merging events\u2026'));
            this.actionSelectedGroups(itemIds => {
                (0, group_1.mergeGroups)(api, Object.assign({ orgId,
                    itemIds,
                    query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                    complete: () => {
                        (0, indicator_1.clearIndicators)();
                    },
                });
            });
        };
        this.shouldConfirm = (action) => {
            const selectedItems = selectedGroupStore_1.default.getSelectedIds();
            switch (action) {
                case utils_1.ConfirmAction.RESOLVE:
                case utils_1.ConfirmAction.UNRESOLVE:
                case utils_1.ConfirmAction.IGNORE:
                case utils_1.ConfirmAction.UNBOOKMARK: {
                    const { pageSelected } = this.state;
                    return pageSelected && selectedItems.size > 1;
                }
                case utils_1.ConfirmAction.BOOKMARK:
                    return selectedItems.size > 1;
                case utils_1.ConfirmAction.MERGE:
                case utils_1.ConfirmAction.DELETE:
                default:
                    return true; // By default, should confirm ...
            }
        };
    }
    componentDidMount() {
        this.handleSelectedGroupChange();
    }
    componentWillUnmount() {
        (0, callIfFunction_1.callIfFunction)(this.listener);
    }
    actionSelectedGroups(callback) {
        let selectedIds;
        if (this.state.allInQuerySelected) {
            selectedIds = undefined; // undefined means "all"
        }
        else {
            const itemIdSet = selectedGroupStore_1.default.getSelectedIds();
            selectedIds = this.props.groupIds.filter(itemId => itemIdSet.has(itemId));
        }
        callback(selectedIds);
        this.deselectAll();
    }
    deselectAll() {
        selectedGroupStore_1.default.deselectAll();
        this.setState({ allInQuerySelected: false });
    }
    // Handler for when `SelectedGroupStore` changes
    handleSelectedGroupChange() {
        const selected = selectedGroupStore_1.default.getSelectedIds();
        const projects = [...selected]
            .map(id => groupStore_1.default.get(id))
            .filter((group) => !!(group && group.project))
            .map(group => group.project.slug);
        const uniqProjects = (0, uniq_1.default)(projects);
        // we only want selectedProjectSlug set if there is 1 project
        // more or fewer should result in a null so that the action toolbar
        // can behave correctly.
        const selectedProjectSlug = uniqProjects.length === 1 ? uniqProjects[0] : undefined;
        this.setState({
            pageSelected: selectedGroupStore_1.default.allSelected(),
            multiSelected: selectedGroupStore_1.default.multiSelected(),
            anySelected: selectedGroupStore_1.default.anySelected(),
            allInQuerySelected: false,
            selectedIds: selectedGroupStore_1.default.getSelectedIds(),
            selectedProjectSlug,
        });
    }
    handleSelectAll() {
        selectedGroupStore_1.default.toggleSelectAll();
    }
    render() {
        const { allResultsVisible, queryCount, query, statsPeriod, selection, organization, displayReprocessingActions, } = this.props;
        const { allInQuerySelected, anySelected, pageSelected, selectedIds: issues, multiSelected, selectedProjectSlug, } = this.state;
        const numIssues = issues.size;
        return (<Sticky>
        <StyledFlex>
          <ActionsCheckbox isReprocessingQuery={displayReprocessingActions}>
            <checkbox_1.default onChange={this.handleSelectAll} checked={pageSelected} disabled={displayReprocessingActions}/>
          </ActionsCheckbox>
          {!displayReprocessingActions && (<actionSet_1.default orgSlug={organization.slug} queryCount={queryCount} query={query} issues={issues} allInQuerySelected={allInQuerySelected} anySelected={anySelected} multiSelected={multiSelected} selectedProjectSlug={selectedProjectSlug} onShouldConfirm={this.shouldConfirm} onDelete={this.handleDelete} onMerge={this.handleMerge} onUpdate={this.handleUpdate}/>)}
          <headers_1.default onSelectStatsPeriod={this.handleSelectStatsPeriod} anySelected={anySelected} selection={selection} statsPeriod={statsPeriod} isReprocessingQuery={displayReprocessingActions}/>
        </StyledFlex>
        {!allResultsVisible && pageSelected && (<SelectAllNotice>
            {allInQuerySelected ? (queryCount >= utils_1.BULK_LIMIT ? ((0, locale_1.tct)('Selected up to the first [count] issues that match this search query.', {
                    count: utils_1.BULK_LIMIT_STR,
                })) : ((0, locale_1.tct)('Selected all [count] issues that match this search query.', {
                    count: queryCount,
                }))) : (<React.Fragment>
                {(0, locale_1.tn)('%s issue on this page selected.', '%s issues on this page selected.', numIssues)}
                <SelectAllLink onClick={this.handleApplyToAll}>
                  {queryCount >= utils_1.BULK_LIMIT
                        ? (0, locale_1.tct)('Select the first [count] issues that match this search query.', {
                            count: utils_1.BULK_LIMIT_STR,
                        })
                        : (0, locale_1.tct)('Select all [count] issues that match this search query.', {
                            count: queryCount,
                        })}
                </SelectAllLink>
              </React.Fragment>)}
          </SelectAllNotice>)}
      </Sticky>);
    }
}
exports.IssueListActions = IssueListActions;
const Sticky = (0, styled_1.default)('div') `
  position: sticky;
  z-index: ${p => p.theme.zIndex.issuesList.stickyHeader};
  top: -1px;
`;
const StyledFlex = (0, styled_1.default)('div') `
  display: flex;
  box-sizing: border-box;
  min-height: 45px;
  padding-top: ${(0, space_1.default)(1)};
  padding-bottom: ${(0, space_1.default)(1)};
  align-items: center;
  background: ${p => p.theme.backgroundSecondary};
  border: 1px solid ${p => p.theme.border};
  border-top: none;
  border-radius: ${p => p.theme.borderRadius} ${p => p.theme.borderRadius} 0 0;
  margin: 0 -1px -1px;
`;
const ActionsCheckbox = (0, styled_1.default)('div') `
  padding-left: ${(0, space_1.default)(2)};
  margin-bottom: 1px;
  & input[type='checkbox'] {
    margin: 0;
    display: block;
  }
  ${p => p.isReprocessingQuery && 'flex: 1'};
`;
const SelectAllNotice = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.yellow100};
  border-top: 1px solid ${p => p.theme.yellow300};
  border-bottom: 1px solid ${p => p.theme.yellow300};
  color: ${p => p.theme.black};
  font-size: ${p => p.theme.fontSizeMedium};
  text-align: center;
  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1.5)};
`;
const SelectAllLink = (0, styled_1.default)('a') `
  margin-left: ${(0, space_1.default)(1)};
`;
exports.default = (0, withApi_1.default)(IssueListActions);
//# sourceMappingURL=index.jsx.map