Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const constants_1 = require("app/constants");
class DropdownMenu extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isOpen: false,
        };
        this.dropdownMenu = null;
        this.dropdownActor = null;
        this.mouseLeaveId = null;
        this.mouseEnterId = null;
        // Gets open state from props or local state when appropriate
        this.isOpen = () => {
            const { isOpen } = this.props;
            const isControlled = typeof isOpen !== 'undefined';
            return (isControlled && isOpen) || this.state.isOpen;
        };
        // Checks if click happens inside of dropdown menu (or its button)
        // Closes dropdownmenu if it is "outside"
        this.checkClickOutside = (e) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { onClickOutside, shouldIgnoreClickOutside } = this.props;
            if (!this.dropdownMenu || !this.isOpen()) {
                return;
            }
            if (!(e.target instanceof Element)) {
                return;
            }
            // Dropdown menu itself
            if (this.dropdownMenu.contains(e.target)) {
                return;
            }
            if (!this.dropdownActor) {
                // Log an error, should be lower priority
                Sentry.withScope(scope => {
                    scope.setLevel(Sentry.Severity.Warning);
                    Sentry.captureException(new Error('DropdownMenu does not have "Actor" attached'));
                });
            }
            // Button that controls visibility of dropdown menu
            if (this.dropdownActor && this.dropdownActor.contains(e.target)) {
                return;
            }
            if (typeof shouldIgnoreClickOutside === 'function' && shouldIgnoreClickOutside(e)) {
                return;
            }
            if (typeof onClickOutside === 'function') {
                onClickOutside(e);
            }
            // Wait until the current macrotask completes, in the case that the click
            // happened on a hovercard or some other element rendered outside of the
            // dropdown, but controlled by the existence of the dropdown, we need to
            // ensure any click handlers are run.
            yield new Promise(resolve => setTimeout(resolve));
            this.handleClose();
        });
        // Opens dropdown menu
        this.handleOpen = (e) => {
            const { onOpen, isOpen, alwaysRenderMenu, isNestedDropdown } = this.props;
            const isControlled = typeof isOpen !== 'undefined';
            if (!isControlled) {
                this.setState({
                    isOpen: true,
                });
            }
            if (this.mouseLeaveId) {
                window.clearTimeout(this.mouseLeaveId);
            }
            // If we always render menu (e.g. DropdownLink), then add the check click outside handlers when we open the menu
            // instead of when the menu component mounts. Otherwise we will have many click handlers attached on initial load.
            if (alwaysRenderMenu || isNestedDropdown) {
                document.addEventListener('click', this.checkClickOutside, true);
            }
            if (typeof onOpen === 'function') {
                onOpen(e);
            }
        };
        // Decide whether dropdown should be closed when mouse leaves element
        // Only for nested dropdowns
        this.handleMouseLeave = (e) => {
            const { isNestedDropdown } = this.props;
            if (!isNestedDropdown) {
                return;
            }
            const toElement = e.relatedTarget;
            try {
                if (this.dropdownMenu &&
                    (!(toElement instanceof Element) || !this.dropdownMenu.contains(toElement))) {
                    this.mouseLeaveId = window.setTimeout(() => {
                        this.handleClose(e);
                    }, constants_1.MENU_CLOSE_DELAY);
                }
            }
            catch (err) {
                Sentry.withScope(scope => {
                    scope.setExtra('event', e);
                    scope.setExtra('relatedTarget', e.relatedTarget);
                    Sentry.captureException(err);
                });
            }
        };
        // Closes dropdown menu
        this.handleClose = (e) => {
            const { onClose, isOpen, alwaysRenderMenu, isNestedDropdown } = this.props;
            const isControlled = typeof isOpen !== 'undefined';
            if (!isControlled) {
                this.setState({ isOpen: false });
            }
            // Clean up click handlers when the menu is closed for menus that are always rendered,
            // otherwise the click handlers get cleaned up when menu is unmounted
            if (alwaysRenderMenu || isNestedDropdown) {
                document.removeEventListener('click', this.checkClickOutside, true);
            }
            if (typeof onClose === 'function') {
                onClose(e);
            }
        };
        // When dropdown menu is displayed and mounted to DOM,
        // bind a click handler to `document` to listen for clicks outside of
        // this component and close menu if so
        this.handleMenuMount = (ref) => {
            if (ref && !(ref instanceof Element)) {
                return;
            }
            const { alwaysRenderMenu, isNestedDropdown } = this.props;
            this.dropdownMenu = ref;
            // Don't add document event listeners here if we are always rendering menu
            // Instead add when menu is opened
            if (alwaysRenderMenu || isNestedDropdown) {
                return;
            }
            if (this.dropdownMenu) {
                // 3rd arg = useCapture = so event capturing vs event bubbling
                document.addEventListener('click', this.checkClickOutside, true);
            }
            else {
                document.removeEventListener('click', this.checkClickOutside, true);
            }
        };
        this.handleActorMount = (ref) => {
            if (ref && !(ref instanceof Element)) {
                return;
            }
            this.dropdownActor = ref;
        };
        this.handleToggle = (e) => {
            if (this.isOpen()) {
                this.handleClose(e);
            }
            else {
                this.handleOpen(e);
            }
        };
        // Control whether we should hide dropdown menu when it is clicked
        this.handleDropdownMenuClick = (e) => {
            if (this.props.keepMenuOpen) {
                return;
            }
            this.handleClose(e);
        };
        // Actor is the component that will open the dropdown menu
        this.getActorProps = (_a = {}) => {
            var { onClick, onMouseEnter, onMouseLeave, onKeyDown, style = {} } = _a, props = (0, tslib_1.__rest)(_a, ["onClick", "onMouseEnter", "onMouseLeave", "onKeyDown", "style"]);
            const { isNestedDropdown, closeOnEscape } = this.props;
            const refProps = { ref: this.handleActorMount };
            // Props that the actor needs to have <DropdownMenu> work
            return Object.assign(Object.assign(Object.assign({}, props), refProps), { style: Object.assign(Object.assign({}, style), { outline: 'none' }), onKeyDown: (e) => {
                    if (typeof onKeyDown === 'function') {
                        onKeyDown(e);
                    }
                    if (e.key === 'Escape' && closeOnEscape) {
                        this.handleClose(e);
                    }
                }, onMouseEnter: (e) => {
                    if (typeof onMouseEnter === 'function') {
                        onMouseEnter(e);
                    }
                    // Only handle mouse enter for nested dropdowns
                    if (!isNestedDropdown) {
                        return;
                    }
                    if (this.mouseLeaveId) {
                        window.clearTimeout(this.mouseLeaveId);
                    }
                    this.mouseEnterId = window.setTimeout(() => {
                        this.handleOpen(e);
                    }, constants_1.MENU_CLOSE_DELAY);
                }, onMouseLeave: (e) => {
                    if (typeof onMouseLeave === 'function') {
                        onMouseLeave(e);
                    }
                    if (this.mouseEnterId) {
                        window.clearTimeout(this.mouseEnterId);
                    }
                    this.handleMouseLeave(e);
                }, onClick: (e) => {
                    // If we are a nested dropdown, clicking the actor
                    // should be a no-op so that the menu doesn't close.
                    if (isNestedDropdown) {
                        e.preventDefault();
                        e.stopPropagation();
                        return;
                    }
                    this.handleToggle(e);
                    if (typeof onClick === 'function') {
                        onClick(e);
                    }
                } });
        };
        // Menu is the menu component that <DropdownMenu> will control
        this.getMenuProps = (_a = {}) => {
            var { onClick, onMouseLeave, onMouseEnter } = _a, props = (0, tslib_1.__rest)(_a, ["onClick", "onMouseLeave", "onMouseEnter"]);
            const refProps = { ref: this.handleMenuMount };
            // Props that the menu needs to have <DropdownMenu> work
            return Object.assign(Object.assign(Object.assign({}, props), refProps), { onMouseEnter: (e) => {
                    if (typeof onMouseEnter === 'function') {
                        onMouseEnter(e);
                    }
                    // There is a delay before closing a menu on mouse leave, cancel this action if mouse enters menu again
                    if (this.mouseLeaveId) {
                        window.clearTimeout(this.mouseLeaveId);
                    }
                }, onMouseLeave: (e) => {
                    if (typeof onMouseLeave === 'function') {
                        onMouseLeave(e);
                    }
                    this.handleMouseLeave(e);
                }, onClick: (e) => {
                    this.handleDropdownMenuClick(e);
                    if (typeof onClick === 'function') {
                        onClick(e);
                    }
                } });
        };
    }
    componentWillUnmount() {
        document.removeEventListener('click', this.checkClickOutside, true);
    }
    getRootProps(props) {
        return props;
    }
    render() {
        const { children } = this.props;
        // Default anchor = left
        const shouldShowDropdown = this.isOpen();
        return children({
            isOpen: shouldShowDropdown,
            getRootProps: this.getRootProps,
            getActorProps: this.getActorProps,
            getMenuProps: this.getMenuProps,
            actions: {
                open: this.handleOpen,
                close: this.handleClose,
            },
        });
    }
}
DropdownMenu.defaultProps = {
    keepMenuOpen: false,
    closeOnEscape: true,
};
exports.default = DropdownMenu;
//# sourceMappingURL=dropdownMenu.jsx.map