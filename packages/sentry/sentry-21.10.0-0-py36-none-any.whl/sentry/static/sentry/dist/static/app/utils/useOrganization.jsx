Object.defineProperty(exports, "__esModule", { value: true });
exports.useOrgSlug = exports.useOrganization = void 0;
const react_1 = require("react");
const organizationContext_1 = require("app/views/organizationContext");
function useOrganization() {
    const organization = (0, react_1.useContext)(organizationContext_1.OrganizationContext);
    if (!organization) {
        throw new Error('useOrganization called but organization is not set.');
    }
    return organization;
}
exports.useOrganization = useOrganization;
function useOrgSlug() {
    return useOrganization().slug;
}
exports.useOrgSlug = useOrgSlug;
//# sourceMappingURL=useOrganization.jsx.map