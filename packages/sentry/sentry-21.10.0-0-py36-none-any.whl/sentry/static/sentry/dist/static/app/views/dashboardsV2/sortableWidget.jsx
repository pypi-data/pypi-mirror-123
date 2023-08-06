Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const React = (0, tslib_1.__importStar)(require("react"));
const sortable_1 = require("@dnd-kit/sortable");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const widgetCard_1 = (0, tslib_1.__importDefault)(require("./widgetCard"));
const widgetWrapper_1 = (0, tslib_1.__importDefault)(require("./widgetWrapper"));
const initialStyles = {
    zIndex: 'auto',
};
function SortableWidget(props) {
    const { widget, dragId, isEditing, onDelete, onEdit } = props;
    const { attributes, listeners, setNodeRef, transform, isDragging: currentWidgetDragging, isSorting, } = (0, sortable_1.useSortable)({
        id: dragId,
        transition: null,
    });
    (0, react_1.useEffect)(() => {
        if (!currentWidgetDragging) {
            return undefined;
        }
        document.body.style.cursor = 'grabbing';
        return function cleanup() {
            document.body.style.cursor = '';
        };
    }, [currentWidgetDragging]);
    return (<widgetWrapper_1.default ref={setNodeRef} displayType={widget.displayType} layoutId={dragId} style={{
            // Origin is set to top right-hand corner where the drag handle is placed.
            // Otherwise, set the origin to be the top left-hand corner when swapping widgets.
            originX: currentWidgetDragging ? 1 : 0,
            originY: 0,
            boxShadow: currentWidgetDragging ? theme_1.default.dropShadowHeavy : 'none',
            borderRadius: currentWidgetDragging ? theme_1.default.borderRadius : undefined,
        }} animate={transform
            ? {
                x: transform.x,
                y: transform.y,
                scaleX: (transform === null || transform === void 0 ? void 0 : transform.scaleX) && transform.scaleX <= 1 ? transform.scaleX : 1,
                scaleY: (transform === null || transform === void 0 ? void 0 : transform.scaleY) && transform.scaleY <= 1 ? transform.scaleY : 1,
                zIndex: currentWidgetDragging ? theme_1.default.zIndex.modal : 'auto',
            }
            : initialStyles} transformTemplate={(___transform, generatedTransform) => {
            if (isEditing && !!transform) {
                return generatedTransform;
            }
            return 'none';
        }} transition={{
            duration: !currentWidgetDragging ? 0.25 : 0,
            easings: {
                type: 'spring',
            },
        }}>
      <widgetCard_1.default widget={widget} isEditing={isEditing} onDelete={onDelete} onEdit={onEdit} isSorting={isSorting} hideToolbar={isSorting} currentWidgetDragging={currentWidgetDragging} draggableProps={{
            attributes,
            listeners,
        }} showContextMenu/>
    </widgetWrapper_1.default>);
}
exports.default = SortableWidget;
//# sourceMappingURL=sortableWidget.jsx.map