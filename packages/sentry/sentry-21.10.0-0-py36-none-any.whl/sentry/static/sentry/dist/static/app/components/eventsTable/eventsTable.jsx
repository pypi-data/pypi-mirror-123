Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const eventsTableRow_1 = (0, tslib_1.__importDefault)(require("app/components/eventsTable/eventsTableRow"));
const locale_1 = require("app/locale");
class EventsTable extends react_1.Component {
    render() {
        const { events, tagList, orgId, projectId, groupId } = this.props;
        const hasUser = !!events.find(event => event.user);
        return (<table className="table events-table">
        <thead>
          <tr>
            <th>{(0, locale_1.t)('ID')}</th>
            {hasUser && <th>{(0, locale_1.t)('User')}</th>}

            {tagList.map(tag => (<th key={tag.key}>{tag.name}</th>))}
          </tr>
        </thead>
        <tbody>
          {events.map(event => (<eventsTableRow_1.default key={event.id} event={event} orgId={orgId} projectId={projectId} groupId={groupId} tagList={tagList} hasUser={hasUser}/>))}
        </tbody>
      </table>);
    }
}
exports.default = EventsTable;
//# sourceMappingURL=eventsTable.jsx.map