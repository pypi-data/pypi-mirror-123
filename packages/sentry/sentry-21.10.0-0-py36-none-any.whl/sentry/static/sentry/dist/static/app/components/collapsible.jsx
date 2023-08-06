Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
/**
 * This component is used to show first X items and collapse the rest
 */
const Collapsible = ({ collapseButton, expandButton, maxVisibleItems = 5, children, }) => {
    const [isCollapsed, setCollapsed] = React.useState(true);
    const handleCollapseToggle = () => setCollapsed(!isCollapsed);
    const items = React.Children.toArray(children);
    const canCollapse = items.length > maxVisibleItems;
    if (!canCollapse) {
        return <React.Fragment>{children}</React.Fragment>;
    }
    const visibleItems = isCollapsed ? items.slice(0, maxVisibleItems) : items;
    const numberOfHiddenItems = items.length - visibleItems.length;
    const showDefault = (numberOfHiddenItems > 0 && !expandButton) ||
        (numberOfHiddenItems === 0 && !collapseButton);
    return (<React.Fragment>
      {visibleItems}

      {showDefault && (<button_1.default priority="link" onClick={handleCollapseToggle}>
          {isCollapsed
                ? (0, locale_1.tn)('Show %s hidden item', 'Show %s hidden items', numberOfHiddenItems)
                : (0, locale_1.t)('Collapse')}
        </button_1.default>)}

      {numberOfHiddenItems > 0 &&
            (expandButton === null || expandButton === void 0 ? void 0 : expandButton({ onExpand: handleCollapseToggle, numberOfHiddenItems }))}
      {numberOfHiddenItems === 0 && (collapseButton === null || collapseButton === void 0 ? void 0 : collapseButton({ onCollapse: handleCollapseToggle }))}
    </React.Fragment>);
};
exports.default = Collapsible;
//# sourceMappingURL=collapsible.jsx.map