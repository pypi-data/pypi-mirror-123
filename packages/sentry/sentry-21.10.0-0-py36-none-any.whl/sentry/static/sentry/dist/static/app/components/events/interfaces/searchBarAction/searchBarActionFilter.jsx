Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const checkboxFancy_1 = (0, tslib_1.__importDefault)(require("app/components/checkboxFancy/checkboxFancy"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dropDownButton_1 = (0, tslib_1.__importDefault)(require("./dropDownButton"));
function SearchBarActionFilter({ options, onChange }) {
    const checkedQuantity = Object.values(options)
        .flatMap(option => option)
        .filter(option => option.isChecked).length;
    function handleClick(category, option) {
        const updatedOptions = Object.assign(Object.assign({}, options), { [category]: options[category].map(groupedOption => {
                if (option.id === groupedOption.id) {
                    return Object.assign(Object.assign({}, groupedOption), { isChecked: !groupedOption.isChecked });
                }
                return groupedOption;
            }) });
        onChange(updatedOptions);
    }
    return (<Wrapper>
      <dropdownControl_1.default button={({ isOpen, getActorProps }) => (<dropDownButton_1.default isOpen={isOpen} getActorProps={getActorProps} checkedQuantity={checkedQuantity}/>)}>
        {({ getMenuProps, isOpen }) => (<StyledContent {...getMenuProps()} data-test-id="filter-dropdown-menu" alignMenu="left" width="240px" isOpen={isOpen} blendWithActor blendCorner>
            {Object.keys(options).map(category => (<react_1.Fragment key={category}>
                <Header>{category}</Header>
                <StyledList>
                  {options[category].map(groupedOption => {
                    const { symbol, isChecked, id, description } = groupedOption;
                    return (<StyledListItem key={id} onClick={event => {
                            event.stopPropagation();
                            handleClick(category, groupedOption);
                        }} isChecked={isChecked} hasDescription={!!description}>
                        {symbol}
                        {description && <Description>{description}</Description>}
                        <checkboxFancy_1.default isChecked={isChecked}/>
                      </StyledListItem>);
                })}
                </StyledList>
              </react_1.Fragment>))}
          </StyledContent>)}
      </dropdownControl_1.default>
    </Wrapper>);
}
exports.default = SearchBarActionFilter;
const Wrapper = (0, styled_1.default)('div') `
  position: relative;
  display: flex;
`;
const StyledContent = (0, styled_1.default)(dropdownControl_1.Content) `
  top: calc(100% + ${(0, space_1.default)(0.5)} - 1px);
  border-radius: ${p => p.theme.borderRadius};
  > ul:last-child {
    > li:last-child {
      border-bottom: none;
    }
  }
`;
const Header = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin: 0;
  background-color: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.gray300};
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
`;
const StyledList = (0, styled_1.default)(list_1.default) `
  grid-gap: 0;
`;
const StyledListItem = (0, styled_1.default)(listItem_1.default) `
  display: grid;
  grid-template-columns: ${p => p.hasDescription ? 'max-content 1fr max-content' : '1fr max-content'};
  grid-column-gap: ${(0, space_1.default)(1)};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
  align-items: center;
  cursor: pointer;
  ${checkboxFancy_1.default} {
    opacity: ${p => (p.isChecked ? 1 : 0.3)};
  }

  :hover {
    background-color: ${p => p.theme.backgroundSecondary};
    ${checkboxFancy_1.default} {
      opacity: 1;
    }
    span {
      color: ${p => p.theme.blue300};
      text-decoration: underline;
    }
  }
`;
const Description = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
`;
//# sourceMappingURL=searchBarActionFilter.jsx.map