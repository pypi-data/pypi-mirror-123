Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const documentationSetup_1 = (0, tslib_1.__importDefault)(require("./documentationSetup"));
const integrationSetup_1 = (0, tslib_1.__importDefault)(require("./integrationSetup"));
const otherSetup_1 = (0, tslib_1.__importDefault)(require("./otherSetup"));
const SdkConfiguration = (props) => {
    const parsed = qs.parse(window.location.search);
    const { platform } = props;
    const integrationSlug = platform && integrationUtil_1.platformToIntegrationMap[platform];
    // check for manual override query param
    if (integrationSlug && parsed.manual !== '1') {
        return <integrationSetup_1.default integrationSlug={integrationSlug} {...props}/>;
    }
    else if (platform === 'other') {
        return <otherSetup_1.default {...props}/>;
    }
    return <documentationSetup_1.default {...props}/>;
};
exports.default = SdkConfiguration;
//# sourceMappingURL=sdkConfiguration.jsx.map