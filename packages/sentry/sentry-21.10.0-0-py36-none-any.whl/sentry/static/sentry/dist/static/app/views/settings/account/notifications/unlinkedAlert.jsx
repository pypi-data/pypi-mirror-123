Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
class UnlinkedAlert extends react_1.default.Component {
    constructor() {
        super(...arguments);
        this.render = () => {
            const { organizations } = this.props;
            return (<StyledAlert type="warning" icon={<icons_1.IconWarning />}>
        {(0, locale_1.t)('You\'ve selected Slack as your delivery method, but do not have a linked account for the following organizations. You\'ll receive email notifications instead until you type "/sentry link" into your Slack workspace to link your account. If slash commands are not working, please re-install the Slack integration.')}
        <ul>
          {organizations.map(organization => (<li key={organization.id}>{organization.slug}</li>))}
        </ul>
      </StyledAlert>);
        };
    }
}
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin: 20px 0px;
`;
exports.default = UnlinkedAlert;
//# sourceMappingURL=unlinkedAlert.jsx.map