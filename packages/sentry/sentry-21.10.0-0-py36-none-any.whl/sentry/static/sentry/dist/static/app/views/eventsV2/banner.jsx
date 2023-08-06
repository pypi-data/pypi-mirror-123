Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const discover_tour_alert_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/discover-tour-alert.svg"));
const discover_tour_explore_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/discover-tour-explore.svg"));
const discover_tour_filter_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/discover-tour-filter.svg"));
const discover_tour_group_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/discover-tour-group.svg"));
const banner_1 = (0, tslib_1.__importDefault)(require("app/components/banner"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const featureTourModal_1 = (0, tslib_1.__importStar)(require("app/components/modals/featureTourModal"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const useMedia_1 = (0, tslib_1.__importDefault)(require("app/utils/useMedia"));
const backgroundSpace_1 = (0, tslib_1.__importDefault)(require("./backgroundSpace"));
const docsUrl = 'https://docs.sentry.io/product/discover-queries/';
const docsLink = (<button_1.default external href={docsUrl}>
    {(0, locale_1.t)('View Docs')}
  </button_1.default>);
const TOUR_STEPS = [
    {
        title: (0, locale_1.t)('Explore Data over Time'),
        image: <featureTourModal_1.TourImage src={discover_tour_explore_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Analyze and visualize all of your data over time to find answers to your most complex problems.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: (0, locale_1.t)('Filter on Event Attributes.'),
        image: <featureTourModal_1.TourImage src={discover_tour_filter_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Drill down on data by any custom tag or field to reduce noise and hone in on specific areas.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: (0, locale_1.t)('Group Data by Tags'),
        image: <featureTourModal_1.TourImage src={discover_tour_group_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Go beyond Issues and create custom groupings to investigate events from a different lens.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: (0, locale_1.t)('Save, Share and Alert'),
        image: <featureTourModal_1.TourImage src={discover_tour_alert_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Send insights to your team and set alerts to monitor any future spikes.')}
      </featureTourModal_1.TourText>),
    },
];
function DiscoverBanner({ organization, resultsUrl }) {
    function onAdvance(step, duration) {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'discover_v2.tour.advance',
            eventName: 'Discoverv2: Tour Advance',
            organization_id: parseInt(organization.id, 10),
            step,
            duration,
        });
    }
    function onCloseModal(step, duration) {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'discover_v2.tour.close',
            eventName: 'Discoverv2: Tour Close',
            organization_id: parseInt(organization.id, 10),
            step,
            duration,
        });
    }
    const isSmallBanner = (0, useMedia_1.default)(`(max-width: ${theme_1.default.breakpoints[1]})`);
    return (<banner_1.default title={(0, locale_1.t)('Discover Trends')} subtitle={(0, locale_1.t)('Customize and save queries by search conditions, event fields, and tags')} backgroundComponent={<backgroundSpace_1.default />} dismissKey="discover">
      <button_1.default size={isSmallBanner ? 'xsmall' : undefined} to={resultsUrl} onClick={() => {
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.build_new_query',
                eventName: 'Discoverv2: Build a new Discover Query',
                organization_id: parseInt(organization.id, 10),
            });
        }}>
        {(0, locale_1.t)('Build a new query')}
      </button_1.default>
      <featureTourModal_1.default steps={TOUR_STEPS} doneText={(0, locale_1.t)('View all Events')} doneUrl={resultsUrl} onAdvance={onAdvance} onCloseModal={onCloseModal}>
        {({ showModal }) => (<button_1.default size={isSmallBanner ? 'xsmall' : undefined} onClick={() => {
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'discover_v2.tour.start',
                    eventName: 'Discoverv2: Tour Start',
                    organization_id: parseInt(organization.id, 10),
                });
                showModal();
            }}>
            {(0, locale_1.t)('Get a Tour')}
          </button_1.default>)}
      </featureTourModal_1.default>
    </banner_1.default>);
}
exports.default = DiscoverBanner;
//# sourceMappingURL=banner.jsx.map