Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const settingsBreadcrumbActions_1 = (0, tslib_1.__importDefault)(require("app/actions/settingsBreadcrumbActions"));
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const storeConfig = {
    pathMap: {},
    init() {
        this.reset();
        this.listenTo(settingsBreadcrumbActions_1.default.mapTitle, this.onUpdateRouteMap);
        this.listenTo(settingsBreadcrumbActions_1.default.trimMappings, this.onTrimMappings);
    },
    reset() {
        this.pathMap = {};
    },
    getPathMap() {
        return this.pathMap;
    },
    onUpdateRouteMap({ routes, title }) {
        this.pathMap[(0, getRouteStringFromRoutes_1.default)(routes)] = title;
        this.trigger(this.pathMap);
    },
    onTrimMappings(routes) {
        const routePath = (0, getRouteStringFromRoutes_1.default)(routes);
        for (const fullPath in this.pathMap) {
            if (!routePath.startsWith(fullPath)) {
                delete this.pathMap[fullPath];
            }
        }
        this.trigger(this.pathMap);
    },
};
const SettingsBreadcrumbStore = reflux_1.default.createStore(storeConfig);
exports.default = SettingsBreadcrumbStore;
//# sourceMappingURL=settingsBreadcrumbStore.jsx.map