Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const actorAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/actorAvatar"));
class ValueComponent extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleClick = () => {
            this.props.onRemove(this.props.value);
        };
    }
    render() {
        return (<a onClick={this.handleClick}>
        <actorAvatar_1.default actor={this.props.value.actor} size={28}/>
      </a>);
    }
}
exports.default = ValueComponent;
//# sourceMappingURL=valueComponent.jsx.map