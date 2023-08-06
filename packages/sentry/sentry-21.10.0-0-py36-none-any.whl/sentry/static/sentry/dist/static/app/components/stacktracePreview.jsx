Object.defineProperty(exports, "__esModule", { value: true });
exports.STACKTRACE_PREVIEW_TOOLTIP_DELAY = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const stacktrace_1 = require("app/components/events/interfaces/stacktrace");
const stacktraceContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/stacktraceContent"));
const stacktraceContentV2_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/stacktraceContentV2"));
const hovercard_1 = (0, tslib_1.__importStar)(require("app/components/hovercard"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const event_1 = require("app/types/event");
const utils_1 = require("app/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const findBestThread_1 = (0, tslib_1.__importDefault)(require("./events/interfaces/threads/threadSelector/findBestThread"));
const getThreadStacktrace_1 = (0, tslib_1.__importDefault)(require("./events/interfaces/threads/threadSelector/getThreadStacktrace"));
const HOVERCARD_DELAY = 500;
exports.STACKTRACE_PREVIEW_TOOLTIP_DELAY = 1000;
class StacktracePreview extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            loadingVisible: false,
        };
        this.loaderTimeout = null;
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, api, issueId, eventId, projectSlug } = this.props;
            if (this.state.event || (!issueId && !(eventId && projectSlug))) {
                return;
            }
            this.loaderTimeout = window.setTimeout(() => {
                this.setState({ loadingVisible: true });
            }, HOVERCARD_DELAY);
            try {
                const event = yield api.requestPromise(eventId && projectSlug
                    ? `/projects/${organization.slug}/${projectSlug}/events/${eventId}/`
                    : `/issues/${issueId}/events/latest/`);
                clearTimeout(this.loaderTimeout);
                this.setState({ event, loading: false, loadingVisible: false });
            }
            catch (_a) {
                clearTimeout(this.loaderTimeout);
                this.setState({ loading: false, loadingVisible: false });
            }
        });
        this.handleStacktracePreviewClick = (event) => {
            event.stopPropagation();
        };
    }
    getStacktrace() {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        const { event } = this.state;
        if (!event) {
            return undefined;
        }
        const exceptionsWithStacktrace = (_c = (_b = (_a = event.entries
            .find(e => e.type === event_1.EntryType.EXCEPTION)) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.values.filter(({ stacktrace }) => (0, utils_1.defined)(stacktrace))) !== null && _c !== void 0 ? _c : [];
        const exceptionStacktrace = (0, stacktrace_1.isStacktraceNewestFirst)()
            ? (_d = exceptionsWithStacktrace[exceptionsWithStacktrace.length - 1]) === null || _d === void 0 ? void 0 : _d.stacktrace
            : (_e = exceptionsWithStacktrace[0]) === null || _e === void 0 ? void 0 : _e.stacktrace;
        if (exceptionStacktrace) {
            return exceptionStacktrace;
        }
        const threads = (_h = (_g = (_f = event.entries.find(e => e.type === event_1.EntryType.THREADS)) === null || _f === void 0 ? void 0 : _f.data) === null || _g === void 0 ? void 0 : _g.values) !== null && _h !== void 0 ? _h : [];
        const bestThread = (0, findBestThread_1.default)(threads);
        if (!bestThread) {
            return undefined;
        }
        const bestThreadStacktrace = (0, getThreadStacktrace_1.default)(false, bestThread);
        if (bestThreadStacktrace) {
            return bestThreadStacktrace;
        }
        return undefined;
    }
    renderHovercardBody(stacktrace) {
        var _a, _b, _c, _d;
        const { event, loading, loadingVisible } = this.state;
        if (loading && loadingVisible) {
            return (<NoStackTraceWrapper>
          <loadingIndicator_1.default hideMessage size={32}/>
        </NoStackTraceWrapper>);
        }
        if (loading) {
            return null;
        }
        if (!stacktrace) {
            return (<NoStackTraceWrapper onClick={this.handleStacktracePreviewClick}>
          {(0, locale_1.t)("There's no stack trace available for this issue.")}
        </NoStackTraceWrapper>);
        }
        const { organization, groupingCurrentLevel } = this.props;
        if (event) {
            const platform = ((_a = event.platform) !== null && _a !== void 0 ? _a : 'other');
            return (<div onClick={this.handleStacktracePreviewClick}>
          {!!((_b = organization.features) === null || _b === void 0 ? void 0 : _b.includes('grouping-stacktrace-ui')) ? (<stacktraceContentV2_1.default data={stacktrace} expandFirstFrame={false} includeSystemFrames={((_c = stacktrace.frames) !== null && _c !== void 0 ? _c : []).every(frame => !frame.inApp)} platform={platform} newestFirst={(0, stacktrace_1.isStacktraceNewestFirst)()} event={event} groupingCurrentLevel={groupingCurrentLevel} isHoverPreviewed/>) : (<stacktraceContent_1.default data={stacktrace} expandFirstFrame={false} includeSystemFrames={((_d = stacktrace.frames) !== null && _d !== void 0 ? _d : []).every(frame => !frame.inApp)} platform={platform} newestFirst={(0, stacktrace_1.isStacktraceNewestFirst)()} event={event} isHoverPreviewed/>)}
        </div>);
        }
        return null;
    }
    render() {
        const { children, disablePreview, theme, className } = this.props;
        const { loading, loadingVisible } = this.state;
        const stacktrace = this.getStacktrace();
        if (disablePreview) {
            return children;
        }
        return (<span className={className} onMouseEnter={this.fetchData}>
        <StyledHovercard body={this.renderHovercardBody(stacktrace)} position="right" modifiers={{
                flip: {
                    enabled: false,
                },
                preventOverflow: {
                    padding: 20,
                    enabled: true,
                    boundariesElement: 'viewport',
                },
            }} state={loading && loadingVisible ? 'loading' : !stacktrace ? 'empty' : 'done'} tipBorderColor={theme.border} tipColor={theme.background}>
          {children}
        </StyledHovercard>
      </span>);
    }
}
const StyledHovercard = (0, styled_1.default)(hovercard_1.default) `
  /* Lower z-index to match the modals (10000 vs 10002) to allow stackTraceLinkModal be on top of stack trace preview. */
  z-index: ${p => p.theme.zIndex.modal};
  width: ${p => {
    if (p.state === 'loading') {
        return 'auto';
    }
    if (p.state === 'empty') {
        return '340px';
    }
    return '700px';
}};

  ${hovercard_1.Body} {
    padding: 0;
    max-height: 300px;
    overflow-y: auto;
    border-bottom-left-radius: ${p => p.theme.borderRadius};
    border-bottom-right-radius: ${p => p.theme.borderRadius};
  }

  .traceback {
    margin-bottom: 0;
    border: 0;
    box-shadow: none;
  }

  .loading {
    margin: 0 auto;
    .loading-indicator {
      /**
      * Overriding the .less file - for default 64px loader we have the width of border set to 6px
      * For 32px we therefore need 3px to keep the same thickness ratio
      */
      border-width: 3px;
    }
  }

  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    display: none;
  }
`;
const NoStackTraceWrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  padding: ${(0, space_1.default)(1.5)};
  font-size: ${p => p.theme.fontSizeMedium};
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 56px;
`;
exports.default = (0, withApi_1.default)((0, react_1.withTheme)(StacktracePreview));
//# sourceMappingURL=stacktracePreview.jsx.map