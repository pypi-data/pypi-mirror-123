Object.defineProperty(exports, "__esModule", { value: true });
const utils_1 = require("app/utils");
function getException(exceptionData, exceptionDataValues, thread) {
    if (exceptionDataValues.length === 1 && !exceptionDataValues[0].stacktrace) {
        return Object.assign(Object.assign({}, exceptionData), { values: [
                Object.assign(Object.assign({}, exceptionDataValues[0]), { stacktrace: thread.stacktrace, rawStacktrace: thread.rawStacktrace }),
            ] });
    }
    const exceptionHasAtLeastOneStacktrace = !!exceptionDataValues.find(exceptionDataValue => exceptionDataValue.stacktrace);
    if (!!exceptionHasAtLeastOneStacktrace) {
        return exceptionData;
    }
    return undefined;
}
function getThreadException(event, thread) {
    const exceptionEntry = event.entries.find(entry => entry.type === 'exception');
    if (!exceptionEntry) {
        return undefined;
    }
    const exceptionData = exceptionEntry.data;
    const exceptionDataValues = exceptionData.values;
    if (!(exceptionDataValues === null || exceptionDataValues === void 0 ? void 0 : exceptionDataValues.length) || !thread) {
        return undefined;
    }
    const matchedStacktraceAndExceptionThread = exceptionDataValues.find(exceptionDataValue => exceptionDataValue.threadId === thread.id);
    if (matchedStacktraceAndExceptionThread) {
        return getException(exceptionData, exceptionDataValues, thread);
    }
    if (exceptionDataValues.every(exceptionDataValue => !(0, utils_1.defined)(exceptionDataValue.threadId)) &&
        thread.crashed) {
        return getException(exceptionData, exceptionDataValues, thread);
    }
    return undefined;
}
exports.default = getThreadException;
//# sourceMappingURL=getThreadException.jsx.map