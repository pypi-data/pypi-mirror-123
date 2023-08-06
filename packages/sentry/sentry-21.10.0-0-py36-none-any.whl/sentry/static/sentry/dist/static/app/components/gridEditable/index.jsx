Object.defineProperty(exports, "__esModule", { value: true });
exports.COL_WIDTH_MINIMUM = exports.COL_WIDTH_UNDEFINED = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const styles_1 = require("./styles");
// Auto layout width.
exports.COL_WIDTH_UNDEFINED = -1;
// Set to 90 as the edit/trash icons need this much space.
exports.COL_WIDTH_MINIMUM = 90;
class GridEditable extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            numColumn: 0,
        };
        this.refGrid = React.createRef();
        this.resizeWindowLifecycleEvents = {
            mousemove: [],
            mouseup: [],
        };
        this.onResetColumnSize = (e, i) => {
            e.stopPropagation();
            const nextColumnOrder = [...this.props.columnOrder];
            nextColumnOrder[i] = Object.assign(Object.assign({}, nextColumnOrder[i]), { width: exports.COL_WIDTH_UNDEFINED });
            this.setGridTemplateColumns(nextColumnOrder);
            const onResizeColumn = this.props.grid.onResizeColumn;
            if (onResizeColumn) {
                onResizeColumn(i, Object.assign(Object.assign({}, nextColumnOrder[i]), { width: exports.COL_WIDTH_UNDEFINED }));
            }
        };
        this.onResizeMouseDown = (e, i = -1) => {
            e.stopPropagation();
            // Block right-click and other funky stuff
            if (i === -1 || e.type === 'contextmenu') {
                return;
            }
            // <GridResizer> is nested 1 level down from <GridHeadCell>
            const cell = e.currentTarget.parentElement;
            if (!cell) {
                return;
            }
            // HACK: Do not put into state to prevent re-rendering of component
            this.resizeMetadata = {
                columnIndex: i,
                columnWidth: cell.offsetWidth,
                cursorX: e.clientX,
            };
            window.addEventListener('mousemove', this.onResizeMouseMove);
            this.resizeWindowLifecycleEvents.mousemove.push(this.onResizeMouseMove);
            window.addEventListener('mouseup', this.onResizeMouseUp);
            this.resizeWindowLifecycleEvents.mouseup.push(this.onResizeMouseUp);
        };
        this.onResizeMouseUp = (e) => {
            const metadata = this.resizeMetadata;
            const onResizeColumn = this.props.grid.onResizeColumn;
            if (!metadata || !onResizeColumn) {
                return;
            }
            const { columnOrder } = this.props;
            const widthChange = e.clientX - metadata.cursorX;
            onResizeColumn(metadata.columnIndex, Object.assign(Object.assign({}, columnOrder[metadata.columnIndex]), { width: metadata.columnWidth + widthChange }));
            this.resizeMetadata = undefined;
            this.clearWindowLifecycleEvents();
        };
        this.onResizeMouseMove = (e) => {
            const { resizeMetadata } = this;
            if (!resizeMetadata) {
                return;
            }
            window.requestAnimationFrame(() => this.resizeGridColumn(e, resizeMetadata));
        };
        /**
         * Recalculate the dimensions of Grid and Columns and redraws them
         */
        this.redrawGridColumn = () => {
            this.setGridTemplateColumns(this.props.columnOrder);
        };
        this.renderGridBodyRow = (dataRow, row) => {
            const { columnOrder, grid } = this.props;
            const prependColumns = grid.renderPrependColumns
                ? grid.renderPrependColumns(false, dataRow, row)
                : [];
            return (<styles_1.GridRow key={row}>
        {prependColumns &&
                    prependColumns.map((item, i) => (<styles_1.GridBodyCell key={`prepend-${i}`}>{item}</styles_1.GridBodyCell>))}
        {columnOrder.map((col, i) => (<styles_1.GridBodyCell key={`${col.key}${i}`}>
            {grid.renderBodyCell
                        ? grid.renderBodyCell(col, dataRow, row, i)
                        : dataRow[col.key]}
          </styles_1.GridBodyCell>))}
      </styles_1.GridRow>);
        };
    }
    // Static methods do not allow the use of generics bounded to the parent class
    // For more info: https://github.com/microsoft/TypeScript/issues/14600
    static getDerivedStateFromProps(props, prevState) {
        return Object.assign(Object.assign({}, prevState), { numColumn: props.columnOrder.length });
    }
    componentDidMount() {
        window.addEventListener('resize', this.redrawGridColumn);
        this.setGridTemplateColumns(this.props.columnOrder);
    }
    componentDidUpdate() {
        // Redraw columns whenever new props are received
        this.setGridTemplateColumns(this.props.columnOrder);
    }
    componentWillUnmount() {
        this.clearWindowLifecycleEvents();
        window.removeEventListener('resize', this.redrawGridColumn);
    }
    clearWindowLifecycleEvents() {
        Object.keys(this.resizeWindowLifecycleEvents).forEach(e => {
            this.resizeWindowLifecycleEvents[e].forEach(c => window.removeEventListener(e, c));
            this.resizeWindowLifecycleEvents[e] = [];
        });
    }
    resizeGridColumn(e, metadata) {
        const grid = this.refGrid.current;
        if (!grid) {
            return;
        }
        const widthChange = e.clientX - metadata.cursorX;
        const nextColumnOrder = [...this.props.columnOrder];
        nextColumnOrder[metadata.columnIndex] = Object.assign(Object.assign({}, nextColumnOrder[metadata.columnIndex]), { width: Math.max(metadata.columnWidth + widthChange, 0) });
        this.setGridTemplateColumns(nextColumnOrder);
    }
    /**
     * Set the CSS for Grid Column
     */
    setGridTemplateColumns(columnOrder) {
        const grid = this.refGrid.current;
        if (!grid) {
            return;
        }
        const prependColumns = this.props.grid.prependColumnWidths || [];
        const prepend = prependColumns.join(' ');
        const widths = columnOrder.map((item, index) => {
            if (item.width === exports.COL_WIDTH_UNDEFINED) {
                return `minmax(${exports.COL_WIDTH_MINIMUM}px, auto)`;
            }
            else if (typeof item.width === 'number' && item.width > exports.COL_WIDTH_MINIMUM) {
                if (index === columnOrder.length - 1) {
                    return `minmax(${item.width}px, auto)`;
                }
                return `${item.width}px`;
            }
            if (index === columnOrder.length - 1) {
                return `minmax(${exports.COL_WIDTH_MINIMUM}px, auto)`;
            }
            return `${exports.COL_WIDTH_MINIMUM}px`;
        });
        // The last column has no resizer and should always be a flexible column
        // to prevent underflows.
        grid.style.gridTemplateColumns = `${prepend} ${widths.join(' ')}`;
    }
    renderGridHead() {
        const { error, isLoading, columnOrder, grid, data } = this.props;
        // Ensure that the last column cannot be removed
        const numColumn = columnOrder.length;
        const prependColumns = grid.renderPrependColumns
            ? grid.renderPrependColumns(true)
            : [];
        return (<styles_1.GridRow>
        {prependColumns &&
                prependColumns.map((item, i) => (<styles_1.GridHeadCellStatic key={`prepend-${i}`}>{item}</styles_1.GridHeadCellStatic>))}
        {
            /* Note that this.onResizeMouseDown assumes GridResizer is nested
              1 levels under GridHeadCell */
            columnOrder.map((column, i) => (<styles_1.GridHeadCell key={`${i}.${column.key}`} isFirst={i === 0}>
              {grid.renderHeadCell ? grid.renderHeadCell(column, i) : column.name}
              {i !== numColumn - 1 && (<styles_1.GridResizer dataRows={!error && !isLoading && data ? data.length : 0} onMouseDown={e => this.onResizeMouseDown(e, i)} onDoubleClick={e => this.onResetColumnSize(e, i)} onContextMenu={this.onResizeMouseDown}/>)}
            </styles_1.GridHeadCell>))}
      </styles_1.GridRow>);
    }
    renderGridBody() {
        const { data, error, isLoading } = this.props;
        if (error) {
            return this.renderError();
        }
        if (isLoading) {
            return this.renderLoading();
        }
        if (!data || data.length === 0) {
            return this.renderEmptyData();
        }
        return data.map(this.renderGridBodyRow);
    }
    renderError() {
        return (<styles_1.GridRow>
        <styles_1.GridBodyCellStatus>
          <icons_1.IconWarning color="gray300" size="lg"/>
        </styles_1.GridBodyCellStatus>
      </styles_1.GridRow>);
    }
    renderLoading() {
        return (<styles_1.GridRow>
        <styles_1.GridBodyCellStatus>
          <loadingIndicator_1.default />
        </styles_1.GridBodyCellStatus>
      </styles_1.GridRow>);
    }
    renderEmptyData() {
        return (<styles_1.GridRow>
        <styles_1.GridBodyCellStatus>
          <emptyStateWarning_1.default>
            <p>{(0, locale_1.t)('No results found for your query')}</p>
          </emptyStateWarning_1.default>
        </styles_1.GridBodyCellStatus>
      </styles_1.GridRow>);
    }
    render() {
        const { title, headerButtons } = this.props;
        const showHeader = title || headerButtons;
        return (<React.Fragment>
        {showHeader && (<styles_1.Header>
            {title && <styles_1.HeaderTitle>{title}</styles_1.HeaderTitle>}
            {headerButtons && (<styles_1.HeaderButtonContainer>{headerButtons()}</styles_1.HeaderButtonContainer>)}
          </styles_1.Header>)}
        <styles_1.Body>
          <styles_1.Grid data-test-id="grid-editable" ref={this.refGrid}>
            <styles_1.GridHead>{this.renderGridHead()}</styles_1.GridHead>
            <styles_1.GridBody>{this.renderGridBody()}</styles_1.GridBody>
          </styles_1.Grid>
        </styles_1.Body>
      </React.Fragment>);
    }
}
exports.default = GridEditable;
//# sourceMappingURL=index.jsx.map