Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
/**
 * Does not fire the onlick event if the mouse has moved outside of the
 * original click location upon release.
 *
 * <StrictClick onClick={this.onClickHandler}>
 *   <button>Some button</button>
 * </StrictClick>
 */
class StrictClick extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.handleMouseDown = ({ screenX, screenY }) => this.setState({ startCoords: [screenX, screenY] });
        this.handleMouseClick = (evt) => {
            if (!this.props.onClick) {
                return;
            }
            // Click happens if mouse down/up in same element - click will not fire if
            // either initial mouse down OR final mouse up occurs in different element
            const [x, y] = this.state.startCoords;
            const deltaX = Math.abs(evt.screenX - x);
            const deltaY = Math.abs(evt.screenY - y);
            // If mouse hasn't moved more than 10 pixels in either Y or X direction,
            // fire onClick
            if (deltaX < StrictClick.MAX_DELTA_X && deltaY < StrictClick.MAX_DELTA_Y) {
                this.props.onClick(evt);
            }
            this.setState({ startCoords: undefined });
        };
    }
    render() {
        // Bail out early if there is no onClick handler
        if (!this.props.onClick) {
            return this.props.children;
        }
        return React.cloneElement(this.props.children, {
            onMouseDown: this.handleMouseDown,
            onClick: this.handleMouseClick,
        });
    }
}
StrictClick.MAX_DELTA_X = 10;
StrictClick.MAX_DELTA_Y = 10;
exports.default = StrictClick;
//# sourceMappingURL=strictClick.jsx.map