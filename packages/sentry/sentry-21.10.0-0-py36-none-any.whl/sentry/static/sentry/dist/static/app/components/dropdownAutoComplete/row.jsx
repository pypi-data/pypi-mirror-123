Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function Row({ item, style, itemSize, highlightedIndex, inputValue, getItemProps, }) {
    const { index } = item;
    if (item.groupLabel) {
        return (<LabelWithBorder style={style}>
        {item.label && <GroupLabel>{item.label}</GroupLabel>}
      </LabelWithBorder>);
    }
    return (<AutoCompleteItem itemSize={itemSize} disabled={item.disabled} isHighlighted={index === highlightedIndex} {...getItemProps({ item, index, style })}>
      {typeof item.label === 'function' ? item.label({ inputValue }) : item.label}
    </AutoCompleteItem>);
}
exports.default = Row;
const getItemPaddingForSize = (itemSize) => {
    if (itemSize === 'small') {
        return `${(0, space_1.default)(0.5)} ${(0, space_1.default)(1)}`;
    }
    if (itemSize === 'zero') {
        return '0';
    }
    return (0, space_1.default)(1);
};
const LabelWithBorder = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.backgroundSecondary};
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  border-width: 1px 0;
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};

  :first-child {
    border-top: none;
  }
  :last-child {
    border-bottom: none;
  }
`;
const GroupLabel = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(1)};
`;
const AutoCompleteItem = (0, styled_1.default)('div') `
  /* needed for virtualized lists that do not fill parent height */
  /* e.g. breadcrumbs (org height > project, but want same fixed height for both) */
  display: flex;
  flex-direction: column;
  justify-content: center;

  font-size: 0.9em;
  background-color: ${p => (p.isHighlighted ? p.theme.focus : 'transparent')};
  color: ${p => (p.isHighlighted ? p.theme.textColor : 'inherit')};
  padding: ${p => getItemPaddingForSize(p.itemSize)};
  cursor: ${p => (p.disabled ? 'not-allowed' : 'pointer')};
  border-bottom: 1px solid ${p => p.theme.innerBorder};

  :last-child {
    border-bottom: none;
  }

  :hover {
    color: ${p => p.theme.textColor};
    background-color: ${p => p.theme.focus};
  }
`;
//# sourceMappingURL=row.jsx.map