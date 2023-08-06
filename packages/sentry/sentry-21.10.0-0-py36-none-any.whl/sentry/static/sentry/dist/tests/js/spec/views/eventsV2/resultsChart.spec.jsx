Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const locale_1 = require("app/locale");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const types_1 = require("app/utils/discover/types");
const resultsChart_1 = (0, tslib_1.__importDefault)(require("app/views/eventsV2/resultsChart"));
describe('EventsV2 > ResultsChart', function () {
    const features = ['discover-basic', 'connect-discover-and-dashboards'];
    const location = {
        query: { query: 'tag:value' },
        pathname: '/',
    };
    let organization, eventView, initialData;
    beforeEach(() => {
        // @ts-expect-error
        organization = TestStubs.Organization({
            features,
            // @ts-expect-error
            projects: [TestStubs.Project()],
        });
        initialData = (0, initializeOrg_1.initializeOrg)({
            organization,
            router: {
                location,
            },
            project: 1,
            projects: [],
        });
        // @ts-expect-error
        eventView = eventView_1.default.fromSavedQueryOrLocation(undefined, location);
    });
    it('only allows default, daily, and previous period display modes when multiple y axis are selected', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const wrapper = (0, enzyme_1.mountWithTheme)(<resultsChart_1.default 
            // @ts-expect-error
            router={TestStubs.router()} organization={organization} eventView={eventView} 
            // @ts-expect-error
            location={location} onAxisChange={() => undefined} onDisplayChange={() => undefined} total={1} confirmedQuery yAxis={['count()', 'failure_count()']}/>, initialData.routerContext);
            const displayOptions = wrapper.find('ChartFooter').props().displayOptions;
            displayOptions.forEach(({ value, disabled }) => {
                if (![types_1.DisplayModes.DEFAULT, types_1.DisplayModes.DAILY, types_1.DisplayModes.PREVIOUS].includes(value)) {
                    expect(disabled).toBe(true);
                }
            });
        });
    });
    it('does not display a chart if no y axis is selected', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const wrapper = (0, enzyme_1.mountWithTheme)(<resultsChart_1.default 
            // @ts-expect-error
            router={TestStubs.router()} organization={organization} eventView={eventView} 
            // @ts-expect-error
            location={location} onAxisChange={() => undefined} onDisplayChange={() => undefined} total={1} confirmedQuery yAxis={[]}/>, initialData.routerContext);
            expect(wrapper.find('NoChartContainer').children().children().html()).toEqual((0, locale_1.t)('No Y-Axis selected.'));
        });
    });
});
//# sourceMappingURL=resultsChart.spec.jsx.map