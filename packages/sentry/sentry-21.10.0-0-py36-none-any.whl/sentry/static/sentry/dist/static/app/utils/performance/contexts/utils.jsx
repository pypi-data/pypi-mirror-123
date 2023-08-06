Object.defineProperty(exports, "__esModule", { value: true });
exports.createDefinedContext = void 0;
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
/*
 * Creates provider, context and useContext hook, guarding against calling useContext without a provider.
 * [0]: https://github.com/chakra-ui/chakra-ui/blob/c0f9c287df0397e2aa9bd90eb3d5c2f2c08aa0b1/packages/utils/src/react-helpers.ts#L27
 *
 * Renamed to createDefinedContext to not conflate with React context.
 */
function createDefinedContext(options) {
    const { strict = true, errorMessage = `useContext for "${options.name}" must be inside a Provider with a value`, name, } = options;
    const Context = react_1.default.createContext(undefined);
    Context.displayName = name;
    function useContext() {
        const context = react_1.default.useContext(Context);
        if (!context && strict)
            throw new Error(errorMessage);
        return context;
    }
    return [Context.Provider, useContext, Context];
}
exports.createDefinedContext = createDefinedContext;
//# sourceMappingURL=utils.jsx.map