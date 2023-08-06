Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializePerformanceData_1 = require("sentry-test/performance/initializePerformanceData");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const organizationContext_1 = require("app/views/organizationContext");
const landing_1 = require("app/views/performance/landing");
const utils_1 = require("app/views/performance/landing/utils");
const WrappedComponent = ({ data }) => {
    const eventView = eventView_1.default.fromLocation(data.router.location);
    return (<organizationContext_1.OrganizationContext.Provider value={data.organization}>
      <landing_1.PerformanceLanding organization={data.organization} location={data.router.location} eventView={eventView} projects={data.projects} shouldShowOnboarding={false} handleSearch={() => { }} handleTrendsClick={() => { }} setError={() => { }}/>
    </organizationContext_1.OrganizationContext.Provider>);
};
describe('Performance > Landing > Index', function () {
    let eventStatsMock;
    beforeEach(function () {
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/sdk-updates/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/prompts-activity/',
            body: {},
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            method: 'GET',
            url: `/organizations/org-slug/key-transactions-list/`,
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            method: 'GET',
            url: `/organizations/org-slug/legacy-key-transactions-count/`,
            body: [],
        });
        // @ts-expect-error
        eventStatsMock = MockApiClient.addMockResponse({
            method: 'GET',
            url: `/organizations/org-slug/events-stats/`,
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            method: 'GET',
            url: `/organizations/org-slug/events-trends-stats/`,
            body: [],
        });
    });
    afterEach(function () {
        // @ts-expect-error
        MockApiClient.clearMockResponses();
    });
    it('renders basic UI elements', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const data = (0, initializePerformanceData_1.initializeData)();
            const wrapper = (0, enzyme_1.mountWithTheme)(<WrappedComponent data={data}/>, data.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('div[data-test-id="performance-landing-v3"]').exists()).toBe(true);
        });
    });
    it('renders frontend pageload view', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const data = (0, initializePerformanceData_1.initializeData)({
                query: { landingDisplay: utils_1.LandingDisplayField.FRONTEND_PAGELOAD },
            });
            const wrapper = (0, enzyme_1.mountWithTheme)(<WrappedComponent data={data}/>, data.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('div[data-test-id="frontend-pageload-view"]').exists()).toBe(true);
            expect(wrapper.find('Table')).toHaveLength(1);
        });
    });
    it('renders frontend other view', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const data = (0, initializePerformanceData_1.initializeData)({
                query: { landingDisplay: utils_1.LandingDisplayField.FRONTEND_OTHER },
            });
            const wrapper = (0, enzyme_1.mountWithTheme)(<WrappedComponent data={data}/>, data.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('Table').exists()).toBe(true);
        });
    });
    it('renders backend view', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const data = (0, initializePerformanceData_1.initializeData)({
                query: { landingDisplay: utils_1.LandingDisplayField.BACKEND },
            });
            const wrapper = (0, enzyme_1.mountWithTheme)(<WrappedComponent data={data}/>, data.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('Table').exists()).toBe(true);
        });
    });
    it('renders mobile view', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const data = (0, initializePerformanceData_1.initializeData)({
                query: { landingDisplay: utils_1.LandingDisplayField.MOBILE },
            });
            const wrapper = (0, enzyme_1.mountWithTheme)(<WrappedComponent data={data}/>, data.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('Table').exists()).toBe(true);
        });
    });
    it('renders all transactions view', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const data = (0, initializePerformanceData_1.initializeData)({
                query: { landingDisplay: utils_1.LandingDisplayField.ALL },
            });
            const wrapper = (0, enzyme_1.mountWithTheme)(<WrappedComponent data={data}/>, data.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('Table').exists()).toBe(true);
            expect(eventStatsMock).toHaveBeenCalledTimes(5); // Currently defaulting to 5 event stat charts on all transactions view.
            const titles = wrapper.find('div[data-test-id="performance-widget-title"]');
            expect(titles).toHaveLength(5);
            expect(titles.at(0).text()).toEqual('User Misery');
            expect(titles.at(1).text()).toEqual('Transactions Per Minute');
            expect(titles.at(2).text()).toEqual('Failure Rate');
            expect(titles.at(3).text()).toEqual('Transactions Per Minute');
            expect(titles.at(4).text()).toEqual('Transactions Per Minute');
        });
    });
});
//# sourceMappingURL=index.spec.jsx.map