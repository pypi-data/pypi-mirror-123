Object.defineProperty(exports, "__esModule", { value: true });
exports.updateQuery = exports.Actions = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_popper_1 = require("react-popper");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const color_1 = (0, tslib_1.__importDefault)(require("color"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const fields_1 = require("app/utils/discover/fields");
const formatters_1 = require("app/utils/formatters");
var Actions;
(function (Actions) {
    Actions["ADD"] = "add";
    Actions["EXCLUDE"] = "exclude";
    Actions["SHOW_GREATER_THAN"] = "show_greater_than";
    Actions["SHOW_LESS_THAN"] = "show_less_than";
    Actions["TRANSACTION"] = "transaction";
    Actions["RELEASE"] = "release";
    Actions["DRILLDOWN"] = "drilldown";
    Actions["EDIT_THRESHOLD"] = "edit_threshold";
})(Actions = exports.Actions || (exports.Actions = {}));
function updateQuery(results, action, column, value) {
    const key = column.name;
    if (column.type === 'duration' && typeof value === 'number') {
        // values are assumed to be in milliseconds
        value = (0, formatters_1.getDuration)(value / 1000, 2, true);
    }
    // De-duplicate array values
    if (Array.isArray(value)) {
        value = [...new Set(value)];
        if (value.length === 1) {
            value = value[0];
        }
    }
    switch (action) {
        case Actions.ADD:
            // If the value is null/undefined create a has !has condition.
            if (value === null || value === undefined) {
                // Adding a null value is the same as excluding truthy values.
                // Remove inclusion if it exists.
                results.removeFilterValue('has', key);
                results.addFilterValues('!has', [key]);
            }
            else {
                // Remove exclusion if it exists.
                results.removeFilter(`!${key}`);
                if (Array.isArray(value)) {
                    // For array values, add to existing filters
                    const currentFilters = results.getFilterValues(key);
                    value = [...new Set([...currentFilters, ...value])];
                }
                else {
                    value = [String(value)];
                }
                results.setFilterValues(key, value);
            }
            break;
        case Actions.EXCLUDE:
            if (value === null || value === undefined) {
                // Excluding a null value is the same as including truthy values.
                // Remove exclusion if it exists.
                results.removeFilterValue('!has', key);
                results.addFilterValues('has', [key]);
            }
            else {
                // Remove positive if it exists.
                results.removeFilter(key);
                // Negations should stack up.
                const negation = `!${key}`;
                value = Array.isArray(value) ? value : [String(value)];
                const currentNegations = results.getFilterValues(negation);
                value = [...new Set([...currentNegations, ...value])];
                results.setFilterValues(negation, value);
            }
            break;
        case Actions.SHOW_GREATER_THAN: {
            // Remove query token if it already exists
            results.setFilterValues(key, [`>${value}`]);
            break;
        }
        case Actions.SHOW_LESS_THAN: {
            // Remove query token if it already exists
            results.setFilterValues(key, [`<${value}`]);
            break;
        }
        // these actions do not modify the query in any way,
        // instead they have side effects
        case Actions.TRANSACTION:
        case Actions.RELEASE:
        case Actions.DRILLDOWN:
            break;
        default:
            throw new Error(`Unknown action type. ${action}`);
    }
}
exports.updateQuery = updateQuery;
class CellAction extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isHovering: false,
            isOpen: false,
        };
        this.handleClickOutside = (event) => {
            if (!this.menuEl) {
                return;
            }
            if (!(event.target instanceof Element)) {
                return;
            }
            if (this.menuEl.contains(event.target)) {
                return;
            }
            this.setState({ isOpen: false, isHovering: false });
        };
        this.handleMouseEnter = () => {
            this.setState({ isHovering: true });
        };
        this.handleMouseLeave = () => {
            this.setState(state => {
                // Don't hide the button if the menu is open.
                if (state.isOpen) {
                    return state;
                }
                return Object.assign(Object.assign({}, state), { isHovering: false });
            });
        };
        this.handleMenuToggle = (event) => {
            event.preventDefault();
            this.setState({ isOpen: !this.state.isOpen });
        };
        let portal = document.getElementById('cell-action-portal');
        if (!portal) {
            portal = document.createElement('div');
            portal.setAttribute('id', 'cell-action-portal');
            document.body.appendChild(portal);
        }
        this.portalEl = portal;
        this.menuEl = null;
    }
    componentDidUpdate(_props, prevState) {
        if (this.state.isOpen && prevState.isOpen === false) {
            document.addEventListener('click', this.handleClickOutside, true);
        }
        if (this.state.isOpen === false && prevState.isOpen) {
            document.removeEventListener('click', this.handleClickOutside, true);
        }
    }
    componentWillUnmount() {
        document.removeEventListener('click', this.handleClickOutside, true);
    }
    renderMenuButtons() {
        const { dataRow, column, handleCellAction, allowActions } = this.props;
        // Do not render context menu buttons for the span op breakdown field.
        if ((0, fields_1.isRelativeSpanOperationBreakdownField)(column.name)) {
            return null;
        }
        // Do not render context menu buttons for the equation fields until we can query on them
        if ((0, fields_1.isEquationAlias)(column.name)) {
            return null;
        }
        const fieldAlias = (0, fields_1.getAggregateAlias)(column.name);
        let value = dataRow[fieldAlias];
        // error.handled is a strange field where null = true.
        if (Array.isArray(value) &&
            value[0] === null &&
            column.column.kind === 'field' &&
            column.column.field === 'error.handled') {
            value = 1;
        }
        const actions = [];
        function addMenuItem(action, menuItem) {
            if ((Array.isArray(allowActions) && allowActions.includes(action)) ||
                !allowActions) {
                actions.push(menuItem);
            }
        }
        if (!['duration', 'number', 'percentage'].includes(column.type) ||
            (value === null && column.column.kind === 'field')) {
            addMenuItem(Actions.ADD, <ActionItem key="add-to-filter" data-test-id="add-to-filter" onClick={() => handleCellAction(Actions.ADD, value)}>
          {(0, locale_1.t)('Add to filter')}
        </ActionItem>);
            if (column.type !== 'date') {
                addMenuItem(Actions.EXCLUDE, <ActionItem key="exclude-from-filter" data-test-id="exclude-from-filter" onClick={() => handleCellAction(Actions.EXCLUDE, value)}>
            {(0, locale_1.t)('Exclude from filter')}
          </ActionItem>);
            }
        }
        if (['date', 'duration', 'integer', 'number', 'percentage'].includes(column.type) &&
            value !== null) {
            addMenuItem(Actions.SHOW_GREATER_THAN, <ActionItem key="show-values-greater-than" data-test-id="show-values-greater-than" onClick={() => handleCellAction(Actions.SHOW_GREATER_THAN, value)}>
          {(0, locale_1.t)('Show values greater than')}
        </ActionItem>);
            addMenuItem(Actions.SHOW_LESS_THAN, <ActionItem key="show-values-less-than" data-test-id="show-values-less-than" onClick={() => handleCellAction(Actions.SHOW_LESS_THAN, value)}>
          {(0, locale_1.t)('Show values less than')}
        </ActionItem>);
        }
        if (column.column.kind === 'field' && column.column.field === 'transaction') {
            addMenuItem(Actions.TRANSACTION, <ActionItem key="transaction-summary" data-test-id="transaction-summary" onClick={() => handleCellAction(Actions.TRANSACTION, value)}>
          {(0, locale_1.t)('Go to summary')}
        </ActionItem>);
        }
        if (column.column.kind === 'field' && column.column.field === 'release' && value) {
            addMenuItem(Actions.RELEASE, <ActionItem key="release" data-test-id="release" onClick={() => handleCellAction(Actions.RELEASE, value)}>
          {(0, locale_1.t)('Go to release')}
        </ActionItem>);
        }
        if (column.column.kind === 'function' &&
            column.column.function[0] === 'count_unique') {
            addMenuItem(Actions.DRILLDOWN, <ActionItem key="drilldown" data-test-id="per-cell-drilldown" onClick={() => handleCellAction(Actions.DRILLDOWN, value)}>
          {(0, locale_1.t)('View Stacks')}
        </ActionItem>);
        }
        if (column.column.kind === 'function' &&
            column.column.function[0] === 'user_misery' &&
            (0, utils_1.defined)(dataRow.project_threshold_config)) {
            addMenuItem(Actions.EDIT_THRESHOLD, <ActionItem key="edit_threshold" data-test-id="edit-threshold" onClick={() => handleCellAction(Actions.EDIT_THRESHOLD, value)}>
          {(0, locale_1.tct)('Edit threshold ([threshold]ms)', {
                    threshold: dataRow.project_threshold_config[1],
                })}
        </ActionItem>);
        }
        if (actions.length === 0) {
            return null;
        }
        return (<MenuButtons onClick={event => {
                // prevent clicks from propagating further
                event.stopPropagation();
            }}>
        {actions}
      </MenuButtons>);
    }
    renderMenu() {
        const { isOpen } = this.state;
        const menuButtons = this.renderMenuButtons();
        if (menuButtons === null) {
            // do not render the menu if there are no per cell actions
            return null;
        }
        const modifiers = {
            hide: {
                enabled: false,
            },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
        };
        let menu = null;
        if (isOpen) {
            menu = react_dom_1.default.createPortal(<react_popper_1.Popper placement="top" modifiers={modifiers}>
          {({ ref: popperRef, style, placement, arrowProps }) => (<Menu ref={ref => {
                        popperRef(ref);
                        this.menuEl = ref;
                    }} style={style}>
              <MenuArrow ref={arrowProps.ref} data-placement={placement} style={arrowProps.style}/>
              {menuButtons}
            </Menu>)}
        </react_popper_1.Popper>, this.portalEl);
        }
        return (<MenuRoot>
        <react_popper_1.Manager>
          <react_popper_1.Reference>
            {({ ref }) => (<MenuButton ref={ref} onClick={this.handleMenuToggle}>
                <icons_1.IconEllipsis size="sm" data-test-id="cell-action" color="blue300"/>
              </MenuButton>)}
          </react_popper_1.Reference>
          {menu}
        </react_popper_1.Manager>
      </MenuRoot>);
    }
    render() {
        const { children } = this.props;
        const { isHovering } = this.state;
        return (<Container onMouseEnter={this.handleMouseEnter} onMouseLeave={this.handleMouseLeave}>
        {children}
        {isHovering && this.renderMenu()}
      </Container>);
    }
}
exports.default = CellAction;
const Container = (0, styled_1.default)('div') `
  position: relative;
  width: 100%;
  height: 100%;
`;
const MenuRoot = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  right: 0;
`;
const Menu = (0, styled_1.default)('div') `
  margin: ${(0, space_1.default)(1)} 0;

  z-index: ${p => p.theme.zIndex.tooltip};
`;
const MenuButtons = (0, styled_1.default)('div') `
  background: ${p => p.theme.background};
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius};
  box-shadow: ${p => p.theme.dropShadowHeavy};
  overflow: hidden;
`;
const MenuArrow = (0, styled_1.default)('span') `
  position: absolute;
  width: 18px;
  height: 9px;
  /* left and top set by popper */

  &[data-placement*='bottom'] {
    margin-top: -9px;
    &::before {
      border-width: 0 9px 9px 9px;
      border-color: transparent transparent ${p => p.theme.border} transparent;
    }
    &::after {
      top: 1px;
      left: 1px;
      border-width: 0 8px 8px 8px;
      border-color: transparent transparent ${p => p.theme.background} transparent;
    }
  }
  &[data-placement*='top'] {
    margin-bottom: -8px;
    bottom: 0;
    &::before {
      border-width: 9px 9px 0 9px;
      border-color: ${p => p.theme.border} transparent transparent transparent;
    }
    &::after {
      bottom: 1px;
      left: 1px;
      border-width: 8px 8px 0 8px;
      border-color: ${p => p.theme.background} transparent transparent transparent;
    }
  }

  &::before,
  &::after {
    width: 0;
    height: 0;
    content: '';
    display: block;
    position: absolute;
    border-style: solid;
  }
`;
const ActionItem = (0, styled_1.default)('button') `
  display: block;
  width: 100%;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  background: transparent;

  outline: none;
  border: 0;
  border-bottom: 1px solid ${p => p.theme.innerBorder};

  font-size: ${p => p.theme.fontSizeMedium};
  text-align: left;
  line-height: 1.2;

  &:hover {
    background: ${p => p.theme.backgroundSecondary};
  }

  &:last-child {
    border-bottom: 0;
  }
`;
const MenuButton = (0, styled_1.default)('button') `
  display: flex;
  width: 24px;
  height: 24px;
  padding: 0;
  justify-content: center;
  align-items: center;

  background: ${p => (0, color_1.default)(p.theme.background).alpha(0.85).string()};
  border-radius: ${p => p.theme.borderRadius};
  border: 1px solid ${p => p.theme.border};
  cursor: pointer;
  outline: none;
`;
//# sourceMappingURL=cellAction.jsx.map