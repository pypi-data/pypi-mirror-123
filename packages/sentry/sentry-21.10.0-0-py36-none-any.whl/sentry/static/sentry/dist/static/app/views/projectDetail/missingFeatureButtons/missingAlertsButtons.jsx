Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const createAlertButton_1 = (0, tslib_1.__importDefault)(require("app/components/createAlertButton"));
const locale_1 = require("app/locale");
const DOCS_URL = 'https://docs.sentry.io/product/alerts-notifications/metric-alerts/';
function MissingAlertsButtons({ organization, projectSlug }) {
    return (<StyledButtonBar gap={1}>
      <createAlertButton_1.default organization={organization} iconProps={{ size: 'xs' }} size="small" priority="primary" referrer="project_detail" projectSlug={projectSlug} hideIcon>
        {(0, locale_1.t)('Create Alert')}
      </createAlertButton_1.default>
      <button_1.default size="small" external href={DOCS_URL}>
        {(0, locale_1.t)('Learn More')}
      </button_1.default>
    </StyledButtonBar>);
}
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);
`;
exports.default = MissingAlertsButtons;
//# sourceMappingURL=missingAlertsButtons.jsx.map