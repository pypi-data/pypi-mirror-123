Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
/**
 * Inspired by [Downshift](https://github.com/paypal/downshift)
 *
 * Implemented with a stripped-down, compatible API for our use case.
 * May be worthwhile to switch if we find we need more features
 *
 * Basic idea is that we call `children` with props necessary to render with any sort of component structure.
 * This component handles logic like when the dropdown menu should be displayed, as well as handling keyboard input, how
 * it is rendered should be left to the child.
 */
const React = (0, tslib_1.__importStar)(require("react"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const defaultProps = {
    itemToString: () => '',
    /**
     * If input should be considered an "actor". If there is another parent actor, then this should be `false`.
     * e.g. You have a button that opens this <AutoComplete> in a dropdown.
     */
    inputIsActor: true,
    disabled: false,
    closeOnSelect: true,
    /**
     * Can select autocomplete item with "Enter" key
     */
    shouldSelectWithEnter: true,
    /**
     * Can select autocomplete item with "Tab" key
     */
    shouldSelectWithTab: false,
};
class AutoComplete extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.items = new Map();
        this.isControlled = () => typeof this.props.isOpen !== 'undefined';
        this.getOpenState = () => {
            const { isOpen } = this.props;
            return this.isControlled() ? isOpen : this.state.isOpen;
        };
        /**
         * Resets `this.items` and `this.state.highlightedIndex`.
         * Should be called whenever `inputValue` changes.
         */
        this.resetHighlightState = () => {
            // reset items and expect `getInputProps` in child to give us a list of new items
            this.setState({
                highlightedIndex: this.props.defaultHighlightedIndex || 0,
            });
        };
        this.handleInputChange = ({ onChange }) => (e) => {
            const value = e.target.value;
            // We force `isOpen: true` here because:
            // 1) it's possible to have menu closed but input with focus (i.e. hitting "Esc")
            // 2) you select an item, input still has focus, and then change input
            this.openMenu();
            this.setState({
                inputValue: value,
            });
            onChange === null || onChange === void 0 ? void 0 : onChange(e);
        };
        this.handleInputFocus = ({ onFocus }) => (e) => {
            this.openMenu();
            onFocus === null || onFocus === void 0 ? void 0 : onFocus(e);
        };
        /**
         *
         * We need this delay because we want to close the menu when input
         * is blurred (i.e. clicking or via keyboard). However we have to handle the
         * case when we want to click on the dropdown and causes focus.
         *
         * Clicks outside should close the dropdown immediately via <DropdownMenu />,
         * however blur via keyboard will have a 200ms delay
         */
        this.handleInputBlur = ({ onBlur }) => (e) => {
            this.blurTimer = setTimeout(() => {
                this.closeMenu();
                onBlur === null || onBlur === void 0 ? void 0 : onBlur(e);
            }, 200);
        };
        // Dropdown detected click outside, we should close
        this.handleClickOutside = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // Otherwise, it's possible that this gets fired multiple times
            // e.g. click outside triggers closeMenu and at the same time input gets blurred, so
            // a timer is set to close the menu
            if (this.blurTimer) {
                clearTimeout(this.blurTimer);
            }
            // Wait until the current macrotask completes, in the case that the click
            // happened on a hovercard or some other element rendered outside of the
            // autocomplete, but controlled by the existence of the autocomplete, we
            // need to ensure any click handlers are run.
            yield new Promise(resolve => setTimeout(resolve));
            this.closeMenu();
        });
        this.handleInputKeyDown = ({ onKeyDown }) => (e) => {
            const hasHighlightedItem = this.items.size && this.items.has(this.state.highlightedIndex);
            const canSelectWithEnter = this.props.shouldSelectWithEnter && e.key === 'Enter';
            const canSelectWithTab = this.props.shouldSelectWithTab && e.key === 'Tab';
            if (hasHighlightedItem && (canSelectWithEnter || canSelectWithTab)) {
                const item = this.items.get(this.state.highlightedIndex);
                if (!item.disabled) {
                    this.handleSelect(item, e);
                }
                e.preventDefault();
            }
            if (e.key === 'ArrowUp') {
                this.moveHighlightedIndex(-1);
                e.preventDefault();
            }
            if (e.key === 'ArrowDown') {
                this.moveHighlightedIndex(1);
                e.preventDefault();
            }
            if (e.key === 'Escape') {
                this.closeMenu();
            }
            onKeyDown === null || onKeyDown === void 0 ? void 0 : onKeyDown(e);
        };
        this.handleItemClick = ({ item, index }) => (e) => {
            if (item.disabled) {
                return;
            }
            if (this.blurTimer) {
                clearTimeout(this.blurTimer);
            }
            this.setState({ highlightedIndex: index });
            this.handleSelect(item, e);
        };
        this.handleMenuMouseDown = () => {
            // Cancel close menu from input blur (mouseDown event can occur before input blur :()
            setTimeout(() => {
                if (this.blurTimer) {
                    clearTimeout(this.blurTimer);
                }
            });
        };
        /**
         * When an item is selected via clicking or using the keyboard (e.g. pressing "Enter")
         */
        this.handleSelect = (item, e) => {
            const { onSelect, itemToString, closeOnSelect } = this.props;
            onSelect === null || onSelect === void 0 ? void 0 : onSelect(item, this.state, e);
            if (closeOnSelect) {
                this.closeMenu();
                this.setState({
                    inputValue: itemToString(item),
                    selectedItem: item,
                });
                return;
            }
            this.setState({ selectedItem: item });
        };
        /**
         * Open dropdown menu
         *
         * This is exposed to render function
         */
        this.openMenu = (...args) => {
            const { onOpen, disabled } = this.props;
            onOpen === null || onOpen === void 0 ? void 0 : onOpen(...args);
            if (disabled || this.isControlled()) {
                return;
            }
            this.resetHighlightState();
            this.setState({
                isOpen: true,
            });
        };
        /**
         * Close dropdown menu
         *
         * This is exposed to render function
         */
        this.closeMenu = (...args) => {
            const { onClose, resetInputOnClose } = this.props;
            onClose === null || onClose === void 0 ? void 0 : onClose(...args);
            if (this.isControlled()) {
                return;
            }
            this.setState(state => ({
                isOpen: false,
                inputValue: resetInputOnClose ? '' : state.inputValue,
            }));
        };
        this.getInputProps = (inputProps) => {
            const _a = inputProps !== null && inputProps !== void 0 ? inputProps : {}, { onChange, onKeyDown, onFocus, onBlur } = _a, rest = (0, tslib_1.__rest)(_a, ["onChange", "onKeyDown", "onFocus", "onBlur"]);
            return Object.assign(Object.assign({}, rest), { value: this.state.inputValue, onChange: this.handleInputChange({ onChange }), onKeyDown: this.handleInputKeyDown({ onKeyDown }), onFocus: this.handleInputFocus({ onFocus }), onBlur: this.handleInputBlur({ onBlur }) });
        };
        this.getItemProps = (itemProps) => {
            const _a = itemProps !== null && itemProps !== void 0 ? itemProps : {}, { item, index } = _a, props = (0, tslib_1.__rest)(_a, ["item", "index"]);
            if (!item) {
                // eslint-disable-next-line no-console
                console.warn('getItemProps requires an object with an `item` key');
            }
            const newIndex = index !== null && index !== void 0 ? index : this.items.size;
            this.items.set(newIndex, item);
            return Object.assign(Object.assign({}, props), { onClick: this.handleItemClick(Object.assign({ item, index: newIndex }, props)) });
        };
        this.getMenuProps = (props) => {
            this.itemCount = props === null || props === void 0 ? void 0 : props.itemCount;
            return Object.assign(Object.assign({}, (props !== null && props !== void 0 ? props : {})), { onMouseDown: this.handleMenuMouseDown });
        };
    }
    getInitialState() {
        const { defaultHighlightedIndex, isOpen, defaultInputValue } = this.props;
        return {
            isOpen: !!isOpen,
            highlightedIndex: defaultHighlightedIndex || 0,
            inputValue: defaultInputValue || '',
            selectedItem: undefined,
        };
    }
    UNSAFE_componentWillReceiveProps(nextProps, nextState) {
        // If we do NOT want to close on select, then we should not reset highlight state
        // when we select an item (when we select an item, `this.state.selectedItem` changes)
        if (!nextProps.closeOnSelect && this.state.selectedItem !== nextState.selectedItem) {
            return;
        }
        this.resetHighlightState();
    }
    UNSAFE_componentWillUpdate() {
        this.items.clear();
    }
    moveHighlightedIndex(step) {
        let newIndex = this.state.highlightedIndex + step;
        // when this component is in virtualized mode, only a subset of items will be passed
        // down, making the array length inaccurate. instead we manually pass the length as itemCount
        const listSize = this.itemCount || this.items.size;
        // Make sure new index is within bounds
        newIndex = Math.max(0, Math.min(newIndex, listSize - 1));
        this.setState({ highlightedIndex: newIndex });
    }
    render() {
        const { children, onMenuOpen, inputIsActor } = this.props;
        const { selectedItem, inputValue, highlightedIndex } = this.state;
        const isOpen = this.getOpenState();
        return (<dropdownMenu_1.default isOpen={isOpen} onClickOutside={this.handleClickOutside} onOpen={onMenuOpen}>
        {dropdownMenuProps => children(Object.assign(Object.assign({}, dropdownMenuProps), { getMenuProps: (props) => dropdownMenuProps.getMenuProps(this.getMenuProps(props)), getInputProps: (props) => {
                    const inputProps = this.getInputProps(props);
                    if (!inputIsActor) {
                        return inputProps;
                    }
                    return dropdownMenuProps.getActorProps(inputProps);
                }, getItemProps: this.getItemProps, inputValue,
                selectedItem,
                highlightedIndex, actions: {
                    open: this.openMenu,
                    close: this.closeMenu,
                } }))}
      </dropdownMenu_1.default>);
    }
}
AutoComplete.defaultProps = defaultProps;
exports.default = AutoComplete;
//# sourceMappingURL=autoComplete.jsx.map