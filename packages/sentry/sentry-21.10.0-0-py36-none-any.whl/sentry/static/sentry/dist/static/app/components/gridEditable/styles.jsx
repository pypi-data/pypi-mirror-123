Object.defineProperty(exports, "__esModule", { value: true });
exports.GridResizer = exports.GridBodyCellStatus = exports.GridBodyCell = exports.GridBody = exports.GridHeadCellStatic = exports.GridHeadCell = exports.GridHead = exports.GridRow = exports.Grid = exports.Body = exports.HeaderButtonContainer = exports.HeaderTitle = exports.Header = exports.GRID_STATUS_MESSAGE_HEIGHT = exports.GRID_BODY_ROW_HEIGHT = exports.GRID_HEAD_ROW_HEIGHT = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.GRID_HEAD_ROW_HEIGHT = 45;
exports.GRID_BODY_ROW_HEIGHT = 40;
exports.GRID_STATUS_MESSAGE_HEIGHT = exports.GRID_BODY_ROW_HEIGHT * 4;
/**
 * Local z-index stacking context
 * https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Positioning/Understanding_z_index/The_stacking_context
 */
// Parent context is Panel
const Z_INDEX_PANEL = 1;
const Z_INDEX_GRID_STATUS = -1;
const Z_INDEX_GRID = 5;
// Parent context is GridHeadCell
const Z_INDEX_GRID_RESIZER = 1;
exports.Header = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(1)};
`;
exports.HeaderTitle = (0, styled_1.default)('h4') `
  margin: 0;
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.subText};
`;
exports.HeaderButtonContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-auto-flow: column;
  grid-auto-columns: auto;
  justify-items: end;

  /* Hovercard anchor element when features are disabled. */
  & > span {
    display: flex;
    flex-direction: row;
  }
`;
const PanelWithProtectedBorder = (0, styled_1.default)(panels_1.Panel) `
  overflow: hidden;
  z-index: ${Z_INDEX_PANEL};
`;
const Body = props => (<PanelWithProtectedBorder>
    <panels_1.PanelBody>{props.children}</panels_1.PanelBody>
  </PanelWithProtectedBorder>);
exports.Body = Body;
/**
 * Grid is the parent element for the tableResizable component.
 *
 * On newer browsers, it will use CSS Grids to implement its layout.
 *
 * However, it is based on <table>, which has a distinction between header/body
 * HTML elements, which allows CSS selectors to its full potential. This has
 * the added advantage that older browsers will still have a chance of
 * displaying the data correctly (but this is untested).
 *
 * <thead>, <tbody>, <tr> are ignored by CSS Grid.
 * The entire layout is determined by the usage of <th> and <td>.
 */
exports.Grid = (0, styled_1.default)('table') `
  position: inherit;
  display: grid;

  /* Overwritten by GridEditable.setGridTemplateColumns */
  grid-template-columns: repeat(auto-fill, minmax(50px, auto));

  box-sizing: border-box;
  border-collapse: collapse;
  margin: 0;

  z-index: ${Z_INDEX_GRID};
  overflow-x: auto;
`;
exports.GridRow = (0, styled_1.default)('tr') `
  display: contents;

  &:last-child,
  &:last-child > td:first-child,
  &:last-child > td:last-child {
    border-bottom-left-radius: ${p => p.theme.borderRadius};
    border-bottom-right-radius: ${p => p.theme.borderRadius};
  }
`;
/**
 * GridHead is the collection of elements that builds the header section of the
 * Grid. As the entirety of the add/remove/resize actions are performed on the
 * header, most of the elements behave different for each stage.
 */
exports.GridHead = (0, styled_1.default)('thead') `
  display: contents;
`;
exports.GridHeadCell = (0, styled_1.default)('th') `
  /* By default, a grid item cannot be smaller than the size of its content.
     We override this by setting min-width to be 0. */
  position: relative; /* Used by GridResizer */
  height: ${exports.GRID_HEAD_ROW_HEIGHT}px;
  display: flex;
  align-items: center;
  min-width: 24px;
  padding: 0 ${(0, space_1.default)(2)};

  border-right: 1px solid transparent;
  border-left: 1px solid transparent;
  background-color: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.subText};

  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 600;
  text-transform: uppercase;
  user-select: none;

  a,
  div,
  span {
    line-height: 1.1;
    color: inherit;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  &:first-child {
    border-top-left-radius: ${p => p.theme.borderRadius};
  }

  &:last-child {
    border-top-right-radius: ${p => p.theme.borderRadius};
    border-right: none;
  }

  &:hover {
    border-left-color: ${p => (p.isFirst ? 'transparent' : p.theme.border)};
    border-right-color: ${p => p.theme.border};
  }
`;
/**
 * Create spacing/padding similar to GridHeadCellWrapper but
 * without interactive aspects.
 */
exports.GridHeadCellStatic = (0, styled_1.default)('th') `
  height: ${exports.GRID_HEAD_ROW_HEIGHT}px;
  display: flex;
  align-items: center;
  padding: 0 ${(0, space_1.default)(2)};
  background-color: ${p => p.theme.backgroundSecondary};
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 600;
  line-height: 1;
  text-transform: uppercase;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;

  &:first-child {
    border-top-left-radius: ${p => p.theme.borderRadius};
    padding: ${(0, space_1.default)(1)} 0 ${(0, space_1.default)(1)} ${(0, space_1.default)(3)};
  }
`;
/**
 * GridBody are the collection of elements that contains and display the data
 * of the Grid. They are rather simple.
 */
exports.GridBody = (0, styled_1.default)('tbody') `
  display: contents;

  > tr:first-child td {
    border-top: 1px solid ${p => p.theme.border};
  }
`;
exports.GridBodyCell = (0, styled_1.default)('td') `
  /* By default, a grid item cannot be smaller than the size of its content.
     We override this by setting min-width to be 0. */
  min-width: 0;
  /* Locking in the height makes calculation for resizer to be easier.
     min-height is used to allow a cell to expand and this is used to display
     feedback during empty/error state */
  min-height: ${exports.GRID_BODY_ROW_HEIGHT}px;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};

  background-color: ${p => p.theme.background};
  border-top: 1px solid ${p => p.theme.innerBorder};

  font-size: ${p => p.theme.fontSizeMedium};

  &:first-child {
    padding: ${(0, space_1.default)(1)} 0 ${(0, space_1.default)(1)} ${(0, space_1.default)(3)};
  }

  &:last-child {
    border-right: none;
  }
`;
const GridStatusWrapper = (0, styled_1.default)(exports.GridBodyCell) `
  grid-column: 1 / -1;
  width: 100%;
  height: ${exports.GRID_STATUS_MESSAGE_HEIGHT}px;
  background-color: transparent;
`;
const GridStatusFloat = (0, styled_1.default)('div') `
  position: absolute;
  top: 45px;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: ${exports.GRID_STATUS_MESSAGE_HEIGHT}px;

  z-index: ${Z_INDEX_GRID_STATUS};
  background: ${p => p.theme.background};
`;
const GridBodyCellStatus = props => (<GridStatusWrapper>
    <GridStatusFloat>{props.children}</GridStatusFloat>
  </GridStatusWrapper>);
exports.GridBodyCellStatus = GridBodyCellStatus;
/**
 * We have a fat GridResizer and we use the ::after pseudo-element to draw
 * a thin 1px border.
 *
 * The right most cell does not have a resizer as resizing from that side does strange things.
 */
exports.GridResizer = (0, styled_1.default)('div') `
  position: absolute;
  top: 0px;
  right: -6px;
  width: 11px;

  height: ${p => {
    const numOfRows = p.dataRows;
    let height = exports.GRID_HEAD_ROW_HEIGHT + numOfRows * exports.GRID_BODY_ROW_HEIGHT;
    if (numOfRows >= 2) {
        // account for border-bottom height
        height += numOfRows - 1;
    }
    return height;
}}px;

  padding-left: 5px;
  padding-right: 5px;

  cursor: col-resize;
  z-index: ${Z_INDEX_GRID_RESIZER};

  /**
   * This element allows us to have a fat GridResizer that is easy to hover and
   * drag, but still draws an appealing thin line for the border
   */
  &::after {
    content: ' ';
    display: block;
    width: 100%; /* Equivalent to 1px */
    height: 100%;
  }

  &:hover::after {
    background-color: ${p => p.theme.gray200};
  }

  /**
   * Ensure that this rule is after :hover, otherwise it will flicker when
   * the GridResizer is dragged
   */
  &:active::after,
  &:focus::after {
    background-color: ${p => p.theme.purple300};
  }

  /**
   * This element gives the resize handle a more visible knob to grab
   */
  &:hover::before {
    position: absolute;
    top: 0;
    left: 2px;
    content: ' ';
    display: block;
    width: 7px;
    height: ${exports.GRID_HEAD_ROW_HEIGHT}px;
    background-color: ${p => p.theme.purple300};
    opacity: 0.4;
  }
`;
//# sourceMappingURL=styles.jsx.map