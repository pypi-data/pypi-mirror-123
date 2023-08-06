Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const modal_1 = require("app/actionCreators/modal");
const locale_1 = require("app/locale");
const sentryAppExternalForm_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/sentryAppExternalForm"));
const SentryAppRuleModal = ({ Header, Body, sentryAppInstallationUuid, appName, config, resetValues, onSubmitSuccess, }) => (<react_1.Fragment>
    <Header closeButton>{(0, locale_1.tct)('[name] Settings', { name: appName })}</Header>
    <Body>
      <sentryAppExternalForm_1.default sentryAppInstallationUuid={sentryAppInstallationUuid} appName={appName} config={config} element="alert-rule-action" action="create" onSubmitSuccess={(...params) => {
        onSubmitSuccess(...params);
        (0, modal_1.closeModal)();
    }} resetValues={{ settings: resetValues === null || resetValues === void 0 ? void 0 : resetValues.settings }}/>
    </Body>
  </react_1.Fragment>);
exports.default = SentryAppRuleModal;
//# sourceMappingURL=sentryAppRuleModal.jsx.map