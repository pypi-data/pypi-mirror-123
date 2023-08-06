Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const stacktrace_1 = require("app/types/stacktrace");
const utils_1 = require("app/utils");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const stacktraceContent_1 = (0, tslib_1.__importDefault)(require("./stacktraceContent"));
const stacktraceContentV2_1 = (0, tslib_1.__importDefault)(require("./stacktraceContentV2"));
const ExceptionStacktraceContent = ({ stackView, stacktrace, chainedException, platform, newestFirst, groupingCurrentLevel, hasHierarchicalGrouping, data, expandFirstFrame, event, }) => {
    var _a, _b;
    if (!(0, utils_1.defined)(stacktrace)) {
        return null;
    }
    if (stackView === stacktrace_1.STACK_VIEW.APP &&
        ((_a = stacktrace.frames) !== null && _a !== void 0 ? _a : []).filter(frame => frame.inApp).length === 0 &&
        !chainedException) {
        return (<panels_1.Panel dashedBorder>
        <emptyMessage_1.default icon={<icons_1.IconWarning size="xs"/>} title={hasHierarchicalGrouping
                ? (0, locale_1.t)('No relevant stack trace has been found!')
                : (0, locale_1.t)('No app only stack trace has been found!')}/>
      </panels_1.Panel>);
    }
    if (!data) {
        return null;
    }
    const includeSystemFrames = stackView === stacktrace_1.STACK_VIEW.FULL ||
        (chainedException && ((_b = data.frames) === null || _b === void 0 ? void 0 : _b.every(frame => !frame.inApp)));
    /**
     * Armin, Markus:
     * If all frames are in app, then no frame is in app.
     * This normally does not matter for the UI but when chained exceptions
     * are used this causes weird behavior where one exception appears to not have a stack trace.
     *
     * It is easier to fix the UI logic to show a non-empty stack trace for chained exceptions
     */
    if (hasHierarchicalGrouping) {
        return (<stacktraceContentV2_1.default data={data} expandFirstFrame={expandFirstFrame} includeSystemFrames={includeSystemFrames} groupingCurrentLevel={groupingCurrentLevel} platform={platform} newestFirst={newestFirst} event={event}/>);
    }
    return (<stacktraceContent_1.default data={data} expandFirstFrame={expandFirstFrame} includeSystemFrames={includeSystemFrames} platform={platform} newestFirst={newestFirst} event={event}/>);
};
exports.default = ExceptionStacktraceContent;
//# sourceMappingURL=exceptionStacktraceContent.jsx.map