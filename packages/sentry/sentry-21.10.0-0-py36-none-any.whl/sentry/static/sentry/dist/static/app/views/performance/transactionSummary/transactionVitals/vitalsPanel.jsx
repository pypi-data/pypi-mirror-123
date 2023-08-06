Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const panels_1 = require("app/components/panels");
const histogramQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/histogram/histogramQuery"));
const constants_1 = require("app/utils/performance/vitals/constants");
const vitalsCardsDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/vitals/vitalsCardsDiscoverQuery"));
const queryString_1 = require("app/utils/queryString");
const constants_2 = require("./constants");
const vitalCard_1 = (0, tslib_1.__importDefault)(require("./vitalCard"));
class VitalsPanel extends react_1.Component {
    renderVitalCard(vital, isLoading, error, data, histogram, color, min, max, precision) {
        const { location, organization, eventView, dataFilter } = this.props;
        const vitalDetails = constants_1.WEB_VITAL_DETAILS[vital];
        const zoomed = min !== undefined || max !== undefined;
        return (<histogramQuery_1.default location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={constants_2.NUM_BUCKETS} fields={zoomed ? [vital] : []} min={min} max={max} precision={precision} dataFilter={dataFilter}>
        {results => {
                var _a, _b;
                const loading = zoomed ? results.isLoading : isLoading;
                const errored = zoomed ? results.error !== null : error;
                const chartData = zoomed ? (_b = (_a = results.histograms) === null || _a === void 0 ? void 0 : _a[vital]) !== null && _b !== void 0 ? _b : histogram : histogram;
                return (<vitalCard_1.default location={location} isLoading={loading} error={errored} vital={vital} vitalDetails={vitalDetails} summaryData={data} chartData={chartData} colors={color} eventView={eventView} organization={organization} min={min} max={max} precision={precision} dataFilter={dataFilter}/>);
            }}
      </histogramQuery_1.default>);
    }
    renderVitalGroup(group, summaryResults) {
        const { location, organization, eventView, dataFilter } = this.props;
        const { vitals, colors, min, max, precision } = group;
        const bounds = vitals.reduce((allBounds, vital) => {
            const slug = constants_1.WEB_VITAL_DETAILS[vital].slug;
            allBounds[vital] = {
                start: (0, queryString_1.decodeScalar)(location.query[`${slug}Start`]),
                end: (0, queryString_1.decodeScalar)(location.query[`${slug}End`]),
            };
            return allBounds;
        }, {});
        return (<histogramQuery_1.default location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={constants_2.NUM_BUCKETS} fields={vitals} min={min} max={max} precision={precision} dataFilter={dataFilter}>
        {multiHistogramResults => {
                const isLoading = summaryResults.isLoading || multiHistogramResults.isLoading;
                const error = summaryResults.error !== null || multiHistogramResults.error !== null;
                return (<react_1.Fragment>
              {vitals.map((vital, index) => {
                        var _a, _b, _c, _d, _e;
                        const data = (_b = (_a = summaryResults === null || summaryResults === void 0 ? void 0 : summaryResults.vitalsData) === null || _a === void 0 ? void 0 : _a[vital]) !== null && _b !== void 0 ? _b : null;
                        const histogram = (_d = (_c = multiHistogramResults.histograms) === null || _c === void 0 ? void 0 : _c[vital]) !== null && _d !== void 0 ? _d : [];
                        const { start, end } = (_e = bounds[vital]) !== null && _e !== void 0 ? _e : {};
                        return (<react_1.Fragment key={vital}>
                    {this.renderVitalCard(vital, isLoading, error, data, histogram, [colors[index]], parseBound(start, precision), parseBound(end, precision), precision)}
                  </react_1.Fragment>);
                    })}
            </react_1.Fragment>);
            }}
      </histogramQuery_1.default>);
    }
    render() {
        const { location, organization, eventView } = this.props;
        const allVitals = constants_2.VITAL_GROUPS.reduce((keys, { vitals }) => {
            return keys.concat(vitals);
        }, []);
        return (<panels_1.Panel>
        <vitalsCardsDiscoverQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} vitals={allVitals}>
          {results => (<react_1.Fragment>
              {constants_2.VITAL_GROUPS.map(vitalGroup => (<react_1.Fragment key={vitalGroup.vitals.join('')}>
                  {this.renderVitalGroup(vitalGroup, results)}
                </react_1.Fragment>))}
            </react_1.Fragment>)}
        </vitalsCardsDiscoverQuery_1.default>
      </panels_1.Panel>);
    }
}
function parseBound(boundString, precision) {
    if (boundString === undefined) {
        return undefined;
    }
    else if (precision === undefined || precision === 0) {
        return parseInt(boundString, 10);
    }
    return parseFloat(boundString);
}
exports.default = VitalsPanel;
//# sourceMappingURL=vitalsPanel.jsx.map