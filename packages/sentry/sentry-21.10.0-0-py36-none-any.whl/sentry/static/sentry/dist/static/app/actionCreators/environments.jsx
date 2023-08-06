Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchOrganizationEnvironments = void 0;
const tslib_1 = require("tslib");
const environmentActions_1 = (0, tslib_1.__importDefault)(require("app/actions/environmentActions"));
/**
 * Fetches all environments for an organization
 *
 * @param organizationSlug The organization slug
 */
function fetchOrganizationEnvironments(api, organizationSlug) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        environmentActions_1.default.fetchEnvironments();
        try {
            const environments = yield api.requestPromise(`/organizations/${organizationSlug}/environments/`);
            if (!environments) {
                environmentActions_1.default.fetchEnvironmentsError(new Error('retrieved environments is falsey'));
                return;
            }
            environmentActions_1.default.fetchEnvironmentsSuccess(environments);
        }
        catch (err) {
            environmentActions_1.default.fetchEnvironmentsError(err);
        }
    });
}
exports.fetchOrganizationEnvironments = fetchOrganizationEnvironments;
//# sourceMappingURL=environments.jsx.map