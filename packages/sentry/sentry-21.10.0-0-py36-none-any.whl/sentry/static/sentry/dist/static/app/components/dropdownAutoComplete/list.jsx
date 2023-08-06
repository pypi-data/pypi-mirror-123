Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_virtualized_1 = require("react-virtualized");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const row_1 = (0, tslib_1.__importDefault)(require("./row"));
function getHeight(items, maxHeight, virtualizedHeight, virtualizedLabelHeight) {
    const minHeight = virtualizedLabelHeight
        ? items.reduce((a, r) => a + (r.groupLabel ? virtualizedLabelHeight : virtualizedHeight), 0)
        : items.length * virtualizedHeight;
    return Math.min(minHeight, maxHeight);
}
const List = ({ virtualizedHeight, virtualizedLabelHeight, onScroll, items, itemSize, highlightedIndex, inputValue, getItemProps, maxHeight, }) => {
    if (virtualizedHeight) {
        return (<react_virtualized_1.AutoSizer disableHeight>
        {({ width }) => (<StyledList width={width} height={getHeight(items, maxHeight, virtualizedHeight, virtualizedLabelHeight)} onScroll={onScroll} rowCount={items.length} rowHeight={({ index }) => items[index].groupLabel && virtualizedLabelHeight
                    ? virtualizedLabelHeight
                    : virtualizedHeight} rowRenderer={({ key, index, style }) => (<row_1.default key={key} item={items[index]} style={style} itemSize={itemSize} highlightedIndex={highlightedIndex} inputValue={inputValue} getItemProps={getItemProps}/>)}/>)}
      </react_virtualized_1.AutoSizer>);
    }
    return (<React.Fragment>
      {items.map((item, index) => (<row_1.default 
        // Using only the index of the row might not re-render properly,
        // because the items shift around the list
        key={`${item.value}-${index}`} item={item} itemSize={itemSize} highlightedIndex={highlightedIndex} inputValue={inputValue} getItemProps={getItemProps}/>))}
    </React.Fragment>);
};
exports.default = List;
// XXX(ts): Emotion11 has some trouble with List's defaultProps
const StyledList = (0, styled_1.default)(react_virtualized_1.List) `
  outline: none;
`;
//# sourceMappingURL=list.jsx.map