Object.defineProperty(exports, "__esModule", { value: true });
require("echarts/lib/chart/map");
function MapSeries(props = {}) {
    return Object.assign(Object.assign({ roam: true, itemStyle: {
            // TODO(ts): label doesn't seem to exist on the emphasis? I have not
            //           verified if removing this has an affect on the world chart.
            emphasis: { label: { show: false } },
        } }, props), { type: 'map' });
}
exports.default = MapSeries;
//# sourceMappingURL=mapSeries.jsx.map