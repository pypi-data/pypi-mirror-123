Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const FeedbackAlert = ({ className }) => (<StyledAlert type="info" icon={<icons_1.IconInfo />} className={className}>
    {(0, locale_1.tct)('Got feedback? Email [email:ecosystem-feedback@sentry.io].', {
        email: <a href="mailto:ecosystem-feedback@sentry.io"/>,
    })}
  </StyledAlert>);
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin: 20px 0px;
`;
exports.default = FeedbackAlert;
//# sourceMappingURL=feedbackAlert.jsx.map