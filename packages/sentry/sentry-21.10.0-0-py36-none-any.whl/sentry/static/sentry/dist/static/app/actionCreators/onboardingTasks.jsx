Object.defineProperty(exports, "__esModule", { value: true });
exports.updateOnboardingTask = void 0;
const tslib_1 = require("tslib");
const organizationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationActions"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
/**
 * Update an onboarding task.
 *
 * If no API client is provided the task will not be updated on the server side
 * and will only update in the organization store.
 */
function updateOnboardingTask(api, organization, updatedTask) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        if (api !== null) {
            api.requestPromise(`/organizations/${organization.slug}/onboarding-tasks/`, {
                method: 'POST',
                data: updatedTask,
            });
        }
        const hasExistingTask = organization.onboardingTasks.find(task => task.task === updatedTask.task);
        const user = configStore_1.default.get('user');
        const onboardingTasks = hasExistingTask
            ? organization.onboardingTasks.map(task => task.task === updatedTask.task ? Object.assign(Object.assign({}, task), updatedTask) : task)
            : [...organization.onboardingTasks, Object.assign(Object.assign({}, updatedTask), { user })];
        organizationActions_1.default.update({ onboardingTasks });
    });
}
exports.updateOnboardingTask = updateOnboardingTask;
//# sourceMappingURL=onboardingTasks.jsx.map