Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_popper_1 = require("react-popper");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("@sentry/utils");
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const heatMapChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/heatMapChart"));
const styles_1 = require("app/components/charts/styles");
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const dropdownControl_1 = require("app/components/dropdownControl");
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const styles_2 = require("app/components/quickTrace/styles");
const truncate_1 = (0, tslib_1.__importDefault)(require("app/components/truncate"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const charts_1 = require("app/utils/discover/charts");
const formatters_1 = require("app/utils/formatters");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const tagTransactionsQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/segmentExplorer/tagTransactionsQuery"));
const queryString_1 = require("app/utils/queryString");
const utils_2 = require("../../utils");
const utils_3 = require("../transactionEvents/utils");
const utils_4 = require("../utils");
const utils_5 = require("./utils");
const findRowKey = row => {
    return Object.keys(row).find(key => key.includes('histogram'));
};
class VirtualReference {
    constructor(element) {
        this.boundingRect = element.getBoundingClientRect();
    }
    getBoundingClientRect() {
        return this.boundingRect;
    }
    get clientWidth() {
        return this.getBoundingClientRect().width;
    }
    get clientHeight() {
        return this.getBoundingClientRect().height;
    }
}
const getPortal = (0, memoize_1.default)(() => {
    let portal = document.getElementById('heatmap-portal');
    if (!portal) {
        portal = document.createElement('div');
        portal.setAttribute('id', 'heatmap-portal');
        document.body.appendChild(portal);
    }
    return portal;
});
const TagsHeatMap = (props) => {
    const { tableData, isLoading, organization, eventView, location, tagKey, transactionName, aggregateColumn, } = props;
    const chartRef = (0, react_1.useRef)(null);
    const [chartElement, setChartElement] = (0, react_1.useState)();
    const [transactionEventView, setTransactionEventView] = (0, react_1.useState)();
    const [isMenuOpen, setIsMenuOpen] = (0, react_1.useState)(false);
    // TODO(k-fish): Replace with actual theme colors.
    const purples = ['#D1BAFC', '#9282F3', '#6056BA', '#313087', '#021156'];
    const xValues = new Set();
    const histogramData = tableData &&
        tableData.histogram &&
        tableData.histogram.data &&
        tableData.histogram.data.length
        ? tableData.histogram.data
        : undefined;
    const tagData = tableData && tableData.tags && tableData.tags.data ? tableData.tags.data : undefined;
    const rowKey = histogramData && findRowKey(histogramData[0]);
    // Reverse since e-charts takes the axis labels in the opposite order.
    const columnNames = tagData ? tagData.map(tag => tag.tags_value).reverse() : [];
    let maxCount = 0;
    const _data = rowKey && histogramData
        ? histogramData.map(row => {
            const rawDuration = row[rowKey];
            const x = (0, utils_2.getPerformanceDuration)(rawDuration);
            const y = row.tags_value;
            xValues.add(x);
            maxCount = Math.max(maxCount, row.count);
            return [x, y, row.count];
        })
        : null;
    _data &&
        _data.sort((a, b) => {
            if (a[0] === b[0]) {
                return b[1] - a[1];
            }
            return b[0] - a[0];
        });
    // TODO(k-fish): Cleanup options
    const chartOptions = {
        height: 290,
        animation: false,
        colors: purples,
        tooltip: {},
        yAxis: {
            type: 'category',
            data: Array.from(columnNames),
            splitArea: {
                show: true,
            },
            axisLabel: {
                formatter: (value) => (0, utils_1.truncate)(value, 30),
            },
        },
        xAxis: {
            boundaryGap: true,
            type: 'category',
            splitArea: {
                show: true,
            },
            data: Array.from(xValues),
            axisLabel: {
                show: true,
                showMinLabel: true,
                showMaxLabel: true,
                formatter: (value) => (0, charts_1.axisLabelFormatter)(value, 'Count'),
            },
            axisLine: {},
            axisPointer: {
                show: false,
            },
            axisTick: {
                show: true,
                interval: 0,
                alignWithLabel: true,
            },
        },
        grid: {
            left: (0, space_1.default)(3),
            right: (0, space_1.default)(3),
            top: '25px',
            bottom: (0, space_1.default)(4),
        },
    };
    const visualMaps = [
        {
            min: 0,
            max: maxCount,
            show: false,
            orient: 'horizontal',
            calculable: true,
            inRange: {
                color: purples,
            },
        },
    ];
    const series = [];
    if (_data) {
        series.push({
            seriesName: 'Count',
            dataArray: _data,
            label: {
                show: true,
                formatter: data => (0, formatters_1.formatAbbreviatedNumber)(data.value[2]),
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)',
                },
            },
        }); // TODO(k-fish): Fix heatmap data typing
    }
    const onOpenMenu = () => {
        setIsMenuOpen(true);
    };
    const onCloseMenu = () => {
        setIsMenuOpen(false);
    };
    const shouldIgnoreMenuClose = e => {
        var _a;
        if ((_a = chartRef.current) === null || _a === void 0 ? void 0 : _a.getEchartsInstance().getDom().contains(e.target)) {
            // Ignore the menu being closed if the echart is being clicked.
            return true;
        }
        return false;
    };
    const histogramBucketInfo = histogramData && (0, utils_5.parseHistogramBucketInfo)(histogramData[0]);
    return (<StyledPanel>
      <StyledHeaderTitleLegend>
        {(0, locale_1.t)('Heat Map')}
        <questionTooltip_1.default size="sm" position="top" title={(0, locale_1.t)('This heatmap shows the frequency for each duration across the most common tag values')}/>
      </StyledHeaderTitleLegend>

      <transitionChart_1.default loading={isLoading} reloading={isLoading}>
        <transparentLoadingMask_1.default visible={isLoading}/>
        <dropdownMenu_1.default onOpen={onOpenMenu} onClose={onCloseMenu} shouldIgnoreClickOutside={shouldIgnoreMenuClose}>
          {({ isOpen, getMenuProps, actions }) => {
            const onChartClick = bucket => {
                const htmlEvent = bucket.event.event;
                // Make a copy of the dims because echarts can remove elements after this click happens.
                // TODO(k-fish): Look at improving this to respond properly to resize events.
                const virtualRef = new VirtualReference(htmlEvent.target);
                setChartElement(virtualRef);
                const newTransactionEventView = eventView.clone();
                newTransactionEventView.fields = [{ field: aggregateColumn }];
                const [_, tagValue] = bucket.value;
                if (histogramBucketInfo && histogramData) {
                    const row = histogramData[bucket.dataIndex];
                    const currentBucketStart = parseInt(`${row[histogramBucketInfo.histogramField]}`, 10);
                    const currentBucketEnd = currentBucketStart + histogramBucketInfo.bucketSize;
                    newTransactionEventView.additionalConditions.setFilterValues(aggregateColumn, [`>=${currentBucketStart}`, `<${currentBucketEnd}`]);
                }
                if (tagKey) {
                    newTransactionEventView.additionalConditions.setFilterValues(tagKey, [
                        tagValue,
                    ]);
                }
                setTransactionEventView(newTransactionEventView);
                (0, utils_5.trackTagPageInteraction)(organization);
                if (!isMenuOpen) {
                    actions.open();
                }
            };
            return (<react_1.default.Fragment>
                {react_dom_1.default.createPortal(<div>
                    {chartElement ? (<react_popper_1.Popper referenceElement={chartElement} placement="bottom">
                        {({ ref, style, placement }) => (<StyledDropdownContainer ref={ref} style={style} className="anchor-middle" data-placement={placement}>
                            <StyledDropdownContent {...getMenuProps({
                            className: (0, classnames_1.default)('dropdown-menu'),
                        })} isOpen={isOpen} alignMenu="right" blendCorner={false}>
                              {transactionEventView ? (<tagTransactionsQuery_1.default query={transactionEventView.getQueryWithAdditionalConditions()} location={location} eventView={transactionEventView} orgSlug={organization.slug} limit={4} referrer="api.performance.tag-page">
                                  {({ isLoading: isTransactionsLoading, tableData: transactionTableData, }) => {
                                    const moreEventsTarget = isTransactionsLoading
                                        ? null
                                        : (0, utils_3.eventsRouteWithQuery)({
                                            orgSlug: organization.slug,
                                            transaction: transactionName,
                                            projectID: (0, queryString_1.decodeScalar)(location.query.project),
                                            query: Object.assign(Object.assign({}, transactionEventView.generateQueryStringObject()), { query: transactionEventView.getQueryWithAdditionalConditions() }),
                                        });
                                    return (<react_1.default.Fragment>
                                        {isTransactionsLoading ? (<LoadingContainer>
                                            <loadingIndicator_1.default size={40} hideMessage/>
                                          </LoadingContainer>) : (<div>
                                            {!transactionTableData.data.length ? (<placeholder_1.default />) : null}
                                            {[...transactionTableData.data]
                                                .slice(0, 3)
                                                .map(row => {
                                                const target = (0, utils_4.generateTransactionLink)(transactionName)(organization, row, location.query);
                                                return (<styles_2.DropdownItem width="small" key={row.id} to={target}>
                                                    <DropdownItemContainer>
                                                      <truncate_1.default value={row.id} maxLength={12}/>
                                                      <styles_2.SectionSubtext>
                                                        <utils_2.PerformanceDuration milliseconds={row[aggregateColumn]} abbreviation/>
                                                      </styles_2.SectionSubtext>
                                                    </DropdownItemContainer>
                                                  </styles_2.DropdownItem>);
                                            })}
                                            {moreEventsTarget &&
                                                transactionTableData.data.length > 3 ? (<styles_2.DropdownItem width="small" to={moreEventsTarget}>
                                                <DropdownItemContainer>
                                                  {(0, locale_1.t)('View all events')}
                                                </DropdownItemContainer>
                                              </styles_2.DropdownItem>) : null}
                                          </div>)}
                                      </react_1.default.Fragment>);
                                }}
                                </tagTransactionsQuery_1.default>) : null}
                            </StyledDropdownContent>
                          </StyledDropdownContainer>)}
                      </react_popper_1.Popper>) : null}
                  </div>, getPortal())}

                {(0, getDynamicText_1.default)({
                    value: (<heatMapChart_1.default ref={chartRef} visualMaps={visualMaps} series={series} onClick={onChartClick} {...chartOptions}/>),
                    fixed: <placeholder_1.default height="290px" testId="skeleton-ui"/>,
                })}
              </react_1.default.Fragment>);
        }}
        </dropdownMenu_1.default>
      </transitionChart_1.default>
    </StyledPanel>);
};
const LoadingContainer = (0, styled_1.default)('div') `
  width: 200px;
  height: 100px;

  display: flex;
  align-items: center;
  justify-content: center;
`;
const DropdownItemContainer = (0, styled_1.default)('div') `
  width: 100%;
  display: flex;
  flex-direction: row;

  justify-content: space-between;
`;
const StyledDropdownContainer = (0, styled_1.default)(styles_2.DropdownContainer) `
  z-index: ${p => p.theme.zIndex.dropdown};
`;
const StyledDropdownContent = (0, styled_1.default)(dropdownControl_1.Content) `
  right: auto;
  transform: translate(-50%);

  overflow: visible;
`;
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(3)} 0 ${(0, space_1.default)(3)};
  margin-bottom: 0;
  border-bottom: 0;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
`;
const StyledHeaderTitleLegend = (0, styled_1.default)(styles_1.HeaderTitleLegend) ``;
exports.default = TagsHeatMap;
//# sourceMappingURL=tagsHeatMap.jsx.map