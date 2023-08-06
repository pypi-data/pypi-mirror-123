Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const breakdownBars_1 = (0, tslib_1.__importDefault)(require("app/components/charts/breakdownBars"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const styles_1 = require("app/components/charts/styles");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const data_1 = require("app/views/performance/data");
function StatusBreakdown({ eventView, location, organization }) {
    const breakdownView = eventView
        .withColumns([
        { kind: 'function', function: ['count', '', '', undefined] },
        { kind: 'field', field: 'transaction.status' },
    ])
        .withSorts([{ kind: 'desc', field: 'count' }]);
    return (<react_1.Fragment>
      <styles_1.SectionHeading>
        {(0, locale_1.t)('Status Breakdown')}
        <questionTooltip_1.default position="top" title={(0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.STATUS_BREAKDOWN)} size="sm"/>
      </styles_1.SectionHeading>
      <discoverQuery_1.default eventView={breakdownView} location={location} orgSlug={organization.slug} referrer="api.performance.status-breakdown">
        {({ isLoading, error, tableData }) => {
            if (isLoading) {
                return <placeholder_1.default height="124px"/>;
            }
            if (error) {
                return (<errorPanel_1.default height="124px">
                <icons_1.IconWarning color="gray300" size="lg"/>
              </errorPanel_1.default>);
            }
            if (!tableData || tableData.data.length === 0) {
                return (<EmptyStatusBreakdown small>{(0, locale_1.t)('No statuses found')}</EmptyStatusBreakdown>);
            }
            const points = tableData.data.map(row => ({
                label: String(row['transaction.status']),
                value: parseInt(String(row.count), 10),
                onClick: () => {
                    const query = new tokenizeSearch_1.MutableSearch(eventView.query);
                    query
                        .removeFilter('!transaction.status')
                        .setFilterValues('transaction.status', [row['transaction.status']]);
                    react_router_1.browserHistory.push({
                        pathname: location.pathname,
                        query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query: query.formatString() }),
                    });
                },
            }));
            return <breakdownBars_1.default data={points}/>;
        }}
      </discoverQuery_1.default>
    </react_1.Fragment>);
}
const EmptyStatusBreakdown = (0, styled_1.default)(emptyStateWarning_1.default) `
  height: 124px;
  padding: 50px 15%;
`;
exports.default = StatusBreakdown;
//# sourceMappingURL=statusBreakdown.jsx.map