Object.defineProperty(exports, "__esModule", { value: true });
exports.withScrollbarManager = exports.Consumer = exports.Provider = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const utils_1 = require("app/components/performance/waterfall/utils");
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const userselect_1 = require("app/utils/userselect");
const ScrollbarManagerContext = React.createContext({
    generateContentSpanBarRef: () => () => undefined,
    virtualScrollbarRef: React.createRef(),
    scrollBarAreaRef: React.createRef(),
    onDragStart: () => { },
    onScroll: () => { },
    updateScrollState: () => { },
});
const selectRefs = (refs, transform) => {
    if (!(refs instanceof Set)) {
        if (refs.current) {
            transform(refs.current);
        }
        return;
    }
    refs.forEach(element => {
        if (document.body.contains(element)) {
            transform(element);
        }
    });
};
// simple linear interpolation between start and end such that needle is between [0, 1]
const lerp = (start, end, needle) => {
    return start + needle * (end - start);
};
class Provider extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            maxContentWidth: undefined,
        };
        this.contentSpanBar = new Set();
        this.virtualScrollbar = React.createRef();
        this.scrollBarArea = React.createRef();
        this.isDragging = false;
        this.previousUserSelect = null;
        this.initializeScrollState = () => {
            if (this.contentSpanBar.size === 0 || !this.hasInteractiveLayer()) {
                return;
            }
            // reset all span bar content containers to their natural widths
            selectRefs(this.contentSpanBar, (spanBarDOM) => {
                spanBarDOM.style.removeProperty('width');
                spanBarDOM.style.removeProperty('max-width');
                spanBarDOM.style.removeProperty('overflow');
                spanBarDOM.style.removeProperty('transform');
            });
            // Find the maximum content width. We set each content spanbar to be this maximum width,
            // such that all content spanbar widths are uniform.
            const maxContentWidth = Array.from(this.contentSpanBar).reduce((currentMaxWidth, currentSpanBar) => {
                const isHidden = currentSpanBar.offsetParent === null;
                if (!document.body.contains(currentSpanBar) || isHidden) {
                    return currentMaxWidth;
                }
                const maybeMaxWidth = currentSpanBar.scrollWidth;
                if (maybeMaxWidth > currentMaxWidth) {
                    return maybeMaxWidth;
                }
                return currentMaxWidth;
            }, 0);
            selectRefs(this.contentSpanBar, (spanBarDOM) => {
                spanBarDOM.style.width = `${maxContentWidth}px`;
                spanBarDOM.style.maxWidth = `${maxContentWidth}px`;
                spanBarDOM.style.overflow = 'hidden';
            });
            // set inner width of scrollbar area
            selectRefs(this.scrollBarArea, (scrollBarArea) => {
                scrollBarArea.style.width = `${maxContentWidth}px`;
                scrollBarArea.style.maxWidth = `${maxContentWidth}px`;
            });
            selectRefs(this.props.interactiveLayerRef, (interactiveLayerRefDOM) => {
                interactiveLayerRefDOM.scrollLeft = 0;
            });
            const spanBarDOM = this.getReferenceSpanBar();
            if (spanBarDOM) {
                this.syncVirtualScrollbar(spanBarDOM);
            }
        };
        this.syncVirtualScrollbar = (spanBar) => {
            // sync the virtual scrollbar's width to the spanBar's width
            if (!this.virtualScrollbar.current || !this.hasInteractiveLayer()) {
                return;
            }
            const virtualScrollbarDOM = this.virtualScrollbar.current;
            const maxContentWidth = spanBar.getBoundingClientRect().width;
            if (maxContentWidth === undefined || maxContentWidth <= 0) {
                virtualScrollbarDOM.style.width = '0';
                return;
            }
            const visibleWidth = this.props.interactiveLayerRef.current.getBoundingClientRect().width;
            // This is the width of the content not visible.
            const maxScrollDistance = maxContentWidth - visibleWidth;
            const virtualScrollbarWidth = visibleWidth / (visibleWidth + maxScrollDistance);
            if (virtualScrollbarWidth >= 1) {
                virtualScrollbarDOM.style.width = '0';
                return;
            }
            virtualScrollbarDOM.style.width = `max(50px, ${(0, utils_1.toPercent)(virtualScrollbarWidth)})`;
            virtualScrollbarDOM.style.removeProperty('transform');
        };
        this.generateContentSpanBarRef = () => {
            let previousInstance = null;
            const addContentSpanBarRef = (instance) => {
                if (previousInstance) {
                    this.contentSpanBar.delete(previousInstance);
                    previousInstance = null;
                }
                if (instance) {
                    this.contentSpanBar.add(instance);
                    previousInstance = instance;
                }
            };
            return addContentSpanBarRef;
        };
        this.hasInteractiveLayer = () => !!this.props.interactiveLayerRef.current;
        this.initialMouseClickX = undefined;
        this.onScroll = () => {
            if (this.isDragging || !this.hasInteractiveLayer()) {
                return;
            }
            const interactiveLayerRefDOM = this.props.interactiveLayerRef.current;
            const interactiveLayerRect = interactiveLayerRefDOM.getBoundingClientRect();
            const scrollLeft = interactiveLayerRefDOM.scrollLeft;
            // Update scroll position of the virtual scroll bar
            selectRefs(this.scrollBarArea, (scrollBarAreaDOM) => {
                selectRefs(this.virtualScrollbar, (virtualScrollbarDOM) => {
                    const scrollBarAreaRect = scrollBarAreaDOM.getBoundingClientRect();
                    const virtualScrollbarPosition = scrollLeft / scrollBarAreaRect.width;
                    const virtualScrollBarRect = (0, utils_1.rectOfContent)(virtualScrollbarDOM);
                    const maxVirtualScrollableArea = 1 - virtualScrollBarRect.width / interactiveLayerRect.width;
                    const virtualLeft = (0, utils_1.clamp)(virtualScrollbarPosition, 0, maxVirtualScrollableArea) *
                        interactiveLayerRect.width;
                    virtualScrollbarDOM.style.transform = `translate3d(${virtualLeft}px, 0, 0)`;
                    virtualScrollbarDOM.style.transformOrigin = 'left';
                });
            });
            // Update scroll positions of all the span bars
            selectRefs(this.contentSpanBar, (spanBarDOM) => {
                const left = -scrollLeft;
                spanBarDOM.style.transform = `translate3d(${left}px, 0, 0)`;
                spanBarDOM.style.transformOrigin = 'left';
            });
        };
        this.onDragStart = (event) => {
            if (this.isDragging ||
                event.type !== 'mousedown' ||
                !this.hasInteractiveLayer() ||
                !this.virtualScrollbar.current) {
                return;
            }
            event.stopPropagation();
            const virtualScrollbarRect = (0, utils_1.rectOfContent)(this.virtualScrollbar.current);
            // get intitial x-coordinate of the mouse click on the virtual scrollbar
            this.initialMouseClickX = Math.abs(event.clientX - virtualScrollbarRect.x);
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
            // indicate drag has begun
            this.isDragging = true;
            selectRefs(this.virtualScrollbar, scrollbarDOM => {
                scrollbarDOM.classList.add('dragging');
                document.body.style.setProperty('cursor', 'grabbing', 'important');
            });
        };
        this.onDragMove = (event) => {
            if (!this.isDragging ||
                event.type !== 'mousemove' ||
                !this.hasInteractiveLayer() ||
                !this.virtualScrollbar.current ||
                this.initialMouseClickX === undefined) {
                return;
            }
            const virtualScrollbarDOM = this.virtualScrollbar.current;
            const interactiveLayerRect = this.props.interactiveLayerRef.current.getBoundingClientRect();
            const virtualScrollBarRect = (0, utils_1.rectOfContent)(virtualScrollbarDOM);
            // Mouse x-coordinate relative to the interactive layer's left side
            const localDragX = event.pageX - interactiveLayerRect.x;
            // The drag movement with respect to the interactive layer's width.
            const rawMouseX = (localDragX - this.initialMouseClickX) / interactiveLayerRect.width;
            const maxVirtualScrollableArea = 1 - virtualScrollBarRect.width / interactiveLayerRect.width;
            // clamp rawMouseX to be within [0, 1]
            const virtualScrollbarPosition = (0, utils_1.clamp)(rawMouseX, 0, 1);
            const virtualLeft = (0, utils_1.clamp)(virtualScrollbarPosition, 0, maxVirtualScrollableArea) *
                interactiveLayerRect.width;
            virtualScrollbarDOM.style.transform = `translate3d(${virtualLeft}px, 0, 0)`;
            virtualScrollbarDOM.style.transformOrigin = 'left';
            const virtualScrollPercentage = (0, utils_1.clamp)(rawMouseX / maxVirtualScrollableArea, 0, 1);
            // Update scroll positions of all the span bars
            selectRefs(this.contentSpanBar, (spanBarDOM) => {
                const maxScrollDistance = spanBarDOM.getBoundingClientRect().width - interactiveLayerRect.width;
                const left = -lerp(0, maxScrollDistance, virtualScrollPercentage);
                spanBarDOM.style.transform = `translate3d(${left}px, 0, 0)`;
                spanBarDOM.style.transformOrigin = 'left';
            });
            // Update the scroll position of the scroll bar area
            selectRefs(this.props.interactiveLayerRef, (interactiveLayerRefDOM) => {
                selectRefs(this.scrollBarArea, (scrollBarAreaDOM) => {
                    const maxScrollDistance = scrollBarAreaDOM.getBoundingClientRect().width - interactiveLayerRect.width;
                    const left = lerp(0, maxScrollDistance, virtualScrollPercentage);
                    interactiveLayerRefDOM.scrollLeft = left;
                });
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
            selectRefs(this.virtualScrollbar, scrollbarDOM => {
                scrollbarDOM.classList.remove('dragging');
                document.body.style.removeProperty('cursor');
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
    componentDidMount() {
        // React will guarantee that refs are set before componentDidMount() is called;
        // but only for DOM elements that actually got rendered
        this.initializeScrollState();
    }
    componentDidUpdate(prevProps) {
        // Re-initialize the scroll state whenever:
        // - the window was selected via the minimap or,
        // - the divider was re-positioned.
        const dividerPositionChanged = this.props.dividerPosition !== prevProps.dividerPosition;
        const viewWindowChanged = prevProps.dragProps &&
            this.props.dragProps &&
            (prevProps.dragProps.viewWindowStart !== this.props.dragProps.viewWindowStart ||
                prevProps.dragProps.viewWindowEnd !== this.props.dragProps.viewWindowEnd);
        if (dividerPositionChanged || viewWindowChanged) {
            this.initializeScrollState();
        }
    }
    componentWillUnmount() {
        this.cleanUpListeners();
    }
    getReferenceSpanBar() {
        for (const currentSpanBar of this.contentSpanBar) {
            const isHidden = currentSpanBar.offsetParent === null;
            if (!document.body.contains(currentSpanBar) || isHidden) {
                continue;
            }
            return currentSpanBar;
        }
        return undefined;
    }
    render() {
        const childrenProps = {
            generateContentSpanBarRef: this.generateContentSpanBarRef,
            onDragStart: this.onDragStart,
            onScroll: this.onScroll,
            virtualScrollbarRef: this.virtualScrollbar,
            scrollBarAreaRef: this.scrollBarArea,
            updateScrollState: this.initializeScrollState,
        };
        return (<ScrollbarManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </ScrollbarManagerContext.Provider>);
    }
}
exports.Provider = Provider;
exports.Consumer = ScrollbarManagerContext.Consumer;
const withScrollbarManager = (WrappedComponent) => { var _a; return _a = class extends React.Component {
        render() {
            return (<ScrollbarManagerContext.Consumer>
          {context => {
                    const props = Object.assign(Object.assign({}, this.props), context);
                    return <WrappedComponent {...props}/>;
                }}
        </ScrollbarManagerContext.Consumer>);
        }
    },
    _a.displayName = `withScrollbarManager(${(0, getDisplayName_1.default)(WrappedComponent)})`,
    _a; };
exports.withScrollbarManager = withScrollbarManager;
//# sourceMappingURL=scrollbarManager.jsx.map