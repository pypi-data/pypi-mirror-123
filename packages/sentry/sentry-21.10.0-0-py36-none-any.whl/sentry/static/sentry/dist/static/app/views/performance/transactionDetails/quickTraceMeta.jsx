Object.defineProperty(exports, "__esModule", { value: true });
exports.QuickTraceMetaBase = void 0;
const tslib_1 = require("tslib");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const quickTrace_1 = (0, tslib_1.__importDefault)(require("app/components/quickTrace"));
const utils_1 = require("app/components/quickTrace/utils");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const docs_1 = require("app/utils/docs");
const events_1 = require("app/utils/events");
const useOrganization_1 = require("app/utils/useOrganization");
const styles_1 = require("./styles");
function handleTraceLink(organization) {
    (0, analytics_1.trackAnalyticsEvent)({
        eventKey: 'quick_trace.trace_id.clicked',
        eventName: 'Quick Trace: Trace ID clicked',
        organization_id: parseInt(organization.id, 10),
        source: 'events',
    });
}
function QuickTraceMeta({ event, location, quickTrace, traceMeta, anchor, errorDest, transactionDest, project, }) {
    var _a, _b, _c;
    const organization = (0, useOrganization_1.useOrganization)();
    const features = ['performance-view'];
    const noFeatureMessage = (0, locale_1.t)('Requires performance monitoring.');
    const docsLink = (0, docs_1.getConfigureTracingDocsLink)(project);
    const traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : null;
    const traceTarget = (0, utils_1.generateTraceTarget)(event, organization);
    let body;
    let footer;
    if (!traceId || !quickTrace || quickTrace.trace === null) {
        // this platform doesn't support performance don't show anything here
        if (docsLink === null) {
            return null;
        }
        body = (0, locale_1.t)('Missing Trace');
        // need to configure tracing
        footer = <externalLink_1.default href={docsLink}>{(0, locale_1.t)('Read the docs')}</externalLink_1.default>;
    }
    else {
        if (quickTrace.isLoading) {
            body = <placeholder_1.default height="24px"/>;
        }
        else if (quickTrace.error) {
            body = '\u2014';
        }
        else {
            body = (<errorBoundary_1.default mini>
          <quickTrace_1.default event={event} quickTrace={{
                    type: quickTrace.type,
                    trace: quickTrace.trace,
                }} location={location} organization={organization} anchor={anchor} errorDest={errorDest} transactionDest={transactionDest}/>
        </errorBoundary_1.default>);
        }
        footer = (<link_1.default to={traceTarget} onClick={() => handleTraceLink(organization)}>
        {(0, locale_1.tct)('View Full Trace: [id][events]', {
                id: (0, events_1.getShortEventId)(traceId !== null && traceId !== void 0 ? traceId : ''),
                events: traceMeta
                    ? (0, locale_1.tn)(' (%s event)', ' (%s events)', traceMeta.transactions + traceMeta.errors)
                    : '',
            })}
      </link_1.default>);
    }
    return (<feature_1.default hookName="feature-disabled:performance-quick-trace" features={features}>
      {({ hasFeature }) => {
            // also need to enable the performance feature
            if (!hasFeature) {
                footer = (<hovercard_1.default body={<featureDisabled_1.default features={features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
              {footer}
            </hovercard_1.default>);
            }
            return <QuickTraceMetaBase body={body} footer={footer}/>;
        }}
    </feature_1.default>);
}
exports.default = QuickTraceMeta;
function QuickTraceMetaBase({ body, footer }) {
    return (<styles_1.MetaData headingText={(0, locale_1.t)('Trace Navigator')} tooltipText={(0, locale_1.t)('An abbreviated version of the full trace. Related frontend and backend services can be added to provide further visibility.')} bodyText={<div data-test-id="quick-trace-body">{body}</div>} subtext={<div data-test-id="quick-trace-footer">{footer}</div>}/>);
}
exports.QuickTraceMetaBase = QuickTraceMetaBase;
//# sourceMappingURL=quickTraceMeta.jsx.map