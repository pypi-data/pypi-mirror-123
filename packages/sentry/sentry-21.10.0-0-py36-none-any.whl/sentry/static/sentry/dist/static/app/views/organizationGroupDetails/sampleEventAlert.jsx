Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const pageAlertBar_1 = (0, tslib_1.__importDefault)(require("app/components/pageAlertBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
function SampleEventAlert({ selection, organization, projects, }) {
    if (projects.length === 0) {
        return null;
    }
    if (selection.projects.length !== 1) {
        return null;
    }
    const selectedProject = projects.find(p => p.id === selection.projects[0].toString());
    if (!selectedProject || selectedProject.firstEvent) {
        return null;
    }
    return (<pageAlertBar_1.default>
      <icons_1.IconLightning />
      <TextWrapper>
        {(0, locale_1.t)('You are viewing a sample error. Configure Sentry to start viewing real errors.')}
      </TextWrapper>
      <button_1.default size="xsmall" priority="primary" to={`/${organization.slug}/${selectedProject.slug}/getting-started/${selectedProject.platform || ''}`} onClick={() => (0, trackAdvancedAnalyticsEvent_1.default)('growth.sample_error_onboarding_link_clicked', {
            project_id: selectedProject.id,
            organization,
            platform: selectedProject.platform,
        })}>
        {(0, locale_1.t)('Get Started')}
      </button_1.default>
    </pageAlertBar_1.default>);
}
exports.default = (0, withProjects_1.default)((0, withOrganization_1.default)((0, withGlobalSelection_1.default)(SampleEventAlert)));
const TextWrapper = (0, styled_1.default)('span') `
  margin: 0 ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=sampleEventAlert.jsx.map