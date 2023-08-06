Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteExternalIssue = void 0;
const tslib_1 = require("tslib");
const platformExternalIssueActions_1 = (0, tslib_1.__importDefault)(require("app/actions/platformExternalIssueActions"));
function deleteExternalIssue(api, groupId, externalIssueId) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        platformExternalIssueActions_1.default.delete(groupId, externalIssueId);
        try {
            const data = yield api.requestPromise(`/issues/${groupId}/external-issues/${externalIssueId}/`, {
                method: 'DELETE',
            });
            platformExternalIssueActions_1.default.deleteSuccess(data);
            return data;
        }
        catch (error) {
            platformExternalIssueActions_1.default.deleteError(error);
            throw error;
        }
    });
}
exports.deleteExternalIssue = deleteExternalIssue;
//# sourceMappingURL=platformExternalIssues.jsx.map