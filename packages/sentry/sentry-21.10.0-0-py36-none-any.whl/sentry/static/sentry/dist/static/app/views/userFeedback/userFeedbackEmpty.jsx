Object.defineProperty(exports, "__esModule", { value: true });
exports.UserFeedbackEmpty = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const feedback_empty_state_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/feedback-empty-state.svg"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const onboardingPanel_1 = (0, tslib_1.__importDefault)(require("app/components/onboardingPanel"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
class UserFeedbackEmpty extends react_1.Component {
    componentDidMount() {
        const { organization, projectIds } = this.props;
        window.sentryEmbedCallback = function (embed) {
            // Mock the embed's submit xhr to always be successful
            // NOTE: this will not have errors if the form is empty
            embed.submit = function (_body) {
                this._submitInProgress = true;
                setTimeout(() => {
                    this._submitInProgress = false;
                    this.onSuccess();
                }, 500);
            };
        };
        if (this.hasAnyFeedback === false) {
            // send to reload only due to higher event volume
            (0, analytics_1.trackAdhocEvent)({
                eventKey: 'user_feedback.viewed',
                org_id: parseInt(organization.id, 10),
                projects: projectIds,
            });
        }
    }
    componentWillUnmount() {
        window.sentryEmbedCallback = null;
    }
    get selectedProjects() {
        const { projects, projectIds } = this.props;
        return projectIds && projectIds.length
            ? projects.filter(({ id }) => projectIds.includes(id))
            : projects;
    }
    get hasAnyFeedback() {
        return this.selectedProjects.some(({ hasUserReports }) => hasUserReports);
    }
    trackAnalytics({ eventKey, eventName }) {
        const { organization, projectIds } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey,
            eventName,
            organization_id: organization.id,
            projects: projectIds,
        });
    }
    render() {
        // Show no user reports if waiting for projects to load or if there is no feedback
        if (this.props.loadingProjects || this.hasAnyFeedback !== false) {
            return (<emptyStateWarning_1.default>
          <p>{(0, locale_1.t)('Sorry, no user reports match your filters.')}</p>
        </emptyStateWarning_1.default>);
        }
        // Show landing page after projects have loaded and it is confirmed no projects have feedback
        return (<onboardingPanel_1.default image={<img src={feedback_empty_state_svg_1.default}/>}>
        <h3>{(0, locale_1.t)('What do users think?')}</h3>
        <p>
          {(0, locale_1.t)(`You can't read minds. At least we hope not. Ask users for feedback on the impact of their crashes or bugs and you shall receive.`)}
        </p>
        <ButtonList gap={1}>
          <button_1.default external priority="primary" onClick={() => this.trackAnalytics({
                eventKey: 'user_feedback.docs_clicked',
                eventName: 'User Feedback Docs Clicked',
            })} href="https://docs.sentry.io/product/user-feedback/">
            {(0, locale_1.t)('Read the docs')}
          </button_1.default>
          <button_1.default onClick={() => {
                Sentry.showReportDialog({
                    // should never make it to the Sentry API, but just in case, use throwaway id
                    eventId: '00000000000000000000000000000000',
                });
                this.trackAnalytics({
                    eventKey: 'user_feedback.dialog_opened',
                    eventName: 'User Feedback Dialog Opened',
                });
            }}>
            {(0, locale_1.t)('See an example')}
          </button_1.default>
        </ButtonList>
      </onboardingPanel_1.default>);
    }
}
exports.UserFeedbackEmpty = UserFeedbackEmpty;
const ButtonList = (0, styled_1.default)(buttonBar_1.default) `
  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));
`;
exports.default = (0, withOrganization_1.default)((0, withProjects_1.default)(UserFeedbackEmpty));
//# sourceMappingURL=userFeedbackEmpty.jsx.map