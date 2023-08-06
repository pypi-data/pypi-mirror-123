Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const simpleTableChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/simpleTableChart"));
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const utils_1 = require("app/components/charts/utils");
const worldMapChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/worldMapChart"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const charts_1 = require("app/utils/discover/charts");
const fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
const fields_1 = require("app/utils/discover/fields");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
class WidgetCardChart extends React.Component {
    shouldComponentUpdate(nextProps) {
        // Widget title changes should not update the WidgetCardChart component tree
        const currentProps = Object.assign(Object.assign({}, this.props), { widget: Object.assign(Object.assign({}, this.props.widget), { title: '' }) });
        nextProps = Object.assign(Object.assign({}, nextProps), { widget: Object.assign(Object.assign({}, nextProps.widget), { title: '' }) });
        return !(0, isEqual_1.default)(currentProps, nextProps);
    }
    tableResultComponent({ loading, errorMessage, tableResults, }) {
        const { location, widget, organization } = this.props;
        if (errorMessage) {
            return (<errorPanel_1.default>
          <icons_1.IconWarning color="gray500" size="lg"/>
        </errorPanel_1.default>);
        }
        if (typeof tableResults === 'undefined' || loading) {
            // Align height to other charts.
            return <placeholder_1.default height="200px"/>;
        }
        return tableResults.map((result, i) => {
            var _a, _b;
            const fields = (_b = (_a = widget.queries[i]) === null || _a === void 0 ? void 0 : _a.fields) !== null && _b !== void 0 ? _b : [];
            return (<StyledSimpleTableChart key={`table:${result.title}`} location={location} fields={fields} title={tableResults.length > 1 ? result.title : ''} loading={loading} metadata={result.meta} data={result.data} organization={organization}/>);
        });
    }
    bigNumberComponent({ loading, errorMessage, tableResults, }) {
        if (errorMessage) {
            return (<errorPanel_1.default>
          <icons_1.IconWarning color="gray500" size="lg"/>
        </errorPanel_1.default>);
        }
        if (typeof tableResults === 'undefined' || loading) {
            return <BigNumber>{'\u2014'}</BigNumber>;
        }
        return tableResults.map(result => {
            var _a;
            const tableMeta = (_a = result.meta) !== null && _a !== void 0 ? _a : {};
            const fields = Object.keys(tableMeta !== null && tableMeta !== void 0 ? tableMeta : {});
            const field = fields[0];
            if (!field || !result.data.length) {
                return <BigNumber key={`big_number:${result.title}`}>{'\u2014'}</BigNumber>;
            }
            const dataRow = result.data[0];
            const fieldRenderer = (0, fieldRenderers_1.getFieldFormatter)(field, tableMeta);
            const rendered = fieldRenderer(dataRow);
            return <BigNumber key={`big_number:${result.title}`}>{rendered}</BigNumber>;
        });
    }
    chartComponent(chartProps) {
        const { widget } = this.props;
        switch (widget.displayType) {
            case 'bar':
                return <barChart_1.default {...chartProps}/>;
            case 'area':
            case 'top_n':
                return <areaChart_1.default stacked {...chartProps}/>;
            case 'world_map':
                return <worldMapChart_1.default {...chartProps}/>;
            case 'line':
            default:
                return <lineChart_1.default {...chartProps}/>;
        }
    }
    render() {
        var _a, _b, _c;
        const { theme, tableResults, timeseriesResults, errorMessage, loading, widget } = this.props;
        if (widget.displayType === 'table') {
            return (<transitionChart_1.default loading={loading} reloading={loading}>
          <LoadingScreen loading={loading}/>
          {this.tableResultComponent({ tableResults, loading, errorMessage })}
        </transitionChart_1.default>);
        }
        if (widget.displayType === 'big_number') {
            return (<transitionChart_1.default loading={loading} reloading={loading}>
          <LoadingScreen loading={loading}/>
          {this.bigNumberComponent({ tableResults, loading, errorMessage })}
        </transitionChart_1.default>);
        }
        if (errorMessage) {
            return (<errorPanel_1.default>
          <icons_1.IconWarning color="gray500" size="lg"/>
        </errorPanel_1.default>);
        }
        const { location, router, selection } = this.props;
        const { start, end, period, utc } = selection.datetime;
        if (widget.displayType === 'world_map') {
            const DEFAULT_GEO_DATA = {
                title: '',
                data: [],
            };
            const processTableResults = () => {
                var _a;
                if (!tableResults || !tableResults.length) {
                    return DEFAULT_GEO_DATA;
                }
                const tableResult = tableResults[0];
                const { data, meta } = tableResult;
                if (!data || !data.length || !meta) {
                    return DEFAULT_GEO_DATA;
                }
                const preAggregate = Object.keys(meta).find(column => {
                    return column !== 'geo.country_code';
                });
                if (!preAggregate) {
                    return DEFAULT_GEO_DATA;
                }
                return {
                    title: (_a = tableResult.title) !== null && _a !== void 0 ? _a : '',
                    data: data
                        .filter(row => row['geo.country_code'])
                        .map(row => {
                        return { name: row['geo.country_code'], value: row[preAggregate] };
                    }),
                };
            };
            const { data, title } = processTableResults();
            const series = [
                {
                    seriesName: title,
                    data,
                },
            ];
            return (<transitionChart_1.default loading={loading} reloading={loading}>
          <LoadingScreen loading={loading}/>
          <ChartWrapper>
            {(0, getDynamicText_1.default)({
                    value: this.chartComponent({
                        series,
                    }),
                    fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                })}
          </ChartWrapper>
        </transitionChart_1.default>);
        }
        const legend = {
            left: 0,
            top: 0,
            selected: (0, utils_1.getSeriesSelection)(location),
            formatter: (seriesName) => {
                const arg = (0, fields_1.getAggregateArg)(seriesName);
                if (arg !== null) {
                    const slug = (0, fields_1.getMeasurementSlug)(arg);
                    if (slug !== null) {
                        seriesName = slug.toUpperCase();
                    }
                }
                if ((0, fields_1.maybeEquationAlias)(seriesName)) {
                    seriesName = (0, fields_1.stripEquationPrefix)(seriesName);
                }
                return seriesName;
            },
        };
        const axisField = (_c = (_b = (_a = widget.queries[0]) === null || _a === void 0 ? void 0 : _a.fields) === null || _b === void 0 ? void 0 : _b[0]) !== null && _c !== void 0 ? _c : 'count()';
        const chartOptions = {
            grid: {
                left: 4,
                right: 0,
                top: '40px',
                bottom: 0,
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: charts_1.tooltipFormatter,
            },
            yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    formatter: (value) => (0, charts_1.axisLabelFormatter)(value, axisField),
                },
            },
        };
        return (<chartZoom_1.default router={router} period={period} start={start} end={end} utc={utc}>
        {zoomRenderProps => {
                if (errorMessage) {
                    return (<errorPanel_1.default>
                <icons_1.IconWarning color="gray500" size="lg"/>
              </errorPanel_1.default>);
                }
                const colors = timeseriesResults
                    ? theme.charts.getColorPalette(timeseriesResults.length - 2)
                    : [];
                // TODO(wmak): Need to change this when updating dashboards to support variable topEvents
                if (widget.displayType === 'top_n' &&
                    timeseriesResults &&
                    timeseriesResults.length > 5) {
                    colors[colors.length - 1] = theme.chartOther;
                }
                // Create a list of series based on the order of the fields,
                const series = timeseriesResults
                    ? timeseriesResults.map((values, i) => (Object.assign(Object.assign({}, values), { color: colors[i] })))
                    : [];
                return (<transitionChart_1.default loading={loading} reloading={loading}>
              <LoadingScreen loading={loading}/>
              <ChartWrapper>
                {(0, getDynamicText_1.default)({
                        value: this.chartComponent(Object.assign(Object.assign(Object.assign({}, zoomRenderProps), chartOptions), { legend,
                            series })),
                        fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                    })}
              </ChartWrapper>
            </transitionChart_1.default>);
            }}
      </chartZoom_1.default>);
    }
}
const StyledTransparentLoadingMask = (0, styled_1.default)(props => (<transparentLoadingMask_1.default {...props} maskBackgroundColor="transparent"/>)) `
  display: flex;
  justify-content: center;
  align-items: center;
`;
const LoadingScreen = ({ loading }) => {
    if (!loading) {
        return null;
    }
    return (<StyledTransparentLoadingMask visible={loading}>
      <loadingIndicator_1.default mini/>
    </StyledTransparentLoadingMask>);
};
const BigNumber = (0, styled_1.default)('div') `
  font-size: 32px;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(3)} ${(0, space_1.default)(3)} ${(0, space_1.default)(3)};
  * {
    text-align: left !important;
  }
`;
const ChartWrapper = (0, styled_1.default)('div') `
  padding: 0 ${(0, space_1.default)(3)} ${(0, space_1.default)(3)};
`;
const StyledSimpleTableChart = (0, styled_1.default)(simpleTableChart_1.default) `
  margin-top: ${(0, space_1.default)(1.5)};
  border-bottom-left-radius: ${p => p.theme.borderRadius};
  border-bottom-right-radius: ${p => p.theme.borderRadius};
  font-size: ${p => p.theme.fontSizeMedium};
  box-shadow: none;
`;
exports.default = (0, react_1.withTheme)(WidgetCardChart);
//# sourceMappingURL=widgetCardChart.jsx.map