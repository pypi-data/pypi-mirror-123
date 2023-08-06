Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const parser_1 = require("app/components/arithmeticInput/parser");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const styles_1 = require("app/components/charts/styles");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const fields_1 = require("app/utils/discover/fields");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const touch_1 = require("app/utils/touch");
const userselect_1 = require("app/utils/userselect");
const queryField_1 = require("./queryField");
const types_1 = require("./types");
const DRAG_CLASS = 'draggable-item';
const GHOST_PADDING = 4;
const MAX_COL_COUNT = 20;
var PlaceholderPosition;
(function (PlaceholderPosition) {
    PlaceholderPosition[PlaceholderPosition["TOP"] = 0] = "TOP";
    PlaceholderPosition[PlaceholderPosition["BOTTOM"] = 1] = "BOTTOM";
})(PlaceholderPosition || (PlaceholderPosition = {}));
class ColumnEditCollection extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isDragging: false,
            draggingIndex: void 0,
            draggingTargetIndex: void 0,
            draggingGrabbedOffset: void 0,
            error: new Map(),
            left: void 0,
            top: void 0,
        };
        this.previousUserSelect = null;
        this.portal = null;
        this.dragGhostRef = React.createRef();
        // Signal to the parent that a new column has been added.
        this.handleAddColumn = () => {
            const newColumn = { kind: 'field', field: '' };
            this.props.onChange([...this.props.columns, newColumn]);
        };
        this.handleAddEquation = () => {
            const { organization } = this.props;
            const newColumn = { kind: types_1.FieldValueKind.EQUATION, field: '' };
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.add_equation',
                eventName: 'Discoverv2: Equation added',
                organization_id: parseInt(organization.id, 10),
            });
            this.props.onChange([...this.props.columns, newColumn]);
        };
        this.handleUpdateColumn = (index, updatedColumn) => {
            const newColumns = [...this.props.columns];
            if (updatedColumn.kind === 'equation') {
                this.setState(prevState => {
                    const error = new Map(prevState.error);
                    error.set(index, (0, parser_1.parseArithmetic)(updatedColumn.field).error);
                    return Object.assign(Object.assign({}, prevState), { error });
                });
            }
            else {
                // Update any equations that contain the existing column
                this.updateEquationFields(newColumns, index, updatedColumn);
            }
            newColumns.splice(index, 1, updatedColumn);
            this.props.onChange(newColumns);
        };
        this.updateEquationFields = (newColumns, index, updatedColumn) => {
            const oldColumn = newColumns[index];
            const existingColumn = (0, fields_1.generateFieldAsString)(newColumns[index]);
            const updatedColumnString = (0, fields_1.generateFieldAsString)(updatedColumn);
            if (!(0, fields_1.isLegalEquationColumn)(updatedColumn) || (0, fields_1.hasDuplicate)(newColumns, oldColumn)) {
                return;
            }
            // Find the equations in the list of columns
            for (let i = 0; i < newColumns.length; i++) {
                const newColumn = newColumns[i];
                if (newColumn.kind === 'equation') {
                    const result = (0, parser_1.parseArithmetic)(newColumn.field);
                    let newEquation = '';
                    // Track where to continue from, not reconstructing from result so we don't have to worry
                    // about spacing
                    let lastIndex = 0;
                    // the parser separates fields & functions, so we only need to check one
                    const fields = oldColumn.kind === 'function' ? result.tc.functions : result.tc.fields;
                    // for each field, add the text before it, then the new function and update index
                    // to be where we want to start again
                    for (const field of fields) {
                        if (field.term === existingColumn && lastIndex !== field.location.end.offset) {
                            newEquation +=
                                newColumn.field.substring(lastIndex, field.location.start.offset) +
                                    updatedColumnString;
                            lastIndex = field.location.end.offset;
                        }
                    }
                    // Add whatever remains to be added from the equation, if existing field wasn't found
                    // add the entire equation
                    newEquation += newColumn.field.substring(lastIndex);
                    newColumns[i] = {
                        kind: 'equation',
                        field: newEquation,
                    };
                }
            }
        };
        this.onDragMove = (event) => {
            var _a, _b;
            const { isDragging, draggingTargetIndex, draggingGrabbedOffset } = this.state;
            if (!isDragging || !['mousemove', 'touchmove'].includes(event.type)) {
                return;
            }
            event.preventDefault();
            event.stopPropagation();
            const pointerX = (0, touch_1.getPointerPosition)(event, 'pageX');
            const pointerY = (0, touch_1.getPointerPosition)(event, 'pageY');
            const dragOffsetX = (_a = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.x) !== null && _a !== void 0 ? _a : 0;
            const dragOffsetY = (_b = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.y) !== null && _b !== void 0 ? _b : 0;
            if (this.dragGhostRef.current) {
                // move the ghost box
                const ghostDOM = this.dragGhostRef.current;
                // Adjust so cursor is over the grab handle.
                ghostDOM.style.left = `${pointerX - dragOffsetX}px`;
                ghostDOM.style.top = `${pointerY - dragOffsetY}px`;
            }
            const dragItems = document.querySelectorAll(`.${DRAG_CLASS}`);
            // Find the item that the ghost is currently over.
            const targetIndex = Array.from(dragItems).findIndex(dragItem => {
                const rects = dragItem.getBoundingClientRect();
                const top = pointerY;
                const thresholdStart = window.scrollY + rects.top;
                const thresholdEnd = window.scrollY + rects.top + rects.height;
                return top >= thresholdStart && top <= thresholdEnd;
            });
            if (targetIndex >= 0 && targetIndex !== draggingTargetIndex) {
                this.setState({ draggingTargetIndex: targetIndex });
            }
        };
        this.onDragEnd = (event) => {
            if (!this.state.isDragging || !['mouseup', 'touchend'].includes(event.type)) {
                return;
            }
            const sourceIndex = this.state.draggingIndex;
            const targetIndex = this.state.draggingTargetIndex;
            if (typeof sourceIndex !== 'number' || typeof targetIndex !== 'number') {
                return;
            }
            // remove listeners that were attached in startColumnDrag
            this.cleanUpListeners();
            // restore body user-select values
            if (this.previousUserSelect) {
                (0, userselect_1.setBodyUserSelect)(this.previousUserSelect);
                this.previousUserSelect = null;
            }
            // Reorder columns and trigger change.
            const newColumns = [...this.props.columns];
            const removed = newColumns.splice(sourceIndex, 1);
            newColumns.splice(targetIndex, 0, removed[0]);
            this.checkColumnErrors(newColumns);
            this.props.onChange(newColumns);
            this.setState({
                isDragging: false,
                left: undefined,
                top: undefined,
                draggingIndex: undefined,
                draggingTargetIndex: undefined,
                draggingGrabbedOffset: undefined,
            });
        };
    }
    componentDidMount() {
        if (!this.portal) {
            const portal = document.createElement('div');
            portal.style.position = 'absolute';
            portal.style.top = '0';
            portal.style.left = '0';
            portal.style.zIndex = String(theme_1.default.zIndex.modal);
            this.portal = portal;
            document.body.appendChild(this.portal);
        }
        this.checkColumnErrors(this.props.columns);
    }
    componentWillUnmount() {
        if (this.portal) {
            document.body.removeChild(this.portal);
        }
        this.cleanUpListeners();
    }
    checkColumnErrors(columns) {
        const error = new Map();
        for (let i = 0; i < columns.length; i += 1) {
            const column = columns[i];
            if (column.kind === 'equation') {
                const result = (0, parser_1.parseArithmetic)(column.field);
                if (result.error) {
                    error.set(i, result.error);
                }
            }
        }
        this.setState({ error });
    }
    keyForColumn(column, isGhost) {
        if (column.kind === 'function') {
            return [...column.function, isGhost].join(':');
        }
        return [...column.field, isGhost].join(':');
    }
    cleanUpListeners() {
        if (this.state.isDragging) {
            window.removeEventListener('mousemove', this.onDragMove);
            window.removeEventListener('touchmove', this.onDragMove);
            window.removeEventListener('mouseup', this.onDragEnd);
            window.removeEventListener('touchend', this.onDragEnd);
        }
    }
    removeColumn(index) {
        const newColumns = [...this.props.columns];
        newColumns.splice(index, 1);
        this.checkColumnErrors(newColumns);
        this.props.onChange(newColumns);
    }
    startDrag(event, index) {
        const isDragging = this.state.isDragging;
        if (isDragging || !['mousedown', 'touchstart'].includes(event.type)) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        const top = (0, touch_1.getPointerPosition)(event, 'pageY');
        const left = (0, touch_1.getPointerPosition)(event, 'pageX');
        // Compute where the user clicked on the drag handle. Avoids the element
        // jumping from the cursor on mousedown.
        const { x, y } = Array.from(document.querySelectorAll(`.${DRAG_CLASS}`))
            .find(n => n.contains(event.currentTarget))
            .getBoundingClientRect();
        const draggingGrabbedOffset = {
            x: left - x + GHOST_PADDING,
            y: top - y + GHOST_PADDING,
        };
        // prevent the user from selecting things when dragging a column.
        this.previousUserSelect = (0, userselect_1.setBodyUserSelect)({
            userSelect: 'none',
            MozUserSelect: 'none',
            msUserSelect: 'none',
            webkitUserSelect: 'none',
        });
        // attach event listeners so that the mouse cursor can drag anywhere
        window.addEventListener('mousemove', this.onDragMove);
        window.addEventListener('touchmove', this.onDragMove);
        window.addEventListener('mouseup', this.onDragEnd);
        window.addEventListener('touchend', this.onDragEnd);
        this.setState({
            isDragging: true,
            draggingIndex: index,
            draggingTargetIndex: index,
            draggingGrabbedOffset,
            top,
            left,
        });
    }
    renderGhost(gridColumns) {
        var _a, _b;
        const { isDragging, draggingIndex, draggingGrabbedOffset } = this.state;
        const index = draggingIndex;
        if (typeof index !== 'number' || !isDragging || !this.portal) {
            return null;
        }
        const dragOffsetX = (_a = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.x) !== null && _a !== void 0 ? _a : 0;
        const dragOffsetY = (_b = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.y) !== null && _b !== void 0 ? _b : 0;
        const top = Number(this.state.top) - dragOffsetY;
        const left = Number(this.state.left) - dragOffsetX;
        const col = this.props.columns[index];
        const style = {
            top: `${top}px`,
            left: `${left}px`,
        };
        const ghost = (<Ghost ref={this.dragGhostRef} style={style}>
        {this.renderItem(col, index, { isGhost: true, gridColumns })}
      </Ghost>);
        return react_dom_1.default.createPortal(ghost, this.portal);
    }
    renderItem(col, i, { canDelete = true, canDrag = true, isGhost = false, gridColumns = 2, }) {
        const { columns, fieldOptions } = this.props;
        const { isDragging, draggingTargetIndex, draggingIndex } = this.state;
        let placeholder = null;
        // Add a placeholder above the target row.
        if (isDragging && isGhost === false && draggingTargetIndex === i) {
            placeholder = (<DragPlaceholder key={`placeholder:${this.keyForColumn(col, isGhost)}`} className={DRAG_CLASS}/>);
        }
        // If the current row is the row in the drag ghost return the placeholder
        // or a hole if the placeholder is elsewhere.
        if (isDragging && isGhost === false && draggingIndex === i) {
            return placeholder;
        }
        const position = Number(draggingTargetIndex) <= Number(draggingIndex)
            ? PlaceholderPosition.TOP
            : PlaceholderPosition.BOTTOM;
        return (<React.Fragment key={`${i}:${this.keyForColumn(col, isGhost)}`}>
        {position === PlaceholderPosition.TOP && placeholder}
        <RowContainer className={isGhost ? '' : DRAG_CLASS}>
          {canDrag ? (<button_1.default aria-label={(0, locale_1.t)('Drag to reorder')} onMouseDown={event => this.startDrag(event, i)} onTouchStart={event => this.startDrag(event, i)} icon={<icons_1.IconGrabbable size="xs"/>} size="zero" borderless/>) : (<span />)}
          <queryField_1.QueryField fieldOptions={fieldOptions} gridColumns={gridColumns} fieldValue={col} onChange={value => this.handleUpdateColumn(i, value)} error={this.state.error.get(i)} takeFocus={i === this.props.columns.length - 1} otherColumns={columns}/>
          {canDelete || col.kind === 'equation' ? (<button_1.default aria-label={(0, locale_1.t)('Remove column')} onClick={() => this.removeColumn(i)} icon={<icons_1.IconDelete />} borderless/>) : (<span />)}
        </RowContainer>
        {position === PlaceholderPosition.BOTTOM && placeholder}
      </React.Fragment>);
    }
    render() {
        const { className, columns } = this.props;
        const canDelete = columns.filter(field => field.kind !== 'equation').length > 1;
        const canDrag = columns.length > 1;
        const canAdd = columns.length < MAX_COL_COUNT;
        const title = canAdd
            ? undefined
            : `Sorry, you reached the maximum number of columns. Delete columns to add more.`;
        // Get the longest number of columns so we can layout the rows.
        // We always want at least 2 columns.
        const gridColumns = Math.max(...columns.map(col => col.kind === 'function' && fields_1.AGGREGATIONS[col.function[0]].parameters.length === 2
            ? 3
            : 2));
        return (<div className={className}>
        {this.renderGhost(gridColumns)}
        <RowContainer>
          <Heading gridColumns={gridColumns}>
            <StyledSectionHeading>{(0, locale_1.t)('Tag / Field / Function')}</StyledSectionHeading>
            <StyledSectionHeading>{(0, locale_1.t)('Field Parameter')}</StyledSectionHeading>
          </Heading>
        </RowContainer>
        {columns.map((col, i) => this.renderItem(col, i, { canDelete, canDrag, gridColumns }))}
        <RowContainer>
          <Actions>
            <button_1.default size="small" label={(0, locale_1.t)('Add a Column')} onClick={this.handleAddColumn} title={title} disabled={!canAdd} icon={<icons_1.IconAdd isCircled size="xs"/>}>
              {(0, locale_1.t)('Add a Column')}
            </button_1.default>
            <button_1.default size="small" label={(0, locale_1.t)('Add an Equation')} onClick={this.handleAddEquation} title={title} disabled={!canAdd} icon={<icons_1.IconAdd isCircled size="xs"/>}>
              {(0, locale_1.t)('Add an Equation')}
            </button_1.default>
          </Actions>
        </RowContainer>
      </div>);
    }
}
const RowContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: ${(0, space_1.default)(3)} 1fr ${(0, space_1.default)(3)};
  justify-content: center;
  align-items: center;
  width: 100%;
  touch-action: none;
  padding-bottom: ${(0, space_1.default)(1)};
`;
const Ghost = (0, styled_1.default)('div') `
  background: ${p => p.theme.background};
  display: block;
  position: absolute;
  padding: ${GHOST_PADDING}px;
  border-radius: ${p => p.theme.borderRadius};
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.15);
  width: 710px;
  opacity: 0.8;
  cursor: grabbing;
  padding-right: ${(0, space_1.default)(2)};

  & > ${RowContainer} {
    padding-bottom: 0;
  }

  & svg {
    cursor: grabbing;
  }
`;
const DragPlaceholder = (0, styled_1.default)('div') `
  margin: 0 ${(0, space_1.default)(3)} ${(0, space_1.default)(1)} ${(0, space_1.default)(3)};
  border: 2px dashed ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius};
  height: 41px;
`;
const Actions = (0, styled_1.default)('div') `
  grid-column: 2 / 3;

  & button {
    margin-right: ${(0, space_1.default)(1)};
  }
`;
const Heading = (0, styled_1.default)('div') `
  grid-column: 2 / 3;

  /* Emulate the grid used in the column editor rows */
  display: grid;
  grid-template-columns: repeat(${p => p.gridColumns}, 1fr);
  grid-column-gap: ${(0, space_1.default)(1)};
`;
const StyledSectionHeading = (0, styled_1.default)(styles_1.SectionHeading) `
  margin: 0;
`;
exports.default = ColumnEditCollection;
//# sourceMappingURL=columnEditCollection.jsx.map