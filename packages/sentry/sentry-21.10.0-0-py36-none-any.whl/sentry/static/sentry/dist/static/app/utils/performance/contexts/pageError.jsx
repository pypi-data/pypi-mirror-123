Object.defineProperty(exports, "__esModule", { value: true });
exports.usePageError = exports.PageErrorAlert = exports.PageErrorProvider = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const pageErrorContext = (0, react_1.createContext)({
    pageError: undefined,
    setPageError: (_) => { },
});
const PageErrorProvider = ({ children }) => {
    const [pageError, setPageError] = (0, react_1.useState)();
    return (<pageErrorContext.Provider value={{
            pageError,
            setPageError,
        }}>
      {children}
    </pageErrorContext.Provider>);
};
exports.PageErrorProvider = PageErrorProvider;
const PageErrorAlert = () => {
    const { pageError } = (0, react_1.useContext)(pageErrorContext);
    if (!pageError) {
        return null;
    }
    return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
      {pageError}
    </alert_1.default>);
};
exports.PageErrorAlert = PageErrorAlert;
const usePageError = () => (0, react_1.useContext)(pageErrorContext);
exports.usePageError = usePageError;
//# sourceMappingURL=pageError.jsx.map