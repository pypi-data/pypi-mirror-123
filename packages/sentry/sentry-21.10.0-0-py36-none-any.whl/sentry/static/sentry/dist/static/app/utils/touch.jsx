Object.defineProperty(exports, "__esModule", { value: true });
exports.getPointerPosition = void 0;
function isReactEvent(maybe) {
    return 'nativeEvent' in maybe;
}
/**
 * Handle getting position out of both React and Raw DOM events
 * as both are handled here due to mousedown/mousemove events
 * working differently.
 */
function getPointerPosition(event, property) {
    const actual = isReactEvent(event) ? event.nativeEvent : event;
    if (window.TouchEvent && actual instanceof TouchEvent) {
        return actual.targetTouches[0][property];
    }
    if (actual instanceof MouseEvent) {
        return actual[property];
    }
    return 0;
}
exports.getPointerPosition = getPointerPosition;
//# sourceMappingURL=touch.jsx.map