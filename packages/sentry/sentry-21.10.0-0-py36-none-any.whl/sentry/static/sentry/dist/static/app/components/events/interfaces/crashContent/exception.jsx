Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const exceptionContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/exceptionContent"));
const rawExceptionContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/rawExceptionContent"));
const stacktrace_1 = require("app/types/stacktrace");
const Exception = ({ stackView, stackType, projectId, values, event, newestFirst, hasHierarchicalGrouping, groupingCurrentLevel, platform = 'other', }) => (<errorBoundary_1.default mini>
    {stackView === stacktrace_1.STACK_VIEW.RAW ? (<rawExceptionContent_1.default eventId={event.id} projectId={projectId} type={stackType} values={values} platform={platform}/>) : (<exceptionContent_1.default type={stackType} stackView={stackView} values={values} platform={platform} newestFirst={newestFirst} event={event} hasHierarchicalGrouping={hasHierarchicalGrouping} groupingCurrentLevel={groupingCurrentLevel}/>)}
  </errorBoundary_1.default>);
exports.default = Exception;
//# sourceMappingURL=exception.jsx.map