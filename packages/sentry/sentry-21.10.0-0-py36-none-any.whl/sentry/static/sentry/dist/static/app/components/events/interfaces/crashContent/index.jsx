Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const exception_1 = (0, tslib_1.__importDefault)(require("./exception"));
const stacktrace_1 = (0, tslib_1.__importDefault)(require("./stacktrace"));
const CrashContent = ({ event, stackView, stackType, newestFirst, projectId, groupingCurrentLevel, hasHierarchicalGrouping, exception, stacktrace, }) => {
    var _a;
    const platform = ((_a = event.platform) !== null && _a !== void 0 ? _a : 'other');
    if (exception) {
        return (<exception_1.default stackType={stackType} stackView={stackView} projectId={projectId} newestFirst={newestFirst} event={event} platform={platform} values={exception.values} groupingCurrentLevel={groupingCurrentLevel} hasHierarchicalGrouping={hasHierarchicalGrouping}/>);
    }
    if (stacktrace) {
        return (<stacktrace_1.default stacktrace={stacktrace} stackView={stackView} newestFirst={newestFirst} event={event} platform={platform} groupingCurrentLevel={groupingCurrentLevel} hasHierarchicalGrouping={hasHierarchicalGrouping}/>);
    }
    return null;
};
exports.default = CrashContent;
//# sourceMappingURL=index.jsx.map