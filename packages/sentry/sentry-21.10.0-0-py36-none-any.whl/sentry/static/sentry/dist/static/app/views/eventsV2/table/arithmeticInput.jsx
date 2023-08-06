Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fields_1 = require("app/utils/discover/fields");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const NONE_SELECTED = -1;
class ArithmeticInput extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            query: this.props.value,
            partialTerm: null,
            rawOptions: this.props.options,
            dropdownVisible: false,
            dropdownOptionGroups: makeOptions(this.props.options, null),
            activeSelection: NONE_SELECTED,
        };
        this.input = (0, react_1.createRef)();
        this.blur = () => {
            var _a;
            (_a = this.input.current) === null || _a === void 0 ? void 0 : _a.blur();
        };
        this.focus = (position) => {
            var _a, _b;
            (_a = this.input.current) === null || _a === void 0 ? void 0 : _a.focus();
            (_b = this.input.current) === null || _b === void 0 ? void 0 : _b.setSelectionRange(position, position);
        };
        this.handleChange = (event) => {
            const query = event.target.value.replace('\n', '');
            this.setState({ query }, this.updateAutocompleteOptions);
        };
        this.handleClick = () => {
            this.updateAutocompleteOptions();
        };
        this.handleFocus = () => {
            this.setState({ dropdownVisible: true });
        };
        this.handleBlur = () => {
            this.props.onUpdate(this.state.query);
            this.setState({ dropdownVisible: false });
        };
        this.handleKeyDown = (event) => {
            const { key } = event;
            const { options } = this.props;
            const { activeSelection, partialTerm } = this.state;
            const startedSelection = activeSelection >= 0;
            // handle arrow navigation
            if (key === 'ArrowDown' || key === 'ArrowUp') {
                event.preventDefault();
                const newOptionGroups = makeOptions(options, partialTerm);
                const flattenedOptions = newOptionGroups.map(group => group.options).flat();
                if (flattenedOptions.length === 0) {
                    return;
                }
                let newSelection;
                if (!startedSelection) {
                    newSelection = key === 'ArrowUp' ? flattenedOptions.length - 1 : 0;
                }
                else {
                    newSelection =
                        key === 'ArrowUp'
                            ? (activeSelection - 1 + flattenedOptions.length) % flattenedOptions.length
                            : (activeSelection + 1) % flattenedOptions.length;
                }
                // This is modifying the `active` value of the references so make sure to
                // use `newOptionGroups` at the end.
                flattenedOptions[newSelection].active = true;
                this.setState({
                    activeSelection: newSelection,
                    dropdownOptionGroups: newOptionGroups,
                });
                return;
            }
            // handle selection
            if (startedSelection && (key === 'Tab' || key === 'Enter')) {
                event.preventDefault();
                const selection = this.getSelection(activeSelection);
                if (selection) {
                    this.handleSelect(selection);
                }
                return;
            }
            if (key === 'Enter') {
                this.blur();
                return;
            }
        };
        this.handleKeyUp = (event) => {
            // Other keys are managed at handleKeyDown function
            if (event.key !== 'Escape') {
                return;
            }
            event.preventDefault();
            const { activeSelection } = this.state;
            const startedSelection = activeSelection >= 0;
            if (!startedSelection) {
                this.blur();
                return;
            }
        };
        this.handleSelect = (option) => {
            const { prefix, suffix } = this.splitQuery();
            this.setState({
                // make sure to insert a space after the autocompleted term
                query: `${prefix}${option.value} ${suffix}`,
                activeSelection: NONE_SELECTED,
            }, () => {
                // updating the query will cause the input to lose focus
                // and make sure to move the cursor behind the space after
                // the end of the autocompleted term
                this.focus(prefix.length + option.value.length + 1);
                this.updateAutocompleteOptions();
            });
        };
    }
    static getDerivedStateFromProps(props, state) {
        const changed = !(0, isEqual_1.default)(state.rawOptions, props.options);
        if (changed) {
            return Object.assign(Object.assign({}, state), { rawOptions: props.options, dropdownOptionGroups: makeOptions(props.options, state.partialTerm), activeSelection: NONE_SELECTED });
        }
        return Object.assign({}, state);
    }
    getCursorPosition() {
        var _a, _b;
        return (_b = (_a = this.input.current) === null || _a === void 0 ? void 0 : _a.selectionStart) !== null && _b !== void 0 ? _b : -1;
    }
    splitQuery() {
        const { query } = this.state;
        const currentPosition = this.getCursorPosition();
        // The current term is delimited by whitespaces. So if no spaces are found,
        // the entire string is taken to be 1 term.
        //
        // TODO: add support for when there are no spaces
        const matches = [...query.substring(0, currentPosition).matchAll(/\s|^/g)];
        const match = matches[matches.length - 1];
        const startOfTerm = match[0] === '' ? 0 : (match.index || 0) + 1;
        const cursorOffset = query.slice(currentPosition).search(/\s|$/);
        const endOfTerm = currentPosition + (cursorOffset === -1 ? 0 : cursorOffset);
        return {
            startOfTerm,
            endOfTerm,
            prefix: query.substring(0, startOfTerm),
            term: query.substring(startOfTerm, endOfTerm),
            suffix: query.substring(endOfTerm),
        };
    }
    getSelection(selection) {
        const { dropdownOptionGroups } = this.state;
        for (const group of dropdownOptionGroups) {
            if (selection >= group.options.length) {
                selection -= group.options.length;
                continue;
            }
            return group.options[selection];
        }
        return null;
    }
    updateAutocompleteOptions() {
        const { options } = this.props;
        const { term } = this.splitQuery();
        const partialTerm = term || null;
        this.setState({
            dropdownOptionGroups: makeOptions(options, partialTerm),
            partialTerm,
        });
    }
    render() {
        const _a = this.props, { onUpdate: _onUpdate, options: _options } = _a, props = (0, tslib_1.__rest)(_a, ["onUpdate", "options"]);
        const { dropdownVisible, dropdownOptionGroups } = this.state;
        return (<Container isOpen={dropdownVisible}>
        <StyledInput {...props} ref={this.input} autoComplete="off" className="form-control" value={this.state.query} onClick={this.handleClick} onChange={this.handleChange} onBlur={this.handleBlur} onFocus={this.handleFocus} onKeyDown={this.handleKeyDown} spellCheck={false}/>
        <TermDropdown isOpen={dropdownVisible} optionGroups={dropdownOptionGroups} handleSelect={this.handleSelect}/>
      </Container>);
    }
}
exports.default = ArithmeticInput;
ArithmeticInput.defaultProps = {
    options: [],
};
const Container = (0, styled_1.default)('div') `
  border: 1px solid ${p => p.theme.border};
  box-shadow: inset ${p => p.theme.dropShadowLight};
  background: ${p => p.theme.background};
  position: relative;

  border-radius: ${p => p.isOpen
    ? `${p.theme.borderRadius} ${p.theme.borderRadius} 0 0`
    : p.theme.borderRadius};

  .show-sidebar & {
    background: ${p => p.theme.backgroundSecondary};
  }
`;
const StyledInput = (0, styled_1.default)(input_1.default) `
  height: 40px;
  padding: 7px 10px;
  border: 0;
  box-shadow: none;

  &:hover,
  &:focus {
    border: 0;
    box-shadow: none;
  }
`;
function TermDropdown({ isOpen, optionGroups, handleSelect }) {
    return (<DropdownContainer isOpen={isOpen}>
      <DropdownItemsList>
        {optionGroups.map(group => {
            const { title, options } = group;
            return (<react_1.Fragment key={title}>
              <ListItem>
                <DropdownTitle>{title}</DropdownTitle>
              </ListItem>
              {options.map(option => {
                    return (<DropdownListItem key={option.value} className={option.active ? 'active' : undefined} onClick={() => handleSelect(option)} 
                    // prevent the blur event on the input from firing
                    onMouseDown={event => event.preventDefault()} 
                    // scroll into view if it is the active element
                    ref={element => { var _a; return option.active && ((_a = element === null || element === void 0 ? void 0 : element.scrollIntoView) === null || _a === void 0 ? void 0 : _a.call(element, { block: 'nearest' })); }}>
                    <DropdownItemTitleWrapper>{option.value}</DropdownItemTitleWrapper>
                  </DropdownListItem>);
                })}
              {options.length === 0 && <Info>{(0, locale_1.t)('No items found')}</Info>}
            </react_1.Fragment>);
        })}
      </DropdownItemsList>
    </DropdownContainer>);
}
function makeFieldOptions(columns, partialTerm) {
    const fieldValues = new Set();
    const options = columns
        .filter(({ kind }) => kind !== 'equation')
        .filter(fields_1.isLegalEquationColumn)
        .map(option => ({
        kind: 'field',
        active: false,
        value: (0, fields_1.generateFieldAsString)(option),
    }))
        .filter(({ value }) => {
        if (fieldValues.has(value)) {
            return false;
        }
        else {
            fieldValues.add(value);
            return true;
        }
    })
        .filter(({ value }) => (partialTerm ? value.includes(partialTerm) : true));
    return {
        title: 'Fields',
        options,
    };
}
function makeOperatorOptions(partialTerm) {
    const options = ['+', '-', '*', '/', '(', ')']
        .filter(operator => (partialTerm ? operator.includes(partialTerm) : true))
        .map(operator => ({
        kind: 'operator',
        active: false,
        value: operator,
    }));
    return {
        title: 'Operators',
        options,
    };
}
function makeOptions(columns, partialTerm) {
    return [makeFieldOptions(columns, partialTerm), makeOperatorOptions(partialTerm)];
}
const DropdownContainer = (0, styled_1.default)('div') `
  /* Container has a border that we need to account for */
  display: ${p => (p.isOpen ? 'block' : 'none')};
  position: absolute;
  top: 100%;
  left: -1px;
  right: -1px;
  z-index: ${p => p.theme.zIndex.dropdown};
  background: ${p => p.theme.background};
  box-shadow: ${p => p.theme.dropShadowLight};
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadiusBottom};
  max-height: 300px;
  overflow-y: auto;
`;
const DropdownItemsList = (0, styled_1.default)('ul') `
  padding-left: 0;
  list-style: none;
  margin-bottom: 0;
`;
const ListItem = (0, styled_1.default)('li') `
  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }
`;
const DropdownTitle = (0, styled_1.default)('header') `
  display: flex;
  align-items: center;

  background-color: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.gray300};
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};

  margin: 0;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};

  & > svg {
    margin-right: ${(0, space_1.default)(1)};
  }
`;
const DropdownListItem = (0, styled_1.default)(ListItem) `
  scroll-margin: 40px 0;
  font-size: ${p => p.theme.fontSizeLarge};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  cursor: pointer;

  &:hover,
  &.active {
    background: ${p => p.theme.focus};
  }
`;
const DropdownItemTitleWrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};
  margin: 0;
  line-height: ${p => p.theme.text.lineHeightHeading};
  ${overflowEllipsis_1.default};
`;
const Info = (0, styled_1.default)('div') `
  display: flex;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  font-size: ${p => p.theme.fontSizeLarge};
  color: ${p => p.theme.gray300};

  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }
`;
//# sourceMappingURL=arithmeticInput.jsx.map