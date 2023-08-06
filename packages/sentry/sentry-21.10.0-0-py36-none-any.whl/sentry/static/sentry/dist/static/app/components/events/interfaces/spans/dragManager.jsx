Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const utils_1 = require("app/components/performance/waterfall/utils");
const userselect_1 = require("app/utils/userselect");
// we establish the minimum window size so that the window size of 0% is not possible
const MINIMUM_WINDOW_SIZE = 0.5 / 100; // 0.5% window size
var ViewHandleType;
(function (ViewHandleType) {
    ViewHandleType[ViewHandleType["Left"] = 0] = "Left";
    ViewHandleType[ViewHandleType["Right"] = 1] = "Right";
})(ViewHandleType || (ViewHandleType = {}));
class DragManager extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            // draggable handles
            isDragging: false,
            currentDraggingHandle: void 0,
            leftHandlePosition: 0,
            rightHandlePosition: 1,
            // window selection
            isWindowSelectionDragging: false,
            windowSelectionInitial: 0,
            windowSelectionCurrent: 0,
            windowSelectionSize: 0,
            // window sizes
            viewWindowStart: 0,
            viewWindowEnd: 1,
        };
        this.previousUserSelect = null;
        this.hasInteractiveLayer = () => !!this.props.interactiveLayerRef.current;
        this.onDragStart = (viewHandle) => (event) => {
            const isDragging = this.state.isDragging || this.state.isWindowSelectionDragging;
            if (isDragging || event.type !== 'mousedown' || !this.hasInteractiveLayer()) {
                return;
            }
            // prevent the user from selecting things outside the minimap when dragging
            // the mouse cursor outside the minimap
            this.previousUserSelect = (0, userselect_1.setBodyUserSelect)({
                userSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                webkitUserSelect: 'none',
            });
            // attach event listeners so that the mouse cursor can drag outside of the
            // minimap
            window.addEventListener('mousemove', this.onDragMove);
            window.addEventListener('mouseup', this.onDragEnd);
            // indicate drag has begun
            this.setState({
                isDragging: true,
                isWindowSelectionDragging: false,
                currentDraggingHandle: viewHandle,
            });
        };
        this.onLeftHandleDragStart = (event) => {
            this.onDragStart(ViewHandleType.Left)(event);
        };
        this.onRightHandleDragStart = (event) => {
            this.onDragStart(ViewHandleType.Right)(event);
        };
        this.onDragMove = (event) => {
            if (!this.state.isDragging ||
                event.type !== 'mousemove' ||
                !this.hasInteractiveLayer()) {
                return;
            }
            const rect = (0, utils_1.rectOfContent)(this.props.interactiveLayerRef.current);
            // mouse x-coordinate relative to the interactive layer's left side
            const rawMouseX = (event.pageX - rect.x) / rect.width;
            switch (this.state.currentDraggingHandle) {
                case ViewHandleType.Left: {
                    const min = 0;
                    const max = this.state.rightHandlePosition - MINIMUM_WINDOW_SIZE;
                    this.setState({
                        // clamp rawMouseX to be within [0, rightHandlePosition - MINIMUM_WINDOW_SIZE]
                        leftHandlePosition: (0, utils_1.clamp)(rawMouseX, min, max),
                    });
                    break;
                }
                case ViewHandleType.Right: {
                    const min = this.state.leftHandlePosition + MINIMUM_WINDOW_SIZE;
                    const max = 1;
                    this.setState({
                        // clamp rawMouseX to be within [leftHandlePosition + MINIMUM_WINDOW_SIZE, 1]
                        rightHandlePosition: (0, utils_1.clamp)(rawMouseX, min, max),
                    });
                    break;
                }
                default: {
                    throw Error('this.state.currentDraggingHandle is undefined');
                }
            }
        };
        this.onDragEnd = (event) => {
            if (!this.state.isDragging ||
                event.type !== 'mouseup' ||
                !this.hasInteractiveLayer()) {
                return;
            }
            // remove listeners that were attached in onDragStart
            this.cleanUpListeners();
            // restore body styles
            if (this.previousUserSelect) {
                (0, userselect_1.setBodyUserSelect)(this.previousUserSelect);
                this.previousUserSelect = null;
            }
            // indicate drag has ended
            switch (this.state.currentDraggingHandle) {
                case ViewHandleType.Left: {
                    this.setState(state => ({
                        isDragging: false,
                        currentDraggingHandle: void 0,
                        // commit leftHandlePosition to be viewWindowStart
                        viewWindowStart: state.leftHandlePosition,
                    }));
                    return;
                }
                case ViewHandleType.Right: {
                    this.setState(state => ({
                        isDragging: false,
                        currentDraggingHandle: void 0,
                        // commit rightHandlePosition to be viewWindowEnd
                        viewWindowEnd: state.rightHandlePosition,
                    }));
                    return;
                }
                default: {
                    throw Error('this.state.currentDraggingHandle is undefined');
                }
            }
        };
        this.onWindowSelectionDragStart = (event) => {
            const isDragging = this.state.isDragging || this.state.isWindowSelectionDragging;
            if (isDragging || event.type !== 'mousedown' || !this.hasInteractiveLayer()) {
                return;
            }
            // prevent the user from selecting things outside the minimap when dragging
            // the mouse cursor outside the minimap
            this.previousUserSelect = (0, userselect_1.setBodyUserSelect)({
                userSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                webkitUserSelect: 'none',
            });
            // attach event listeners so that the mouse cursor can drag outside of the
            // minimap
            window.addEventListener('mousemove', this.onWindowSelectionDragMove);
            window.addEventListener('mouseup', this.onWindowSelectionDragEnd);
            // indicate drag has begun
            const rect = (0, utils_1.rectOfContent)(this.props.interactiveLayerRef.current);
            // mouse x-coordinate relative to the interactive layer's left side
            const rawMouseX = (event.pageX - rect.x) / rect.width;
            this.setState({
                isDragging: false,
                isWindowSelectionDragging: true,
                windowSelectionInitial: rawMouseX,
                windowSelectionCurrent: rawMouseX, // between 0 (0%) and 1 (100%)
            });
        };
        this.onWindowSelectionDragMove = (event) => {
            if (!this.state.isWindowSelectionDragging ||
                event.type !== 'mousemove' ||
                !this.hasInteractiveLayer()) {
                return;
            }
            const rect = (0, utils_1.rectOfContent)(this.props.interactiveLayerRef.current);
            // mouse x-coordinate relative to the interactive layer's left side
            const rawMouseX = (event.pageX - rect.x) / rect.width;
            const min = 0;
            const max = 1;
            // clamp rawMouseX to be within [0, 1]
            const windowSelectionCurrent = (0, utils_1.clamp)(rawMouseX, min, max);
            const windowSelectionSize = (0, utils_1.clamp)(Math.abs(this.state.windowSelectionInitial - windowSelectionCurrent), min, max);
            this.setState({
                windowSelectionCurrent,
                windowSelectionSize,
            });
        };
        this.onWindowSelectionDragEnd = (event) => {
            if (!this.state.isWindowSelectionDragging ||
                event.type !== 'mouseup' ||
                !this.hasInteractiveLayer()) {
                return;
            }
            // remove listeners that were attached in onWindowSelectionDragStart
            this.cleanUpListeners();
            // restore body styles
            if (this.previousUserSelect) {
                (0, userselect_1.setBodyUserSelect)(this.previousUserSelect);
                this.previousUserSelect = null;
            }
            // indicate drag has ended
            this.setState(state => {
                let viewWindowStart = Math.min(state.windowSelectionInitial, state.windowSelectionCurrent);
                let viewWindowEnd = Math.max(state.windowSelectionInitial, state.windowSelectionCurrent);
                // enforce minimum window size
                if (viewWindowEnd - viewWindowStart < MINIMUM_WINDOW_SIZE) {
                    viewWindowEnd = viewWindowStart + MINIMUM_WINDOW_SIZE;
                    if (viewWindowEnd > 1) {
                        viewWindowEnd = 1;
                        viewWindowStart = 1 - MINIMUM_WINDOW_SIZE;
                    }
                }
                return {
                    isWindowSelectionDragging: false,
                    windowSelectionInitial: 0,
                    windowSelectionCurrent: 0,
                    windowSelectionSize: 0,
                    leftHandlePosition: viewWindowStart,
                    rightHandlePosition: viewWindowEnd,
                    viewWindowStart,
                    viewWindowEnd,
                };
            });
        };
        this.cleanUpListeners = () => {
            if (this.state.isDragging) {
                window.removeEventListener('mousemove', this.onDragMove);
                window.removeEventListener('mouseup', this.onDragEnd);
            }
            if (this.state.isWindowSelectionDragging) {
                window.removeEventListener('mousemove', this.onWindowSelectionDragMove);
                window.removeEventListener('mouseup', this.onWindowSelectionDragEnd);
            }
        };
    }
    componentWillUnmount() {
        this.cleanUpListeners();
    }
    render() {
        const childrenProps = {
            isDragging: this.state.isDragging,
            // left handle
            onLeftHandleDragStart: this.onLeftHandleDragStart,
            leftHandlePosition: this.state.leftHandlePosition,
            // right handle
            onRightHandleDragStart: this.onRightHandleDragStart,
            rightHandlePosition: this.state.rightHandlePosition,
            // window selection
            isWindowSelectionDragging: this.state.isWindowSelectionDragging,
            windowSelectionInitial: this.state.windowSelectionInitial,
            windowSelectionCurrent: this.state.windowSelectionCurrent,
            windowSelectionSize: this.state.windowSelectionSize,
            onWindowSelectionDragStart: this.onWindowSelectionDragStart,
            // window sizes
            viewWindowStart: this.state.viewWindowStart,
            viewWindowEnd: this.state.viewWindowEnd,
        };
        return this.props.children(childrenProps);
    }
}
exports.default = DragManager;
//# sourceMappingURL=dragManager.jsx.map