Object.defineProperty(exports, "__esModule", { value: true });
exports.Consumer = exports.Provider = void 0;
const react_1 = require("react");
const SpanEntryContext = (0, react_1.createContext)({
    getViewChildTransactionTarget: () => undefined,
});
exports.Provider = SpanEntryContext.Provider;
exports.Consumer = SpanEntryContext.Consumer;
//# sourceMappingURL=context.jsx.map