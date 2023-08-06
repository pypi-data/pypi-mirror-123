Object.defineProperty(exports, "__esModule", { value: true });
exports.getMergedTasks = exports.getOnboardingTasks = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const utils_1 = require("app/components/onboardingWizard/utils");
const platformCategories_1 = require("app/data/platformCategories");
const locale_1 = require("app/locale");
const pulsingIndicator_1 = (0, tslib_1.__importDefault)(require("app/styles/pulsingIndicator"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const eventWaiter_1 = (0, tslib_1.__importDefault)(require("app/utils/eventWaiter"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
function hasPlatformWithSourceMaps(projects) {
    return projects !== undefined
        ? projects.some(({ platform }) => platform && platformCategories_1.sourceMaps.includes(platform))
        : false;
}
function getOnboardingTasks({ organization, projects, }) {
    return [
        {
            task: types_1.OnboardingTaskKey.FIRST_PROJECT,
            title: (0, locale_1.t)('Create a project'),
            description: (0, locale_1.t)("Monitor in seconds by adding a simple lines of code to your project. It's as easy as microwaving leftover pizza."),
            skippable: false,
            requisites: [],
            actionType: 'app',
            location: `/organizations/${organization.slug}/projects/new/`,
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.FIRST_EVENT,
            title: (0, locale_1.t)('Capture your first error'),
            description: (0, locale_1.t)("Time to test it out. Now that you've created a project, capture your first error. We've got an example you can fiddle with."),
            skippable: false,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'app',
            location: `/settings/${organization.slug}/projects/:projectId/install/`,
            display: true,
            SupplementComponent: (0, withApi_1.default)(({ api, task, onCompleteTask }) => !!(projects === null || projects === void 0 ? void 0 : projects.length) && task.requisiteTasks.length === 0 && !task.completionSeen ? (<eventWaiter_1.default api={api} organization={organization} project={projects[0]} eventType="error" onIssueReceived={() => !(0, utils_1.taskIsDone)(task) && onCompleteTask()}>
            {() => <EventWaitingIndicator />}
          </eventWaiter_1.default>) : null),
        },
        {
            task: types_1.OnboardingTaskKey.INVITE_MEMBER,
            title: (0, locale_1.t)('Invite your team'),
            description: (0, locale_1.t)('Assign issues and comment on shared errors with coworkers so you always know who to blame when sh*t hits the fan.'),
            skippable: true,
            requisites: [],
            actionType: 'action',
            action: () => (0, modal_1.openInviteMembersModal)({ source: 'onboarding_widget' }),
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.SECOND_PLATFORM,
            title: (0, locale_1.t)('Create another project'),
            description: (0, locale_1.t)('Easy, right? Don’t stop at one. Set up another project to keep things running smoothly in both the frontend and backend.'),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: `/organizations/${organization.slug}/projects/new/`,
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.FIRST_TRANSACTION,
            title: (0, locale_1.t)('Boost performance'),
            description: (0, locale_1.t)("Don't keep users waiting. Trace transactions, investigate spans and cross-reference related issues for those mission-critical endpoints."),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'external',
            location: 'https://docs.sentry.io/product/performance/getting-started/',
            display: true,
            SupplementComponent: (0, withApi_1.default)(({ api, task, onCompleteTask }) => !!(projects === null || projects === void 0 ? void 0 : projects.length) && task.requisiteTasks.length === 0 && !task.completionSeen ? (<eventWaiter_1.default api={api} organization={organization} project={projects[0]} eventType="transaction" onIssueReceived={() => !(0, utils_1.taskIsDone)(task) && onCompleteTask()}>
            {() => <EventWaitingIndicator />}
          </eventWaiter_1.default>) : null),
        },
        {
            task: types_1.OnboardingTaskKey.USER_CONTEXT,
            title: (0, locale_1.t)('Get more user context'),
            description: (0, locale_1.t)('Enable us to pinpoint which users are suffering from that bad code, so you can debug the problem more swiftly and maybe even apologize for it.'),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'external',
            location: 'https://docs.sentry.io/platform-redirect/?next=/enriching-events/identify-user/',
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.RELEASE_TRACKING,
            title: (0, locale_1.t)('Track releases'),
            description: (0, locale_1.t)('Take an in-depth look at the health of each and every release with crash analytics, errors, related issues and suspect commits.'),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: `/settings/${organization.slug}/projects/:projectId/release-tracking/`,
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.SOURCEMAPS,
            title: (0, locale_1.t)('Upload source maps'),
            description: (0, locale_1.t)("Deminify Javascript source code to debug with context. Seeing code in it's original form will help you debunk the ghosts of errors past."),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'external',
            location: 'https://docs.sentry.io/platforms/javascript/sourcemaps/',
            display: hasPlatformWithSourceMaps(projects),
        },
        {
            task: types_1.OnboardingTaskKey.USER_REPORTS,
            title: 'User crash reports',
            description: (0, locale_1.t)('Collect user feedback when your application crashes'),
            skippable: true,
            requisites: [
                types_1.OnboardingTaskKey.FIRST_PROJECT,
                types_1.OnboardingTaskKey.FIRST_EVENT,
                types_1.OnboardingTaskKey.USER_CONTEXT,
            ],
            actionType: 'app',
            location: `/settings/${organization.slug}/projects/:projectId/user-reports/`,
            display: false,
        },
        {
            task: types_1.OnboardingTaskKey.ISSUE_TRACKER,
            title: (0, locale_1.t)('Set up issue tracking'),
            description: (0, locale_1.t)('Link to Sentry issues within your issue tracker'),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: `/settings/${organization.slug}/projects/:projectId/plugins/`,
            display: false,
        },
        {
            task: types_1.OnboardingTaskKey.ALERT_RULE,
            title: (0, locale_1.t)('Get smarter alerts'),
            description: (0, locale_1.t)("Customize alerting rules by issue or metric. You'll get the exact information you need precisely when you need it."),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'app',
            location: `/organizations/${organization.slug}/alerts/rules/`,
            display: true,
        },
    ];
}
exports.getOnboardingTasks = getOnboardingTasks;
function getMergedTasks({ organization, projects }) {
    const taskDescriptors = getOnboardingTasks({ organization, projects });
    const serverTasks = organization.onboardingTasks;
    // Map server task state (i.e. completed status) with tasks objects
    const allTasks = taskDescriptors.map(desc => (Object.assign(Object.assign(Object.assign({}, desc), serverTasks.find(serverTask => serverTask.task === desc.task)), { requisiteTasks: [] })));
    // Map incomplete requisiteTasks as full task objects
    return allTasks.map(task => (Object.assign(Object.assign({}, task), { requisiteTasks: task.requisites
            .map(key => allTasks.find(task2 => task2.task === key))
            .filter(reqTask => reqTask.status !== 'complete') })));
}
exports.getMergedTasks = getMergedTasks;
const PulsingIndicator = (0, styled_1.default)('div') `
  ${pulsingIndicator_1.default};
  margin-right: ${(0, space_1.default)(1)};
`;
const EventWaitingIndicator = (0, styled_1.default)((p) => (<div {...p}>
    <PulsingIndicator />
    {(0, locale_1.t)('Waiting for event')}
  </div>)) `
  display: flex;
  align-items: center;
  flex-grow: 1;
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.orange400};
`;
//# sourceMappingURL=taskConfig.jsx.map