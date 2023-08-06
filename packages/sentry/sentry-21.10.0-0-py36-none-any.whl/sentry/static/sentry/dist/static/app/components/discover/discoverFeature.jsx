Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const locale_1 = require("app/locale");
/**
 * Provide a component that passes a prop to indicate if the current
 * organization doesn't have access to discover results.
 */
function DiscoverFeature({ children }) {
    const noFeatureMessage = (0, locale_1.t)('Requires discover feature.');
    const renderDisabled = p => (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
      {p.children(p)}
    </hovercard_1.default>);
    return (<feature_1.default hookName="feature-disabled:open-discover" features={['organizations:discover-basic']} renderDisabled={renderDisabled}>
      {({ hasFeature }) => children({ hasFeature })}
    </feature_1.default>);
}
exports.default = DiscoverFeature;
//# sourceMappingURL=discoverFeature.jsx.map