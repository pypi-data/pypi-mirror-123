Object.defineProperty(exports, "__esModule", { value: true });
require("echarts/lib/component/dataZoomInside");
const DEFAULT = {
    type: 'inside',
    // Mouse wheel can not trigger zoom
    zoomOnMouseWheel: false,
    // The translation (by mouse drag or touch drag) is avialable but zoom is not
    zoomLock: true,
    throttle: 50,
};
function DataZoomInside(props) {
    // `props` can be boolean, if so return default
    if (!props || !Array.isArray(props)) {
        const dataZoom = Object.assign(Object.assign({}, DEFAULT), props);
        return [dataZoom];
    }
    return props;
}
exports.default = DataZoomInside;
//# sourceMappingURL=dataZoomInside.jsx.map