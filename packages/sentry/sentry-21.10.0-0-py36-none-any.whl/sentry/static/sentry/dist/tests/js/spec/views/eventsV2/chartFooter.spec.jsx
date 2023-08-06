Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const locale_1 = require("app/locale");
const types_1 = require("app/utils/discover/types");
const chartFooter_1 = (0, tslib_1.__importDefault)(require("app/views/eventsV2/chartFooter"));
describe('EventsV2 > ChartFooter', function () {
    const features = ['discover-basic'];
    const yAxisValue = ['count()', 'failure_count()'];
    const yAxisOptions = [
        { label: 'count()', value: 'count()' },
        { label: 'failure_count()', value: 'failure_count()' },
    ];
    afterEach(function () { });
    it('renders yAxis option using OptionSelector using only the first yAxisValue without feature flag', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            const organization = TestStubs.Organization({
                features,
                // @ts-expect-error
                projects: [TestStubs.Project()],
            });
            // Start off with an invalid view (empty is invalid)
            const initialData = (0, initializeOrg_1.initializeOrg)({
                organization,
                router: {
                    location: { query: { query: 'tag:value' } },
                },
                project: 1,
                projects: [],
            });
            const wrapper = (0, enzyme_1.mountWithTheme)(<chartFooter_1.default organization={organization} total={100} yAxisValue={yAxisValue} yAxisOptions={yAxisOptions} onAxisChange={() => undefined} displayMode={types_1.DisplayModes.DEFAULT} displayOptions={[{ label: types_1.DisplayModes.DEFAULT, value: types_1.DisplayModes.DEFAULT }]} onDisplayChange={() => undefined} onTopEventsChange={() => undefined} topEvents="5"/>, initialData.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            const optionSelector = wrapper.find('OptionSelector').last();
            expect(optionSelector.props().title).toEqual((0, locale_1.t)('Y-Axis'));
            expect(optionSelector.props().selected).toEqual(yAxisValue[0]);
        });
    });
    it('renders yAxis option using OptionCheckboxSelector using entire yAxisValue with feature flag', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            const organization = TestStubs.Organization({
                features: [...features, 'connect-discover-and-dashboards'],
            });
            // Start off with an invalid view (empty is invalid)
            const initialData = (0, initializeOrg_1.initializeOrg)({
                organization,
                router: {
                    location: { query: { query: 'tag:value' } },
                },
                project: 1,
                projects: [],
            });
            const wrapper = (0, enzyme_1.mountWithTheme)(<chartFooter_1.default organization={organization} total={100} yAxisValue={yAxisValue} yAxisOptions={yAxisOptions} onAxisChange={() => undefined} displayMode={types_1.DisplayModes.DEFAULT} displayOptions={[{ label: types_1.DisplayModes.DEFAULT, value: types_1.DisplayModes.DEFAULT }]} onDisplayChange={() => undefined} onTopEventsChange={() => undefined} topEvents="5"/>, initialData.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            const optionCheckboxSelector = wrapper.find('OptionCheckboxSelector').last();
            expect(optionCheckboxSelector.props().title).toEqual((0, locale_1.t)('Y-Axis'));
            expect(optionCheckboxSelector.props().selected).toEqual(yAxisValue);
        });
    });
    it('renders display limits with default limit when top 5 mode is selected', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            const organization = TestStubs.Organization({
                features: [...features, 'discover-top-events'],
            });
            // Start off with an invalid view (empty is invalid)
            const initialData = (0, initializeOrg_1.initializeOrg)({
                organization,
                router: {
                    location: { query: { query: 'tag:value' } },
                },
                project: 1,
                projects: [],
            });
            const wrapper = (0, enzyme_1.mountWithTheme)(<chartFooter_1.default organization={organization} total={100} yAxisValue={yAxisValue} yAxisOptions={yAxisOptions} onAxisChange={() => undefined} displayMode={types_1.DisplayModes.TOP5} displayOptions={[{ label: types_1.DisplayModes.DEFAULT, value: types_1.DisplayModes.DEFAULT }]} onDisplayChange={() => undefined} onTopEventsChange={() => undefined} topEvents="5"/>, initialData.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            const optionSelector = wrapper.find('OptionSelector[title="Limit"]');
            expect(optionSelector.props().selected).toEqual('5');
        });
    });
});
//# sourceMappingURL=chartFooter.spec.jsx.map