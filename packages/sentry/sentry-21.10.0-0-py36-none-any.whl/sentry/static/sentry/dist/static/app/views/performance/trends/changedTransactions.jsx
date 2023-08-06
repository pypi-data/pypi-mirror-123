Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const styles_1 = require("app/components/charts/styles");
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const radio_1 = (0, tslib_1.__importDefault)(require("app/components/radio"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
const trendsDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/trends/trendsDiscoverQuery"));
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const radioGroup_1 = require("app/views/settings/components/forms/controls/radioGroup");
const charts_1 = require("../transactionSummary/transactionOverview/charts");
const utils_1 = require("../transactionSummary/utils");
const chart_1 = (0, tslib_1.__importDefault)(require("./chart"));
const types_1 = require("./types");
const utils_2 = require("./utils");
const makeTrendsCursorHandler = (trendChangeType) => (cursor, path, query) => {
    const cursorQuery = {};
    if (trendChangeType === types_1.TrendChangeType.IMPROVED) {
        cursorQuery.improvedCursor = cursor;
    }
    else if (trendChangeType === types_1.TrendChangeType.REGRESSION) {
        cursorQuery.regressionCursor = cursor;
    }
    const selectedQueryKey = (0, utils_2.getSelectedQueryKey)(trendChangeType);
    delete query[selectedQueryKey];
    react_router_1.browserHistory.push({
        pathname: path,
        query: Object.assign(Object.assign({}, query), cursorQuery),
    });
};
function getChartTitle(trendChangeType) {
    switch (trendChangeType) {
        case types_1.TrendChangeType.IMPROVED:
            return (0, locale_1.t)('Most Improved Transactions');
        case types_1.TrendChangeType.REGRESSION:
            return (0, locale_1.t)('Most Regressed Transactions');
        default:
            throw new Error('No trend type passed');
    }
}
function getSelectedTransaction(location, trendChangeType, transactions) {
    const queryKey = (0, utils_2.getSelectedQueryKey)(trendChangeType);
    const selectedTransactionName = (0, queryString_1.decodeScalar)(location.query[queryKey]);
    if (!transactions) {
        return undefined;
    }
    const selectedTransaction = transactions.find(transaction => `${transaction.transaction}-${transaction.project}` === selectedTransactionName);
    if (selectedTransaction) {
        return selectedTransaction;
    }
    return transactions.length > 0 ? transactions[0] : undefined;
}
function handleChangeSelected(location, trendChangeType) {
    return function updateSelected(transaction) {
        const selectedQueryKey = (0, utils_2.getSelectedQueryKey)(trendChangeType);
        const query = Object.assign({}, location.query);
        if (!transaction) {
            delete query[selectedQueryKey];
        }
        else {
            query[selectedQueryKey] = transaction
                ? `${transaction.transaction}-${transaction.project}`
                : undefined;
        }
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query,
        });
    };
}
var FilterSymbols;
(function (FilterSymbols) {
    FilterSymbols["GREATER_THAN_EQUALS"] = ">=";
    FilterSymbols["LESS_THAN_EQUALS"] = "<=";
})(FilterSymbols || (FilterSymbols = {}));
function handleFilterTransaction(location, transaction) {
    const queryString = (0, queryString_1.decodeScalar)(location.query.query);
    const conditions = new tokenizeSearch_1.MutableSearch(queryString !== null && queryString !== void 0 ? queryString : '');
    conditions.addFilterValues('!transaction', [transaction]);
    const query = conditions.formatString();
    react_router_1.browserHistory.push({
        pathname: location.pathname,
        query: Object.assign(Object.assign({}, location.query), { query: String(query).trim() }),
    });
}
function handleFilterDuration(location, value, symbol) {
    const durationTag = (0, utils_2.getCurrentTrendParameter)(location).column;
    const queryString = (0, queryString_1.decodeScalar)(location.query.query);
    const conditions = new tokenizeSearch_1.MutableSearch(queryString !== null && queryString !== void 0 ? queryString : '');
    const existingValues = conditions.getFilterValues(durationTag);
    const alternateSymbol = symbol === FilterSymbols.GREATER_THAN_EQUALS ? '>' : '<';
    if (existingValues) {
        existingValues.forEach(existingValue => {
            if (existingValue.startsWith(symbol) || existingValue.startsWith(alternateSymbol)) {
                conditions.removeFilterValue(durationTag, existingValue);
            }
        });
    }
    conditions.addFilterValues(durationTag, [`${symbol}${value}`]);
    const query = conditions.formatString();
    react_router_1.browserHistory.push({
        pathname: location.pathname,
        query: Object.assign(Object.assign({}, location.query), { query: String(query).trim() }),
    });
}
function ChangedTransactions(props) {
    const { location, trendChangeType, previousTrendFunction, previousTrendColumn, organization, projects, setError, } = props;
    const api = (0, useApi_1.default)();
    const trendView = props.trendView.clone();
    const chartTitle = getChartTitle(trendChangeType);
    (0, utils_2.modifyTrendView)(trendView, location, trendChangeType);
    const onCursor = makeTrendsCursorHandler(trendChangeType);
    const cursor = (0, queryString_1.decodeScalar)(location.query[utils_2.trendCursorNames[trendChangeType]]);
    return (<trendsDiscoverQuery_1.default eventView={trendView} orgSlug={organization.slug} location={location} trendChangeType={trendChangeType} cursor={cursor} limit={5} setError={setError}>
      {({ isLoading, trendsData, pageLinks }) => {
            const trendFunction = (0, utils_2.getCurrentTrendFunction)(location);
            const trendParameter = (0, utils_2.getCurrentTrendParameter)(location);
            const events = (0, utils_2.normalizeTrends)((trendsData && trendsData.events && trendsData.events.data) || []);
            const selectedTransaction = getSelectedTransaction(location, trendChangeType, events);
            const statsData = (trendsData === null || trendsData === void 0 ? void 0 : trendsData.stats) || {};
            const transactionsList = events && events.slice ? events.slice(0, 5) : [];
            const currentTrendFunction = isLoading && previousTrendFunction
                ? previousTrendFunction
                : trendFunction.field;
            const currentTrendColumn = isLoading && previousTrendColumn ? previousTrendColumn : trendParameter.column;
            const titleTooltipContent = (0, locale_1.t)('This compares the baseline (%s) of the past with the present.', trendFunction.legendLabel);
            return (<TransactionsListContainer>
            <TrendsTransactionPanel>
              <StyledHeaderTitleLegend>
                {chartTitle}
                <questionTooltip_1.default size="sm" position="top" title={titleTooltipContent}/>
              </StyledHeaderTitleLegend>
              {isLoading ? (<loadingIndicator_1.default style={{
                        margin: '237px auto',
                    }}/>) : (<react_1.Fragment>
                  {transactionsList.length ? (<react_1.Fragment>
                      <ChartContainer>
                        <chart_1.default statsData={statsData} query={trendView.query} project={trendView.project} environment={trendView.environment} start={trendView.start} end={trendView.end} statsPeriod={trendView.statsPeriod} transaction={selectedTransaction} isLoading={isLoading} {...props}/>
                      </ChartContainer>
                      {transactionsList.map((transaction, index) => (<TrendsListItem api={api} currentTrendFunction={currentTrendFunction} currentTrendColumn={currentTrendColumn} trendView={props.trendView} organization={organization} transaction={transaction} key={transaction.transaction} index={index} trendChangeType={trendChangeType} transactions={transactionsList} location={location} projects={projects} statsData={statsData} handleSelectTransaction={handleChangeSelected(location, trendChangeType)}/>))}
                    </react_1.Fragment>) : (<StyledEmptyStateWarning small>
                      {(0, locale_1.t)('No results')}
                    </StyledEmptyStateWarning>)}
                </react_1.Fragment>)}
            </TrendsTransactionPanel>
            <pagination_1.default pageLinks={pageLinks} onCursor={onCursor}/>
          </TransactionsListContainer>);
        }}
    </trendsDiscoverQuery_1.default>);
}
function TrendsListItem(props) {
    const { transaction, transactions, trendChangeType, currentTrendFunction, currentTrendColumn, index, location, projects, handleSelectTransaction, } = props;
    const color = utils_2.trendToColor[trendChangeType].default;
    const selectedTransaction = getSelectedTransaction(location, trendChangeType, transactions);
    const isSelected = selectedTransaction === transaction;
    const project = projects.find(({ slug }) => slug === transaction.project);
    const currentPeriodValue = transaction.aggregate_range_2;
    const previousPeriodValue = transaction.aggregate_range_1;
    const absolutePercentChange = (0, formatters_1.formatPercentage)(Math.abs(transaction.trend_percentage - 1), 0);
    const previousDuration = (0, formatters_1.getDuration)(previousPeriodValue / 1000, previousPeriodValue < 1000 && previousPeriodValue > 10 ? 0 : 2);
    const currentDuration = (0, formatters_1.getDuration)(currentPeriodValue / 1000, currentPeriodValue < 1000 && currentPeriodValue > 10 ? 0 : 2);
    const percentChangeExplanation = (0, locale_1.t)('Over this period, the %s for %s has %s %s from %s to %s', currentTrendFunction, currentTrendColumn, trendChangeType === types_1.TrendChangeType.IMPROVED ? (0, locale_1.t)('decreased') : (0, locale_1.t)('increased'), absolutePercentChange, previousDuration, currentDuration);
    const longestPeriodValue = trendChangeType === types_1.TrendChangeType.IMPROVED
        ? previousPeriodValue
        : currentPeriodValue;
    const longestDuration = trendChangeType === types_1.TrendChangeType.IMPROVED ? previousDuration : currentDuration;
    return (<ListItemContainer data-test-id={'trends-list-item-' + trendChangeType}>
      <ItemRadioContainer color={color}>
        <tooltip_1.default title={<TooltipContent>
              <span>{(0, locale_1.t)('Total Events')}</span>
              <span>
                <count_1.default value={transaction.count_range_1}/>
                <StyledIconArrow direction="right" size="xs"/>
                <count_1.default value={transaction.count_range_2}/>
              </span>
            </TooltipContent>} disableForVisualTest // Disabled tooltip in snapshots because of overlap order issues.
    >
          <radioGroup_1.RadioLineItem index={index} role="radio">
            <radio_1.default checked={isSelected} onChange={() => handleSelectTransaction(transaction)}/>
          </radioGroup_1.RadioLineItem>
        </tooltip_1.default>
      </ItemRadioContainer>
      <TransactionSummaryLink {...props}/>
      <ItemTransactionPercentage>
        <tooltip_1.default title={percentChangeExplanation}>
          <react_1.Fragment>
            {trendChangeType === types_1.TrendChangeType.REGRESSION ? '+' : ''}
            {(0, formatters_1.formatPercentage)(transaction.trend_percentage - 1, 0)}
          </react_1.Fragment>
        </tooltip_1.default>
      </ItemTransactionPercentage>
      <dropdownLink_1.default caret={false} anchorRight title={<StyledButton size="xsmall" icon={<icons_1.IconEllipsis data-test-id="trends-item-action" size="xs"/>}/>}>
        <menuItem_1.default onClick={() => handleFilterDuration(location, longestPeriodValue, FilterSymbols.LESS_THAN_EQUALS)}>
          <StyledMenuAction>{(0, locale_1.t)('Show \u2264 %s', longestDuration)}</StyledMenuAction>
        </menuItem_1.default>
        <menuItem_1.default onClick={() => handleFilterDuration(location, longestPeriodValue, FilterSymbols.GREATER_THAN_EQUALS)}>
          <StyledMenuAction>{(0, locale_1.t)('Show \u2265 %s', longestDuration)}</StyledMenuAction>
        </menuItem_1.default>
        <menuItem_1.default onClick={() => handleFilterTransaction(location, transaction.transaction)}>
          <StyledMenuAction>{(0, locale_1.t)('Hide from list')}</StyledMenuAction>
        </menuItem_1.default>
      </dropdownLink_1.default>
      <ItemTransactionDurationChange>
        {project && (<tooltip_1.default title={transaction.project}>
            <idBadge_1.default avatarSize={16} project={project} hideName/>
          </tooltip_1.default>)}
        <CompareDurations {...props}/>
      </ItemTransactionDurationChange>
      <ItemTransactionStatus color={color}>
        <ValueDelta {...props}/>
      </ItemTransactionStatus>
    </ListItemContainer>);
}
const CompareDurations = ({ transaction }) => {
    const { fromSeconds, toSeconds, showDigits } = (0, utils_2.transformDeltaSpread)(transaction.aggregate_range_1, transaction.aggregate_range_2);
    return (<DurationChange>
      <duration_1.default seconds={fromSeconds} fixedDigits={showDigits ? 1 : 0} abbreviation/>
      <StyledIconArrow direction="right" size="xs"/>
      <duration_1.default seconds={toSeconds} fixedDigits={showDigits ? 1 : 0} abbreviation/>
    </DurationChange>);
};
const ValueDelta = ({ transaction, trendChangeType }) => {
    const { seconds, fixedDigits, changeLabel } = (0, utils_2.transformValueDelta)(transaction.trend_difference, trendChangeType);
    return (<span>
      <duration_1.default seconds={seconds} fixedDigits={fixedDigits} abbreviation/> {changeLabel}
    </span>);
};
const TransactionSummaryLink = (props) => {
    const { organization, trendView: eventView, transaction, projects, currentTrendFunction, currentTrendColumn, } = props;
    const summaryView = eventView.clone();
    const projectID = (0, utils_2.getTrendProjectId)(transaction, projects);
    const target = (0, utils_1.transactionSummaryRouteWithQuery)({
        orgSlug: organization.slug,
        transaction: String(transaction.transaction),
        query: summaryView.generateQueryStringObject(),
        projectID,
        display: charts_1.DisplayModes.TREND,
        trendFunction: currentTrendFunction,
        trendColumn: currentTrendColumn,
    });
    return <ItemTransactionName to={target}>{transaction.transaction}</ItemTransactionName>;
};
const TransactionsListContainer = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
`;
const TrendsTransactionPanel = (0, styled_1.default)(panels_1.Panel) `
  margin: 0;
  flex-grow: 1;
`;
const ChartContainer = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(3)};
`;
const StyledHeaderTitleLegend = (0, styled_1.default)(styles_1.HeaderTitleLegend) `
  border-radius: ${p => p.theme.borderRadius};
  margin: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)};
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  vertical-align: middle;
`;
const StyledMenuAction = (0, styled_1.default)('div') `
  white-space: nowrap;
  color: ${p => p.theme.textColor};
`;
const StyledEmptyStateWarning = (0, styled_1.default)(emptyStateWarning_1.default) `
  min-height: 300px;
  justify-content: center;
`;
const ListItemContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 24px auto 100px 30px;
  grid-template-rows: repeat(2, auto);
  grid-column-gap: ${(0, space_1.default)(1)};
  border-top: 1px solid ${p => p.theme.border};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
`;
const ItemRadioContainer = (0, styled_1.default)('div') `
  grid-row: 1/3;
  input {
    cursor: pointer;
  }
  input:checked::after {
    background-color: ${p => p.color};
  }
`;
const ItemTransactionName = (0, styled_1.default)(link_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};
  margin-right: ${(0, space_1.default)(1)};
  ${overflowEllipsis_1.default};
`;
const ItemTransactionDurationChange = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  font-size: ${p => p.theme.fontSizeSmall};
`;
const DurationChange = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray300};
  margin: 0 ${(0, space_1.default)(1)};
`;
const ItemTransactionPercentage = (0, styled_1.default)('div') `
  text-align: right;
  font-size: ${p => p.theme.fontSizeMedium};
`;
const ItemTransactionStatus = (0, styled_1.default)('div') `
  color: ${p => p.color};
  text-align: right;
  font-size: ${p => p.theme.fontSizeSmall};
`;
const TooltipContent = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  align-items: center;
`;
const StyledIconArrow = (0, styled_1.default)(icons_1.IconArrow) `
  margin: 0 ${(0, space_1.default)(1)};
`;
exports.default = (0, withProjects_1.default)((0, withOrganization_1.default)(ChangedTransactions));
//# sourceMappingURL=changedTransactions.jsx.map