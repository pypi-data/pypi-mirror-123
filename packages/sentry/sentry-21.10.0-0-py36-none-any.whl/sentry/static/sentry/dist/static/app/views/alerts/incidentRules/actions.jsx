Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteRule = exports.addOrUpdateRule = void 0;
const tslib_1 = require("tslib");
function isSavedRule(rule) {
    return !!rule.id;
}
/**
 * Add a new rule or update an existing rule
 *
 * @param api API Client
 * @param orgId Organization slug
 * @param rule Saved or Unsaved Metric Rule
 * @param query Query parameters for the request eg - referrer
 */
function addOrUpdateRule(api, orgId, projectId, rule, query) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const isExisting = isSavedRule(rule);
        const endpoint = `/projects/${orgId}/${projectId}/alert-rules/${isSavedRule(rule) ? `${rule.id}/` : ''}`;
        const method = isExisting ? 'PUT' : 'POST';
        return api.requestPromise(endpoint, {
            method,
            data: rule,
            query,
            includeAllArgs: true,
        });
    });
}
exports.addOrUpdateRule = addOrUpdateRule;
/**
 * Delete an existing rule
 *
 * @param api API Client
 * @param orgId Organization slug
 * @param rule Saved or Unsaved Metric Rule
 */
function deleteRule(api, orgId, rule) {
    return api.requestPromise(`/organizations/${orgId}/alert-rules/${rule.id}/`, {
        method: 'DELETE',
    });
}
exports.deleteRule = deleteRule;
//# sourceMappingURL=actions.jsx.map