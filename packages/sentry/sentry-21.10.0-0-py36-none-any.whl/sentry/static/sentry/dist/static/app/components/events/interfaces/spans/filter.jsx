Object.defineProperty(exports, "__esModule", { value: true });
exports.toggleAllFilters = exports.toggleFilter = exports.noFilter = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const checkboxFancy_1 = (0, tslib_1.__importDefault)(require("app/components/checkboxFancy/checkboxFancy"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownControl_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownControl"));
const utils_1 = require("app/components/performance/waterfall/utils");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.noFilter = {
    type: 'no_filter',
};
class Filter extends React.Component {
    isOperationNameActive(operationName) {
        const { operationNameFilter } = this.props;
        if (operationNameFilter.type === 'no_filter') {
            return false;
        }
        // invariant: operationNameFilter.type === 'active_filter'
        return operationNameFilter.operationNames.has(operationName);
    }
    getNumberOfActiveFilters() {
        const { operationNameFilter } = this.props;
        if (operationNameFilter.type === 'no_filter') {
            return 0;
        }
        return operationNameFilter.operationNames.size;
    }
    render() {
        const { operationNameCounts } = this.props;
        if (operationNameCounts.size === 0) {
            return null;
        }
        const checkedQuantity = this.getNumberOfActiveFilters();
        const dropDownButtonProps = {
            children: (<React.Fragment>
          <icons_1.IconFilter size="xs"/>
          <FilterLabel>{(0, locale_1.t)('Filter')}</FilterLabel>
        </React.Fragment>),
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        if (checkedQuantity > 0) {
            dropDownButtonProps.children = (<span>{(0, locale_1.tn)('%s Active Filter', '%s Active Filters', checkedQuantity)}</span>);
            dropDownButtonProps.priority = 'primary';
            dropDownButtonProps.hasDarkBorderBottomColor = true;
        }
        return (<Wrapper data-test-id="op-filter-dropdown">
        <dropdownControl_1.default menuWidth="240px" blendWithActor button={({ isOpen, getActorProps }) => (<StyledDropdownButton {...getActorProps()} showChevron={false} isOpen={isOpen} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
              {dropDownButtonProps.children}
            </StyledDropdownButton>)}>
          <MenuContent onClick={event => {
                // propagated clicks will dismiss the menu; we stop this here
                event.stopPropagation();
            }}>
            <Header>
              <span>{(0, locale_1.t)('Operation')}</span>
              <checkboxFancy_1.default isChecked={checkedQuantity > 0} isIndeterminate={checkedQuantity > 0 && checkedQuantity !== operationNameCounts.size} onClick={event => {
                event.stopPropagation();
                this.props.toggleAllOperationNameFilters();
            }}/>
            </Header>
            <List>
              {Array.from(operationNameCounts, ([operationName, operationCount]) => {
                const isActive = this.isOperationNameActive(operationName);
                return (<ListItem key={operationName} isChecked={isActive}>
                    <OperationDot backgroundColor={(0, utils_1.pickBarColor)(operationName)}/>
                    <OperationName>{operationName}</OperationName>
                    <OperationCount>{operationCount}</OperationCount>
                    <checkboxFancy_1.default isChecked={isActive} onClick={event => {
                        event.stopPropagation();
                        this.props.toggleOperationNameFilter(operationName);
                    }}/>
                  </ListItem>);
            })}
            </List>
          </MenuContent>
        </dropdownControl_1.default>
      </Wrapper>);
    }
}
const FilterLabel = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(1)};
`;
const Wrapper = (0, styled_1.default)('div') `
  position: relative;
  display: flex;

  margin-right: ${(0, space_1.default)(1)};
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  white-space: nowrap;
  max-width: 200px;

  &:hover,
  &:active {
    ${p => !p.isOpen &&
    p.hasDarkBorderBottomColor &&
    `
          border-bottom-color: ${p.theme.button.primary.border};
        `}
  }

  ${p => !p.isOpen &&
    p.hasDarkBorderBottomColor &&
    `
      border-bottom-color: ${p.theme.button.primary.border};
    `}
`;
const MenuContent = (0, styled_1.default)('div') `
  max-height: 250px;
  overflow-y: auto;
  border-top: 1px solid ${p => p.theme.gray200};
`;
const Header = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto min-content;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;

  margin: 0;
  background-color: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.gray300};
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
`;
const List = (0, styled_1.default)('ul') `
  list-style: none;
  margin: 0;
  padding: 0;
`;
const ListItem = (0, styled_1.default)('li') `
  display: grid;
  grid-template-columns: max-content 1fr max-content max-content;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
  :hover {
    background-color: ${p => p.theme.backgroundSecondary};
  }
  ${checkboxFancy_1.default} {
    opacity: ${p => (p.isChecked ? 1 : 0.3)};
  }

  &:hover ${checkboxFancy_1.default} {
    opacity: 1;
  }

  &:hover span {
    color: ${p => p.theme.blue300};
    text-decoration: underline;
  }
`;
const OperationDot = (0, styled_1.default)('div') `
  content: '';
  display: block;
  width: 8px;
  min-width: 8px;
  height: 8px;
  margin-right: ${(0, space_1.default)(1)};
  border-radius: 100%;

  background-color: ${p => p.backgroundColor};
`;
const OperationName = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  ${overflowEllipsis_1.default};
`;
const OperationCount = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
`;
function toggleFilter(previousState, operationName) {
    if (previousState.type === 'no_filter') {
        return {
            type: 'active_filter',
            operationNames: new Set([operationName]),
        };
    }
    // invariant: previousState.type === 'active_filter'
    // invariant: previousState.operationNames.size >= 1
    const { operationNames } = previousState;
    if (operationNames.has(operationName)) {
        operationNames.delete(operationName);
    }
    else {
        operationNames.add(operationName);
    }
    if (operationNames.size > 0) {
        return {
            type: 'active_filter',
            operationNames,
        };
    }
    return {
        type: 'no_filter',
    };
}
exports.toggleFilter = toggleFilter;
function toggleAllFilters(previousState, operationNames) {
    if (previousState.type === 'no_filter') {
        return {
            type: 'active_filter',
            operationNames: new Set(operationNames),
        };
    }
    // invariant: previousState.type === 'active_filter'
    if (previousState.operationNames.size === operationNames.length) {
        // all filters were selected, so the next state should un-select all filters
        return {
            type: 'no_filter',
        };
    }
    // not all filters were selected, so the next state is to select all the remaining filters
    return {
        type: 'active_filter',
        operationNames: new Set(operationNames),
    };
}
exports.toggleAllFilters = toggleAllFilters;
exports.default = Filter;
//# sourceMappingURL=filter.jsx.map