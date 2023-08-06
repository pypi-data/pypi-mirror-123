Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
const isRenderFunc_1 = require("app/utils/isRenderFunc");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class Role extends React.Component {
    hasRole() {
        var _a;
        const user = configStore_1.default.get('user');
        const { organization, role } = this.props;
        const { availableRoles } = organization;
        const currentRole = (_a = organization.role) !== null && _a !== void 0 ? _a : '';
        if (!user) {
            return false;
        }
        if ((0, isActiveSuperuser_1.isActiveSuperuser)()) {
            return true;
        }
        if (!Array.isArray(availableRoles)) {
            return false;
        }
        const roleIds = availableRoles.map(r => r.id);
        if (!roleIds.includes(role) || !roleIds.includes(currentRole)) {
            return false;
        }
        const requiredIndex = roleIds.indexOf(role);
        const currentIndex = roleIds.indexOf(currentRole);
        return currentIndex >= requiredIndex;
    }
    render() {
        const { children } = this.props;
        const hasRole = this.hasRole();
        if ((0, isRenderFunc_1.isRenderFunc)(children)) {
            return children({ hasRole });
        }
        return hasRole && children ? children : null;
    }
}
exports.default = (0, withOrganization_1.default)(Role);
//# sourceMappingURL=role.jsx.map