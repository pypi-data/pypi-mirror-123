Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const prompts_1 = require("app/actionCreators/prompts");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const quickTrace_1 = (0, tslib_1.__importDefault)(require("app/components/quickTrace"));
const utils_1 = require("app/components/quickTrace/utils");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const quickTraceQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/quickTrace/quickTraceQuery"));
const promptIsDismissed_1 = require("app/utils/promptIsDismissed");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class IssueQuickTrace extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            shouldShow: null,
        };
        this.snoozePrompt = () => {
            const { api, event, organization } = this.props;
            const data = {
                projectId: event.projectID,
                organizationId: organization.id,
                feature: 'quick_trace_missing',
                status: 'snoozed',
            };
            (0, prompts_1.promptsUpdate)(api, data).then(() => this.setState({ shouldShow: false }));
        };
    }
    componentDidMount() {
        this.promptsCheck();
    }
    shouldComponentUpdate(nextProps, nextState) {
        return (this.props.event !== nextProps.event ||
            this.state.shouldShow !== nextState.shouldShow);
    }
    promptsCheck() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, event, organization } = this.props;
            const data = yield (0, prompts_1.promptsCheck)(api, {
                organizationId: organization.id,
                projectId: event.projectID,
                feature: 'quick_trace_missing',
            });
            this.setState({ shouldShow: !(0, promptIsDismissed_1.promptIsDismissed)(data !== null && data !== void 0 ? data : {}, 30) });
        });
    }
    handleTraceLink(organization) {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'quick_trace.trace_id.clicked',
            eventName: 'Quick Trace: Trace ID clicked',
            organization_id: parseInt(organization.id, 10),
            source: 'issues',
        });
    }
    renderTraceLink({ isLoading, error, trace, type }) {
        const { event, organization } = this.props;
        if (isLoading || error !== null || trace === null || type === 'empty') {
            return null;
        }
        return (<LinkContainer>
        <link_1.default to={(0, utils_1.generateTraceTarget)(event, organization)} onClick={() => this.handleTraceLink(organization)}>
          {(0, locale_1.t)('View Full Trace')}
        </link_1.default>
      </LinkContainer>);
    }
    renderQuickTrace(results) {
        const { event, location, organization } = this.props;
        const { shouldShow } = this.state;
        const { isLoading, error, trace, type } = results;
        if (isLoading) {
            return <placeholder_1.default height="24px"/>;
        }
        if (error || trace === null || trace.length === 0) {
            if (!shouldShow) {
                return null;
            }
            return (<StyledAlert type="info" icon={<icons_1.IconInfo size="sm"/>}>
          <AlertContent>
            {(0, locale_1.tct)('The [type] for this error cannot be found. [link]', {
                    type: type === 'missing' ? (0, locale_1.t)('transaction') : (0, locale_1.t)('trace'),
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/sentry-basics/tracing/trace-view/#troubleshooting">
                  {(0, locale_1.t)('Read the docs to understand why.')}
                </externalLink_1.default>),
                })}
            <button_1.default priority="link" title={(0, locale_1.t)('Dismiss for a month')} onClick={this.snoozePrompt}>
              <icons_1.IconClose />
            </button_1.default>
          </AlertContent>
        </StyledAlert>);
        }
        return (<quickTrace_1.default event={event} quickTrace={results} location={location} organization={organization} anchor="left" errorDest="issue" transactionDest="performance"/>);
    }
    render() {
        const { event, organization, location } = this.props;
        return (<errorBoundary_1.default mini>
        <quickTraceQuery_1.default event={event} location={location} orgSlug={organization.slug}>
          {results => {
                return (<react_1.Fragment>
                {this.renderTraceLink(results)}
                <QuickTraceWrapper>{this.renderQuickTrace(results)}</QuickTraceWrapper>
              </react_1.Fragment>);
            }}
        </quickTraceQuery_1.default>
      </errorBoundary_1.default>);
    }
}
const LinkContainer = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(1)};
  padding-left: ${(0, space_1.default)(1)};
  position: relative;

  &:before {
    display: block;
    position: absolute;
    content: '';
    left: 0;
    top: 2px;
    height: 14px;
    border-left: 1px solid ${p => p.theme.border};
  }
`;
const QuickTraceWrapper = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(0.5)};
`;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin: 0;
`;
const AlertContent = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    justify-content: space-between;
  }
`;
exports.default = (0, withApi_1.default)(IssueQuickTrace);
//# sourceMappingURL=issueQuickTrace.jsx.map