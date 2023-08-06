Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const eventAttachmentActions_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventAttachmentActions"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const attachmentUrl_1 = (0, tslib_1.__importDefault)(require("app/utils/attachmentUrl"));
const types_1 = require("app/views/organizationGroupDetails/groupEventAttachments/types");
const GroupEventAttachmentsTableRow = ({ attachment, projectId, onDelete, isDeleted, orgId, groupId, }) => (<TableRow isDeleted={isDeleted}>
    <td>
      <h5>
        {attachment.name}
        <br />
        <small>
          <dateTime_1.default date={attachment.dateCreated}/> &middot;{' '}
          <link_1.default to={`/organizations/${orgId}/issues/${groupId}/events/${attachment.event_id}/`}>
            {attachment.event_id}
          </link_1.default>
        </small>
      </h5>
    </td>

    <td>{types_1.types[attachment.type] || (0, locale_1.t)('Other')}</td>

    <td>
      <fileSize_1.default bytes={attachment.size}/>
    </td>

    <td>
      <ActionsWrapper>
        <attachmentUrl_1.default projectId={projectId} eventId={attachment.event_id} attachment={attachment}>
          {url => !isDeleted && (<eventAttachmentActions_1.default url={url} onDelete={onDelete} attachmentId={attachment.id}/>)}
        </attachmentUrl_1.default>
      </ActionsWrapper>
    </td>
  </TableRow>);
const TableRow = (0, styled_1.default)('tr') `
  opacity: ${p => (p.isDeleted ? 0.3 : 1)};
  td {
    text-decoration: ${p => (p.isDeleted ? 'line-through' : 'normal')};
  }
`;
const ActionsWrapper = (0, styled_1.default)('div') `
  display: inline-block;
`;
exports.default = GroupEventAttachmentsTableRow;
//# sourceMappingURL=groupEventAttachmentsTableRow.jsx.map