Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const sortLink_1 = (0, tslib_1.__importDefault)(require("app/components/gridEditable/sortLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panelTable_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelTable"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
const fields_1 = require("app/utils/discover/fields");
const urls_1 = require("app/utils/discover/urls");
const formatters_1 = require("app/utils/formatters");
const cellAction_1 = (0, tslib_1.__importDefault)(require("app/views/eventsV2/table/cellAction"));
const styles_1 = require("app/views/performance/styles");
const utils_1 = require("app/views/performance/utils");
class TransactionsTable extends React.PureComponent {
    getTitles() {
        const { eventView, titles } = this.props;
        return titles !== null && titles !== void 0 ? titles : eventView.getFields();
    }
    renderHeader() {
        const { tableData, columnOrder, baselineTransactionName } = this.props;
        const tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
        const generateSortLink = () => undefined;
        const tableTitles = this.getTitles();
        const headers = tableTitles.map((title, index) => {
            const column = columnOrder[index];
            const align = (0, fields_1.fieldAlignment)(column.name, column.type, tableMeta);
            if (column.key === 'span_ops_breakdown.relative') {
                return (<HeadCellContainer key={index}>
            <guideAnchor_1.default target="span_op_relative_breakdowns">
              <sortLink_1.default align={align} title={title === (0, locale_1.t)('operation duration') ? (<React.Fragment>
                      {title}
                      <StyledIconQuestion size="xs" position="top" title={(0, locale_1.t)(`Span durations are summed over the course of an entire transaction. Any overlapping spans are only counted once.`)}/>
                    </React.Fragment>) : (title)} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
            </guideAnchor_1.default>
          </HeadCellContainer>);
            }
            return (<HeadCellContainer key={index}>
          <sortLink_1.default align={align} title={title} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
        </HeadCellContainer>);
        });
        if (baselineTransactionName) {
            headers.push(<HeadCellContainer key="baseline">
          <sortLink_1.default align="right" title={(0, locale_1.t)('Compared to Baseline')} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
        </HeadCellContainer>);
        }
        return headers;
    }
    renderRow(row, rowIndex, columnOrder, tableMeta) {
        const { eventView, organization, location, generateLink, baselineTransactionName, baselineData, handleBaselineClick, handleCellAction, titles, } = this.props;
        const fields = eventView.getFields();
        if (titles && titles.length) {
            // Slice to match length of given titles
            columnOrder = columnOrder.slice(0, titles.length);
        }
        const resultsRow = columnOrder.map((column, index) => {
            var _a;
            const field = String(column.key);
            // TODO add a better abstraction for this in fieldRenderers.
            const fieldName = (0, fields_1.getAggregateAlias)(field);
            const fieldType = tableMeta[fieldName];
            const fieldRenderer = (0, fieldRenderers_1.getFieldRenderer)(field, tableMeta);
            let rendered = fieldRenderer(row, { organization, location });
            const target = (_a = generateLink === null || generateLink === void 0 ? void 0 : generateLink[field]) === null || _a === void 0 ? void 0 : _a.call(generateLink, organization, row, location.query);
            if (target) {
                rendered = (<link_1.default data-test-id={`view-${fields[index]}`} to={target}>
            {rendered}
          </link_1.default>);
            }
            const isNumeric = ['integer', 'number', 'duration'].includes(fieldType);
            const key = `${rowIndex}:${column.key}:${index}`;
            rendered = isNumeric ? (<styles_1.GridCellNumber>{rendered}</styles_1.GridCellNumber>) : (<styles_1.GridCell>{rendered}</styles_1.GridCell>);
            if (handleCellAction) {
                rendered = (<cellAction_1.default column={column} dataRow={row} handleCellAction={handleCellAction(column)}>
            {rendered}
          </cellAction_1.default>);
            }
            return <BodyCellContainer key={key}>{rendered}</BodyCellContainer>;
        });
        if (baselineTransactionName) {
            if (baselineData) {
                const currentTransactionDuration = Number(row['transaction.duration']) || 0;
                const duration = baselineData['transaction.duration'];
                const delta = Math.abs(currentTransactionDuration - duration);
                const relativeSpeed = currentTransactionDuration < duration
                    ? (0, locale_1.t)('faster')
                    : currentTransactionDuration > duration
                        ? (0, locale_1.t)('slower')
                        : '';
                const target = (0, utils_1.getTransactionComparisonUrl)({
                    organization,
                    baselineEventSlug: (0, urls_1.generateEventSlug)(baselineData),
                    regressionEventSlug: (0, urls_1.generateEventSlug)(row),
                    transaction: baselineTransactionName,
                    query: location.query,
                });
                resultsRow.push(<BodyCellContainer data-test-id="baseline-cell" key={`${rowIndex}-baseline`} style={{ textAlign: 'right' }}>
            <styles_1.GridCell>
              <link_1.default to={target} onClick={handleBaselineClick}>
                {`${(0, formatters_1.getDuration)(delta / 1000, delta < 1000 ? 0 : 2)} ${relativeSpeed}`}
              </link_1.default>
            </styles_1.GridCell>
          </BodyCellContainer>);
            }
            else {
                resultsRow.push(<BodyCellContainer data-test-id="baseline-cell" key={`${rowIndex}-baseline`}>
            {'\u2014'}
          </BodyCellContainer>);
            }
        }
        return resultsRow;
    }
    renderResults() {
        const { isLoading, tableData, columnOrder } = this.props;
        let cells = [];
        if (isLoading) {
            return cells;
        }
        if (!tableData || !tableData.meta || !tableData.data) {
            return cells;
        }
        tableData.data.forEach((row, i) => {
            // Another check to appease tsc
            if (!tableData.meta) {
                return;
            }
            cells = cells.concat(this.renderRow(row, i, columnOrder, tableData.meta));
        });
        return cells;
    }
    render() {
        const { isLoading, tableData } = this.props;
        const hasResults = tableData && tableData.data && tableData.meta && tableData.data.length > 0;
        // Custom set the height so we don't have layout shift when results are loaded.
        const loader = <loadingIndicator_1.default style={{ margin: '70px auto' }}/>;
        return (<panelTable_1.default isEmpty={!hasResults} emptyMessage={(0, locale_1.t)('No transactions found')} headers={this.renderHeader()} isLoading={isLoading} disablePadding loader={loader}>
        {this.renderResults()}
      </panelTable_1.default>);
    }
}
const HeadCellContainer = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
`;
const BodyCellContainer = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  ${overflowEllipsis_1.default};
`;
const StyledIconQuestion = (0, styled_1.default)(questionTooltip_1.default) `
  position: relative;
  top: 1px;
  left: 4px;
`;
exports.default = TransactionsTable;
//# sourceMappingURL=transactionsTable.jsx.map