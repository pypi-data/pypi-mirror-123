Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const groupEventAttachmentsFilter_1 = require("app/views/organizationGroupDetails/groupEventAttachments/groupEventAttachmentsFilter");
const alert_1 = (0, tslib_1.__importDefault)(require("../alert"));
const link_1 = (0, tslib_1.__importDefault)(require("../links/link"));
const EventAttachmentsCrashReportsNotice = ({ orgSlug, projectSlug, location, groupId, }) => {
    const settingsUrl = `/settings/${orgSlug}/projects/${projectSlug}/security-and-privacy/`;
    const attachmentsUrl = {
        pathname: `/organizations/${orgSlug}/issues/${groupId}/attachments/`,
        query: Object.assign(Object.assign({}, location.query), { types: groupEventAttachmentsFilter_1.crashReportTypes }),
    };
    return (<alert_1.default type="info" icon={<icons_1.IconInfo size="md"/>}>
      {(0, locale_1.tct)('Your limit of stored crash reports has been reached for this issue. [attachmentsLink: View crashes] or [settingsLink: configure limit].', {
            attachmentsLink: <link_1.default to={attachmentsUrl}/>,
            settingsLink: <link_1.default to={settingsUrl}/>,
        })}
    </alert_1.default>);
};
exports.default = EventAttachmentsCrashReportsNotice;
//# sourceMappingURL=eventAttachmentsCrashReportsNotice.jsx.map