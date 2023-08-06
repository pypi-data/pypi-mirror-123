Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const platform_1 = (0, tslib_1.__importDefault)(require("./platform"));
const platformIntegrationSetup_1 = (0, tslib_1.__importDefault)(require("./platformIntegrationSetup"));
const PlatformOrIntegration = (props) => {
    const parsed = qs.parse(window.location.search);
    const { platform } = props.params;
    const integrationSlug = platform && integrationUtil_1.platformToIntegrationMap[platform];
    // check for manual override query param
    if (integrationSlug && parsed.manual !== '1') {
        return <platformIntegrationSetup_1.default integrationSlug={integrationSlug} {...props}/>;
    }
    return <platform_1.default {...props}/>;
};
exports.default = PlatformOrIntegration;
//# sourceMappingURL=platformOrIntegration.jsx.map