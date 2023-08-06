Object.defineProperty(exports, "__esModule", { value: true });
exports.PERFORMANCE_TOUR_STEPS = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const performance_empty_state_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/performance-empty-state.svg"));
const performance_tour_alert_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/performance-tour-alert.svg"));
const performance_tour_correlate_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/performance-tour-correlate.svg"));
const performance_tour_metrics_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/performance-tour-metrics.svg"));
const performance_tour_trace_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/performance-tour-trace.svg"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const featureTourModal_1 = (0, tslib_1.__importStar)(require("app/components/modals/featureTourModal"));
const onboardingPanel_1 = (0, tslib_1.__importDefault)(require("app/components/onboardingPanel"));
const locale_1 = require("app/locale");
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const performanceSetupUrl = 'https://docs.sentry.io/performance-monitoring/getting-started/';
const docsLink = (<button_1.default external href={performanceSetupUrl}>
    {(0, locale_1.t)('Setup')}
  </button_1.default>);
exports.PERFORMANCE_TOUR_STEPS = [
    {
        title: (0, locale_1.t)('Track Application Metrics'),
        image: <featureTourModal_1.TourImage src={performance_tour_metrics_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Monitor your slowest pageloads and APIs to see which users are having the worst time.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: (0, locale_1.t)('Correlate Errors and Performance'),
        image: <featureTourModal_1.TourImage src={performance_tour_correlate_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('See what errors occurred within a transaction and the impact of those errors.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: (0, locale_1.t)('Watch and Alert'),
        image: <featureTourModal_1.TourImage src={performance_tour_alert_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Highlight mission-critical pages and APIs and set latency alerts to notify you before things go wrong.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: (0, locale_1.t)('Trace Across Systems'),
        image: <featureTourModal_1.TourImage src={performance_tour_trace_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)("Follow a trace from a user's session and drill down to identify any bottlenecks that occur.")}
      </featureTourModal_1.TourText>),
    },
];
function Onboarding({ organization, project }) {
    const api = (0, useApi_1.default)();
    function handleAdvance(step, duration) {
        (0, trackAdvancedAnalyticsEvent_1.default)('performance_views.tour.advance', {
            step,
            duration,
            organization,
        });
    }
    function handleClose(step, duration) {
        (0, trackAdvancedAnalyticsEvent_1.default)('performance_views.tour.close', {
            step,
            duration,
            organization,
        });
    }
    return (<onboardingPanel_1.default image={<PerfImage src={performance_empty_state_svg_1.default}/>}>
      <h3>{(0, locale_1.t)('Pinpoint problems')}</h3>
      <p>
        {(0, locale_1.t)('Something seem slow? Track down transactions to connect the dots between 10-second page loads and poor-performing API calls or slow database queries.')}
      </p>
      <ButtonList gap={1}>
        <button_1.default priority="primary" target="_blank" href="https://docs.sentry.io/performance-monitoring/getting-started/">
          {(0, locale_1.t)('Start Setup')}
        </button_1.default>
        <button_1.default data-test-id="create-sample-transaction-btn" onClick={() => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            (0, trackAdvancedAnalyticsEvent_1.default)('performance_views.create_sample_transaction', {
                platform: project.platform,
                organization,
            });
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Processing sample event...'), {
                duration: 15000,
            });
            const url = `/projects/${organization.slug}/${project.slug}/create-sample-transaction/`;
            try {
                const eventData = yield api.requestPromise(url, { method: 'POST' });
                react_router_1.browserHistory.push(`/organizations/${organization.slug}/performance/${project.slug}:${eventData.eventID}/`);
                (0, indicator_1.clearIndicators)();
            }
            catch (error) {
                Sentry.withScope(scope => {
                    scope.setExtra('error', error);
                    Sentry.captureException(new Error('Failed to create sample event'));
                });
                (0, indicator_1.clearIndicators)();
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to create a new sample event'));
                return;
            }
        })}>
          {(0, locale_1.t)('View Sample Transaction')}
        </button_1.default>
      </ButtonList>
      <featureTourModal_1.default steps={exports.PERFORMANCE_TOUR_STEPS} onAdvance={handleAdvance} onCloseModal={handleClose} doneUrl={performanceSetupUrl} doneText={(0, locale_1.t)('Start Setup')}>
        {({ showModal }) => (<button_1.default priority="link" onClick={() => {
                (0, trackAdvancedAnalyticsEvent_1.default)('performance_views.tour.start', { organization });
                showModal();
            }}>
            {(0, locale_1.t)('Take a Tour')}
          </button_1.default>)}
      </featureTourModal_1.default>
    </onboardingPanel_1.default>);
}
const PerfImage = (0, styled_1.default)('img') `
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    max-width: unset;
    user-select: none;
    position: absolute;
    top: 75px;
    bottom: 0;
    width: 450px;
    margin-top: auto;
    margin-bottom: auto;
  }

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    width: 480px;
  }

  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    width: 600px;
  }
`;
const ButtonList = (0, styled_1.default)(buttonBar_1.default) `
  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));
  margin-bottom: 16px;
`;
exports.default = Onboarding;
//# sourceMappingURL=onboarding.jsx.map