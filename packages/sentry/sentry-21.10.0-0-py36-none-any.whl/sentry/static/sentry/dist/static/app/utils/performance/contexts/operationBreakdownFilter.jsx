Object.defineProperty(exports, "__esModule", { value: true });
exports.useOpBreakdownFilter = exports.OpBreakdownFilterProvider = void 0;
const react_1 = require("react");
const filter_1 = require("app/views/performance/transactionSummary/filter");
const OpBreakdownFilterContext = (0, react_1.createContext)({
    opBreakdownFilter: filter_1.SpanOperationBreakdownFilter.None,
    setOpBreakdownFilter: (_) => { },
});
const OpBreakdownFilterProvider = ({ filter, children, }) => {
    const [opBreakdownFilter, setOpBreakdownFilter] = (0, react_1.useState)(filter);
    return (<OpBreakdownFilterContext.Provider value={{
            opBreakdownFilter: opBreakdownFilter !== null && opBreakdownFilter !== void 0 ? opBreakdownFilter : filter_1.SpanOperationBreakdownFilter.None,
            setOpBreakdownFilter,
        }}>
      {children}
    </OpBreakdownFilterContext.Provider>);
};
exports.OpBreakdownFilterProvider = OpBreakdownFilterProvider;
const useOpBreakdownFilter = () => (0, react_1.useContext)(OpBreakdownFilterContext);
exports.useOpBreakdownFilter = useOpBreakdownFilter;
//# sourceMappingURL=operationBreakdownFilter.jsx.map