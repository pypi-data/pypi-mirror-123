Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const analytics_1 = require("app/utils/analytics");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const DEFAULT_POLL_INTERVAL = 5000;
const recordAnalyticsFirstEvent = ({ key, organization, project }) => (0, analytics_1.analytics)(`onboarding_v2.${key}`, {
    org_id: parseInt(organization.id, 10),
    project: parseInt(project.id, 10),
});
/**
 * This is a render prop component that can be used to wait for the first event
 * of a project to be received via polling.
 */
class EventWaiter extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            firstIssue: null,
        };
        this.intervalId = null;
        this.pollHandler = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            const { api, organization, project, eventType, onIssueReceived } = this.props;
            let firstEvent = null;
            let firstIssue = null;
            try {
                const resp = yield api.requestPromise(`/projects/${organization.slug}/${project.slug}/`);
                firstEvent = eventType === 'error' ? resp.firstEvent : resp.firstTransactionEvent;
            }
            catch (resp) {
                if (!resp) {
                    return;
                }
                // This means org or project does not exist, we need to stop polling
                // Also stop polling on auth-related errors (403/401)
                if ([404, 403, 401, 0].includes(resp.status)) {
                    // TODO: Add some UX around this... redirect? error message?
                    this.stopPolling();
                    return;
                }
                Sentry.setExtras({
                    status: resp.status,
                    detail: (_a = resp.responseJSON) === null || _a === void 0 ? void 0 : _a.detail,
                });
                Sentry.captureException(new Error(`Error polling for first ${eventType} event`));
            }
            if (firstEvent === null || firstEvent === false) {
                return;
            }
            if (eventType === 'error') {
                // Locate the projects first issue group. The project.firstEvent field will
                // *not* include sample events, while just looking at the issues list will.
                // We will wait until the project.firstEvent is set and then locate the
                // event given that event datetime
                const issues = yield api.requestPromise(`/projects/${organization.slug}/${project.slug}/issues/`);
                // The event may have expired, default to true
                firstIssue = issues.find((issue) => issue.firstSeen === firstEvent) || true;
                // noinspection SpellCheckingInspection
                recordAnalyticsFirstEvent({
                    key: 'first_event_recieved',
                    organization,
                    project,
                });
            }
            else {
                firstIssue = firstEvent;
                // noinspection SpellCheckingInspection
                recordAnalyticsFirstEvent({
                    key: 'first_transaction_recieved',
                    organization,
                    project,
                });
            }
            if (onIssueReceived) {
                onIssueReceived({ firstIssue });
            }
            this.stopPolling();
            this.setState({ firstIssue });
        });
    }
    componentDidMount() {
        this.pollHandler();
        this.startPolling();
    }
    componentDidUpdate() {
        this.stopPolling();
        this.startPolling();
    }
    componentWillUnmount() {
        this.stopPolling();
    }
    startPolling() {
        const { disabled, organization, project } = this.props;
        if (disabled || !organization || !project || this.state.firstIssue) {
            return;
        }
        this.intervalId = window.setInterval(this.pollHandler, this.props.pollInterval || DEFAULT_POLL_INTERVAL);
    }
    stopPolling() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    }
    render() {
        return this.props.children({ firstIssue: this.state.firstIssue });
    }
}
exports.default = (0, withApi_1.default)(EventWaiter);
//# sourceMappingURL=eventWaiter.jsx.map