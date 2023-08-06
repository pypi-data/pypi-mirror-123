Object.defineProperty(exports, "__esModule", { value: true });
exports.getAttachmentUrl = void 0;
function getAttachmentUrl(props, withPrefix) {
    const { orgId, projectId, event, attachment } = props;
    return `${withPrefix ? '/api/0' : ''}/projects/${orgId}/${projectId}/events/${event.id}/attachments/${attachment.id}/?download`;
}
exports.getAttachmentUrl = getAttachmentUrl;
//# sourceMappingURL=utils.jsx.map