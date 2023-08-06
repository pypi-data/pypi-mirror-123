Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchOrganizationDetails = exports.fetchOrganizationByMember = exports.updateOrganization = exports.changeOrganizationSlug = exports.setActiveOrganization = exports.removeAndRedirectToRemainingOrganization = exports.switchOrganization = exports.remove = exports.redirectToRemainingOrganization = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const globalSelection_1 = require("app/actionCreators/globalSelection");
const indicator_1 = require("app/actionCreators/indicator");
const organizationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationActions"));
const organizationsActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationsActions"));
const api_1 = require("app/api");
const organizationsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationsStore"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
/**
 * After removing an organization, this will redirect to a remaining active organization or
 * the screen to create a new organization.
 *
 * Can optionally remove organization from organizations store.
 */
function redirectToRemainingOrganization({ orgId, removeOrg, }) {
    // Remove queued, should redirect
    const allOrgs = organizationsStore_1.default.getAll().filter(org => org.status.id === 'active' && org.slug !== orgId);
    if (!allOrgs.length) {
        react_router_1.browserHistory.push('/organizations/new/');
        return;
    }
    // Let's be smart and select the best org to redirect to
    const firstRemainingOrg = allOrgs[0];
    react_router_1.browserHistory.push(`/${firstRemainingOrg.slug}/`);
    // Remove org from SidebarDropdown
    if (removeOrg) {
        organizationsStore_1.default.remove(orgId);
    }
}
exports.redirectToRemainingOrganization = redirectToRemainingOrganization;
function remove(api, { successMessage, errorMessage, orgId }) {
    const endpoint = `/organizations/${orgId}/`;
    return api
        .requestPromise(endpoint, {
        method: 'DELETE',
    })
        .then(() => {
        organizationsActions_1.default.removeSuccess(orgId);
        if (successMessage) {
            (0, indicator_1.addSuccessMessage)(successMessage);
        }
    })
        .catch(() => {
        organizationsActions_1.default.removeError();
        if (errorMessage) {
            (0, indicator_1.addErrorMessage)(errorMessage);
        }
    });
}
exports.remove = remove;
function switchOrganization() {
    (0, globalSelection_1.resetGlobalSelection)();
}
exports.switchOrganization = switchOrganization;
function removeAndRedirectToRemainingOrganization(api, params) {
    remove(api, params).then(() => redirectToRemainingOrganization(params));
}
exports.removeAndRedirectToRemainingOrganization = removeAndRedirectToRemainingOrganization;
/**
 * Set active organization
 */
function setActiveOrganization(org) {
    organizationsActions_1.default.setActive(org);
}
exports.setActiveOrganization = setActiveOrganization;
function changeOrganizationSlug(prev, next) {
    organizationsActions_1.default.changeSlug(prev, next);
}
exports.changeOrganizationSlug = changeOrganizationSlug;
/**
 * Updates an organization for the store
 *
 * Accepts a partial organization as it will merge will existing organization
 */
function updateOrganization(org) {
    organizationsActions_1.default.update(org);
    organizationActions_1.default.update(org);
}
exports.updateOrganization = updateOrganization;
function fetchOrganizationByMember(memberId, { addOrg, fetchOrgDetails }) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const api = new api_1.Client();
        const data = yield api.requestPromise(`/organizations/?query=member_id:${memberId}`);
        if (!data.length) {
            return null;
        }
        const org = data[0];
        if (addOrg) {
            // add org to SwitchOrganization dropdown
            organizationsStore_1.default.add(org);
        }
        if (fetchOrgDetails) {
            // load SidebarDropdown with org details including `access`
            yield fetchOrganizationDetails(org.slug, { setActive: true, loadProjects: true });
        }
        return org;
    });
}
exports.fetchOrganizationByMember = fetchOrganizationByMember;
function fetchOrganizationDetails(orgId, { setActive, loadProjects, loadTeam }) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const api = new api_1.Client();
        const data = yield api.requestPromise(`/organizations/${orgId}/`);
        if (setActive) {
            setActiveOrganization(data);
        }
        if (loadTeam) {
            teamStore_1.default.loadInitialData(data.teams);
        }
        if (loadProjects) {
            projectsStore_1.default.loadInitialData(data.projects || []);
        }
        return data;
    });
}
exports.fetchOrganizationDetails = fetchOrganizationDetails;
//# sourceMappingURL=organizations.jsx.map