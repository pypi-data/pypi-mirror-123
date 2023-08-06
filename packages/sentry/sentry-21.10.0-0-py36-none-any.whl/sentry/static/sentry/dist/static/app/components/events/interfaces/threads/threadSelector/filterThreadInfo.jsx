Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const utils_1 = require("app/components/events/interfaces/frame/utils");
const getRelevantFrame_1 = (0, tslib_1.__importDefault)(require("./getRelevantFrame"));
const getThreadException_1 = (0, tslib_1.__importDefault)(require("./getThreadException"));
const getThreadStacktrace_1 = (0, tslib_1.__importDefault)(require("./getThreadStacktrace"));
const trimFilename_1 = (0, tslib_1.__importDefault)(require("./trimFilename"));
function filterThreadInfo(event, thread, exception) {
    var _a;
    const threadInfo = {};
    let stacktrace = (0, getThreadStacktrace_1.default)(false, thread);
    if (thread.crashed) {
        const threadException = exception !== null && exception !== void 0 ? exception : (0, getThreadException_1.default)(event, thread);
        const matchedStacktraceAndExceptionThread = threadException === null || threadException === void 0 ? void 0 : threadException.values.find(exceptionDataValue => exceptionDataValue.threadId === thread.id);
        if (matchedStacktraceAndExceptionThread) {
            stacktrace = (_a = matchedStacktraceAndExceptionThread.stacktrace) !== null && _a !== void 0 ? _a : undefined;
        }
        threadInfo.crashedInfo = threadException;
    }
    if (!stacktrace) {
        return threadInfo;
    }
    const relevantFrame = (0, getRelevantFrame_1.default)(stacktrace);
    if (relevantFrame.filename) {
        threadInfo.filename = (0, trimFilename_1.default)(relevantFrame.filename);
    }
    if (relevantFrame.function) {
        threadInfo.label = relevantFrame.function;
        return threadInfo;
    }
    if (relevantFrame.package) {
        threadInfo.label = (0, utils_1.trimPackage)(relevantFrame.package);
        return threadInfo;
    }
    if (relevantFrame.module) {
        threadInfo.label = relevantFrame.module;
        return threadInfo;
    }
    return threadInfo;
}
exports.default = filterThreadInfo;
//# sourceMappingURL=filterThreadInfo.jsx.map