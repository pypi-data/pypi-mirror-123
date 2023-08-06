Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const navigationConfiguration_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/navigationConfiguration"));
const settingsNavigation_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsNavigation"));
const AccountSettingsNavigation = ({ organization }) => (<settingsNavigation_1.default navigationObjects={(0, navigationConfiguration_1.default)({ organization })}/>);
exports.default = AccountSettingsNavigation;
//# sourceMappingURL=accountSettingsNavigation.jsx.map