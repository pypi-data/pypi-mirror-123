Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const featureTourModal_1 = (0, tslib_1.__importDefault)(require("app/components/modals/featureTourModal"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const onboarding_1 = require("app/views/performance/onboarding");
const DOCS_URL = 'https://docs.sentry.io/performance-monitoring/getting-started/';
function MissingPerformanceButtons({ organization }) {
    function handleTourAdvance(step, duration) {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'project_detail.performance_tour.advance',
            eventName: 'Project Detail: Performance Tour Advance',
            organization_id: parseInt(organization.id, 10),
            step,
            duration,
        });
    }
    function handleClose(step, duration) {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'project_detail.performance_tour.close',
            eventName: 'Project Detail: Performance Tour Close',
            organization_id: parseInt(organization.id, 10),
            step,
            duration,
        });
    }
    return (<feature_1.default hookName="feature-disabled:project-performance-score-card" features={['performance-view']} organization={organization}>
      <StyledButtonBar gap={1}>
        <button_1.default size="small" priority="primary" external href={DOCS_URL}>
          {(0, locale_1.t)('Start Setup')}
        </button_1.default>

        <featureTourModal_1.default steps={onboarding_1.PERFORMANCE_TOUR_STEPS} onAdvance={handleTourAdvance} onCloseModal={handleClose} doneText={(0, locale_1.t)('Start Setup')} doneUrl={DOCS_URL}>
          {({ showModal }) => (<button_1.default size="small" onClick={showModal}>
              {(0, locale_1.t)('Get a tour')}
            </button_1.default>)}
        </featureTourModal_1.default>
      </StyledButtonBar>
    </feature_1.default>);
}
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);
`;
exports.default = MissingPerformanceButtons;
//# sourceMappingURL=missingPerformanceButtons.jsx.map