Object.defineProperty(exports, "__esModule", { value: true });
exports.ADD_WIDGET_BUTTON_DRAG_ID = void 0;
const tslib_1 = require("tslib");
const sortable_1 = require("@dnd-kit/sortable");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const types_1 = require("./types");
const widgetWrapper_1 = (0, tslib_1.__importDefault)(require("./widgetWrapper"));
exports.ADD_WIDGET_BUTTON_DRAG_ID = 'add-widget-button';
const initialStyles = {
    x: 0,
    y: 0,
    scaleX: 1,
    scaleY: 1,
};
function AddWidget({ onAddWidget, onOpenWidgetBuilder, orgFeatures }) {
    const onClick = orgFeatures.includes('metrics') ? onOpenWidgetBuilder : onAddWidget;
    const { setNodeRef, transform } = (0, sortable_1.useSortable)({
        disabled: true,
        id: exports.ADD_WIDGET_BUTTON_DRAG_ID,
        transition: null,
    });
    return (<widgetWrapper_1.default key="add" ref={setNodeRef} displayType={types_1.DisplayType.BIG_NUMBER} layoutId={exports.ADD_WIDGET_BUTTON_DRAG_ID} style={{ originX: 0, originY: 0 }} animate={transform
            ? {
                x: transform.x,
                y: transform.y,
                scaleX: (transform === null || transform === void 0 ? void 0 : transform.scaleX) && transform.scaleX <= 1 ? transform.scaleX : 1,
                scaleY: (transform === null || transform === void 0 ? void 0 : transform.scaleY) && transform.scaleY <= 1 ? transform.scaleY : 1,
            }
            : initialStyles} transition={{
            duration: 0.25,
        }}>
      <InnerWrapper onClick={onClick}>
        <AddButton data-test-id="widget-add" onClick={onClick} icon={<icons_1.IconAdd size="lg" isCircled color="inactive"/>}/>
      </InnerWrapper>
    </widgetWrapper_1.default>);
}
exports.default = AddWidget;
const AddButton = (0, styled_1.default)(button_1.default) `
  border: none;
  &,
  &:focus,
  &:active,
  &:hover {
    background: transparent;
    box-shadow: none;
  }
`;
const InnerWrapper = (0, styled_1.default)('div') `
  width: 100%;
  height: 110px;
  border: 2px dashed ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius};
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: ${p => (p.onClick ? 'pointer' : '')};
`;
//# sourceMappingURL=addWidget.jsx.map