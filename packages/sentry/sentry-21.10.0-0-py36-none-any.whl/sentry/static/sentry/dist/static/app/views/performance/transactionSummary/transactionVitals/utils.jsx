Object.defineProperty(exports, "__esModule", { value: true });
exports.mapPoint = exports.asPixelRect = exports.getRefRect = exports.findNearestBucketIndex = exports.vitalsRouteWithQuery = exports.generateVitalsRoute = void 0;
const utils_1 = require("app/utils/performance/histogram/utils");
function generateVitalsRoute({ orgSlug }) {
    return `/organizations/${orgSlug}/performance/summary/vitals/`;
}
exports.generateVitalsRoute = generateVitalsRoute;
function vitalsRouteWithQuery({ orgSlug, transaction, projectID, query, }) {
    const pathname = generateVitalsRoute({
        orgSlug,
    });
    return {
        pathname,
        query: {
            transaction,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
        },
    };
}
exports.vitalsRouteWithQuery = vitalsRouteWithQuery;
/**
 * Given a value on the x-axis, return the index of the nearest bucket or null
 * if it cannot be found.
 *
 * A bucket contains a range of values, and nearest is defined as the bucket the
 * value will fall in.
 */
function findNearestBucketIndex(chartData, xAxis) {
    const width = (0, utils_1.getBucketWidth)(chartData);
    // it's possible that the data is not available yet or the x axis is out of range
    if (!chartData.length || xAxis >= chartData[chartData.length - 1].bin + width) {
        return null;
    }
    else if (xAxis < chartData[0].bin) {
        return -1;
    }
    return Math.floor((xAxis - chartData[0].bin) / width);
}
exports.findNearestBucketIndex = findNearestBucketIndex;
/**
 * To compute pixel coordinates, we need at least 2 unique points on the chart.
 * The two points must have different x axis and y axis values for it to work.
 *
 * If all bars have the same y value, pick the most naive reference rect. This
 * may result in floating point errors, but should be okay for our purposes.
 */
function getRefRect(chartData) {
    // not enough points to construct 2 reference points
    if (chartData.length < 2) {
        return null;
    }
    for (let i = 0; i < chartData.length; i++) {
        const data1 = chartData[i];
        for (let j = i + 1; j < chartData.length; j++) {
            const data2 = chartData[j];
            if (data1.bin !== data2.bin && data1.count !== data2.count) {
                return {
                    point1: { x: i, y: Math.min(data1.count, data2.count) },
                    point2: { x: j, y: Math.max(data1.count, data2.count) },
                };
            }
        }
    }
    // all data points have the same count, just pick any 2 histogram bins
    // and use 0 and 1 as the count as we can rely on them being on the graph
    return {
        point1: { x: 0, y: 0 },
        point2: { x: 1, y: 1 },
    };
}
exports.getRefRect = getRefRect;
/**
 * Given an ECharts instance and a rectangle defined in terms of the x and y axis,
 * compute the corresponding pixel coordinates. If it cannot be done, return null.
 */
function asPixelRect(chartRef, dataRect) {
    const point1 = chartRef.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [
        dataRect.point1.x,
        dataRect.point1.y,
    ]);
    if (isNaN(point1 === null || point1 === void 0 ? void 0 : point1[0]) || isNaN(point1 === null || point1 === void 0 ? void 0 : point1[1])) {
        return null;
    }
    const point2 = chartRef.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [
        dataRect.point2.x,
        dataRect.point2.y,
    ]);
    if (isNaN(point2 === null || point2 === void 0 ? void 0 : point2[0]) || isNaN(point2 === null || point2 === void 0 ? void 0 : point2[1])) {
        return null;
    }
    return {
        point1: { x: point1[0], y: point1[1] },
        point2: { x: point2[0], y: point2[1] },
    };
}
exports.asPixelRect = asPixelRect;
/**
 * Given a point on a source rectangle, map it to the corresponding point on the
 * destination rectangle. Assumes that the two rectangles are related by a simple
 * transformation containing only translations and scaling.
 */
function mapPoint(point, srcRect, destRect) {
    if (srcRect.point1.x === srcRect.point2.x ||
        srcRect.point1.y === srcRect.point2.y ||
        destRect.point1.x === destRect.point2.x ||
        destRect.point1.y === destRect.point2.y) {
        return null;
    }
    const xPercentage = (point.x - srcRect.point1.x) / (srcRect.point2.x - srcRect.point1.x);
    const yPercentage = (point.y - srcRect.point1.y) / (srcRect.point2.y - srcRect.point1.y);
    return {
        x: destRect.point1.x + (destRect.point2.x - destRect.point1.x) * xPercentage,
        y: destRect.point1.y + (destRect.point2.y - destRect.point1.y) * yPercentage,
    };
}
exports.mapPoint = mapPoint;
//# sourceMappingURL=utils.jsx.map