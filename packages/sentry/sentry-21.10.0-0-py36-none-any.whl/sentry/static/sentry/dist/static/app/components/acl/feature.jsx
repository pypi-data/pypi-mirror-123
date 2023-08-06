Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const isRenderFunc_1 = require("app/utils/isRenderFunc");
const withConfig_1 = (0, tslib_1.__importDefault)(require("app/utils/withConfig"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProject_1 = (0, tslib_1.__importDefault)(require("app/utils/withProject"));
const comingSoon_1 = (0, tslib_1.__importDefault)(require("./comingSoon"));
/**
 * Component to handle feature flags.
 */
class Feature extends React.Component {
    getAllFeatures() {
        const { organization, project, config } = this.props;
        return {
            configFeatures: config.features ? Array.from(config.features) : [],
            organization: (organization && organization.features) || [],
            project: (project && project.features) || [],
        };
    }
    hasFeature(feature, features) {
        const shouldMatchOnlyProject = feature.match(/^projects:(.+)/);
        const shouldMatchOnlyOrg = feature.match(/^organizations:(.+)/);
        // Array of feature strings
        const { configFeatures, organization, project } = features;
        // Check config store first as this overrides features scoped to org or
        // project contexts.
        if (configFeatures.includes(feature)) {
            return true;
        }
        if (shouldMatchOnlyProject) {
            return project.includes(shouldMatchOnlyProject[1]);
        }
        if (shouldMatchOnlyOrg) {
            return organization.includes(shouldMatchOnlyOrg[1]);
        }
        // default, check all feature arrays
        return organization.includes(feature) || project.includes(feature);
    }
    render() {
        const { children, features, renderDisabled, hookName, organization, project, requireAll, } = this.props;
        const allFeatures = this.getAllFeatures();
        const method = requireAll ? 'every' : 'some';
        const hasFeature = !features || features[method](feat => this.hasFeature(feat, allFeatures));
        // Default renderDisabled to the ComingSoon component
        let customDisabledRender = renderDisabled === false
            ? false
            : typeof renderDisabled === 'function'
                ? renderDisabled
                : () => <comingSoon_1.default />;
        // Override the renderDisabled function with a hook store function if there
        // is one registered for the feature.
        if (hookName) {
            const hooks = hookStore_1.default.get(hookName);
            if (hooks.length > 0) {
                customDisabledRender = hooks[0];
            }
        }
        const renderProps = {
            organization,
            project,
            features,
            hasFeature,
        };
        if (!hasFeature && customDisabledRender !== false) {
            return customDisabledRender(Object.assign({ children }, renderProps));
        }
        if ((0, isRenderFunc_1.isRenderFunc)(children)) {
            return children(Object.assign({ renderDisabled }, renderProps));
        }
        return hasFeature && children ? children : null;
    }
}
Feature.defaultProps = {
    renderDisabled: false,
    requireAll: true,
};
exports.default = (0, withOrganization_1.default)((0, withProject_1.default)((0, withConfig_1.default)(Feature)));
//# sourceMappingURL=feature.jsx.map