Object.defineProperty(exports, "__esModule", { value: true });
exports.EmailVerificationModal = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const accountEmails_1 = require("app/views/settings/account/accountEmails");
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
function EmailVerificationModal({ Header, Body, actionMessage = 'taking this action', }) {
    return (<React.Fragment>
      <Header closeButton>{(0, locale_1.t)('Action Required')}</Header>
      <Body>
        <textBlock_1.default>
          {(0, locale_1.tct)('Please verify your email before [actionMessage], or [link].', {
            actionMessage,
            link: (<link_1.default to="/settings/account/emails/" data-test-id="email-settings-link">
                {(0, locale_1.t)('go to your email settings')}
              </link_1.default>),
        })}
        </textBlock_1.default>
        <accountEmails_1.EmailAddresses />
      </Body>
    </React.Fragment>);
}
exports.EmailVerificationModal = EmailVerificationModal;
exports.default = (0, react_router_1.withRouter)((0, withApi_1.default)(EmailVerificationModal));
//# sourceMappingURL=emailVerificationModal.jsx.map