Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("echarts/lib/component/tooltip");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const dates_1 = require("app/utils/dates");
const utils_1 = require("../utils");
function defaultFormatAxisLabel(value, isTimestamp, utc, showTimeInTooltip, bucketSize) {
    if (!isTimestamp) {
        return value;
    }
    if (!bucketSize) {
        const format = `MMM D, YYYY ${showTimeInTooltip ? (0, dates_1.getTimeFormat)() : ''}`.trim();
        return (0, dates_1.getFormattedDate)(value, format, { local: !utc });
    }
    const now = (0, moment_1.default)();
    const bucketStart = (0, moment_1.default)(value);
    const bucketEnd = (0, moment_1.default)(value + bucketSize);
    const showYear = now.year() !== bucketStart.year() || now.year() !== bucketEnd.year();
    const showEndDate = bucketStart.date() !== bucketEnd.date();
    const formatStart = `MMM D${showYear ? ', YYYY' : ''} ${showTimeInTooltip ? (0, dates_1.getTimeFormat)() : ''}`.trim();
    const formatEnd = `${showEndDate ? `MMM D${showYear ? ', YYYY' : ''} ` : ''}${showTimeInTooltip ? (0, dates_1.getTimeFormat)() : ''}`.trim();
    return `${(0, dates_1.getFormattedDate)(bucketStart, formatStart, {
        local: !utc,
    })} — ${(0, dates_1.getFormattedDate)(bucketEnd, formatEnd, { local: !utc })}`;
}
function defaultValueFormatter(value) {
    if (typeof value === 'number') {
        return value.toLocaleString();
    }
    return value;
}
function defaultNameFormatter(value) {
    return value;
}
function getSeriesValue(series, offset) {
    if (!series.data) {
        return undefined;
    }
    if (Array.isArray(series.data)) {
        return series.data[offset];
    }
    if (Array.isArray(series.data.value)) {
        return series.data.value[offset];
    }
    return undefined;
}
function getFormatter({ filter, isGroupedByDate, showTimeInTooltip, truncate, formatAxisLabel, utc, bucketSize, valueFormatter = defaultValueFormatter, nameFormatter = defaultNameFormatter, indentLabels = [], }) {
    const getFilter = (seriesParam) => {
        // Series do not necessarily have `data` defined, e.g. releases don't have `data`, but rather
        // has a series using strictly `markLine`s.
        // However, real series will have `data` as a tuple of (label, value) or be
        // an object with value/label keys.
        const value = getSeriesValue(seriesParam, 0);
        if (typeof filter === 'function') {
            return filter(value, seriesParam);
        }
        return true;
    };
    const formatter = seriesParamsOrParam => {
        var _a;
        // If this is a tooltip for the axis, it will include all series for that axis item.
        // In this case seriesParamsOrParam will be of type `Object[]`
        //
        // Otherwise, it will be an `Object`, and is a tooltip for a single item
        const axisFormatterOrDefault = formatAxisLabel || defaultFormatAxisLabel;
        // Special tooltip if component is a `markPoint`
        if (!Array.isArray(seriesParamsOrParam) &&
            // TODO(ts): The EChart types suggest that this can _only_ be `series`,
            //           but assuming this code is correct (which I have not
            //           verified) their types may be wrong.
            seriesParamsOrParam.componentType === 'markPoint') {
            const timestamp = seriesParamsOrParam.data.coord[0];
            const label = axisFormatterOrDefault(timestamp, !!isGroupedByDate, !!utc, !!showTimeInTooltip, bucketSize);
            // eCharts sets seriesName as null when `componentType` !== 'series'
            const truncatedName = (0, utils_1.truncationFormatter)(seriesParamsOrParam.data.labelForValue, truncate);
            const formattedValue = valueFormatter(seriesParamsOrParam.data.coord[1], seriesParamsOrParam.name);
            const className = indentLabels.includes((_a = seriesParamsOrParam.name) !== null && _a !== void 0 ? _a : '')
                ? 'tooltip-label tooltip-label-indent'
                : 'tooltip-label';
            return [
                '<div class="tooltip-series">',
                `<div>
          <span class="${className}"><strong>${seriesParamsOrParam.name}</strong></span>
          ${truncatedName}: ${formattedValue}
        </div>`,
                '</div>',
                `<div class="tooltip-date">${label}</div>`,
                '</div>',
            ].join('');
        }
        const seriesParams = Array.isArray(seriesParamsOrParam)
            ? seriesParamsOrParam
            : [seriesParamsOrParam];
        // If axis, timestamp comes from axis, otherwise for a single item it is defined in the data attribute.
        // The data attribute is usually a list of [name, value] but can also be an object of {name, value} when
        // there is item specific formatting being used.
        const timestamp = Array.isArray(seriesParamsOrParam)
            ? seriesParams[0].axisValue
            : getSeriesValue(seriesParams[0], 0);
        const date = seriesParams.length &&
            axisFormatterOrDefault(timestamp, !!isGroupedByDate, !!utc, !!showTimeInTooltip, bucketSize);
        return [
            '<div class="tooltip-series">',
            seriesParams
                .filter(getFilter)
                .map(s => {
                var _a;
                const formattedLabel = nameFormatter((0, utils_1.truncationFormatter)((_a = s.seriesName) !== null && _a !== void 0 ? _a : '', truncate));
                const value = valueFormatter(getSeriesValue(s, 1), s.seriesName);
                const className = indentLabels.includes(formattedLabel)
                    ? 'tooltip-label tooltip-label-indent'
                    : 'tooltip-label';
                return `<div><span class="${className}">${s.marker} <strong>${formattedLabel}</strong></span> ${value}</div>`;
            })
                .join(''),
            '</div>',
            `<div class="tooltip-date">${date}</div>`,
            `<div class="tooltip-arrow"></div>`,
        ].join('');
    };
    return formatter;
}
function Tooltip(_a = {}) {
    var { filter, isGroupedByDate, showTimeInTooltip, formatter, truncate, utc, bucketSize, formatAxisLabel, valueFormatter, nameFormatter, hideDelay, indentLabels } = _a, props = (0, tslib_1.__rest)(_a, ["filter", "isGroupedByDate", "showTimeInTooltip", "formatter", "truncate", "utc", "bucketSize", "formatAxisLabel", "valueFormatter", "nameFormatter", "hideDelay", "indentLabels"]);
    formatter =
        formatter ||
            getFormatter({
                filter,
                isGroupedByDate,
                showTimeInTooltip,
                truncate,
                utc,
                bucketSize,
                formatAxisLabel,
                valueFormatter,
                nameFormatter,
                indentLabels,
            });
    return Object.assign({ show: true, trigger: 'item', backgroundColor: 'transparent', transitionDuration: 0, padding: 0, 
        // Default hideDelay in echarts docs is 100ms
        hideDelay: hideDelay || 100, position(pos, _params, dom, _rec, _size) {
            // Center the tooltip slightly above the cursor.
            const tipWidth = dom.clientWidth;
            const tipHeight = dom.clientHeight;
            // Get the left offset of the tip container (the chart)
            // so that we can estimate overflows
            const chartLeft = dom.parentNode instanceof Element
                ? dom.parentNode.getBoundingClientRect().left
                : 0;
            // Determine the new left edge.
            let leftPos = Number(pos[0]) - tipWidth / 2;
            let arrowPosition = '50%';
            // And the right edge taking into account the chart left offset
            const rightEdge = chartLeft + Number(pos[0]) + tipWidth / 2;
            // If the tooltip would leave viewport on the right, pin it.
            // and adjust the arrow position.
            if (rightEdge >= window.innerWidth - 20) {
                leftPos -= rightEdge - window.innerWidth + 20;
                arrowPosition = `${Number(pos[0]) - leftPos}px`;
            }
            // If the tooltip would leave viewport on the left, pin it.
            if (leftPos + chartLeft - 20 <= 0) {
                leftPos = chartLeft * -1 + 20;
                arrowPosition = `${Number(pos[0]) - leftPos}px`;
            }
            // Reposition the arrow.
            const arrow = dom.querySelector('.tooltip-arrow');
            if (arrow) {
                arrow.style.left = arrowPosition;
            }
            return { left: leftPos, top: Number(pos[1]) - tipHeight - 20 };
        },
        formatter }, props);
}
exports.default = Tooltip;
//# sourceMappingURL=tooltip.jsx.map