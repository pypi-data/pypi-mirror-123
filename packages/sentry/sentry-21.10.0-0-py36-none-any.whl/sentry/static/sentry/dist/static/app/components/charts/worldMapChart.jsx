Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const echarts_1 = (0, tslib_1.__importDefault)(require("echarts"));
const max_1 = (0, tslib_1.__importDefault)(require("lodash/max"));
const visualMap_1 = (0, tslib_1.__importDefault)(require("./components/visualMap"));
const mapSeries_1 = (0, tslib_1.__importDefault)(require("./series/mapSeries"));
const baseChart_1 = (0, tslib_1.__importDefault)(require("./baseChart"));
class WorldMapChart extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            countryToCodeMap: null,
            map: null,
            codeToCountryMap: null,
        };
    }
    componentDidMount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const [countryToCodeMap, worldMap] = yield Promise.all([
                Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/data/countryCodesMap'))),
                Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/data/world.json'))),
            ]);
            echarts_1.default.registerMap('sentryWorld', worldMap.default);
            // eslint-disable-next-line
            this.setState({
                countryToCodeMap: countryToCodeMap.default,
                map: worldMap.default,
                codeToCountryMap: Object.fromEntries(Object.entries(countryToCodeMap.default).map(([country, code]) => [code, country])),
            });
        });
    }
    render() {
        const { countryToCodeMap, map } = this.state;
        if (countryToCodeMap === null || map === null) {
            return null;
        }
        const _a = this.props, { series, seriesOptions, theme } = _a, props = (0, tslib_1.__rest)(_a, ["series", "seriesOptions", "theme"]);
        const processedSeries = series.map((_a) => {
            var _b;
            var { seriesName, data } = _a, options = (0, tslib_1.__rest)(_a, ["seriesName", "data"]);
            return (0, mapSeries_1.default)(Object.assign(Object.assign(Object.assign({}, seriesOptions), options), { map: 'sentryWorld', name: seriesName, nameMap: (_b = this.state.countryToCodeMap) !== null && _b !== void 0 ? _b : undefined, aspectScale: 0.85, zoom: 1.3, center: [10.97, 9.71], itemStyle: {
                    areaColor: theme.gray200,
                    borderColor: theme.backgroundSecondary,
                    emphasis: {
                        areaColor: theme.orange300,
                    },
                }, label: {
                    emphasis: {
                        show: false,
                    },
                }, data }));
        });
        // TODO(billy):
        // For absolute values, we want min/max to based on min/max of series
        // Otherwise it should be 0-100
        const maxValue = (0, max_1.default)(series.map(({ data }) => (0, max_1.default)(data.map(({ value }) => value)))) || 1;
        const tooltipFormatter = (format) => {
            var _a;
            const { marker, name, value } = Array.isArray(format) ? format[0] : format;
            // If value is NaN, don't show anything because we won't have a country code either
            if (isNaN(value)) {
                return '';
            }
            // `value` should be a number
            const formattedValue = typeof value === 'number' ? value.toLocaleString() : '';
            const countryOrCode = ((_a = this.state.codeToCountryMap) === null || _a === void 0 ? void 0 : _a[name]) || name;
            return [
                `<div class="tooltip-series tooltip-series-solo">
                 <div><span class="tooltip-label">${marker} <strong>${countryOrCode}</strong></span> ${formattedValue}</div>
              </div>`,
                '<div class="tooltip-arrow"></div>',
            ].join('');
        };
        return (<baseChart_1.default options={{
                backgroundColor: theme.background,
                visualMap: [
                    (0, visualMap_1.default)({
                        left: 'right',
                        min: 0,
                        max: maxValue,
                        inRange: {
                            color: [theme.purple200, theme.purple300],
                        },
                        text: ['High', 'Low'],
                        textStyle: {
                            color: theme.textColor,
                        },
                        // Whether show handles, which can be dragged to adjust "selected range".
                        // False because the handles are pretty ugly
                        calculable: false,
                    }),
                ],
            }} {...props} yAxis={null} xAxis={null} series={processedSeries} tooltip={{
                formatter: tooltipFormatter,
            }}/>);
    }
}
exports.default = (0, react_1.withTheme)(WorldMapChart);
//# sourceMappingURL=worldMapChart.jsx.map