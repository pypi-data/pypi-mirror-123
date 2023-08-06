Object.defineProperty(exports, "__esModule", { value: true });
exports.toResourcePermissions = exports.toPermissions = void 0;
const tslib_1 = require("tslib");
const groupBy_1 = (0, tslib_1.__importDefault)(require("lodash/groupBy"));
const invertBy_1 = (0, tslib_1.__importDefault)(require("lodash/invertBy"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const PERMISSION_LEVELS = {
    read: 0,
    write: 1,
    admin: 2,
};
const HUMAN_RESOURCE_NAMES = {
    project: 'Project',
    team: 'Team',
    release: 'Release',
    event: 'Event',
    org: 'Organization',
    member: 'Member',
};
const DEFAULT_RESOURCE_PERMISSIONS = {
    Project: 'no-access',
    Team: 'no-access',
    Release: 'no-access',
    Event: 'no-access',
    Organization: 'no-access',
    Member: 'no-access',
};
const PROJECT_RELEASES = 'project:releases';
/**
 * Numerical value of the scope where Admin is higher than Write,
 * which is higher than Read. Used to sort scopes by access.
 */
const permissionLevel = (scope) => {
    const permission = scope.split(':')[1];
    return PERMISSION_LEVELS[permission];
};
const compareScopes = (a, b) => permissionLevel(a) - permissionLevel(b);
/**
 * Return the most permissive scope for each resource.
 *
 * Example:
 *    Given the full list of scopes:
 *      ['project:read', 'project:write', 'team:read', 'team:write', 'team:admin']
 *
 *    this would return:
 *      ['project:write', 'team:admin']
 */
function topScopes(scopeList) {
    return Object.values((0, groupBy_1.default)(scopeList, scope => scope.split(':')[0]))
        .map(scopes => scopes.sort(compareScopes))
        .map(scopes => scopes.pop());
}
/**
 * Convert into a list of Permissions, grouped by resource.
 *
 * This is used in the new/edit Sentry App form. That page displays permissions
 * in a per-Resource manner, meaning one row for Project, one for Organization, etc.
 *
 * This exposes scopes in a way that works for that UI.
 *
 * Example:
 *    {
 *      'Project': 'read',
 *      'Organization': 'write',
 *      'Team': 'no-access',
 *      ...
 *    }
 */
function toResourcePermissions(scopes) {
    const permissions = Object.assign({}, DEFAULT_RESOURCE_PERMISSIONS);
    let filteredScopes = [...scopes];
    // The scope for releases is `project:releases`, but instead of displaying
    // it as a permission of Project, we want to separate it out into its own
    // row for Releases.
    if (scopes.includes(PROJECT_RELEASES)) {
        permissions.Release = 'admin';
        filteredScopes = scopes.filter((scope) => scope !== PROJECT_RELEASES); // remove project:releases
    }
    topScopes(filteredScopes).forEach((scope) => {
        if (scope) {
            const [resource, permission] = scope.split(':');
            permissions[HUMAN_RESOURCE_NAMES[resource]] = permission;
        }
    });
    return permissions;
}
exports.toResourcePermissions = toResourcePermissions;
/**
 * Convert into a list of Permissions, grouped by access and including a
 * list of resources per access level.
 *
 * This is used in the Permissions Modal when installing an App. It displays
 * scopes in a per-Permission way, meaning one row for Read, one for Write,
 * and one for Admin.
 *
 * This exposes scopes in a way that works for that UI.
 *
 * Example:
 *    {
 *      read:  ['Project', 'Organization'],
 *      write: ['Member'],
 *      admin: ['Release']
 *    }
 */
function toPermissions(scopes) {
    const defaultPermissions = { read: [], write: [], admin: [] };
    const resourcePermissions = toResourcePermissions(scopes);
    // Filter out the 'no-access' permissions
    const permissions = (0, pick_1.default)((0, invertBy_1.default)(resourcePermissions), ['read', 'write', 'admin']);
    return Object.assign(Object.assign({}, defaultPermissions), permissions);
}
exports.toPermissions = toPermissions;
//# sourceMappingURL=consolidatedScopes.jsx.map