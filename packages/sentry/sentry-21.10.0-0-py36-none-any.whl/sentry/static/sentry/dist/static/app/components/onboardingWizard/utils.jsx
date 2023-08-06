Object.defineProperty(exports, "__esModule", { value: true });
exports.findUpcomingTasks = exports.findActiveTasks = exports.findCompleteTasks = exports.taskIsDone = void 0;
const taskIsDone = (task) => ['complete', 'skipped'].includes(task.status);
exports.taskIsDone = taskIsDone;
const findCompleteTasks = (task) => task.completionSeen && ['complete', 'skipped'].includes(task.status);
exports.findCompleteTasks = findCompleteTasks;
const findActiveTasks = (task) => task.requisiteTasks.length === 0 && !(0, exports.findCompleteTasks)(task);
exports.findActiveTasks = findActiveTasks;
const findUpcomingTasks = (task) => task.requisiteTasks.length > 0 && !(0, exports.findCompleteTasks)(task);
exports.findUpcomingTasks = findUpcomingTasks;
//# sourceMappingURL=utils.jsx.map