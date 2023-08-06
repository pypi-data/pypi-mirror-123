Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
/**
 * Component to handle demo mode switches
 */
function DemoModeGate(props) {
    const { organization, children, demoComponent = null } = props;
    if ((organization === null || organization === void 0 ? void 0 : organization.role) === 'member' && configStore_1.default.get('demoMode')) {
        if (typeof demoComponent === 'function') {
            return demoComponent({ children });
        }
        return demoComponent;
    }
    return children;
}
exports.default = (0, withOrganization_1.default)(DemoModeGate);
//# sourceMappingURL=demoModeGate.jsx.map