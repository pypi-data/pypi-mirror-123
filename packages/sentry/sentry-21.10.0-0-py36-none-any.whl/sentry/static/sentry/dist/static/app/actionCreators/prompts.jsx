Object.defineProperty(exports, "__esModule", { value: true });
exports.batchedPromptsCheck = exports.promptsCheck = exports.promptsUpdate = void 0;
const tslib_1 = require("tslib");
/**
 * Update the status of a prompt
 */
function promptsUpdate(api, params) {
    return api.requestPromise('/prompts-activity/', {
        method: 'PUT',
        data: {
            organization_id: params.organizationId,
            project_id: params.projectId,
            feature: params.feature,
            status: params.status,
        },
    });
}
exports.promptsUpdate = promptsUpdate;
/**
 * Get the status of a prompt
 */
function promptsCheck(api, params) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const query = Object.assign({ feature: params.feature, organization_id: params.organizationId }, (params.projectId === undefined ? {} : { project_id: params.projectId }));
        const response = yield api.requestPromise('/prompts-activity/', {
            query,
        });
        const data = response === null || response === void 0 ? void 0 : response.data;
        if (!data) {
            return null;
        }
        return {
            dismissedTime: data.dismissed_ts,
            snoozedTime: data.snoozed_ts,
        };
    });
}
exports.promptsCheck = promptsCheck;
/**
 * Get the status of many prompt
 */
function batchedPromptsCheck(api, features, params) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const query = Object.assign({ feature: features, organization_id: params.organizationId }, (params.projectId === undefined ? {} : { project_id: params.projectId }));
        const response = yield api.requestPromise('/prompts-activity/', {
            query,
        });
        const responseFeatures = response === null || response === void 0 ? void 0 : response.features;
        const result = {};
        if (!responseFeatures) {
            return result;
        }
        for (const featureName of features) {
            const item = responseFeatures[featureName];
            if (item) {
                result[featureName] = {
                    dismissedTime: item.dismissed_ts,
                    snoozedTime: item.snoozed_ts,
                };
            }
            else {
                result[featureName] = null;
            }
        }
        return result;
    });
}
exports.batchedPromptsCheck = batchedPromptsCheck;
//# sourceMappingURL=prompts.jsx.map