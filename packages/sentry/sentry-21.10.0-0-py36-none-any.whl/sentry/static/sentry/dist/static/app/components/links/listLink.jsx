Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
class ListLink extends React.Component {
    constructor() {
        super(...arguments);
        this.getClassName = () => {
            const _classNames = {};
            const { className, activeClassName } = this.props;
            if (className) {
                _classNames[className] = true;
            }
            if (this.isActive() && activeClassName) {
                _classNames[activeClassName] = true;
            }
            return (0, classnames_1.default)(_classNames);
        };
    }
    isActive() {
        const { isActive, to, query, index, router } = this.props;
        const queryData = query ? qs.parse(query) : undefined;
        const target = typeof to === 'string' ? { pathname: to, query: queryData } : to;
        if (typeof isActive === 'function') {
            return isActive(target, index);
        }
        return router.isActive(target, index);
    }
    render() {
        const _a = this.props, { index, children, to, disabled } = _a, props = (0, tslib_1.__rest)(_a, ["index", "children", "to", "disabled"]);
        const carriedProps = (0, omit_1.default)(props, 'activeClassName', 'css', 'isActive', 'index', 'router', 'location');
        return (<StyledLi className={this.getClassName()} disabled={disabled}>
        <react_router_1.Link {...carriedProps} onlyActiveOnIndex={index} to={disabled ? '' : to}>
          {children}
        </react_router_1.Link>
      </StyledLi>);
    }
}
ListLink.displayName = 'ListLink';
ListLink.defaultProps = {
    activeClassName: 'active',
    index: false,
    disabled: false,
};
exports.default = (0, react_router_1.withRouter)(ListLink);
const StyledLi = (0, styled_1.default)('li', {
    shouldForwardProp: prop => prop !== 'disabled',
}) `
  ${p => p.disabled &&
    `
   a {
    color:${p.theme.disabled} !important;
    pointer-events: none;
    :hover {
      color: ${p.theme.disabled}  !important;
    }
   }
`}
`;
//# sourceMappingURL=listLink.jsx.map