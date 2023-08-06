Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const imageViewer_1 = (0, tslib_1.__importDefault)(require("app/components/events/attachmentViewers/imageViewer"));
const jsonViewer_1 = (0, tslib_1.__importDefault)(require("app/components/events/attachmentViewers/jsonViewer"));
const logFileViewer_1 = (0, tslib_1.__importDefault)(require("app/components/events/attachmentViewers/logFileViewer"));
const rrwebJsonViewer_1 = (0, tslib_1.__importDefault)(require("app/components/events/attachmentViewers/rrwebJsonViewer"));
const eventAttachmentActions_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventAttachmentActions"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const attachmentUrl_1 = (0, tslib_1.__importDefault)(require("app/utils/attachmentUrl"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const eventAttachmentsCrashReportsNotice_1 = (0, tslib_1.__importDefault)(require("./eventAttachmentsCrashReportsNotice"));
class EventAttachments extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            expanded: false,
            attachmentPreviews: {},
        };
        this.attachmentPreviewIsOpen = (attachment) => {
            return !!this.state.attachmentPreviews[attachment.id];
        };
    }
    getInlineAttachmentRenderer(attachment) {
        switch (attachment.mimetype) {
            case 'text/plain':
                return attachment.size > 0 ? logFileViewer_1.default : undefined;
            case 'text/json':
            case 'text/x-json':
            case 'application/json':
                if (attachment.name === 'rrweb.json') {
                    return rrwebJsonViewer_1.default;
                }
                return jsonViewer_1.default;
            case 'image/jpeg':
            case 'image/png':
            case 'image/gif':
                return imageViewer_1.default;
            default:
                return undefined;
        }
    }
    hasInlineAttachmentRenderer(attachment) {
        return !!this.getInlineAttachmentRenderer(attachment);
    }
    renderInlineAttachment(attachment) {
        const Component = this.getInlineAttachmentRenderer(attachment);
        if (!Component || !this.attachmentPreviewIsOpen(attachment)) {
            return null;
        }
        return (<AttachmentPreviewWrapper>
        <Component orgId={this.props.orgId} projectId={this.props.projectId} event={this.props.event} attachment={attachment}/>
      </AttachmentPreviewWrapper>);
    }
    togglePreview(attachment) {
        this.setState(({ attachmentPreviews }) => ({
            attachmentPreviews: Object.assign(Object.assign({}, attachmentPreviews), { [attachment.id]: !attachmentPreviews[attachment.id] }),
        }));
    }
    render() {
        const { event, projectId, orgId, location, attachments, onDeleteAttachment } = this.props;
        const crashFileStripped = event.metadata.stripped_crash;
        if (!attachments.length && !crashFileStripped) {
            return null;
        }
        const title = (0, locale_1.t)('Attachments (%s)', attachments.length);
        const lastAttachmentPreviewed = attachments.length > 0 &&
            this.attachmentPreviewIsOpen(attachments[attachments.length - 1]);
        return (<eventDataSection_1.default type="attachments" title={title}>
        {crashFileStripped && (<eventAttachmentsCrashReportsNotice_1.default orgSlug={orgId} projectSlug={projectId} groupId={event.groupID} location={location}/>)}

        {attachments.length > 0 && (<StyledPanelTable headers={[
                    <Name key="name">{(0, locale_1.t)('File Name')}</Name>,
                    <Size key="size">{(0, locale_1.t)('Size')}</Size>,
                    (0, locale_1.t)('Actions'),
                ]}>
            {attachments.map(attachment => (<React.Fragment key={attachment.id}>
                <Name>{attachment.name}</Name>
                <Size>
                  <fileSize_1.default bytes={attachment.size}/>
                </Size>
                <attachmentUrl_1.default projectId={projectId} eventId={event.id} attachment={attachment}>
                  {url => (<div>
                      <eventAttachmentActions_1.default url={url} onDelete={onDeleteAttachment} onPreview={_attachmentId => this.togglePreview(attachment)} withPreviewButton previewIsOpen={this.attachmentPreviewIsOpen(attachment)} hasPreview={this.hasInlineAttachmentRenderer(attachment)} attachmentId={attachment.id}/>
                    </div>)}
                </attachmentUrl_1.default>
                {this.renderInlineAttachment(attachment)}
                {/* XXX: hack to deal with table grid borders */}
                {lastAttachmentPreviewed && (<React.Fragment>
                    <div style={{ display: 'none' }}/>
                    <div style={{ display: 'none' }}/>
                  </React.Fragment>)}
              </React.Fragment>))}
          </StyledPanelTable>)}
      </eventDataSection_1.default>);
    }
}
exports.default = (0, withApi_1.default)(EventAttachments);
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  grid-template-columns: 1fr auto auto;
`;
const Name = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
`;
const Size = (0, styled_1.default)('div') `
  text-align: right;
`;
const AttachmentPreviewWrapper = (0, styled_1.default)('div') `
  grid-column: auto / span 3;
  border: none;
  padding: 0;
`;
//# sourceMappingURL=eventAttachments.jsx.map