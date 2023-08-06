Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const groupEventAttachmentsTableRow_1 = (0, tslib_1.__importDefault)(require("app/views/organizationGroupDetails/groupEventAttachments/groupEventAttachmentsTableRow"));
const GroupEventAttachmentsTable = ({ attachments, orgId, projectId, groupId, onDelete, deletedAttachments, }) => {
    const tableRowNames = [(0, locale_1.t)('Name'), (0, locale_1.t)('Type'), (0, locale_1.t)('Size'), (0, locale_1.t)('Actions')];
    return (<table className="table events-table">
      <thead>
        <tr>
          {tableRowNames.map(name => (<th key={name}>{name}</th>))}
        </tr>
      </thead>
      <tbody>
        {attachments.map(attachment => (<groupEventAttachmentsTableRow_1.default key={attachment.id} attachment={attachment} orgId={orgId} projectId={projectId} groupId={groupId} onDelete={onDelete} isDeleted={deletedAttachments.some(id => attachment.id === id)}/>))}
      </tbody>
    </table>);
};
exports.default = GroupEventAttachmentsTable;
//# sourceMappingURL=groupEventAttachmentsTable.jsx.map