Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const role_1 = (0, tslib_1.__importDefault)(require("app/components/acl/role"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
function AttachmentUrl({ attachment, organization, eventId, projectId, children }) {
    function getDownloadUrl() {
        return `/api/0/projects/${organization.slug}/${projectId}/events/${eventId}/attachments/${attachment.id}/`;
    }
    return (<role_1.default role={organization.attachmentsRole}>
      {({ hasRole }) => children(hasRole ? getDownloadUrl() : null)}
    </role_1.default>);
}
exports.default = (0, withOrganization_1.default)((0, react_1.memo)(AttachmentUrl));
//# sourceMappingURL=attachmentUrl.jsx.map