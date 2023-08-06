Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("echarts/lib/component/toolbox");
function getFeatures(_a) {
    var { dataZoom } = _a, features = (0, tslib_1.__rest)(_a, ["dataZoom"]);
    return Object.assign(Object.assign({}, (dataZoom
        ? {
            dataZoom: Object.assign({ yAxisIndex: 'none', title: {
                    zoom: 'zoom',
                    back: 'undo',
                    restore: 'reset',
                } }, dataZoom),
        }
        : {})), features);
}
function ToolBox(options, features) {
    return Object.assign({ right: 0, top: 0, itemSize: 16, 
        // Stack the toolbox under the legend.
        // so all series names are clickable.
        z: -1, feature: getFeatures(features) }, options);
}
exports.default = ToolBox;
//# sourceMappingURL=toolBox.jsx.map