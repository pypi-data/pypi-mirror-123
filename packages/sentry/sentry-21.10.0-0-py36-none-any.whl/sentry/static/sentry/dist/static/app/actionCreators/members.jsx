Object.defineProperty(exports, "__esModule", { value: true });
exports.getCurrentMember = exports.resendMemberInvite = exports.updateMember = exports.indexMembersByProject = exports.fetchOrgMembers = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const memberActions_1 = (0, tslib_1.__importDefault)(require("app/actions/memberActions"));
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
function getMemberUser(member) {
    return Object.assign(Object.assign({}, member.user), { role: member.role });
}
function fetchOrgMembers(api, orgId, projectIds = null) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const endpoint = `/organizations/${orgId}/users/`;
        const query = projectIds ? { project: projectIds } : {};
        try {
            const members = yield api.requestPromise(endpoint, { method: 'GET', query });
            if (!members) {
                // This shouldn't happen if the request was successful
                // It should at least be an empty list
                Sentry.withScope(scope => {
                    scope.setExtras({
                        orgId,
                        projectIds,
                    });
                    Sentry.captureException(new Error('Members is undefined'));
                });
            }
            const memberUsers = members === null || members === void 0 ? void 0 : members.filter(({ user }) => user);
            if (!memberUsers) {
                return [];
            }
            // Update the store with just the users, as avatars rely on them.
            memberListStore_1.default.loadInitialData(memberUsers.map(getMemberUser));
            return members;
        }
        catch (err) {
            Sentry.setExtras({
                resp: err,
            });
            Sentry.captureException(err);
        }
        return [];
    });
}
exports.fetchOrgMembers = fetchOrgMembers;
/**
 * Convert a list of members with user & project data
 * into a object that maps project slugs : users in that project.
 */
function indexMembersByProject(members) {
    return members.reduce((acc, member) => {
        for (const project of member.projects) {
            if (!acc.hasOwnProperty(project)) {
                acc[project] = [];
            }
            acc[project].push(member.user);
        }
        return acc;
    }, {});
}
exports.indexMembersByProject = indexMembersByProject;
function updateMember(api, { orgId, memberId, data }) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        memberActions_1.default.update(memberId, data);
        const endpoint = `/organizations/${orgId}/members/${memberId}/`;
        try {
            const resp = yield api.requestPromise(endpoint, {
                method: 'PUT',
                data,
            });
            memberActions_1.default.updateSuccess(resp);
            return resp;
        }
        catch (err) {
            memberActions_1.default.updateError(err);
            throw err;
        }
    });
}
exports.updateMember = updateMember;
function resendMemberInvite(api, { orgId, memberId, regenerate, data }) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        memberActions_1.default.resendMemberInvite(orgId, data);
        const endpoint = `/organizations/${orgId}/members/${memberId}/`;
        try {
            const resp = yield api.requestPromise(endpoint, {
                method: 'PUT',
                data: {
                    regenerate,
                    reinvite: true,
                },
            });
            memberActions_1.default.resendMemberInviteSuccess(resp);
            return resp;
        }
        catch (err) {
            memberActions_1.default.resendMemberInviteError(err);
            throw err;
        }
    });
}
exports.resendMemberInvite = resendMemberInvite;
function getCurrentMember(api, orgId) {
    return api.requestPromise(`/organizations/${orgId}/members/me/`);
}
exports.getCurrentMember = getCurrentMember;
//# sourceMappingURL=members.jsx.map