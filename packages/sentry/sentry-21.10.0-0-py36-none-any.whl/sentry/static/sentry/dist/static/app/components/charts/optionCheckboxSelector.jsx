Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const styles_1 = require("app/components/charts/styles");
const checkboxFancy_1 = (0, tslib_1.__importDefault)(require("app/components/checkboxFancy/checkboxFancy"));
const dropdownBubble_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownBubble"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownControl_1 = require("app/components/dropdownControl");
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const truncate_1 = (0, tslib_1.__importDefault)(require("app/components/truncate"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const defaultProps = {
    menuWidth: 'auto',
};
class OptionCheckboxSelector extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {};
        this.menuContainerRef = (0, react_1.createRef)();
    }
    componentDidMount() {
        this.setMenuContainerWidth();
    }
    shouldComponentUpdate(nextProps, nextState) {
        return !(0, isEqual_1.default)(nextProps, this.props) || !(0, isEqual_1.default)(nextState, this.state);
    }
    componentDidUpdate(prevProps) {
        if (prevProps.selected !== this.props.selected) {
            this.setMenuContainerWidth();
        }
    }
    setMenuContainerWidth() {
        var _a, _b;
        const menuContainerWidth = (_b = (_a = this.menuContainerRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetWidth;
        if (menuContainerWidth) {
            this.setState({ menuContainerWidth });
        }
    }
    constructNewSelected(value) {
        return [value];
    }
    selectCheckbox(value) {
        const { selected } = this.props;
        // Cannot have no option selected
        if (selected.length === 1 && selected[0] === value) {
            return selected;
        }
        // Check if the value is already selected.
        // Return a new updated array with the value either selected or deselected depending on previous selected state.
        if (selected.includes(value)) {
            return selected.filter(selectedValue => selectedValue !== value);
        }
        return [...selected, value];
    }
    shouldBeDisabled(value) {
        const { selected } = this.props;
        // Y-Axis is capped at 3 fields
        return selected.length > 2 && !selected.includes(value);
    }
    handleCheckboxClick(event, value) {
        const { onChange } = this.props;
        event.stopPropagation();
        if (!this.shouldBeDisabled(value)) {
            onChange(this.selectCheckbox(value));
        }
    }
    render() {
        const { menuContainerWidth } = this.state;
        const { options, onChange, selected, title, menuWidth } = this.props;
        const selectedOptionLabel = options
            .filter(opt => selected.includes(opt.value))
            .map(({ label }) => label)
            .join(', ') || 'None';
        return (<styles_1.InlineContainer>
        <styles_1.SectionHeading>{title}</styles_1.SectionHeading>
        <MenuContainer ref={this.menuContainerRef}>
          <dropdownMenu_1.default alwaysRenderMenu={false} keepMenuOpen>
            {({ isOpen, getMenuProps, getActorProps }) => (<react_1.Fragment>
                <StyledDropdownButton {...getActorProps()} size="zero" isOpen={isOpen}>
                  <TruncatedLabel>{String(selectedOptionLabel)}</TruncatedLabel>
                </StyledDropdownButton>
                <StyledDropdownBubble {...getMenuProps()} alignMenu="right" width={menuWidth} minWidth={menuContainerWidth} isOpen={isOpen} blendWithActor={false} blendCorner>
                  {options.map(opt => {
                    const disabled = this.shouldBeDisabled(opt.value);
                    return (<StyledDropdownItem key={opt.value} onSelect={eventKey => onChange(this.constructNewSelected(eventKey))} eventKey={opt.value} data-test-id={`option-${opt.value}`} isChecked={selected.includes(opt.value)}>
                        <StyledTruncate isActive={false} value={String(opt.label)} maxLength={60} expandDirection="left"/>
                        <tooltip_1.default title={disabled
                            ? (0, locale_1.t)('Only a maximum of 3 fields can be displayed on the Y-Axis at a time')
                            : undefined}>
                          <checkboxFancy_1.default className={opt.value} isChecked={selected.includes(opt.value)} isDisabled={disabled} onClick={event => this.handleCheckboxClick(event, opt.value)}/>
                        </tooltip_1.default>
                      </StyledDropdownItem>);
                })}
                </StyledDropdownBubble>
              </react_1.Fragment>)}
          </dropdownMenu_1.default>
        </MenuContainer>
      </styles_1.InlineContainer>);
    }
}
OptionCheckboxSelector.defaultProps = defaultProps;
const TruncatedLabel = (0, styled_1.default)('span') `
  ${overflowEllipsis_1.default};
  max-width: 400px;
`;
const StyledTruncate = (0, styled_1.default)(truncate_1.default) `
  flex: auto;
  padding-right: ${(0, space_1.default)(1)};
  & span {
    ${p => p.isActive &&
    `
      color: ${p.theme.white};
      background: ${p.theme.active};
      border: none;
    `}
  }
`;
const MenuContainer = (0, styled_1.default)('div') `
  display: inline-block;
  position: relative;
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  font-weight: normal;
  z-index: ${p => (p.isOpen ? p.theme.zIndex.dropdownAutocomplete.actor : 'auto')};
`;
const StyledDropdownBubble = (0, styled_1.default)(dropdownBubble_1.default) `
  display: ${p => (p.isOpen ? 'block' : 'none')};
  overflow: visible;
  ${p => p.minWidth && p.width === 'auto' && `min-width: calc(${p.minWidth}px + ${(0, space_1.default)(3)})`};
`;
const StyledDropdownItem = (0, styled_1.default)(dropdownControl_1.DropdownItem) `
  line-height: ${p => p.theme.text.lineHeightBody};
  white-space: nowrap;
  ${checkboxFancy_1.default} {
    opacity: ${p => (p.isChecked ? 1 : 0.3)};
  }

  &:hover ${checkboxFancy_1.default} {
    opacity: 1;
  }
`;
exports.default = OptionCheckboxSelector;
//# sourceMappingURL=optionCheckboxSelector.jsx.map