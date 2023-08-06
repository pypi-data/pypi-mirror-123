Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupActivity = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const group_1 = require("app/actionCreators/group");
const indicator_1 = require("app/actionCreators/indicator");
const author_1 = (0, tslib_1.__importDefault)(require("app/components/activity/author"));
const item_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item"));
const note_1 = (0, tslib_1.__importDefault)(require("app/components/activity/note"));
const inputWithStorage_1 = (0, tslib_1.__importDefault)(require("app/components/activity/note/inputWithStorage"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const reprocessedBox_1 = (0, tslib_1.__importDefault)(require("app/components/reprocessedBox"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const guid_1 = require("app/utils/guid");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const groupActivityItem_1 = (0, tslib_1.__importDefault)(require("./groupActivityItem"));
const utils_1 = require("./utils");
class GroupActivity extends react_1.Component {
    constructor() {
        super(...arguments);
        // TODO(dcramer): only re-render on group/activity change
        this.state = {
            createBusy: false,
            error: false,
            errorJSON: null,
            inputId: (0, guid_1.uniqueId)(),
        };
        this.handleNoteDelete = ({ modelId, text: oldText }) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, group } = this.props;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Removing comment...'));
            try {
                yield (0, group_1.deleteNote)(api, group, modelId, oldText);
                (0, indicator_1.clearIndicators)();
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to delete comment'));
            }
        });
        /**
         * Note: This is nearly the same logic as `app/views/alerts/details/activity`
         * This can be abstracted a bit if we create more objects that can have activities
         */
        this.handleNoteCreate = (note) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, group } = this.props;
            this.setState({
                createBusy: true,
            });
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Posting comment...'));
            try {
                yield (0, group_1.createNote)(api, group, note);
                this.setState({
                    createBusy: false,
                    // This is used as a `key` to Note Input so that after successful post
                    // we reset the value of the input
                    inputId: (0, guid_1.uniqueId)(),
                });
                (0, indicator_1.clearIndicators)();
            }
            catch (error) {
                this.setState({
                    createBusy: false,
                    error: true,
                    errorJSON: error.responseJSON || constants_1.DEFAULT_ERROR_JSON,
                });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to post comment'));
            }
        });
        this.handleNoteUpdate = (note, { modelId, text: oldText }) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, group } = this.props;
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Updating comment...'));
            try {
                yield (0, group_1.updateNote)(api, group, note, modelId, oldText);
                (0, indicator_1.clearIndicators)();
            }
            catch (error) {
                this.setState({
                    error: true,
                    errorJSON: error.responseJSON || constants_1.DEFAULT_ERROR_JSON,
                });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to update comment'));
            }
        });
    }
    render() {
        const { group, organization } = this.props;
        const { activity: activities, count, id: groupId } = group;
        const groupCount = Number(count);
        const mostRecentActivity = (0, utils_1.getGroupMostRecentActivity)(activities);
        const reprocessingStatus = (0, utils_1.getGroupReprocessingStatus)(group, mostRecentActivity);
        const me = configStore_1.default.get('user');
        const projectSlugs = group && group.project ? [group.project.slug] : [];
        const noteProps = {
            minHeight: 140,
            group,
            projectSlugs,
            placeholder: (0, locale_1.t)('Add details or updates to this event. \nTag users with @, or teams with #'),
        };
        return (<react_1.Fragment>
        {(reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT ||
                reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HAS_EVENT) && (<StyledReprocessedBox reprocessActivity={mostRecentActivity} groupCount={groupCount} orgSlug={organization.slug} groupId={groupId}/>)}
        <div className="row">
          <div className="col-md-9">
            <div>
              <item_1.default author={{ type: 'user', user: me }}>
                {() => (<inputWithStorage_1.default key={this.state.inputId} storageKey="groupinput:latest" itemKey={group.id} onCreate={this.handleNoteCreate} busy={this.state.createBusy} error={this.state.error} errorJSON={this.state.errorJSON} {...noteProps}/>)}
              </item_1.default>

              {group.activity.map(item => {
                var _a;
                const authorName = item.user ? item.user.name : 'Sentry';
                if (item.type === types_1.GroupActivityType.NOTE) {
                    return (<errorBoundary_1.default mini key={`note-${item.id}`}>
                      <note_1.default showTime={false} text={item.data.text} modelId={item.id} user={item.user} dateCreated={item.dateCreated} authorName={authorName} onDelete={this.handleNoteDelete} onUpdate={this.handleNoteUpdate} {...noteProps}/>
                    </errorBoundary_1.default>);
                }
                return (<errorBoundary_1.default mini key={`item-${item.id}`}>
                    <item_1.default author={{
                        type: item.user ? 'user' : 'system',
                        user: (_a = item.user) !== null && _a !== void 0 ? _a : undefined,
                    }} date={item.dateCreated} header={<groupActivityItem_1.default author={<author_1.default>{authorName}</author_1.default>} activity={item} orgSlug={this.props.params.orgId} projectId={group.project.id}/>}/>
                  </errorBoundary_1.default>);
            })}
            </div>
          </div>
        </div>
      </react_1.Fragment>);
    }
}
exports.GroupActivity = GroupActivity;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(GroupActivity));
const StyledReprocessedBox = (0, styled_1.default)(reprocessedBox_1.default) `
  margin: -${(0, space_1.default)(3)} -${(0, space_1.default)(4)} ${(0, space_1.default)(4)} -${(0, space_1.default)(4)};
  z-index: 1;
`;
//# sourceMappingURL=groupActivity.jsx.map