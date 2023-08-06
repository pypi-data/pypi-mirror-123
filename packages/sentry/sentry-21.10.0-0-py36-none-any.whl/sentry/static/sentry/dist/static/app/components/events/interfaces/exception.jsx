Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const crashContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/crashContent"));
const crashActions_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/crashHeader/crashActions"));
const crashTitle_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/crashHeader/crashTitle"));
const stacktrace_1 = require("app/components/events/interfaces/stacktrace");
const locale_1 = require("app/locale");
const stacktrace_2 = require("app/types/stacktrace");
const utils_1 = require("app/utils");
function Exception({ event, type, data, projectId, hasHierarchicalGrouping, groupingCurrentLevel, hideGuide = false, }) {
    const [stackView, setStackView] = (0, react_1.useState)(data.hasSystemFrames ? stacktrace_2.STACK_VIEW.APP : stacktrace_2.STACK_VIEW.FULL);
    const [stackType, setStackType] = (0, react_1.useState)(stacktrace_2.STACK_TYPE.ORIGINAL);
    const [newestFirst, setNewestFirst] = (0, react_1.useState)((0, stacktrace_1.isStacktraceNewestFirst)());
    const eventHasThreads = !!event.entries.find(entry => entry.type === 'threads');
    /* in case there are threads in the event data, we don't render the
     exception block.  Instead the exception is contained within the
     thread interface. */
    if (eventHasThreads) {
        return null;
    }
    function handleChange({ stackView: newStackView, stackType: newStackType, newestFirst: newNewestFirst, }) {
        if (newStackView) {
            setStackView(newStackView);
        }
        if ((0, utils_1.defined)(newNewestFirst)) {
            setNewestFirst(newNewestFirst);
        }
        if (newStackType) {
            setStackType(newStackType);
        }
    }
    const commonCrashHeaderProps = {
        newestFirst,
        hideGuide,
        onChange: handleChange,
    };
    return (<eventDataSection_1.default type={type} title={<crashTitle_1.default title={(0, locale_1.t)('Exception')} {...commonCrashHeaderProps}/>} actions={<crashActions_1.default stackType={stackType} stackView={stackView} platform={event.platform} exception={data} hasHierarchicalGrouping={hasHierarchicalGrouping} {...commonCrashHeaderProps}/>} wrapTitle={false}>
      <crashContent_1.default projectId={projectId} event={event} stackType={stackType} stackView={stackView} newestFirst={newestFirst} exception={data} groupingCurrentLevel={groupingCurrentLevel} hasHierarchicalGrouping={hasHierarchicalGrouping}/>
    </eventDataSection_1.default>);
}
exports.default = Exception;
//# sourceMappingURL=exception.jsx.map