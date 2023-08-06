Object.defineProperty(exports, "__esModule", { value: true });
exports.Consumer = exports.Provider = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const AppStoreConnectContext = (0, react_1.createContext)(undefined);
const utils_1 = require("./utils");
const Provider = ({ children, project, organization }) => {
    const api = (0, useApi_1.default)();
    const [projectDetails, setProjectDetails] = (0, react_1.useState)();
    const [appStoreConnectValidationData, setAppStoreConnectValidationData] = (0, react_1.useState)(undefined);
    const orgSlug = organization.slug;
    (0, react_1.useEffect)(() => {
        fetchProjectDetails();
    }, [project]);
    (0, react_1.useEffect)(() => {
        fetchAppStoreConnectValidationData();
    }, [projectDetails]);
    function fetchProjectDetails() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!project || projectDetails) {
                return;
            }
            if (project.symbolSources) {
                setProjectDetails(project);
                return;
            }
            try {
                const response = yield api.requestPromise(`/projects/${orgSlug}/${project.slug}/`);
                setProjectDetails(response);
            }
            catch (_a) {
                // do nothing
            }
        });
    }
    function getAppStoreConnectSymbolSourceId(symbolSources) {
        var _a;
        return (_a = (symbolSources ? JSON.parse(symbolSources) : []).find(symbolSource => symbolSource.type.toLowerCase() === 'appstoreconnect')) === null || _a === void 0 ? void 0 : _a.id;
    }
    function fetchAppStoreConnectValidationData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!projectDetails) {
                return;
            }
            const appStoreConnectSymbolSourceId = getAppStoreConnectSymbolSourceId(projectDetails.symbolSources);
            if (!appStoreConnectSymbolSourceId) {
                return;
            }
            try {
                const response = yield api.requestPromise(`/projects/${orgSlug}/${projectDetails.slug}/appstoreconnect/validate/${appStoreConnectSymbolSourceId}/`);
                setAppStoreConnectValidationData(Object.assign({ id: appStoreConnectSymbolSourceId }, response));
            }
            catch (_a) {
                // do nothing
            }
        });
    }
    return (<AppStoreConnectContext.Provider value={appStoreConnectValidationData
            ? Object.assign(Object.assign({}, appStoreConnectValidationData), { updateAlertMessage: (0, utils_1.getAppConnectStoreUpdateAlertMessage)(appStoreConnectValidationData) }) : undefined}>
      {children}
    </AppStoreConnectContext.Provider>);
};
exports.Provider = Provider;
const Consumer = AppStoreConnectContext.Consumer;
exports.Consumer = Consumer;
exports.default = AppStoreConnectContext;
//# sourceMappingURL=index.jsx.map