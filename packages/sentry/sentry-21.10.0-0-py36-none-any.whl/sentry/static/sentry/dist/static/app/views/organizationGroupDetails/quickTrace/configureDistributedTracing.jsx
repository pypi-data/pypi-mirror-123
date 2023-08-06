Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const performance_quick_trace_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/performance-quick-trace.svg"));
const prompts_1 = require("app/actionCreators/prompts");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const docs_1 = require("app/utils/docs");
const promptIsDismissed_1 = require("app/utils/promptIsDismissed");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const DISTRIBUTED_TRACING_FEATURE = 'distributed_tracing';
class ConfigureDistributedTracing extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            shouldShow: null,
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    fetchData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, event, project, organization } = this.props;
            if (!(0, promptIsDismissed_1.promptCanShow)(DISTRIBUTED_TRACING_FEATURE, event.eventID)) {
                this.setState({ shouldShow: false });
                return;
            }
            const data = yield (0, prompts_1.promptsCheck)(api, {
                projectId: project.id,
                organizationId: organization.id,
                feature: DISTRIBUTED_TRACING_FEATURE,
            });
            this.setState({ shouldShow: !(0, promptIsDismissed_1.promptIsDismissed)(data !== null && data !== void 0 ? data : {}, 30) });
        });
    }
    trackAnalytics({ eventKey, eventName }) {
        const { project, organization } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey,
            eventName,
            organization_id: parseInt(organization.id, 10),
            project_id: parseInt(project.id, 10),
            platform: project.platform,
        });
    }
    handleClick({ action, eventKey, eventName }) {
        const { api, project, organization } = this.props;
        const data = {
            projectId: project.id,
            organizationId: organization.id,
            feature: DISTRIBUTED_TRACING_FEATURE,
            status: action,
        };
        (0, prompts_1.promptsUpdate)(api, data).then(() => this.setState({ shouldShow: false }));
        this.trackAnalytics({ eventKey, eventName });
    }
    renderActionButton(docsLink) {
        const features = ['organizations:performance-view'];
        const noFeatureMessage = (0, locale_1.t)('Requires performance monitoring.');
        const renderDisabled = p => (<hovercard_1.default body={<featureDisabled_1.default features={features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
        {p.children(p)}
      </hovercard_1.default>);
        return (<feature_1.default hookName="feature-disabled:configure-distributed-tracing" features={features} renderDisabled={renderDisabled}>
        {() => (<button_1.default size="small" priority="primary" href={docsLink} onClick={() => this.trackAnalytics({
                    eventKey: 'quick_trace.missing_instrumentation.docs',
                    eventName: 'Quick Trace: Missing Instrumentation Docs',
                })}>
            {(0, locale_1.t)('Read the docs')}
          </button_1.default>)}
      </feature_1.default>);
    }
    render() {
        const { project } = this.props;
        const { shouldShow } = this.state;
        if (!shouldShow) {
            return null;
        }
        const docsLink = (0, docs_1.getConfigureTracingDocsLink)(project);
        // if the platform does not support performance, do not show this prompt
        if (docsLink === null) {
            return null;
        }
        return (<ExampleQuickTracePanel dashedBorder>
        <div>
          <Header>{(0, locale_1.t)('Configure Distributed Tracing')}</Header>
          <Description>
            {(0, locale_1.t)('See what happened right before and after this error')}
          </Description>
        </div>
        <Image src={performance_quick_trace_svg_1.default} alt="configure distributed tracing"/>
        <ActionButtons>
          {this.renderActionButton(docsLink)}
          <buttonBar_1.default merged>
            <button_1.default title={(0, locale_1.t)('Remind me next month')} size="small" onClick={() => this.handleClick({
                action: 'snoozed',
                eventKey: 'quick_trace.missing_instrumentation.snoozed',
                eventName: 'Quick Trace: Missing Instrumentation Snoozed',
            })}>
              {(0, locale_1.t)('Snooze')}
            </button_1.default>
            <button_1.default title={(0, locale_1.t)('Dismiss for this project')} size="small" onClick={() => this.handleClick({
                action: 'dismissed',
                eventKey: 'quick_trace.missing_instrumentation.dismissed',
                eventName: 'Quick Trace: Missing Instrumentation Dismissed',
            })}>
              {(0, locale_1.t)('Dismiss')}
            </button_1.default>
          </buttonBar_1.default>
        </ActionButtons>
      </ExampleQuickTracePanel>);
    }
}
const ExampleQuickTracePanel = (0, styled_1.default)(panels_1.Panel) `
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  grid-template-rows: auto max-content;
  grid-gap: ${(0, space_1.default)(1)};
  background: none;
  padding: ${(0, space_1.default)(2)};
  margin: ${(0, space_1.default)(2)} 0;
`;
const Header = (0, styled_1.default)('h3') `
  font-size: ${p => p.theme.fontSizeSmall};
  text-transform: uppercase;
  color: ${p => p.theme.gray300};
  margin-bottom: ${(0, space_1.default)(1)};
`;
const Description = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
`;
const Image = (0, styled_1.default)('img') `
  grid-row: 1/3;
  grid-column: 2/3;
  justify-self: end;
`;
const ActionButtons = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content auto;
  justify-items: start;
  align-items: end;
  grid-column-gap: ${(0, space_1.default)(1)};
`;
exports.default = (0, withApi_1.default)(ConfigureDistributedTracing);
//# sourceMappingURL=configureDistributedTracing.jsx.map