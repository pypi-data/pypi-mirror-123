Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const pageAlertBar_1 = (0, tslib_1.__importDefault)(require("app/components/pageAlertBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
function FinishSetupAlert({ organization, project, }) {
    return (<pageAlertBar_1.default>
      <icons_1.IconLightning />
      <TextWrapper>
        {(0, locale_1.t)('You are viewing a sample transaction. Configure performance to start viewing real transactions.')}
      </TextWrapper>
      <button_1.default size="xsmall" priority="primary" target="_blank" external href="https://docs.sentry.io/performance-monitoring/getting-started/" onClick={() => (0, trackAdvancedAnalyticsEvent_1.default)('growth.sample_transaction_docs_link_clicked', {
            project_id: project.id,
            organization,
        })}>
        {(0, locale_1.t)('Get Started')}
      </button_1.default>
    </pageAlertBar_1.default>);
}
exports.default = FinishSetupAlert;
const TextWrapper = (0, styled_1.default)('span') `
  margin: 0 ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=finishSetupAlert.jsx.map