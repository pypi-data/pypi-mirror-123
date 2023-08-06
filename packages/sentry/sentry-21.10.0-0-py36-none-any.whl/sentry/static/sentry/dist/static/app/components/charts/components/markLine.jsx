Object.defineProperty(exports, "__esModule", { value: true });
require("echarts/lib/component/markLine");
/**
 * eCharts markLine
 *
 * See https://echarts.apache.org/en/option.html#series-line.markLine
 */
function MarkLine(props) {
    return Object.assign({ 
        // The second symbol is a very ugly arrow, we don't want it
        symbol: ['none', 'none'] }, props);
}
exports.default = MarkLine;
//# sourceMappingURL=markLine.jsx.map