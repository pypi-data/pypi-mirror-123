Object.defineProperty(exports, "__esModule", { value: true });
exports.useMutablePerformanceEventView = exports.usePerformanceEventView = exports.PerformanceEventViewProvider = void 0;
const utils_1 = require("./utils");
const [PerformanceEventViewProvider, _usePerformanceEventView] = (0, utils_1.createDefinedContext)({
    name: 'PerformanceEventViewContext',
});
exports.PerformanceEventViewProvider = PerformanceEventViewProvider;
// Provides a readonly event view. Also omits anything that isn't currently read-only, although in the future we should switch the code in EventView instead.
// If you need mutability, use the mutable version.
function usePerformanceEventView() {
    return _usePerformanceEventView().eventView;
}
exports.usePerformanceEventView = usePerformanceEventView;
function useMutablePerformanceEventView() {
    return usePerformanceEventView().clone();
}
exports.useMutablePerformanceEventView = useMutablePerformanceEventView;
//# sourceMappingURL=performanceEventViewContext.jsx.map