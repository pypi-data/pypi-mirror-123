Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const crashActions_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/crashHeader/crashActions"));
const crashTitle_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/crashHeader/crashTitle"));
const stacktrace_1 = require("app/components/events/interfaces/stacktrace");
const locale_1 = require("app/locale");
const stacktrace_2 = require("app/types/stacktrace");
const utils_1 = require("app/utils");
const findBestThread_1 = (0, tslib_1.__importDefault)(require("./threadSelector/findBestThread"));
const getThreadException_1 = (0, tslib_1.__importDefault)(require("./threadSelector/getThreadException"));
const getThreadStacktrace_1 = (0, tslib_1.__importDefault)(require("./threadSelector/getThreadStacktrace"));
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
const threadSelector_1 = (0, tslib_1.__importDefault)(require("./threadSelector"));
const defaultProps = {
    hideGuide: false,
};
function getIntendedStackView(thread, event) {
    const exception = (0, getThreadException_1.default)(event, thread);
    if (exception) {
        return !!exception.values.find(value => { var _a; return !!((_a = value.stacktrace) === null || _a === void 0 ? void 0 : _a.hasSystemFrames); })
            ? stacktrace_2.STACK_VIEW.APP
            : stacktrace_2.STACK_VIEW.FULL;
    }
    const stacktrace = (0, getThreadStacktrace_1.default)(false, thread);
    return (stacktrace === null || stacktrace === void 0 ? void 0 : stacktrace.hasSystemFrames) ? stacktrace_2.STACK_VIEW.APP : stacktrace_2.STACK_VIEW.FULL;
}
class Threads extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.handleSelectNewThread = (thread) => {
            const { event } = this.props;
            this.setState(prevState => ({
                activeThread: thread,
                stackView: prevState.stackView !== stacktrace_2.STACK_VIEW.RAW
                    ? getIntendedStackView(thread, event)
                    : prevState.stackView,
                stackType: stacktrace_2.STACK_TYPE.ORIGINAL,
            }));
        };
        this.handleChangeNewestFirst = ({ newestFirst }) => {
            this.setState({ newestFirst });
        };
        this.handleChangeStackView = ({ stackView, stackType, }) => {
            this.setState(prevState => ({
                stackView: stackView !== null && stackView !== void 0 ? stackView : prevState.stackView,
                stackType: stackType !== null && stackType !== void 0 ? stackType : prevState.stackType,
            }));
        };
    }
    getInitialState() {
        const { data, event } = this.props;
        const thread = (0, utils_1.defined)(data.values) ? (0, findBestThread_1.default)(data.values) : undefined;
        return {
            activeThread: thread,
            stackView: thread ? getIntendedStackView(thread, event) : undefined,
            stackType: stacktrace_2.STACK_TYPE.ORIGINAL,
            newestFirst: (0, stacktrace_1.isStacktraceNewestFirst)(),
        };
    }
    render() {
        const { data, event, projectId, hideGuide, type, hasHierarchicalGrouping, groupingCurrentLevel, } = this.props;
        if (!data.values) {
            return null;
        }
        const threads = data.values;
        const { stackView, stackType, newestFirst, activeThread } = this.state;
        const exception = (0, getThreadException_1.default)(event, activeThread);
        const stacktrace = !exception
            ? (0, getThreadStacktrace_1.default)(stackType !== stacktrace_2.STACK_TYPE.ORIGINAL, activeThread)
            : undefined;
        const stackTraceNotFound = !(exception || stacktrace);
        const hasMoreThanOneThread = threads.length > 1;
        return (<eventDataSection_1.default type={type} title={hasMoreThanOneThread ? (<crashTitle_1.default title="" newestFirst={newestFirst} hideGuide={hideGuide} onChange={this.handleChangeNewestFirst} beforeTitle={activeThread && (<threadSelector_1.default threads={threads} activeThread={activeThread} event={event} onChange={this.handleSelectNewThread} exception={exception}/>)}/>) : (<crashTitle_1.default title={(0, locale_1.t)('Stack Trace')} newestFirst={newestFirst} hideGuide={hideGuide} onChange={!stackTraceNotFound ? this.handleChangeNewestFirst : undefined}/>)} actions={!stackTraceNotFound && (<crashActions_1.default stackView={stackView} platform={event.platform} stacktrace={stacktrace} stackType={stackType} thread={hasMoreThanOneThread ? activeThread : undefined} exception={exception} onChange={this.handleChangeStackView} hasHierarchicalGrouping={hasHierarchicalGrouping}/>)} showPermalink={!hasMoreThanOneThread} wrapTitle={false}>
        <content_1.default data={activeThread} exception={exception} stackView={stackView} stackType={stackType} stacktrace={stacktrace} event={event} newestFirst={newestFirst} projectId={projectId} groupingCurrentLevel={groupingCurrentLevel} stackTraceNotFound={stackTraceNotFound} hasHierarchicalGrouping={hasHierarchicalGrouping}/>
      </eventDataSection_1.default>);
    }
}
Threads.defaultProps = defaultProps;
exports.default = Threads;
//# sourceMappingURL=index.jsx.map