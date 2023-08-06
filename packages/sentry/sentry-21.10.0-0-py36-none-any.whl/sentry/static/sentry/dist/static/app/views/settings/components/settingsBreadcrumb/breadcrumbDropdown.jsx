Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const menu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete/menu"));
const crumb_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/crumb"));
const divider_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/divider"));
const EXIT_DELAY = 0;
class BreadcrumbDropdown extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isOpen: false,
        };
        this.entering = null;
        this.leaving = null;
        this.open = () => {
            this.setState({ isOpen: true });
        };
        this.close = () => {
            this.setState({ isOpen: false });
        };
        this.handleStateChange = () => { };
        // Adds a delay when mouse hovers on actor (in this case the breadcrumb)
        this.handleMouseEnterActor = () => {
            var _a;
            if (this.leaving) {
                clearTimeout(this.leaving);
            }
            this.entering = window.setTimeout(() => this.open(), (_a = this.props.enterDelay) !== null && _a !== void 0 ? _a : 0);
        };
        // handles mouseEnter event on actor and menu, should clear the leaving timeout and keep menu open
        this.handleMouseEnter = () => {
            if (this.leaving) {
                clearTimeout(this.leaving);
            }
            this.open();
        };
        // handles mouseLeave event on actor and menu, adds a timeout before updating state to account for
        // mouseLeave into
        this.handleMouseLeave = () => {
            if (this.entering) {
                clearTimeout(this.entering);
            }
            this.leaving = window.setTimeout(() => this.close(), EXIT_DELAY);
        };
        // Close immediately when actor is clicked clicked
        this.handleClickActor = () => {
            this.close();
        };
        // Close immediately when clicked outside
        this.handleClose = () => {
            this.close();
        };
    }
    render() {
        const _a = this.props, { hasMenu, route, isLast, name, items, onSelect } = _a, dropdownProps = (0, tslib_1.__rest)(_a, ["hasMenu", "route", "isLast", "name", "items", "onSelect"]);
        return (<menu_1.default blendCorner={false} onOpen={this.handleMouseEnter} onClose={this.close} isOpen={this.state.isOpen} menuProps={{
                onMouseEnter: this.handleMouseEnter,
                onMouseLeave: this.handleMouseLeave,
            }} items={items} onSelect={onSelect} virtualizedHeight={41} {...dropdownProps}>
        {({ getActorProps, actions, isOpen }) => (<crumb_1.default {...getActorProps({
                onClick: this.handleClickActor.bind(this, actions),
                onMouseEnter: this.handleMouseEnterActor.bind(this, actions),
                onMouseLeave: this.handleMouseLeave.bind(this, actions),
            })}>
            <span>{name || route.name} </span>
            <divider_1.default isHover={hasMenu && isOpen} isLast={isLast}/>
          </crumb_1.default>)}
      </menu_1.default>);
    }
}
exports.default = BreadcrumbDropdown;
//# sourceMappingURL=breadcrumbDropdown.jsx.map