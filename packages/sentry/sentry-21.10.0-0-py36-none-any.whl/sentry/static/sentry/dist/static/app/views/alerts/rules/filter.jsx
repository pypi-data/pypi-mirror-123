Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const checkboxFancy_1 = (0, tslib_1.__importDefault)(require("app/components/checkboxFancy/checkboxFancy"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function FilterSection({ id, label, items, toggleSection, toggleFilter }) {
    const checkedItemsCount = items.filter(item => item.checked).length;
    return (<react_1.Fragment>
      <Header>
        <span>{label}</span>
        <checkboxFancy_1.default isChecked={checkedItemsCount === items.length} isIndeterminate={checkedItemsCount > 0 && checkedItemsCount !== items.length} onClick={event => {
            event.stopPropagation();
            toggleSection(id);
        }}/>
      </Header>
      {items
            .filter(item => !item.filtered)
            .map(item => (<ListItem key={item.value} isChecked={item.checked} onClick={event => {
                event.stopPropagation();
                toggleFilter(id, item.value);
            }}>
            <TeamName>{item.label}</TeamName>
            <checkboxFancy_1.default isChecked={item.checked}/>
          </ListItem>))}
    </react_1.Fragment>);
}
class Filter extends react_1.Component {
    constructor() {
        super(...arguments);
        this.toggleFilter = (sectionId, value) => {
            const { onFilterChange, dropdownSections } = this.props;
            const section = dropdownSections.find(dropdownSection => dropdownSection.id === sectionId);
            const newSelection = new Set(section.items.filter(item => item.checked).map(item => item.value));
            if (newSelection.has(value)) {
                newSelection.delete(value);
            }
            else {
                newSelection.add(value);
            }
            onFilterChange(sectionId, newSelection);
        };
        this.toggleSection = (sectionId) => {
            const { onFilterChange } = this.props;
            const section = this.props.dropdownSections.find(dropdownSection => dropdownSection.id === sectionId);
            const activeItems = section.items.filter(item => item.checked);
            const newSelection = section.items.length === activeItems.length
                ? new Set()
                : new Set(section.items.map(item => item.value));
            onFilterChange(sectionId, newSelection);
        };
        this.getNumberOfActiveFilters = () => {
            return this.props.dropdownSections
                .map(section => section.items)
                .flat()
                .filter(item => item.checked).length;
        };
    }
    render() {
        const { dropdownSections: dropdownItems, header } = this.props;
        const checkedQuantity = this.getNumberOfActiveFilters();
        const dropDownButtonProps = {
            children: (0, locale_1.t)('Filter'),
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        if (checkedQuantity > 0) {
            dropDownButtonProps.children = (0, locale_1.tn)('%s Active Filter', '%s Active Filters', checkedQuantity);
            dropDownButtonProps.hasDarkBorderBottomColor = true;
        }
        return (<dropdownControl_1.default menuWidth="240px" blendWithActor alwaysRenderMenu={false} button={({ isOpen, getActorProps }) => (<StyledDropdownButton {...getActorProps()} showChevron={false} isOpen={isOpen} icon={<icons_1.IconFilter size="xs"/>} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
            {dropDownButtonProps.children}
          </StyledDropdownButton>)}>
        {({ isOpen, getMenuProps }) => (<MenuContent {...getMenuProps()} isOpen={isOpen} blendCorner alignMenu="left" width="240px">
            <List>
              {header}
              {dropdownItems.map(section => (<FilterSection key={section.id} {...section} toggleSection={this.toggleSection} toggleFilter={this.toggleFilter}/>))}
            </List>
          </MenuContent>)}
      </dropdownControl_1.default>);
    }
}
const MenuContent = (0, styled_1.default)(dropdownControl_1.Content) `
  max-height: 290px;
  overflow-y: auto;
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
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  white-space: nowrap;
  max-width: 200px;

  z-index: ${p => p.theme.zIndex.dropdown};
`;
const List = (0, styled_1.default)('ul') `
  list-style: none;
  margin: 0;
  padding: 0;
`;
const ListItem = (0, styled_1.default)('li') `
  display: grid;
  grid-template-columns: 1fr max-content;
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
const TeamName = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  ${overflowEllipsis_1.default};
`;
exports.default = Filter;
//# sourceMappingURL=filter.jsx.map