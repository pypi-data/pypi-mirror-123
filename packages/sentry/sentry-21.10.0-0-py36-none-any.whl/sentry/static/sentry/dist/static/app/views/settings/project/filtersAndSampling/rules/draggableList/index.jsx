Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = require("react-dom");
const core_1 = require("@dnd-kit/core");
const sortable_1 = require("@dnd-kit/sortable");
const item_1 = (0, tslib_1.__importDefault)(require("./item"));
const sortableItem_1 = (0, tslib_1.__importDefault)(require("./sortableItem"));
class DraggableList extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {};
        this.handleChangeActive = (activeId) => {
            this.setState({ activeId });
        };
    }
    render() {
        const { activeId } = this.state;
        const { items, onUpdateItems, renderItem, disabled, wrapperStyle, innerWrapperStyle } = this.props;
        const getIndex = items.indexOf.bind(items);
        const activeIndex = activeId ? getIndex(activeId) : -1;
        return (<core_1.DndContext onDragStart={({ active }) => {
                if (!active) {
                    return;
                }
                this.handleChangeActive(active.id);
            }} onDragEnd={({ over }) => {
                this.handleChangeActive(undefined);
                if (over) {
                    const overIndex = getIndex(over.id);
                    if (activeIndex !== overIndex) {
                        onUpdateItems({
                            activeIndex,
                            overIndex,
                            reorderedItems: (0, sortable_1.arrayMove)(items, activeIndex, overIndex),
                        });
                    }
                }
            }} onDragCancel={() => this.handleChangeActive(undefined)}>
        <sortable_1.SortableContext items={items} strategy={sortable_1.verticalListSortingStrategy}>
          {items.map((item, index) => (<sortableItem_1.default key={item} id={item} index={index} renderItem={renderItem} disabled={disabled} wrapperStyle={wrapperStyle} innerWrapperStyle={innerWrapperStyle}/>))}
        </sortable_1.SortableContext>
        {(0, react_dom_1.createPortal)(<core_1.DragOverlay>
            {activeId ? (<item_1.default value={items[activeIndex]} renderItem={renderItem} wrapperStyle={wrapperStyle({
                        id: items[activeIndex],
                        index: activeIndex,
                        isDragging: true,
                        isSorting: false,
                    })} innerWrapperStyle={innerWrapperStyle({
                        id: items[activeIndex],
                        index: activeIndex,
                        isSorting: activeId !== null,
                        isDragging: true,
                        overIndex: -1,
                        isDragOverlay: true,
                    })}/>) : null}
          </core_1.DragOverlay>, document.body)}
      </core_1.DndContext>);
    }
}
DraggableList.defaultProps = {
    disabled: false,
    wrapperStyle: () => ({}),
    innerWrapperStyle: () => ({}),
};
exports.default = DraggableList;
//# sourceMappingURL=index.jsx.map