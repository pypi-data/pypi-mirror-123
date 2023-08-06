Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getPendingInvite_1 = (0, tslib_1.__importDefault)(require("app/utils/getPendingInvite"));
const TwoFactorRequired = () => !(0, getPendingInvite_1.default)() ? null : (<StyledAlert data-test-id="require-2fa" type="error" icon={<icons_1.IconFlag size="md"/>}>
      {(0, locale_1.tct)('You have been invited to an organization that requires [link:two-factor authentication].' +
        ' Setup two-factor authentication below to join your organization.', {
        link: <externalLink_1.default href="https://docs.sentry.io/accounts/require-2fa/"/>,
    })}
    </StyledAlert>);
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin: ${(0, space_1.default)(3)} 0;
`;
exports.default = TwoFactorRequired;
//# sourceMappingURL=twoFactorRequired.jsx.map