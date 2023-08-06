Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const locale_1 = require("app/locale");
const actionButtons_1 = (0, tslib_1.__importDefault)(require("./actionButtons"));
const SentryApplicationRowButtons = ({ organization, app, onClickRemove, onClickPublish, }) => {
    const isInternal = app.status === 'internal';
    return (<access_1.default access={['org:admin']}>
      {({ hasAccess }) => {
            let disablePublishReason = '';
            let disableDeleteReason = '';
            // Publish & Delete buttons will always be disabled if the app is published
            if (app.status === 'published') {
                disablePublishReason = (0, locale_1.t)('Published integrations cannot be re-published.');
                disableDeleteReason = (0, locale_1.t)('Published integrations cannot be removed.');
            }
            else if (!hasAccess) {
                disablePublishReason = (0, locale_1.t)('Organization owner permissions are required for this action.');
                disableDeleteReason = (0, locale_1.t)('Organization owner permissions are required for this action.');
            }
            return (<actionButtons_1.default org={organization} app={app} showPublish={!isInternal} showDelete onPublish={onClickPublish} onDelete={onClickRemove} disablePublishReason={disablePublishReason} disableDeleteReason={disableDeleteReason}/>);
        }}
    </access_1.default>);
};
exports.default = SentryApplicationRowButtons;
//# sourceMappingURL=sentryApplicationRowButtons.jsx.map