Object.defineProperty(exports, "__esModule", { value: true });
exports.Consumer = exports.Provider = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const utils_1 = require("app/components/performance/waterfall/utils");
const userselect_1 = require("app/utils/userselect");
// divider handle is positioned at 50% width from the left-hand side
const DEFAULT_DIVIDER_POSITION = 0.4;
const selectRefs = (refs, transform) => {
    refs.forEach(ref => {
        if (ref.current) {
            transform(ref.current);
        }
    });
};
const DividerManagerContext = React.createContext({
    dividerPosition: DEFAULT_DIVIDER_POSITION,
    onDragStart: () => { },
    setHover: () => { },
    addDividerLineRef: () => React.createRef(),
    addGhostDividerLineRef: () => React.createRef(),
});
class Provider extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            dividerPosition: DEFAULT_DIVIDER_POSITION,
        };
        this.previousUserSelect = null;
        this.dividerHandlePosition = DEFAULT_DIVIDER_POSITION;
        this.isDragging = false;
        this.dividerLineRefs = [];
        this.ghostDividerLineRefs = [];
        this.hasInteractiveLayer = () => !!this.props.interactiveLayerRef.current;
        this.addDividerLineRef = () => {
            const ref = React.createRef();
            this.dividerLineRefs.push(ref);
            return ref;
        };
        this.addGhostDividerLineRef = () => {
            const ref = React.createRef();
            this.ghostDividerLineRefs.push(ref);
            return ref;
        };
        this.setHover = (nextHover) => {
            if (this.isDragging) {
                return;
            }
            selectRefs(this.dividerLineRefs, dividerDOM => {
                if (nextHover) {
                    dividerDOM.classList.add('hovering');
                    return;
                }
                dividerDOM.classList.remove('hovering');
            });
        };
        this.onDragStart = (event) => {
            if (this.isDragging || event.type !== 'mousedown' || !this.hasInteractiveLayer()) {
                return;
            }
            event.stopPropagation();
            // prevent the user from selecting things outside the minimap when dragging
            // the mouse cursor inside the minimap
            this.previousUserSelect = (0, userselect_1.setBodyUserSelect)({
                userSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                webkitUserSelect: 'none',
            });
            // attach event listeners so that the mouse cursor does not select text during a drag
            window.addEventListener('mousemove', this.onDragMove);
            window.addEventListener('mouseup', this.onDragEnd);
            this.setHover(true);
            // indicate drag has begun
            this.isDragging = true;
            selectRefs(this.dividerLineRefs, (dividerDOM) => {
                dividerDOM.style.backgroundColor = 'rgba(73,80,87,0.75)';
                dividerDOM.style.cursor = 'col-resize';
            });
            selectRefs(this.ghostDividerLineRefs, (dividerDOM) => {
                dividerDOM.style.cursor = 'col-resize';
                const { parentNode } = dividerDOM;
                if (!parentNode) {
                    return;
                }
                const container = parentNode;
                container.style.display = 'block';
            });
        };
        this.onDragMove = (event) => {
            if (!this.isDragging || event.type !== 'mousemove' || !this.hasInteractiveLayer()) {
                return;
            }
            const rect = (0, utils_1.rectOfContent)(this.props.interactiveLayerRef.current);
            // mouse x-coordinate relative to the interactive layer's left side
            const rawMouseX = (event.pageX - rect.x) / rect.width;
            const min = 0;
            const max = 1;
            // clamp rawMouseX to be within [0, 1]
            this.dividerHandlePosition = (0, utils_1.clamp)(rawMouseX, min, max);
            const dividerHandlePositionString = (0, utils_1.toPercent)(this.dividerHandlePosition);
            selectRefs(this.ghostDividerLineRefs, (dividerDOM) => {
                const { parentNode } = dividerDOM;
                if (!parentNode) {
                    return;
                }
                const container = parentNode;
                container.style.width = `calc(${dividerHandlePositionString} + 0.5px)`;
            });
        };
        this.onDragEnd = (event) => {
            if (!this.isDragging || event.type !== 'mouseup' || !this.hasInteractiveLayer()) {
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
            this.isDragging = false;
            this.setHover(false);
            selectRefs(this.dividerLineRefs, (dividerDOM) => {
                dividerDOM.style.backgroundColor = '';
                dividerDOM.style.cursor = '';
            });
            selectRefs(this.ghostDividerLineRefs, (dividerDOM) => {
                dividerDOM.style.cursor = '';
                const { parentNode } = dividerDOM;
                if (!parentNode) {
                    return;
                }
                const container = parentNode;
                container.style.display = 'none';
            });
            this.setState({
                // commit dividerHandlePosition to be dividerPosition
                dividerPosition: this.dividerHandlePosition,
            });
        };
        this.cleanUpListeners = () => {
            if (this.isDragging) {
                // we only remove listeners during a drag
                window.removeEventListener('mousemove', this.onDragMove);
                window.removeEventListener('mouseup', this.onDragEnd);
            }
        };
    }
    componentWillUnmount() {
        this.cleanUpListeners();
    }
    render() {
        const childrenProps = {
            dividerPosition: this.state.dividerPosition,
            setHover: this.setHover,
            onDragStart: this.onDragStart,
            addDividerLineRef: this.addDividerLineRef,
            addGhostDividerLineRef: this.addGhostDividerLineRef,
        };
        // NOTE: <DividerManagerContext.Provider /> will not re-render its children
        // - if the `value` prop changes, and
        // - if the `children` prop stays the same
        //
        // Thus, only <DividerManagerContext.Consumer /> components will re-render.
        // This is an optimization for when childrenProps changes, but this.props does not change.
        //
        // We prefer to minimize the amount of top-down prop drilling from this component
        // to the respective divider components.
        return (<DividerManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </DividerManagerContext.Provider>);
    }
}
exports.Provider = Provider;
exports.Consumer = DividerManagerContext.Consumer;
//# sourceMappingURL=dividerHandlerManager.jsx.map