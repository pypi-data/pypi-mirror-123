Object.defineProperty(exports, "__esModule", { value: true });
exports.RELEASES_TOUR_STEPS = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const releases_empty_state_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/releases-empty-state.svg"));
const releases_tour_commits_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/releases-tour-commits.svg"));
const releases_tour_email_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/releases-tour-email.svg"));
const releases_tour_resolution_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/releases-tour-resolution.svg"));
const releases_tour_stats_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/releases-tour-stats.svg"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const featureTourModal_1 = (0, tslib_1.__importStar)(require("app/components/modals/featureTourModal"));
const onboardingPanel_1 = (0, tslib_1.__importDefault)(require("app/components/onboardingPanel"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const releasesSetupUrl = 'https://docs.sentry.io/product/releases/';
const docsLink = (<button_1.default external href={releasesSetupUrl}>
    {(0, locale_1.t)('Setup')}
  </button_1.default>);
exports.RELEASES_TOUR_STEPS = [
    {
        title: (0, locale_1.t)('Suspect Commits'),
        image: <featureTourModal_1.TourImage src={releases_tour_commits_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Sentry suggests which commit caused an issue and who is likely responsible so you can triage.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: (0, locale_1.t)('Release Stats'),
        image: <featureTourModal_1.TourImage src={releases_tour_stats_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Get an overview of the commits in each release, and which issues were introduced or fixed.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: (0, locale_1.t)('Easily Resolve'),
        image: <featureTourModal_1.TourImage src={releases_tour_resolution_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Automatically resolve issues by including the issue number in your commit message.')}
      </featureTourModal_1.TourText>),
        actions: docsLink,
    },
    {
        title: (0, locale_1.t)('Deploy Emails'),
        image: <featureTourModal_1.TourImage src={releases_tour_email_svg_1.default}/>,
        body: (<featureTourModal_1.TourText>
        {(0, locale_1.t)('Receive email notifications about when your code gets deployed. This can be customized in settings.')}
      </featureTourModal_1.TourText>),
    },
];
class ReleasePromo extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleTourAdvance = (step, duration) => {
            const { organization, projectId } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'releases.tour.advance',
                eventName: 'Releases: Tour Advance',
                organization_id: parseInt(organization.id, 10),
                project_id: projectId,
                step,
                duration,
            });
        };
        this.handleClose = (step, duration) => {
            const { organization, projectId } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'releases.tour.close',
                eventName: 'Releases: Tour Close',
                organization_id: parseInt(organization.id, 10),
                project_id: projectId,
                step,
                duration,
            });
        };
    }
    componentDidMount() {
        const { organization, projectId } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'releases.landing_card_viewed',
            eventName: 'Releases: Landing Card Viewed',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId,
        });
    }
    render() {
        return (<onboardingPanel_1.default image={<img src={releases_empty_state_svg_1.default}/>}>
        <h3>{(0, locale_1.t)('Demystify Releases')}</h3>
        <p>
          {(0, locale_1.t)('Did you know how many errors your latest release triggered? We do. And more, too.')}
        </p>
        <ButtonList gap={1}>
          <button_1.default priority="primary" href={releasesSetupUrl} external>
            {(0, locale_1.t)('Start Setup')}
          </button_1.default>
          <featureTourModal_1.default steps={exports.RELEASES_TOUR_STEPS} onAdvance={this.handleTourAdvance} onCloseModal={this.handleClose} doneText={(0, locale_1.t)('Start Setup')} doneUrl={releasesSetupUrl}>
            {({ showModal }) => (<button_1.default priority="default" onClick={showModal}>
                {(0, locale_1.t)('Take a Tour')}
              </button_1.default>)}
          </featureTourModal_1.default>
        </ButtonList>
      </onboardingPanel_1.default>);
    }
}
const ButtonList = (0, styled_1.default)(buttonBar_1.default) `
  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));
`;
exports.default = ReleasePromo;
//# sourceMappingURL=releasePromo.jsx.map