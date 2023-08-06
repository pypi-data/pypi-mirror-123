Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const EVENT_POLL_RETRIES = 15;
const EVENT_POLL_INTERVAL = 1000;
function latestEventAvailable(api, groupID) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        let retries = 0;
        // eslint-disable-next-line no-constant-condition
        while (true) {
            if (retries > EVENT_POLL_RETRIES) {
                return { eventCreated: false, retries: retries - 1 };
            }
            yield new Promise(resolve => setTimeout(resolve, EVENT_POLL_INTERVAL));
            try {
                yield api.requestPromise(`/issues/${groupID}/events/latest/`);
                return { eventCreated: true, retries };
            }
            catch (_a) {
                ++retries;
            }
        }
    });
}
class CreateSampleEventButton extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            creating: false,
        };
        this.createSampleGroup = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // TODO(dena): swap out for action creator
            const { api, organization, project } = this.props;
            let eventData;
            if (!project) {
                return;
            }
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.onboarding_view_sample_event', {
                platform: project.platform,
                organization,
            });
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Processing sample event...'), {
                duration: EVENT_POLL_RETRIES * EVENT_POLL_INTERVAL,
            });
            this.setState({ creating: true });
            try {
                const url = `/projects/${organization.slug}/${project.slug}/create-sample/`;
                eventData = yield api.requestPromise(url, { method: 'POST' });
            }
            catch (error) {
                Sentry.withScope(scope => {
                    scope.setExtra('error', error);
                    Sentry.captureException(new Error('Failed to create sample event'));
                });
                this.setState({ creating: false });
                (0, indicator_1.clearIndicators)();
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to create a new sample event'));
                return;
            }
            // Wait for the event to be fully processed and available on the group
            // before redirecting.
            const t0 = performance.now();
            const { eventCreated, retries } = yield latestEventAvailable(api, eventData.groupID);
            const t1 = performance.now();
            (0, indicator_1.clearIndicators)();
            this.setState({ creating: false });
            const duration = Math.ceil(t1 - t0);
            this.recordAnalytics({ eventCreated, retries, duration });
            if (!eventCreated) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to load sample event'));
                Sentry.withScope(scope => {
                    scope.setTag('groupID', eventData.groupID);
                    scope.setTag('platform', project.platform || '');
                    scope.setTag('interval', EVENT_POLL_INTERVAL.toString());
                    scope.setTag('retries', retries.toString());
                    scope.setTag('duration', duration.toString());
                    scope.setLevel(Sentry.Severity.Warning);
                    Sentry.captureMessage('Failed to load sample event');
                });
                return;
            }
            react_router_1.browserHistory.push(`/organizations/${organization.slug}/issues/${eventData.groupID}/?project=${project.id}`);
        });
    }
    componentDidMount() {
        const { organization, project, source } = this.props;
        if (!project) {
            return;
        }
        (0, analytics_1.trackAdhocEvent)({
            eventKey: 'sample_event.button_viewed',
            org_id: organization.id,
            project_id: project.id,
            source,
        });
    }
    recordAnalytics({ eventCreated, retries, duration }) {
        const { organization, project, source } = this.props;
        if (!project) {
            return;
        }
        const eventKey = `sample_event.${eventCreated ? 'created' : 'failed'}`;
        const eventName = `Sample Event ${eventCreated ? 'Created' : 'Failed'}`;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey,
            eventName,
            organization_id: organization.id,
            project_id: project.id,
            platform: project.platform || '',
            interval: EVENT_POLL_INTERVAL,
            retries,
            duration,
            source,
        });
    }
    render() {
        const _a = this.props, { api: _api, organization: _organization, project: _project, source: _source } = _a, props = (0, tslib_1.__rest)(_a, ["api", "organization", "project", "source"]);
        const { creating } = this.state;
        return (<button_1.default {...props} data-test-id="create-sample-event" disabled={props.disabled || creating} onClick={this.createSampleGroup}/>);
    }
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(CreateSampleEventButton));
//# sourceMappingURL=createSampleEventButton.jsx.map