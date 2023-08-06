Object.defineProperty(exports, "__esModule", { value: true });
exports.setLastRoute = exports.navigateTo = void 0;
const tslib_1 = require("tslib");
const modal_1 = require("app/actionCreators/modal");
const navigationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/navigationActions"));
const contextPickerModal_1 = (0, tslib_1.__importDefault)(require("app/components/contextPickerModal"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
// TODO(ts): figure out better typing for react-router here
function navigateTo(to, router, configUrl) {
    var _a, _b;
    // Check for placeholder params
    const needOrg = to.indexOf(':orgId') > -1;
    const needProject = to.indexOf(':projectId') > -1;
    const comingFromProjectId = (_b = (_a = router === null || router === void 0 ? void 0 : router.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.project;
    const needProjectId = !comingFromProjectId || Array.isArray(comingFromProjectId);
    const projectById = projectsStore_1.default.getById(comingFromProjectId);
    if (needOrg || (needProject && (needProjectId || !projectById)) || configUrl) {
        (0, modal_1.openModal)(modalProps => (<contextPickerModal_1.default {...modalProps} nextPath={to} needOrg={needOrg} needProject={needProject} configUrl={configUrl} comingFromProjectId={Array.isArray(comingFromProjectId) ? '' : comingFromProjectId || ''} onFinish={path => {
                modalProps.closeModal();
                setTimeout(() => router.push(path), 0);
            }}/>), {});
    }
    else {
        projectById
            ? router.push(to.replace(':projectId', projectById.slug))
            : router.push(to);
    }
}
exports.navigateTo = navigateTo;
function setLastRoute(route) {
    navigationActions_1.default.setLastRoute(route);
}
exports.setLastRoute = setLastRoute;
//# sourceMappingURL=navigation.jsx.map