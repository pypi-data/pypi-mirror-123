Object.defineProperty(exports, "__esModule", { value: true });
exports.formatHistogramData = exports.computeBuckets = exports.getBucketWidth = void 0;
const formatters_1 = require("app/utils/formatters");
function getBucketWidth(data) {
    // We can assume that all buckets are of equal width, use the first two
    // buckets to get the width. The value of each histogram function indicates
    // the beginning of the bucket.
    return data.length >= 2 ? data[1].bin - data[0].bin : 0;
}
exports.getBucketWidth = getBucketWidth;
function computeBuckets(data) {
    const width = getBucketWidth(data);
    return data.map(item => {
        const bucket = item.bin;
        return {
            start: bucket,
            end: bucket + width,
        };
    });
}
exports.computeBuckets = computeBuckets;
function formatHistogramData(data, { precision, type, additionalFieldsFn, } = {}) {
    const formatter = (value) => {
        switch (type) {
            case 'duration':
                const decimalPlaces = precision !== null && precision !== void 0 ? precision : (value < 1000 ? 0 : 3);
                return (0, formatters_1.getDuration)(value / 1000, decimalPlaces, true);
            case 'number':
                // This is trying to avoid some of potential rounding errors that cause bins
                // have the same label, if the number of bins doesn't visually match what is
                // expected, check that this rounding is correct. If this issue persists,
                // consider formatting the bin as a string in the response
                const factor = Math.pow(10, (precision !== null && precision !== void 0 ? precision : 0));
                return (Math.round((value + Number.EPSILON) * factor) / factor).toLocaleString();
            default:
                throw new Error(`Unable to format type: ${type}`);
        }
    };
    return data.map(item => {
        var _a;
        return Object.assign({ value: item.count, name: formatter(item.bin) }, ((_a = additionalFieldsFn === null || additionalFieldsFn === void 0 ? void 0 : additionalFieldsFn(item.bin)) !== null && _a !== void 0 ? _a : {}));
    });
}
exports.formatHistogramData = formatHistogramData;
//# sourceMappingURL=utils.jsx.map