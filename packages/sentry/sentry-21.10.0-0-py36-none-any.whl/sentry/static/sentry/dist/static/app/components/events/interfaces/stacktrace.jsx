Object.defineProperty(exports, "__esModule", { value: true });
exports.isStacktraceNewestFirst = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const crashContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/crashContent"));
const crashActions_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/crashHeader/crashActions"));
const crashTitle_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/crashHeader/crashTitle"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const stacktrace_1 = require("app/types/stacktrace");
const noStackTraceMessage_1 = (0, tslib_1.__importDefault)(require("./noStackTraceMessage"));
function isStacktraceNewestFirst() {
    const user = configStore_1.default.get('user');
    // user may not be authenticated
    if (!user) {
        return true;
    }
    switch (user.options.stacktraceOrder) {
        case 2:
            return true;
        case 1:
            return false;
        case -1:
        default:
            return true;
    }
}
exports.isStacktraceNewestFirst = isStacktraceNewestFirst;
function StacktraceInterface({ hideGuide = false, projectId, event, data, type, hasHierarchicalGrouping, groupingCurrentLevel, }) {
    var _a;
    const [stackView, setStackView] = (0, react_1.useState)(data.hasSystemFrames ? stacktrace_1.STACK_VIEW.APP : stacktrace_1.STACK_VIEW.FULL);
    const [newestFirst, setNewestFirst] = (0, react_1.useState)(isStacktraceNewestFirst());
    const stackTraceNotFound = !((_a = data.frames) !== null && _a !== void 0 ? _a : []).length;
    return (<eventDataSection_1.default type={type} title={<crashTitle_1.default title={(0, locale_1.t)('Stack Trace')} hideGuide={hideGuide} newestFirst={newestFirst} onChange={!stackTraceNotFound ? value => setNewestFirst(value.newestFirst) : undefined}/>} actions={!stackTraceNotFound && (<crashActions_1.default stackView={stackView} platform={event.platform} stacktrace={data} hasHierarchicalGrouping={hasHierarchicalGrouping} onChange={value => { var _a; return setStackView((_a = value.stackView) !== null && _a !== void 0 ? _a : stackView); }}/>)} wrapTitle={false}>
      {stackTraceNotFound ? (<noStackTraceMessage_1.default />) : (<crashContent_1.default projectId={projectId} event={event} stackView={stackView} newestFirst={newestFirst} stacktrace={data} stackType={stacktrace_1.STACK_TYPE.ORIGINAL} groupingCurrentLevel={groupingCurrentLevel} hasHierarchicalGrouping={hasHierarchicalGrouping}/>)}
    </eventDataSection_1.default>);
}
exports.default = StacktraceInterface;
//# sourceMappingURL=stacktrace.jsx.map