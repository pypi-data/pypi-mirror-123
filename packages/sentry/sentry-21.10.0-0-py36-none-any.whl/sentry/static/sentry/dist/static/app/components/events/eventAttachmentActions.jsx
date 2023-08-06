Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class EventAttachmentActions extends react_1.Component {
    handlePreview() {
        const { onPreview, attachmentId } = this.props;
        if (onPreview) {
            onPreview(attachmentId);
        }
    }
    render() {
        const { url, withPreviewButton, hasPreview, previewIsOpen, onDelete, attachmentId } = this.props;
        return (<buttonBar_1.default gap={1}>
        <confirm_1.default confirmText={(0, locale_1.t)('Delete')} message={(0, locale_1.t)('Are you sure you wish to delete this file?')} priority="danger" onConfirm={() => onDelete(attachmentId)} disabled={!url}>
          <button_1.default size="xsmall" icon={<icons_1.IconDelete size="xs"/>} label={(0, locale_1.t)('Delete')} disabled={!url} title={!url ? (0, locale_1.t)('Insufficient permissions to delete attachments') : undefined}/>
        </confirm_1.default>

        <DownloadButton size="xsmall" icon={<icons_1.IconDownload size="xs"/>} href={url ? `${url}?download=1` : ''} disabled={!url} title={!url ? (0, locale_1.t)('Insufficient permissions to download attachments') : undefined} label={(0, locale_1.t)('Download')}/>

        {withPreviewButton && (<DownloadButton size="xsmall" disabled={!url || !hasPreview} priority={previewIsOpen ? 'primary' : 'default'} icon={<icons_1.IconShow size="xs"/>} onClick={() => this.handlePreview()} title={!url
                    ? (0, locale_1.t)('Insufficient permissions to preview attachments')
                    : !hasPreview
                        ? (0, locale_1.t)('This attachment cannot be previewed')
                        : undefined}>
            {(0, locale_1.t)('Preview')}
          </DownloadButton>)}
      </buttonBar_1.default>);
    }
}
const DownloadButton = (0, styled_1.default)(button_1.default) `
  margin-right: ${(0, space_1.default)(0.5)};
`;
exports.default = (0, withApi_1.default)(EventAttachmentActions);
//# sourceMappingURL=eventAttachmentActions.jsx.map