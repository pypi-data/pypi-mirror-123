Object.defineProperty(exports, "__esModule", { value: true });
exports.Consumer = exports.Provider = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withProject_1 = (0, tslib_1.__importDefault)(require("app/utils/withProject"));
const AppStoreConnectContext = (0, react_1.createContext)(undefined);
const Provider = (0, withApi_1.default)((0, withProject_1.default)(({ api, children, project, orgSlug }) => {
    const [appStoreConnectValidationData, setAppStoreConnectValidationData] = (0, react_1.useState)();
    (0, react_1.useEffect)(() => {
        fetchAppStoreConnectValidationData();
    }, [project]);
    function getAppStoreConnectSymbolSourceId() {
        var _a;
        return (_a = (project.symbolSources ? JSON.parse(project.symbolSources) : []).find(symbolSource => symbolSource.type.toLowerCase() === 'appstoreconnect')) === null || _a === void 0 ? void 0 : _a.id;
    }
    function fetchAppStoreConnectValidationData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const appStoreConnectSymbolSourceId = getAppStoreConnectSymbolSourceId();
            if (!appStoreConnectSymbolSourceId) {
                return;
            }
            try {
                const response = yield api.requestPromise(`/projects/${orgSlug}/${project.slug}/appstoreconnect/validate/${appStoreConnectSymbolSourceId}/`);
                setAppStoreConnectValidationData(Object.assign({ id: appStoreConnectSymbolSourceId }, response));
            }
            catch (_a) {
                // do nothing
            }
        });
    }
    return (<AppStoreConnectContext.Provider value={appStoreConnectValidationData}>
        {children}
      </AppStoreConnectContext.Provider>);
}));
exports.Provider = Provider;
const Consumer = AppStoreConnectContext.Consumer;
exports.Consumer = Consumer;
exports.default = AppStoreConnectContext;
//# sourceMappingURL=appStoreConnectContext.jsx.map