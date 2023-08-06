Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
class NumberDragControl extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isClicked: false,
        };
    }
    render() {
        const _a = this.props, { onChange, axis, step, shiftStep } = _a, props = (0, tslib_1.__rest)(_a, ["onChange", "axis", "step", "shiftStep"]);
        const isX = (axis !== null && axis !== void 0 ? axis : 'x') === 'x';
        return (<Wrapper {...props} onMouseDown={(event) => {
                if (event.button !== 0) {
                    return;
                }
                // XXX(epurkhiser): We can remove this later, just curious if people
                // are actually using the drag control
                (0, analytics_1.trackAnalyticsEvent)({
                    eventName: 'Number Drag Control: Clicked',
                    eventKey: 'number_drag_control.clicked',
                    organization_id: null,
                });
                event.currentTarget.requestPointerLock();
                this.setState({ isClicked: true });
            }} onMouseUp={() => {
                document.exitPointerLock();
                this.setState({ isClicked: false });
            }} onMouseMove={(event) => {
                var _a;
                if (!this.state.isClicked) {
                    return;
                }
                const delta = isX ? event.movementX : event.movementY * -1;
                const deltaOne = delta > 0 ? Math.ceil(delta / 100) : Math.floor(delta / 100);
                const deltaStep = deltaOne * ((_a = (event.shiftKey ? shiftStep : step)) !== null && _a !== void 0 ? _a : 1);
                onChange(deltaStep, event);
            }} isActive={this.state.isClicked} isX={isX}>
        <icons_1.IconArrow direction={isX ? 'left' : 'up'} size="8px"/>
        <icons_1.IconArrow direction={isX ? 'right' : 'down'} size="8px"/>
      </Wrapper>);
    }
}
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  padding: ${(0, space_1.default)(0.5)};
  ${p => p.isX
    ? 'grid-template-columns: max-content max-content'
    : 'grid-template-rows: max-content max-content'};
  cursor: ${p => (p.isX ? 'ew-resize' : 'ns-resize')};
  color: ${p => (p.isActive ? p.theme.gray500 : p.theme.gray300)};
  background: ${p => p.isActive && p.theme.backgroundSecondary};
  border-radius: 2px;
`;
exports.default = NumberDragControl;
//# sourceMappingURL=numberDragControl.jsx.map