Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const baseChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/baseChart"));
describe('BaseChart', function () {
    const { routerContext } = (0, initializeOrg_1.initializeOrg)();
    it('renders with grey dotted previous period when using only a single series', function () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<baseChart_1.default colors={['#444674', '#d6567f', '#f2b712']} previousPeriod={[
                { seriesName: 'count()', data: [{ value: 123, name: new Date().getTime() }] },
            ]}/>, routerContext);
        const series = wrapper.find('ChartContainer').props().children.props.option.series;
        expect(series.length).toEqual(1);
        expect(series[0].lineStyle.color).toEqual('#C6BECF');
        expect(series[0].lineStyle.type).toEqual('dotted');
    });
    it('renders with lightened colored dotted previous period when using multiple series', function () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<baseChart_1.default colors={['#444674', '#d6567f', '#f2b712']} previousPeriod={[
                { seriesName: 'count()', data: [{ value: 123, name: new Date().getTime() }] },
                {
                    seriesName: 'count_unique(user)',
                    data: [{ value: 123, name: new Date().getTime() }],
                },
                {
                    seriesName: 'failure_count()',
                    data: [{ value: 123, name: new Date().getTime() }],
                },
            ]}/>, routerContext);
        const series = wrapper.find('ChartContainer').props().children.props.option.series;
        expect(series.length).toEqual(3);
        expect(series[0].lineStyle.color).toEqual('rgb(98, 100, 146)');
        expect(series[0].lineStyle.type).toEqual('dotted');
        expect(series[1].lineStyle.color).toEqual('rgb(244, 116, 157)');
        expect(series[1].lineStyle.type).toEqual('dotted');
        expect(series[2].lineStyle.color).toEqual('rgb(255, 213, 48)');
        expect(series[2].lineStyle.type).toEqual('dotted');
    });
});
//# sourceMappingURL=baseChart.spec.jsx.map