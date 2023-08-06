Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
/**
 * A context-aware version of Link (from react-router) that falls
 * back to <a> if there is no router present
 */
const BaseLink = (_a) => {
    var { location, disabled, to, ref, router: _router, params: _params, routes: _routes } = _a, props = (0, tslib_1.__rest)(_a, ["location", "disabled", "to", "ref", "router", "params", "routes"]);
    (0, react_1.useEffect)(() => {
        // check if the router is present
        if (!location) {
            Sentry.captureException(new Error('The link component was rendered without being wrapped by a <Router />'));
        }
    }, []);
    if (!disabled && location) {
        return <react_router_1.Link to={to} ref={ref} {...props}/>;
    }
    if (typeof to === 'string') {
        return <Anchor href={to} ref={ref} disabled={disabled} {...props}/>;
    }
    return <Anchor href="" ref={ref} {...props} disabled/>;
};
// Set the displayName for testing convenience
BaseLink.displayName = 'Link';
// Re-assign to Link to make auto-importing smarter
const Link = (0, react_router_1.withRouter)(BaseLink);
exports.default = Link;
const Anchor = (0, styled_1.default)('a', {
    shouldForwardProp: prop => typeof prop === 'string' && (0, is_prop_valid_1.default)(prop) && prop !== 'disabled',
}) `
  ${p => p.disabled &&
    `
  color:${p.theme.disabled};
  pointer-events: none;
  :hover {
    color: ${p.theme.disabled};
  }
  `};
`;
//# sourceMappingURL=link.jsx.map