Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const traceFullQuery_1 = require("app/utils/performance/quickTrace/traceFullQuery");
const traceMetaQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/quickTrace/traceMetaQuery"));
const queryString_1 = require("app/utils/queryString");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
class TraceSummary extends react_1.Component {
    getDocumentTitle() {
        return [(0, locale_1.t)('Trace Details'), (0, locale_1.t)('Performance')].join(' - ');
    }
    getTraceSlug() {
        const { traceSlug } = this.props.params;
        return typeof traceSlug === 'string' ? traceSlug.trim() : '';
    }
    getDateSelection() {
        const { location } = this.props;
        const queryParams = (0, getParams_1.getParams)(location.query, {
            allowAbsolutePageDatetime: true,
        });
        const start = (0, queryString_1.decodeScalar)(queryParams.start);
        const end = (0, queryString_1.decodeScalar)(queryParams.end);
        const statsPeriod = (0, queryString_1.decodeScalar)(queryParams.statsPeriod);
        return { start, end, statsPeriod };
    }
    getTraceEventView() {
        const traceSlug = this.getTraceSlug();
        const { start, end, statsPeriod } = this.getDateSelection();
        return eventView_1.default.fromSavedQuery({
            id: undefined,
            name: `Events with Trace ID ${traceSlug}`,
            fields: ['title', 'event.type', 'project', 'timestamp'],
            orderby: '-timestamp',
            query: `trace:${traceSlug}`,
            projects: [globalSelectionHeader_1.ALL_ACCESS_PROJECTS],
            version: 2,
            start,
            end,
            range: statsPeriod,
        });
    }
    renderContent() {
        const { location, organization, params } = this.props;
        const traceSlug = this.getTraceSlug();
        const { start, end, statsPeriod } = this.getDateSelection();
        const dateSelected = Boolean(statsPeriod || (start && end));
        const content = ({ isLoading, error, traces, meta, }) => (<content_1.default location={location} organization={organization} params={params} traceSlug={traceSlug} traceEventView={this.getTraceEventView()} dateSelected={dateSelected} isLoading={isLoading} error={error} traces={traces} meta={meta}/>);
        if (!dateSelected) {
            return content({
                isLoading: false,
                error: 'date selection not specified',
                traces: null,
                meta: null,
            });
        }
        return (<traceFullQuery_1.TraceFullDetailedQuery location={location} orgSlug={organization.slug} traceId={traceSlug} start={start} end={end} statsPeriod={statsPeriod}>
        {traceResults => (<traceMetaQuery_1.default location={location} orgSlug={organization.slug} traceId={traceSlug} start={start} end={end} statsPeriod={statsPeriod}>
            {metaResults => content({
                    isLoading: traceResults.isLoading || metaResults.isLoading,
                    error: traceResults.error || metaResults.error,
                    traces: traceResults.traces,
                    meta: metaResults.meta,
                })}
          </traceMetaQuery_1.default>)}
      </traceFullQuery_1.TraceFullDetailedQuery>);
    }
    render() {
        const { organization } = this.props;
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <StyledPageContent>
          <noProjectMessage_1.default organization={organization}>
            {this.renderContent()}
          </noProjectMessage_1.default>
        </StyledPageContent>
      </sentryDocumentTitle_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)((0, withApi_1.default)(TraceSummary));
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
//# sourceMappingURL=index.jsx.map