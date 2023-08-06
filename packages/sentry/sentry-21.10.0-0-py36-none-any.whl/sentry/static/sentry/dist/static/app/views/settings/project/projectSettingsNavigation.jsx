Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const appStoreConnectContext_1 = (0, tslib_1.__importDefault)(require("app/components/projects/appStoreConnectContext"));
const withProject_1 = (0, tslib_1.__importDefault)(require("app/utils/withProject"));
const settingsNavigation_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsNavigation"));
const navigationConfiguration_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/navigationConfiguration"));
const ProjectSettingsNavigation = ({ organization, project }) => {
    const appStoreConnectContext = (0, react_1.useContext)(appStoreConnectContext_1.default);
    const debugFilesNeedsReview = !!(appStoreConnectContext === null || appStoreConnectContext === void 0 ? void 0 : appStoreConnectContext.updateAlertMessage);
    return (<settingsNavigation_1.default navigationObjects={(0, navigationConfiguration_1.default)({ project, organization, debugFilesNeedsReview })} access={new Set(organization.access)} features={new Set(organization.features)} organization={organization} project={project}/>);
};
exports.default = (0, withProject_1.default)(ProjectSettingsNavigation);
//# sourceMappingURL=projectSettingsNavigation.jsx.map