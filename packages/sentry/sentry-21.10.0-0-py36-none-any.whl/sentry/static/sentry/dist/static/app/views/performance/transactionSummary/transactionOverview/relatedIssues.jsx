Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const styles_1 = require("app/components/charts/styles");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const groupList_1 = (0, tslib_1.__importDefault)(require("app/components/issues/groupList"));
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const fields_1 = require("app/utils/discover/fields");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const EXCLUDE_TAG_KEYS = new Set([
    // event type can be "transaction" but we're searching for issues
    'event.type',
    // the project is already determined by the transaction,
    // and issue search does not support the project filter
    'project',
]);
class RelatedIssues extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleOpenClick = () => {
            const { organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.summary.open_issues',
                eventName: 'Performance Views: Open issues from transaction summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        this.renderEmptyMessage = () => {
            const { statsPeriod } = this.props;
            const selectedTimePeriod = statsPeriod && constants_1.DEFAULT_RELATIVE_PERIODS[statsPeriod];
            const displayedPeriod = selectedTimePeriod
                ? selectedTimePeriod.toLowerCase()
                : (0, locale_1.t)('given timeframe');
            return (<panels_1.Panel>
        <panels_1.PanelBody>
          <emptyStateWarning_1.default>
            <p>
              {(0, locale_1.tct)('No new issues for this transaction for the [timePeriod].', {
                    timePeriod: displayedPeriod,
                })}
            </p>
          </emptyStateWarning_1.default>
        </panels_1.PanelBody>
      </panels_1.Panel>);
        };
    }
    getIssuesEndpoint() {
        const { transaction, organization, start, end, statsPeriod, location } = this.props;
        const queryParams = Object.assign({ start,
            end,
            statsPeriod, limit: 5, sort: 'new' }, (0, pick_1.default)(location.query, [...Object.values(globalSelectionHeader_1.URL_PARAM), 'cursor']));
        const currentFilter = new tokenizeSearch_1.MutableSearch((0, queryString_1.decodeScalar)(location.query.query, ''));
        currentFilter.getFilterKeys().forEach(tagKey => {
            const searchKey = tagKey.startsWith('!') ? tagKey.substr(1) : tagKey;
            // Remove aggregates and transaction event fields
            if (
            // aggregates
            searchKey.match(/\w+\(.*\)/) ||
                // transaction event fields
                fields_1.TRACING_FIELDS.includes(searchKey) ||
                // tags that we don't want to pass to pass to issue search
                EXCLUDE_TAG_KEYS.has(searchKey)) {
                currentFilter.removeFilter(tagKey);
            }
        });
        currentFilter
            .addFreeText('is:unresolved')
            .setFilterValues('transaction', [transaction]);
        return {
            path: `/organizations/${organization.slug}/issues/`,
            queryParams: Object.assign(Object.assign({}, queryParams), { query: currentFilter.formatString() }),
        };
    }
    render() {
        const { organization } = this.props;
        const { path, queryParams } = this.getIssuesEndpoint();
        const issueSearch = {
            pathname: `/organizations/${organization.slug}/issues/`,
            query: queryParams,
        };
        return (<react_1.Fragment>
        <ControlsWrapper>
          <styles_1.SectionHeading>{(0, locale_1.t)('Related Issues')}</styles_1.SectionHeading>
          <button_1.default data-test-id="issues-open" size="small" to={issueSearch} onClick={this.handleOpenClick}>
            {(0, locale_1.t)('Open in Issues')}
          </button_1.default>
        </ControlsWrapper>

        <TableWrapper>
          <groupList_1.default orgId={organization.slug} endpointPath={path} queryParams={queryParams} query="" canSelectGroups={false} renderEmptyMessage={this.renderEmptyMessage} withChart={false} withPagination={false}/>
        </TableWrapper>
      </react_1.Fragment>);
    }
}
const ControlsWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const TableWrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(4)};
  ${panels_1.Panel} {
    /* smaller space between table and pagination */
    margin-bottom: -${(0, space_1.default)(1)};
  }
`;
exports.default = RelatedIssues;
//# sourceMappingURL=relatedIssues.jsx.map