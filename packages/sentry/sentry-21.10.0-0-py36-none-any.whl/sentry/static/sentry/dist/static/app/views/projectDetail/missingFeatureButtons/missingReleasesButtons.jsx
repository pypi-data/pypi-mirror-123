Object.defineProperty(exports, "__esModule", { value: true });
exports.MissingReleaseButtonBar = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const featureTourModal_1 = (0, tslib_1.__importDefault)(require("app/components/modals/featureTourModal"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const releasePromo_1 = require("app/views/releases/list/releasePromo");
const DOCS_URL = 'https://docs.sentry.io/product/releases/';
const DOCS_HEALTH_URL = 'https://docs.sentry.io/product/releases/health/';
function MissingReleasesButtons({ organization, health, projectId }) {
    function handleTourAdvance(step, duration) {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'project_detail.releases_tour.advance',
            eventName: 'Project Detail: Releases Tour Advance',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId && parseInt(projectId, 10),
            step,
            duration,
        });
    }
    function handleClose(step, duration) {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'project_detail.releases_tour.close',
            eventName: 'Project Detail: Releases Tour Close',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId && parseInt(projectId, 10),
            step,
            duration,
        });
    }
    return (<exports.MissingReleaseButtonBar gap={1}>
      <button_1.default size="small" priority="primary" external href={health ? DOCS_HEALTH_URL : DOCS_URL}>
        {(0, locale_1.t)('Start Setup')}
      </button_1.default>
      {!health && (<featureTourModal_1.default steps={releasePromo_1.RELEASES_TOUR_STEPS} onAdvance={handleTourAdvance} onCloseModal={handleClose} doneText={(0, locale_1.t)('Start Setup')} doneUrl={health ? DOCS_HEALTH_URL : DOCS_URL}>
          {({ showModal }) => (<button_1.default size="small" onClick={showModal}>
              {(0, locale_1.t)('Get a tour')}
            </button_1.default>)}
        </featureTourModal_1.default>)}
    </exports.MissingReleaseButtonBar>);
}
exports.MissingReleaseButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);
`;
exports.default = MissingReleasesButtons;
//# sourceMappingURL=missingReleasesButtons.jsx.map