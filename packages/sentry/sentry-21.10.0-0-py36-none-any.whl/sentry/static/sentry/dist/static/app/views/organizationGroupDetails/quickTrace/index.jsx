Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const configureDistributedTracing_1 = (0, tslib_1.__importDefault)(require("./configureDistributedTracing"));
const issueQuickTrace_1 = (0, tslib_1.__importDefault)(require("./issueQuickTrace"));
function QuickTrace({ event, group, organization, location }) {
    var _a, _b;
    const hasPerformanceView = organization.features.includes('performance-view');
    const hasTraceContext = Boolean((_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id);
    return (<react_1.Fragment>
      {!hasTraceContext && (<configureDistributedTracing_1.default event={event} project={group.project} organization={organization}/>)}
      {hasPerformanceView && hasTraceContext && (<issueQuickTrace_1.default organization={organization} event={event} location={location}/>)}
    </react_1.Fragment>);
}
exports.default = QuickTrace;
//# sourceMappingURL=index.jsx.map