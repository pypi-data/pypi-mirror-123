Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const rawStacktraceContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/rawStacktraceContent"));
const stacktraceContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/stacktraceContent"));
const stacktraceContentV2_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/stacktraceContentV2"));
const stacktrace_1 = require("app/types/stacktrace");
const Stacktrace = ({ stackView, stacktrace, event, newestFirst, platform, hasHierarchicalGrouping, groupingCurrentLevel, }) => {
    return (<errorBoundary_1.default mini>
      {stackView === stacktrace_1.STACK_VIEW.RAW ? (<pre className="traceback plain">
          {(0, rawStacktraceContent_1.default)(stacktrace, event.platform)}
        </pre>) : hasHierarchicalGrouping ? (<stacktraceContentV2_1.default data={stacktrace} className="no-exception" includeSystemFrames={stackView === stacktrace_1.STACK_VIEW.FULL} platform={platform} event={event} newestFirst={newestFirst} groupingCurrentLevel={groupingCurrentLevel}/>) : (<stacktraceContent_1.default data={stacktrace} className="no-exception" includeSystemFrames={stackView === stacktrace_1.STACK_VIEW.FULL} platform={platform} event={event} newestFirst={newestFirst}/>)}
    </errorBoundary_1.default>);
};
exports.default = Stacktrace;
//# sourceMappingURL=stacktrace.jsx.map