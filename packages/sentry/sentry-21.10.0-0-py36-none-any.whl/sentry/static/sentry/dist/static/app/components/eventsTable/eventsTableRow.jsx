Object.defineProperty(exports, "__esModule", { value: true });
exports.EventsTableRow = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const deviceName_1 = (0, tslib_1.__importDefault)(require("app/components/deviceName"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const attachmentUrl_1 = (0, tslib_1.__importDefault)(require("app/utils/attachmentUrl"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class EventsTableRow extends React.Component {
    renderCrashFileLink() {
        const { event, projectId } = this.props;
        if (!event.crashFile) {
            return null;
        }
        const crashFileType = event.crashFile.type === 'event.minidump' ? 'Minidump' : 'Crash file';
        return (<attachmentUrl_1.default projectId={projectId} eventId={event.id} attachment={event.crashFile}>
        {url => {
                var _a, _b;
                return url && (<small>
              {crashFileType}: <a href={`${url}?download=1`}>{(_a = event.crashFile) === null || _a === void 0 ? void 0 : _a.name}</a> (
              <fileSize_1.default bytes={((_b = event.crashFile) === null || _b === void 0 ? void 0 : _b.size) || 0}/>)
            </small>);
            }}
      </attachmentUrl_1.default>);
    }
    render() {
        const { className, event, orgId, groupId, tagList, hasUser } = this.props;
        const tagMap = {};
        event.tags.forEach(tag => {
            tagMap[tag.key] = tag.value;
        });
        const link = `/organizations/${orgId}/issues/${groupId}/events/${event.id}/`;
        return (<tr key={event.id} className={className}>
        <td>
          <h5>
            <globalSelectionLink_1.default to={link}>
              <dateTime_1.default date={event.dateCreated}/>
            </globalSelectionLink_1.default>
            <small>{event.title.substr(0, 100)}</small>
            {this.renderCrashFileLink()}
          </h5>
        </td>

        {hasUser && (<td className="event-user table-user-info">
            {event.user ? (<div>
                <userAvatar_1.default user={event.user} // TODO(ts): Some of the user fields are optional from event, this cast can probably be removed in the future
                 size={24} className="avatar" gravatar={false}/>
                {event.user.email}
              </div>) : (<span>—</span>)}
          </td>)}

        {tagList.map(tag => (<td key={tag.key}>
            <div>
              {tag.key === 'device' ? (<deviceName_1.default value={tagMap[tag.key]}/>) : (tagMap[tag.key])}
            </div>
          </td>))}
      </tr>);
    }
}
exports.EventsTableRow = EventsTableRow;
exports.default = (0, withOrganization_1.default)(EventsTableRow);
//# sourceMappingURL=eventsTableRow.jsx.map