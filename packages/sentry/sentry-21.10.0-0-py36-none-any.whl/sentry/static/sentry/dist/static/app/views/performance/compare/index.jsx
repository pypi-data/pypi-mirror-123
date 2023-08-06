Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
const fetchEvent_1 = (0, tslib_1.__importDefault)(require("./fetchEvent"));
class TransactionComparisonPage extends React.PureComponent {
    getEventSlugs() {
        const { baselineEventSlug, regressionEventSlug } = this.props.params;
        const validatedBaselineEventSlug = typeof baselineEventSlug === 'string' ? baselineEventSlug.trim() : undefined;
        const validatedRegressionEventSlug = typeof regressionEventSlug === 'string' ? regressionEventSlug.trim() : undefined;
        return {
            baselineEventSlug: validatedBaselineEventSlug,
            regressionEventSlug: validatedRegressionEventSlug,
        };
    }
    fetchEvent(eventSlug, renderFunc) {
        if (!eventSlug) {
            return <notFound_1.default />;
        }
        const { organization } = this.props;
        return (<fetchEvent_1.default orgSlug={organization.slug} eventSlug={eventSlug}>
        {renderFunc}
      </fetchEvent_1.default>);
    }
    renderComparison({ baselineEventSlug, regressionEventSlug, }) {
        return this.fetchEvent(baselineEventSlug, baselineEventResults => {
            return this.fetchEvent(regressionEventSlug, regressionEventResults => {
                if (baselineEventResults.isLoading || regressionEventResults.isLoading) {
                    return <loadingIndicator_1.default />;
                }
                if (baselineEventResults.error || regressionEventResults.error) {
                    if (baselineEventResults.error) {
                        Sentry.captureException(baselineEventResults.error);
                    }
                    if (regressionEventResults.error) {
                        Sentry.captureException(regressionEventResults.error);
                    }
                    return <loadingError_1.default />;
                }
                if (!baselineEventResults.event || !regressionEventResults.event) {
                    return <notFound_1.default />;
                }
                const { organization, location, params } = this.props;
                return (<content_1.default organization={organization} location={location} params={params} baselineEvent={baselineEventResults.event} regressionEvent={regressionEventResults.event}/>);
            });
        });
    }
    getDocumentTitle({ baselineEventSlug, regressionEventSlug }) {
        if (typeof baselineEventSlug === 'string' &&
            typeof regressionEventSlug === 'string') {
            const title = (0, locale_1.t)('Comparing %s to %s', baselineEventSlug, regressionEventSlug);
            return [title, (0, locale_1.t)('Performance')].join(' - ');
        }
        return [(0, locale_1.t)('Transaction Comparison'), (0, locale_1.t)('Performance')].join(' - ');
    }
    render() {
        const { organization } = this.props;
        const { baselineEventSlug, regressionEventSlug } = this.getEventSlugs();
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle({ baselineEventSlug, regressionEventSlug })} orgSlug={organization.slug}>
        <React.Fragment>
          <StyledPageContent>
            <noProjectMessage_1.default organization={organization}>
              {this.renderComparison({ baselineEventSlug, regressionEventSlug })}
            </noProjectMessage_1.default>
          </StyledPageContent>
        </React.Fragment>
      </sentryDocumentTitle_1.default>);
    }
}
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
exports.default = (0, withOrganization_1.default)(TransactionComparisonPage);
//# sourceMappingURL=index.jsx.map