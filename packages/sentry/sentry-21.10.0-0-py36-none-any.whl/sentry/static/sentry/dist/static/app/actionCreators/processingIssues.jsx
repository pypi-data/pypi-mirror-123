Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchProcessingIssues = void 0;
function fetchProcessingIssues(api, orgId, projectIds = null) {
    return api.requestPromise(`/organizations/${orgId}/processingissues/`, {
        method: 'GET',
        query: projectIds ? { project: projectIds } : [],
    });
}
exports.fetchProcessingIssues = fetchProcessingIssues;
//# sourceMappingURL=processingIssues.jsx.map