Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const sortable_1 = require("@dnd-kit/sortable");
const item_1 = (0, tslib_1.__importDefault)(require("./item"));
function SortableItem({ id, index, renderItem, disabled, wrapperStyle, innerWrapperStyle, }) {
    const { attributes, isSorting, isDragging, listeners, setNodeRef, overIndex, transform, transition, } = (0, sortable_1.useSortable)({ id, disabled });
    return (<item_1.default forwardRef={setNodeRef} value={id} sorting={isSorting} renderItem={renderItem} index={index} transform={transform} transition={transition} listeners={listeners} attributes={attributes} wrapperStyle={wrapperStyle({ id, index, isDragging, isSorting })} innerWrapperStyle={innerWrapperStyle({
            id,
            index,
            isDragging,
            isSorting,
            overIndex,
            isDragOverlay: false,
        })}/>);
}
exports.default = SortableItem;
//# sourceMappingURL=sortableItem.jsx.map