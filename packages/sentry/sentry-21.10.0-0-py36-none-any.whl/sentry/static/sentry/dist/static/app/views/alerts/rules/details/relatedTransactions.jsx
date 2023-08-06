Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const gridEditable_1 = (0, tslib_1.__importStar)(require("app/components/gridEditable"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
const fields_1 = require("app/utils/discover/fields");
const utils_1 = require("app/views/performance/transactionSummary/utils");
const COLUMN_TITLES = ['slowest transactions', 'project', 'p95', 'users', 'user misery'];
function getProjectID(eventData, projects) {
    const projectSlug = (eventData === null || eventData === void 0 ? void 0 : eventData.project) || undefined;
    if (typeof projectSlug === undefined) {
        return undefined;
    }
    const project = projects.find(currentProject => currentProject.slug === projectSlug);
    if (!project) {
        return undefined;
    }
    return project.id;
}
class Table extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            widths: [],
        };
        this.renderBodyCellWithData = (tableData) => {
            return (column, dataRow) => this.renderBodyCell(tableData, column, dataRow);
        };
        this.renderHeadCellWithMeta = (tableMeta) => {
            return (column, index) => this.renderHeadCell(tableMeta, column, COLUMN_TITLES[index]);
        };
        this.handleResizeColumn = (columnIndex, nextColumn) => {
            const widths = [...this.state.widths];
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : gridEditable_1.COL_WIDTH_UNDEFINED;
            this.setState({ widths });
        };
    }
    renderBodyCell(tableData, column, dataRow) {
        const { eventView, organization, projects, location, summaryConditions } = this.props;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        const tableMeta = tableData.meta;
        const field = String(column.key);
        const fieldRenderer = (0, fieldRenderers_1.getFieldRenderer)(field, tableMeta);
        const rendered = fieldRenderer(dataRow, { organization, location });
        if (field === 'transaction') {
            const projectID = getProjectID(dataRow, projects);
            const summaryView = eventView.clone();
            summaryView.query = summaryConditions;
            const target = (0, utils_1.transactionSummaryRouteWithQuery)({
                orgSlug: organization.slug,
                transaction: String(dataRow.transaction) || '',
                query: summaryView.generateQueryStringObject(),
                projectID,
            });
            return <link_1.default to={target}>{rendered}</link_1.default>;
        }
        return rendered;
    }
    renderHeadCell(tableMeta, column, title) {
        const align = (0, fields_1.fieldAlignment)(column.name, column.type, tableMeta);
        const field = { field: column.name, width: column.width };
        return <HeaderCell align={align}>{title || field.field}</HeaderCell>;
    }
    getSortedEventView() {
        const { eventView } = this.props;
        return eventView.withSorts([...eventView.sorts]);
    }
    render() {
        const { eventView, organization, location } = this.props;
        const { widths } = this.state;
        const columnOrder = eventView
            .getColumns()
            .map((col, i) => {
            if (typeof widths[i] === 'number') {
                return Object.assign(Object.assign({}, col), { width: widths[i] });
            }
            return col;
        });
        const sortedEventView = this.getSortedEventView();
        const columnSortBy = sortedEventView.getSorts();
        return (<React.Fragment>
        <discoverQuery_1.default eventView={sortedEventView} orgSlug={organization.slug} location={location}>
          {({ isLoading, tableData }) => (<gridEditable_1.default isLoading={isLoading} data={tableData ? tableData.data.slice(0, 5) : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                    onResizeColumn: this.handleResizeColumn,
                    renderHeadCell: this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                    renderBodyCell: this.renderBodyCellWithData(tableData),
                }} location={location}/>)}
        </discoverQuery_1.default>
      </React.Fragment>);
    }
}
class RelatedTransactions extends React.Component {
    render() {
        const { rule, projects, filter, location, organization, start, end } = this.props;
        const eventQuery = {
            id: undefined,
            name: 'Slowest Transactions',
            fields: [
                'transaction',
                'project',
                'p95()',
                'count_unique(user)',
                `user_misery(${organization.apdexThreshold})`,
            ],
            orderby: `user_misery(${organization.apdexThreshold})`,
            query: `${rule.query}`,
            version: 2,
            projects: projects.map(project => Number(project.id)),
            start,
            end,
        };
        const eventView = eventView_1.default.fromSavedQuery(eventQuery);
        return (<Table eventView={eventView} projects={projects} organization={organization} location={location} summaryConditions={`${rule.query} ${filter}`}/>);
    }
}
exports.default = RelatedTransactions;
const HeaderCell = (0, styled_1.default)('div') `
  display: block;
  width: 100%;
  white-space: nowrap;
  ${(p) => (p.align ? `text-align: ${p.align};` : '')}
`;
//# sourceMappingURL=relatedTransactions.jsx.map