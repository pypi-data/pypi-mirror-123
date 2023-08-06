Object.defineProperty(exports, "__esModule", { value: true });
exports.initializeData = void 0;
const tslib_1 = require("tslib");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
function initializeData(settings) {
    // @ts-expect-error
    const _defaultProject = TestStubs.Project();
    const _settings = Object.assign({ query: {}, features: [], projects: [_defaultProject], project: _defaultProject }, settings);
    const { query, features } = _settings;
    // @ts-expect-error
    const projects = [TestStubs.Project()];
    const [project] = projects;
    // @ts-expect-error
    const organization = TestStubs.Organization({
        features,
        projects,
    });
    const router = {
        location: {
            query: Object.assign({}, query),
        },
    };
    const initialData = (0, initializeOrg_1.initializeOrg)({ organization, projects, project, router });
    const location = initialData.router.location;
    const eventView = eventView_1.default.fromLocation(location);
    return Object.assign(Object.assign({}, initialData), { location, eventView });
}
exports.initializeData = initializeData;
//# sourceMappingURL=initializePerformanceData.js.map