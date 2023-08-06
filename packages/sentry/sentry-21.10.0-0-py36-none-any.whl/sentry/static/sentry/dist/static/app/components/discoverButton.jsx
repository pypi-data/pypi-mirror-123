Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const discoverFeature_1 = (0, tslib_1.__importDefault)(require("app/components/discover/discoverFeature"));
/**
 * Provide a button that turns itself off if the current organization
 * doesn't have access to discover results.
 */
function DiscoverButton(_a) {
    var { children } = _a, buttonProps = (0, tslib_1.__rest)(_a, ["children"]);
    return (<discoverFeature_1.default>
      {({ hasFeature }) => (<button_1.default disabled={!hasFeature} {...buttonProps}>
          {children}
        </button_1.default>)}
    </discoverFeature_1.default>);
}
exports.default = DiscoverButton;
//# sourceMappingURL=discoverButton.jsx.map